"""Midea Smart Home Packet Builder."""

from datetime import UTC, datetime
from hashlib import md5

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .security import LocalSecurity


class PacketBuilder:
    """Packet builder."""

    def __init__(self, device_id: int, command: bytes) -> None:
        self.security = LocalSecurity()
        self.packet = bytearray(
            [
                0x5A, 0x5A, 0x01, 0x11, 0x00, 0x00, 0x20, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            ],
        )
        self.packet[12:20] = self._packet_time()
        self.packet[20:28] = device_id.to_bytes(8, "little")
        self.command = command

    def finalize(self, msg_type: int = 1) -> bytearray:
        if msg_type != 1:
            self.packet[3] = 0x10
            self.packet[6] = 0x7B
        else:
            self.packet.extend(
                AES.new(self.security.aes_key, AES.MODE_ECB).encrypt(
                    bytearray(pad(self.command, 16))
                )
            )
        self.packet[4:6] = (len(self.packet) + 16).to_bytes(2, "little")
        salt = bytes.fromhex(
            format(
                233912452794221312800602098970898185176935770387238278451789080441632479840061417076563,
                "x",
            ),
        )
        self.packet.extend(md5(self.packet + salt).digest())
        return self.packet

    @staticmethod
    def _packet_time() -> bytearray:
        t = datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S%f")[:16]
        b = bytearray()
        for i in range(0, len(t), 2):
            d = int(t[i : i + 2])
            b.insert(0, d)
        return b
