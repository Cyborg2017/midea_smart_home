import socket
import json
import threading
import logging
import time
from pathlib import Path
from typing import Optional

import lupa.lua51

from .midea_lib.security import LocalSecurity
from .midea_lib.packet_builder import PacketBuilder
from .midea_lib.exceptions import CannotAuthenticate, DataUnexpectedLength, MessageWrongFormat


_LOGGER = logging.getLogger(__name__)

INITIAL_RETRY_DELAY = 1.0
MAX_RETRY_DELAY = 30.0
RETRY_MULTIPLIER = 2.0
CONNECTION_TIMEOUT = 10
SOCKET_TIMEOUT = 10


class LuaRuntime:
    def __init__(self, file_path: str, lua_default_dir: str):
        self._runtime = lupa.lua51.LuaRuntime()
        
        lua_dir = str(Path(file_path).parent).replace("\\", "/")
        lua_default_dir = str(lua_default_dir).replace("\\", "/")
        
        self._runtime.execute(
            f'package.path = "{lua_default_dir}/?.lua;{lua_dir}/?.lua;" .. package.path'
        )
        
        try:
            self._runtime.execute('require "cjson"')
        except lupa.lua51.LuaError as e:
            _LOGGER.warning("Failed to load cjson: %s", e)
            try:
                def lua_json_encode(obj):
                    return json.dumps(obj)
                
                def lua_json_decode(s):
                    return json.loads(s)
                
                cjson_lib = """
local cjson = {}

cjson.encode = lua_json_encode
cjson.decode = lua_json_decode

package.loaded["cjson"] = cjson
_G.cjson = cjson
"""
                self._runtime.globals()['lua_json_encode'] = lua_json_encode
                self._runtime.globals()['lua_json_decode'] = lua_json_decode
                self._runtime.execute(cjson_lib)
                _LOGGER.info("Using Python json module as fallback for cjson")
            except (json.JSONDecodeError, TypeError) as e2:
                _LOGGER.warning("Failed to set up fallback json: %s", e2)

        try:
            self._runtime.execute('require "bit"')
            _LOGGER.info("Using bit.lua file")
        except lupa.lua51.LuaError as e:
            _LOGGER.warning("Failed to load bit: %s", e)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lua_content = f.read()
            lua_content = lua_content.replace('local bit = require("bit")', '-- bit library loaded')
            self._runtime.execute(lua_content)
        except FileNotFoundError:
            raise RuntimeError(f"Lua file not found: {file_path}")
        except lupa.lua51.LuaError as e:
            raise RuntimeError(f"Lua syntax error in {file_path}: {e}")
        except OSError as e:
            raise RuntimeError(f"Failed to load Lua file {file_path}: {e}")
        
        self._lock = threading.Lock()
        try:
            self._json_to_data = self._runtime.eval(
                "function(param) return jsonToData(param) end"
            )
            self._data_to_json = self._runtime.eval(
                "function(param) return dataToJson(param) end"
            )
        except lupa.lua51.LuaError as e:
            raise RuntimeError(f"Lua file {file_path} missing required functions (jsonToData/dataToJson): {e}")

    def json_to_data(self, json_value: str) -> str:
        with self._lock:
            try:
                return self._json_to_data(json_value)
            except lupa.lua51.LuaError as e:
                _LOGGER.error("Lua json_to_data error: %s", e)
                _LOGGER.debug("Failed json value (first 200 chars): %s", str(json_value)[:200])
                return ""

    def data_to_json(self, data_value: str) -> str:
        with self._lock:
            try:
                result = self._data_to_json(data_value)
                _LOGGER.debug("data_to_json input length: %d", len(data_value) if data_value else 0)
                return result
            except lupa.lua51.LuaError as e:
                _LOGGER.error("Lua data_to_json error: %s", e)
                _LOGGER.debug("Failed data value (first 200 chars): %s", str(data_value)[:200])
                return ""


class MideaCodec(LuaRuntime):
    def __init__(
        self,
        file_path: str,
        lua_default_dir: str,
        sn: str = "",
        subtype: int = 0,
        device_type: int = 0,
        sn8: str = ""
    ):
        super().__init__(file_path, lua_default_dir)
        self._sn = sn or ""
        self._subtype = subtype
        self._device_type = device_type
        self._sn8 = sn8 or ""

    def build_query(self, query: Optional[dict] = None) -> str:
        try:
            result = self.json_to_data(json.dumps({
                "deviceinfo": {"deviceSN": self._sn, "deviceSubType": self._subtype},
                "query": query or {}
            }))
            return result or ""
        except (json.JSONEncodeError, TypeError) as e:
            _LOGGER.error("build_query error: %s", e)
            return ""

    def build_control(
        self,
        control: dict,
        current_status: Optional[dict] = None
    ) -> str:
        try:
            result = self.json_to_data(json.dumps({
                "deviceinfo": {"deviceSN": self._sn, "deviceSubType": self._subtype},
                "control": control,
                "status": current_status or {}
            }))
            return result or ""
        except (json.JSONEncodeError, TypeError) as e:
            _LOGGER.error("build_control error: %s", e)
            return ""

    def decode_status(
        self,
        full_message_hex: str,
        is_control_response: bool = False
    ) -> Optional[dict]:
        try:
            result = self.data_to_json(json.dumps({
                "deviceinfo": {"deviceSN": self._sn, "deviceSubType": self._subtype},
                "msg": {"data": full_message_hex}
            }))
            if result:
                status = json.loads(result).get("status")
                return status
            return None
        except json.JSONDecodeError as e:
            _LOGGER.error("decode_status JSON parse error: %s", e)
            return None
        except lupa.lua51.LuaError as e:
            _LOGGER.error("decode_status Lua error: %s", e)
            return None


class DeviceController:
    def __init__(
        self,
        device_id: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        codec: MideaCodec
    ):
        self._device_id = device_id
        self._ip = ip_address
        self._port = port
        self._token = token
        self._key = key
        self._codec = codec
        self._security: Optional[LocalSecurity] = None
        self._sock: Optional[socket.socket] = None
        self._lock = threading.Lock()
        self._connected = False
        self._last_connect_attempt: float = 0
        self._retry_delay: float = INITIAL_RETRY_DELAY
        self._connection_errors: int = 0

    @property
    def device_id(self) -> int:
        return self._device_id

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self) -> bool:
        with self._lock:
            return self._connect_internal()

    def close(self):
        with self._lock:
            self._disconnect_internal()

    def _disconnect_internal(self):
        self._connected = False
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None

    def _should_retry_connect(self) -> bool:
        current_time = time.time()
        time_since_last = current_time - self._last_connect_attempt
        return time_since_last >= self._retry_delay

    def _update_retry_delay(self, success: bool):
        if success:
            self._retry_delay = INITIAL_RETRY_DELAY
            self._connection_errors = 0
        else:
            self._connection_errors += 1
            self._retry_delay = min(
                INITIAL_RETRY_DELAY * (RETRY_MULTIPLIER ** self._connection_errors),
                MAX_RETRY_DELAY
            )

    def _connect_internal(self) -> bool:
        current_time = time.time()
        self._last_connect_attempt = current_time
        
        self._disconnect_internal()
        
        try:
            self._security = LocalSecurity()
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(CONNECTION_TIMEOUT)
            self._sock.connect((self._ip, self._port))
            handshake = self._security.encode_8370(bytes.fromhex(self._token), 0x0)
            self._sock.send(handshake)
            response = self._sock.recv(256)
            
            if len(response) < 72:
                raise DataUnexpectedLength(f"Response too short: {len(response)}")
            
            auth_data = response[8:72]
            self._security.tcp_key(auth_data, bytes.fromhex(self._key))
            self._sock.settimeout(SOCKET_TIMEOUT)
            self._connected = True
            self._update_retry_delay(True)
            _LOGGER.debug("Device %s connected successfully", self._device_id)
            return True
            
        except (socket.timeout, socket.error, OSError) as e:
            _LOGGER.error("Socket error connecting device %s: %s", self._device_id, e)
        except (CannotAuthenticate, DataUnexpectedLength, MessageWrongFormat) as e:
            _LOGGER.error("Authentication error for device %s: %s", self._device_id, e)
        except ValueError as e:
            _LOGGER.error("Invalid token/key format for device %s: %s", self._device_id, e)
        
        self._update_retry_delay(False)
        self._connected = False
        return False

    def _ensure_connection(self) -> bool:
        if self._connected and self._sock is not None:
            return True
        
        if not self._should_retry_connect():
            _LOGGER.debug(
                "Device %s waiting for retry delay (%.1fs remaining)",
                self._device_id,
                self._retry_delay - (time.time() - self._last_connect_attempt)
            )
            return False
        
        return self._connect_internal()

    def _send_and_receive(self, data_hex: str, retry: int = 2) -> Optional[bytes]:
        with self._lock:
            for attempt in range(retry):
                if not self._ensure_connection():
                    continue
                
                try:
                    data_bytes = bytes.fromhex(data_hex)
                    packet = PacketBuilder(self._device_id, data_bytes).finalize()
                    encrypted = self._security.encode_8370(bytes(packet), 0x6)
                    self._sock.send(encrypted)
                    response = self._sock.recv(4096)
                    packets, _ = self._security.decode_8370(response)
                    if packets:
                        data = packets[0]
                        encrypted_data = data[40:-16]
                        self._update_retry_delay(True)
                        return self._security.aes_decrypt(encrypted_data)
                        
                except socket.timeout:
                    _LOGGER.warning(
                        "Timeout for device %s, retry %d/%d",
                        self._device_id, attempt + 1, retry
                    )
                    self._disconnect_internal()
                    
                except (socket.error, OSError) as e:
                    _LOGGER.error(
                        "Socket error for device %s: %s, reconnecting...",
                        self._device_id, e
                    )
                    self._disconnect_internal()
                    
                except (MessageWrongFormat, DataUnexpectedLength) as e:
                    _LOGGER.error(
                        "Protocol error for device %s: %s",
                        self._device_id, e
                    )
                    self._disconnect_internal()
                    
                except ValueError as e:
                    _LOGGER.error(
                        "Data format error for device %s: %s",
                        self._device_id, e
                    )
                    self._disconnect_internal()
                    
            return None

    def get_status(self, query: Optional[dict] = None) -> dict:
        try:
            query_hex = self._codec.build_query(query)
            if not query_hex:
                return {}
            decrypted = self._send_and_receive(query_hex)
            if decrypted:
                return self._codec.decode_status(decrypted.hex()) or {}
            _LOGGER.warning("No decrypted response for device %s", self._device_id)
        except (json.JSONDecodeError, ValueError) as e:
            _LOGGER.error("Failed to get status for device %s: %s", self._device_id, e)
        return {}

    def set_control(
        self,
        attr: str | dict,
        value: str | int | float | bool | None = None,
        current_status: Optional[dict] = None
    ) -> dict:
        if isinstance(attr, dict):
            control = attr
        else:
            control = {attr: value}
        control_hex = self._codec.build_control(control, current_status)
        if not control_hex:
            return {}
        decrypted = self._send_and_receive(control_hex, retry=1)
        if decrypted:
            status = self._codec.decode_status(decrypted.hex(), is_control_response=True)
            if status:
                return status
        return {}
