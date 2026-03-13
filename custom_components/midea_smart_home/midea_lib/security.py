"""Midea Smart Home Security."""

import hmac
from hashlib import md5, sha256
from typing import Any

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor

from .exceptions import (
    CannotAuthenticate,
    DataSignDoesntMatch,
    DataUnexpectedLength,
    MessageWrongFormat,
)

Buffer = bytes | bytearray | memoryview

HEADER_8370_1ST_BYTE = 0x83
HEADER_8370_2ND_BYTE = 0x70
HEADER_8370_4TH_BYTE = 0x20
MIN_DECODE_8370_DATA_LENGTH = 6
MSGTYPE_ENCRYPTED_RESPONSE = 0x3
MSGTYPE_ENCRYPTED_REQUEST = 0x6
TCP_KEY_RESPONSE_LENGTH = 64
MAX_DOUBLE_BYTE_VALUE = 0xFFFF


class CloudSecurity:
    """Cloud security base class."""

    def __init__(
        self,
        login_key: str,
        iot_key: str | None,
        hmac_key: str | None,
        fixed_key: int | None = None,
        fixed_iv: int | None = None,
    ) -> None:
        self._login_key = login_key
        self._iot_key = iot_key
        self._hmac_key = hmac_key
        self._aes_key: bytes | None = None
        self._aes_iv: bytes | None = None
        self._fixed_key = format(fixed_key, "x").encode("ascii") if fixed_key else None
        self._fixed_iv = format(fixed_iv, "x").encode("ascii") if fixed_iv else None

    def sign(self, url: str, data: dict[str, Any] | str, random: str) -> str | None:
        msg: str = self._iot_key or ""
        msg += str(data)
        msg += random
        if not self._hmac_key:
            return None
        sign = hmac.new(self._hmac_key.encode("ascii"), msg.encode("ascii"), sha256)
        return sign.hexdigest()

    def encrypt_password(self, login_id: str, data: str) -> str:
        m = sha256()
        m.update(data.encode("ascii"))
        login_hash = login_id + m.hexdigest() + self._login_key
        m = sha256()
        m.update(login_hash.encode("ascii"))
        return m.hexdigest()

    def encrypt_iam_password(self, login_id: str, data: str) -> str:
        raise NotImplementedError

    @staticmethod
    def get_deviceid(username: str) -> str:
        return sha256(f"Hello, {username}!".encode("ascii")).hexdigest()[:16]

    @staticmethod
    def get_udp_id(appliance_id: int, method: int = 0) -> str | None:
        if method == 0:
            bytes_id = bytes(reversed(appliance_id.to_bytes(8, "big")))
        elif method == 1:
            bytes_id = appliance_id.to_bytes(6, "big")
        elif method == 2:
            bytes_id = appliance_id.to_bytes(6, "little")
        else:
            return None
        data = bytearray(sha256(bytes_id).digest())
        for i in range(16):
            data[i] ^= data[i + 16]
        return data[0:16].hex()

    def set_aes_keys(self, key: bytes | str, iv: bytes | str) -> None:
        if isinstance(key, str):
            key = key.encode("ascii")
        if isinstance(iv, str):
            iv = iv.encode("ascii")
        self._aes_key = key
        self._aes_iv = iv

    def aes_decrypt_with_fixed_key(self, data: str) -> str:
        return self.aes_decrypt(data, self._fixed_key, self._fixed_iv)

    def aes_decrypt(
        self,
        data: str | bytes,
        key: bytes | None = None,
        iv: bytes | None = None,
    ) -> str:
        if len(data) == 0:
            return ""
        aes_key = key if key is not None else self._aes_key
        aes_iv = iv if iv is not None else self._aes_iv
        if aes_key is None:
            raise ValueError("Decrypt need a key")
        if isinstance(data, str):
            data = bytes.fromhex(data)
        if aes_iv is None or aes_iv == b"0":
            return unpad(
                AES.new(aes_key, AES.MODE_ECB).decrypt(data),
                len(aes_key),
            ).decode()
        return unpad(
            AES.new(aes_key, AES.MODE_CBC, iv=aes_iv).decrypt(data),
            len(aes_key),
        ).decode()


class MeijuCloudSecurity(CloudSecurity):
    """Meiju Cloud Security."""

    def __init__(self, login_key: str, iot_key: str, hmac_key: str) -> None:
        super().__init__(login_key, iot_key, hmac_key, 10864842703515613082)

    def encrypt_iam_password(self, login_id: str, data: str) -> str:
        md = md5()
        md.update(data.encode("ascii"))
        md_second = md5()
        md_second.update(md.hexdigest().encode("ascii"))
        return md_second.hexdigest()


class MideaAirSecurity(CloudSecurity):
    """Midea Air Security."""

    def __init__(self, login_key: str) -> None:
        super().__init__(login_key, None, None)

    def sign(self, url: str, data: dict[str, Any] | str, random: str) -> str:
        from urllib.parse import unquote_plus, urlencode, urlparse
        if isinstance(data, str):
            raise ValueError("Data must be dict")
        payload = unquote_plus(urlencode(sorted(data.items(), key=lambda x: x[0])))
        sha = sha256()
        sha.update((urlparse(url).path + payload + self._login_key).encode("ascii"))
        return sha.hexdigest()


class LocalSecurity:
    """Local security for device communication."""

    def __init__(self) -> None:
        self.iv = b"\0" * 16
        self.aes_key = bytes.fromhex(
            format(141661095494369103254425781617665632877, "x"),
        )
        self._tcp_key: bytes
        self._request_count = 0
        self._response_count = 0

    def aes_decrypt(self, raw: bytes) -> bytearray:
        try:
            return bytearray(
                unpad(AES.new(self.aes_key, AES.MODE_ECB).decrypt(bytearray(raw)), 16),
            )
        except ValueError:
            return bytearray(0)

    def aes_cbc_decrypt(self, raw: bytes, key: Buffer) -> bytes:
        return AES.new(key=key, mode=AES.MODE_CBC, iv=self.iv).decrypt(raw)

    def aes_cbc_encrypt(self, raw: bytes, key: Buffer) -> bytes:
        return AES.new(key=key, mode=AES.MODE_CBC, iv=self.iv).encrypt(raw)

    def tcp_key(self, response: bytes, key: Buffer) -> bytes:
        if response == b"ERROR":
            raise CannotAuthenticate
        if len(response) != TCP_KEY_RESPONSE_LENGTH:
            raise DataUnexpectedLength
        payload = response[:32]
        sign = response[32:]
        plain = self.aes_cbc_decrypt(payload, key)
        if sha256(plain).digest() != sign:
            raise DataSignDoesntMatch
        self._tcp_key = strxor(plain, key)
        self._request_count = 0
        self._response_count = 0
        return self._tcp_key

    def encode_8370(self, data: bytes, msgtype: int) -> bytes:
        header = bytearray([0x83, 0x70])
        size, padding = len(data), 0
        if (msgtype in (MSGTYPE_ENCRYPTED_RESPONSE, MSGTYPE_ENCRYPTED_REQUEST)) and (
            (size + 2) % 16 != 0
        ):
            padding = 16 - (size + 2 & 0xF)
            size += padding + 32
            data += get_random_bytes(padding)
        header += size.to_bytes(2, "big")
        header += bytearray([0x20, padding << 4 | msgtype])
        data = self._request_count.to_bytes(2, "big") + data
        self._request_count += 1
        if self._request_count >= MAX_DOUBLE_BYTE_VALUE:
            self._request_count = 0
        if msgtype in (MSGTYPE_ENCRYPTED_RESPONSE, MSGTYPE_ENCRYPTED_REQUEST):
            sign = sha256(header + data).digest()
            data = self.aes_cbc_encrypt(raw=data, key=self._tcp_key) + sign
        return header + data

    def decode_8370(self, data: bytes) -> tuple[list, bytes]:
        if len(data) < MIN_DECODE_8370_DATA_LENGTH:
            return [], data
        header = data[:6]
        if header[0] != HEADER_8370_1ST_BYTE or header[1] != HEADER_8370_2ND_BYTE:
            raise MessageWrongFormat("not an 8370 message")
        size = int.from_bytes(header[2:4], "big") + 8
        leftover = None
        if len(data) > size:
            leftover = data[size:]
            data = data[:size]
        elif len(data) < size:
            return [], data
        if header[4] != HEADER_8370_4TH_BYTE:
            raise MessageWrongFormat("missing byte 4")
        padding = header[5] >> 4
        msgtype = header[5] & 0xF
        data = data[6:]
        if msgtype in (MSGTYPE_ENCRYPTED_RESPONSE, MSGTYPE_ENCRYPTED_REQUEST):
            sign = data[-32:]
            data = data[:-32]
            data = self.aes_cbc_decrypt(raw=data, key=self._tcp_key)
            if sha256(header + data).digest() != sign:
                raise DataSignDoesntMatch
            if padding:
                data = data[:-padding]
        self._response_count = int.from_bytes(data[:2], "big")
        data = data[2:]
        if leftover:
            packets, incomplete = self.decode_8370(leftover)
            return [data, *packets], incomplete
        return [data], b""
