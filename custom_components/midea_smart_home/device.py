import socket
import json
import threading
import logging
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, Optional

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
HEARTBEAT_INTERVAL = 10
MIN_MSG_LENGTH = 56


class LuaRuntime:
    """Lua runtime wrapper for Midea device protocol handling.
    
    This class manages a Lua runtime environment for parsing and building
    device-specific protocol messages. It loads device-specific Lua scripts
    and provides methods for JSON-to-data and data-to-JSON conversions.
    """
    
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


class DeviceController(threading.Thread):
    """Controller for Midea smart devices.
    
    This class manages the connection to a Midea device and handles
    all communication including status queries and control commands.
    It implements automatic reconnection with exponential backoff.
    Runs a background thread to listen for device push notifications.
    """
    
    def __init__(
        self,
        device_id: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        codec: MideaCodec,
        protocol: int = 3
    ):
        threading.Thread.__init__(self)
        self._device_id = device_id
        self._ip = ip_address
        self._port = port
        self._token = token
        self._key = key
        self._codec = codec
        self._protocol = protocol
        self._security: Optional[LocalSecurity] = None
        self._sock: Optional[socket.socket] = None
        self._lock = threading.Lock()
        self._connected = False
        self._last_connect_attempt: float = 0
        self._retry_delay: float = INITIAL_RETRY_DELAY
        self._connection_errors: int = 0
        self._buffer = b""
        self._updates: list[Callable[[dict[str, Any]], None]] = []
        self._is_run = False
        self._available = False
        self._previous_heartbeat: float = 0.0
        self.name = f"MideaDevice-{device_id}"
    
    @property
    def device_id(self) -> int:
        return self._device_id
    
    @property
    def ip(self) -> str:
        return self._ip
    
    @property
    def connected(self) -> bool:
        return self._connected
    
    @property
    def protocol(self) -> int:
        return self._protocol
    
    @property
    def available(self) -> bool:
        return self._available
    
    def register_update(self, update: Callable[[dict[str, Any]], None]) -> None:
        self._updates.append(update)
    
    def update_all(self, status: dict[str, Any]) -> None:
        _LOGGER.debug("[%s] Status update: %s", self._device_id, status)
        for update in self._updates:
            try:
                update(status)
            except Exception as e:
                _LOGGER.error("[%s] Error in update callback: %s", self._device_id, e)
    
    def set_available(self, available: bool = True) -> None:
        self._available = available
        self.update_all({"available": available})
    
    def open(self) -> None:
        if not self._is_run:
            self._is_run = True
            threading.Thread.start(self)
    
    def close(self) -> None:
        self._is_run = False
        self._close_socket()
    
    def _close_socket(self) -> None:
        self._buffer = b""
        self._connected = False
        sock = self._sock
        self._sock = None
        if sock:
            try:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
            except OSError:
                pass
    
    def connect(self) -> bool:
        with self._lock:
            return self._connect_internal()
    
    def _connect_internal(self) -> bool:
        current_time = time.time()
        self._last_connect_attempt = current_time
        
        self._close_socket()
        
        try:
            self._security = LocalSecurity()
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(CONNECTION_TIMEOUT)
            self._sock.connect((self._ip, self._port))
            
            if self._protocol == 3 and self._token and self._key:
                handshake = self._security.encode_8370(bytes.fromhex(self._token), 0x0)
                if self._sock is None:
                    return False
                self._sock.send(handshake)
                response = self._sock.recv(256)
                
                if len(response) < 72:
                    raise DataUnexpectedLength(f"Response too short: {len(response)}")
                
                auth_data = response[8:72]
                self._security.tcp_key(auth_data, bytes.fromhex(self._key))
            
            if self._sock is None:
                return False
            
            self._sock.settimeout(SOCKET_TIMEOUT)
            self._connected = True
            self._update_retry_delay(True)
            _LOGGER.debug("[%s] Connected successfully with protocol V%s", self._device_id, self._protocol)
            return True
            
        except (socket.timeout, socket.error, OSError) as e:
            _LOGGER.debug("[%s] Connection error: %s", self._device_id, e)
        except (CannotAuthenticate, DataUnexpectedLength, MessageWrongFormat) as e:
            _LOGGER.debug("[%s] Authentication error: %s", self._device_id, e)
        except ValueError as e:
            _LOGGER.debug("[%s] Invalid token/key format: %s", self._device_id, e)
        except AttributeError as e:
            _LOGGER.debug("[%s] Socket closed during connection: %s", self._device_id, e)
        
        self._update_retry_delay(False)
        self._connected = False
        return False
    
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
    
    def _fetch_v2_message(self, msg: bytes) -> tuple[list, bytes]:
        result = []
        while len(msg) > 0:
            factual_msg_len = len(msg)
            if factual_msg_len < 6:
                break
            alleged_msg_len = msg[4] + (msg[5] << 8)
            if factual_msg_len >= alleged_msg_len:
                result.append(msg[:alleged_msg_len])
                msg = msg[alleged_msg_len:]
            else:
                break
        return result, msg
    
    def _parse_message(self, msg: bytes) -> bool:
        try:
            if self._protocol == 3:
                messages, self._buffer = self._security.decode_8370(self._buffer + msg)
            else:
                messages, self._buffer = self._fetch_v2_message(self._buffer + msg)
            
            if len(messages) == 0:
                return False
            
            for message in messages:
                if message == b"ERROR":
                    return False
                
                if len(message) > MIN_MSG_LENGTH:
                    payload_len = message[4] + (message[5] << 8) - 56
                    payload_type = message[2] + (message[3] << 8)
                    
                    if payload_type not in [0x1001, 0x0001]:
                        cryptographic = bytes(message[40:-16])
                        if payload_len % 16 == 0:
                            decrypted = self._security.aes_decrypt(cryptographic)
                            receive_time = time.time()
                            status = self._codec.decode_status(decrypted.hex())
                            if status:
                                device_type_hex = hex(self._codec._device_type) if hasattr(self._codec, '_device_type') else 'unknown'
                                _LOGGER.debug("[DeviceType:%s] Received status at %.3f: %s", device_type_hex, receive_time, status)
                                self.update_all(status)
            return True
        except Exception as e:
            _LOGGER.error("[%s] Error parsing message: %s", self._device_id, e)
            return False
    
    def refresh_status(self) -> None:
        query_hex = self._codec.build_query()
        if query_hex:
            self._send_message(query_hex, query=True)
    
    def _send_message(self, data_hex: str, query: bool = False) -> None:
        sock = self._sock
        if not sock or not self._connected:
            return
        
        try:
            data_bytes = bytes.fromhex(data_hex)
            packet = PacketBuilder(self._device_id, data_bytes).finalize()
            
            if self._protocol == 3:
                encrypted = self._security.encode_8370(bytes(packet), 0x6)
                sock.send(encrypted)
            else:
                sock.send(packet)
        except (socket.error, OSError, AttributeError) as e:
            _LOGGER.debug("[%s] Send error: %s", self._device_id, e)
            self._close_socket()
    
    def _send_heartbeat(self) -> None:
        sock = self._sock
        if sock and self._connected:
            try:
                msg = PacketBuilder(self._device_id, bytearray([0x00])).finalize(msg_type=0)
                if self._protocol == 3:
                    encrypted = self._security.encode_8370(msg, 0x6)
                    sock.send(encrypted)
                else:
                    sock.send(msg)
            except (socket.error, OSError, AttributeError):
                self._close_socket()
    
    def _check_heartbeat(self, now: float) -> None:
        if now - self._previous_heartbeat >= HEARTBEAT_INTERVAL:
            self._send_heartbeat()
            self._previous_heartbeat = now
    
    def _connect_loop(self) -> None:
        connection_retries = 0
        while self._is_run and self._sock is None:
            if self._connect_internal():
                self.set_available(True)
                break
            self._close_socket()
            connection_retries += 1
            sleep_time = min(5 * (2 ** (connection_retries - 1)), 600)
            _LOGGER.warning("[%s] Unable to connect, sleep %s seconds", self._device_id, sleep_time)
            time.sleep(sleep_time)
    
    def run(self) -> None:
        while self._is_run:
            self._connect_loop()
            
            timeout_counter = 0
            start = time.time()
            self._previous_heartbeat = start
            
            while self._is_run:
                try:
                    sock = self._sock
                    if not sock:
                        raise OSError("Socket is None")
                    
                    now = time.time()
                    self._check_heartbeat(now)
                    
                    sock.settimeout(SOCKET_TIMEOUT)
                    msg = sock.recv(512)
                    
                    if len(msg) == 0:
                        raise ConnectionResetError("Connection closed by peer")
                    
                    if self._parse_message(msg):
                        timeout_counter = 0
                        
                except socket.timeout:
                    timeout_counter += 1
                    if timeout_counter >= 12:
                        _LOGGER.debug("[%s] Heartbeat timed out", self._device_id)
                        self._close_socket()
                        self.set_available(False)
                        break
                        
                except (socket.error, OSError, ConnectionResetError) as e:
                    _LOGGER.debug("[%s] Connection error: %s", self._device_id, e)
                    self._close_socket()
                    self.set_available(False)
                    break
                    
                except AttributeError as e:
                    _LOGGER.debug("[%s] Socket closed: %s", self._device_id, e)
                    self._close_socket()
                    self.set_available(False)
                    break
                    
                except Exception as e:
                    _LOGGER.error("[%s] Unexpected error: %s", self._device_id, e)
                    self._close_socket()
                    self.set_available(False)
                    break
    
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
        # Send control command asynchronously through background thread
        # Response will be handled by background thread via _parse_message -> update_all
        self._send_message(control_hex)
        # Return the control values that were sent
        # Actual status updates come through the registered update callbacks
        return control
