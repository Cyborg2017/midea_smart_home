"""Midea Smart Home Device Controller."""

import socket
import json
import threading
import logging
import time
from collections.abc import Callable
from typing import Any, Optional

from .security import LocalSecurity
from .packet_builder import PacketBuilder
from .exceptions import CannotAuthenticate, DataUnexpectedLength, MessageWrongFormat
from .lua import MideaCodec
from .extras import DeviceLogicHandler
from .expression import ExpressionEvaluator

_LOGGER = logging.getLogger(__name__)

INITIAL_RETRY_DELAY = 1.0
MAX_RETRY_DELAY = 30.0
RETRY_MULTIPLIER = 2.0
CONNECTION_TIMEOUT = 10
SOCKET_TIMEOUT = 10
HEARTBEAT_INTERVAL = 10
MIN_MSG_LENGTH = 56


class DeviceController(threading.Thread):
    """Low-level controller for Midea smart devices.

    This class manages the socket connection and raw protocol communication.
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
        self.name = f"MideaConnection-{device_id}"

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

    def refresh_status(self, query: Optional[dict] = None) -> None:
        query_hex = self._codec.build_query(query)
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
        while self._is_run:
            if self._sock is not None:
                break
            if self._connect_internal():
                _LOGGER.info("[%s] Connection established, querying status", self._device_id)
                self.set_available(True)
                self.refresh_status()
                break
            self._close_socket()
            connection_retries += 1
            sleep_time = min(5 * (2 ** (connection_retries - 1)), 60)
            _LOGGER.warning("[%s] Unable to connect, sleep %s seconds (retry %d)", self._device_id, sleep_time, connection_retries)
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

    def send_control(
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
        self._send_message(control_hex)
        return control


class MideaDevice:
    """High-level Midea device wrapper.

    Handles device initialization, state management, logic application,
    and control execution.
    """

    def __init__(
        self,
        device_id: int,
        device_type: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        protocol: int,
        model: str,
        subtype: int,
        sn: str,
        sn8: str,
        lua_file: str,
        lua_common_dir: str,
        device_name: str,
        calculate_config: Optional[dict] = None,
        centralized: Optional[list[str]] = None,
        default_values: Optional[dict] = None,
        category: str = "",
    ):
        self._device_id = device_id
        self._device_type = device_type
        self._default_values = default_values or {}
        self._centralized = list(centralized) if isinstance(centralized, (list, tuple, set)) else []

        # Initialize Logic Handler
        self._logic_handler = DeviceLogicHandler(device_type, device_name)

        # Initialize Expression Evaluator
        self._expression_evaluator = ExpressionEvaluator(calculate_config)

        # Initialize Codec
        self._codec = MideaCodec(
            lua_file,
            lua_common_dir,
            sn=sn,
            subtype=subtype,
            device_type=device_type,
            sn8=sn8,
            category=category
        )

        # Initialize Controller
        self._controller = DeviceController(
            device_id=device_id,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            codec=self._codec,
            protocol=protocol,
        )

        self._data = {}
        self._available = False
        self._recent_controls = {}  # {attr: (value, timestamp)}
        self._control_timeout = 5.0
        self._control_hold = 5.0 if self._centralized else 1.0
        self._callbacks = []

        # Register controller update callback
        self._controller.register_update(self._on_device_update)

    @property
    def device_id(self):
        return self._device_id

    @property
    def available(self):
        return self._available

    @property
    def data(self):
        return self._data

    @property
    def controller(self):
        return self._controller

    def open(self):
        self._controller.open()

    def close(self):
        self._controller.close()

    def register_update(self, callback):
        self._callbacks.append(callback)

    def _on_device_update(self, status: dict):
        """Handle updates from the controller."""
        notify = False
        if "available" in status:
            prev_available = self._available
            self._available = status["available"]
            if self._available and not prev_available:
                notify = True
            elif not self._available:
                notify = True
            if notify:
                self._notify_update()
            return

        # Merge with existing data
        new_data = self._data.copy()
        new_data.update(status)

        # Apply logic handler special handling
        self._logic_handler.apply_special_handling(
            new_data,
            self._recent_controls,
            self._control_timeout,
            original_status=status
        )

        # Clean up expired recent controls
        now = time.time()
        self._recent_controls = {
            k: v for k, v in self._recent_controls.items()
            if now - v[1] < self._control_timeout
        }

        for key, (value, timestamp) in self._recent_controls.items():
            if now - timestamp < self._control_hold and new_data.get(key) != value:
                new_data[key] = value

        # Apply default values
        for key, value in self._default_values.items():
            if key not in new_data:
                new_data[key] = value

        # Apply calculations
        new_data = self._expression_evaluator.apply_calculations(new_data)

        self._data = new_data
        self._available = True
        self._notify_update()

    def _notify_update(self):
        for callback in self._callbacks:
            try:
                callback()
            except Exception as e:
                _LOGGER.error("Error in MideaDevice callback: %s", e)

    def set_attribute(self, attr: str, value: Any):
        """Set a device attribute."""
        _LOGGER.debug("Setting attribute %s to %s", attr, value)

        control = {attr: value}

        # Handle centralized control
        if self._centralized:
            now = time.time()
            for key in self._centralized:
                if key == attr:
                    continue
                recent = self._recent_controls.get(key)
                if recent and now - recent[1] < self._control_timeout:
                    control[key] = recent[0]
                elif key in self._data:
                    control[key] = self._data[key]

        # Handle special logic preparation
        control = self._logic_handler.prepare_control_data(control, self._data)

        # Update local state optimistically
        now = time.time()
        for k, v in control.items():
            self._recent_controls[k] = (v, now)

        # Send control
        self._controller.send_control(control, current_status=self._data)

        # Trigger update to reflect optimistic state
        self._on_device_update(control)

    def set_attributes(self, controls: dict):
        """Set multiple device attributes as a single command."""
        _LOGGER.debug("Setting attributes: %s", controls)

        control = controls.copy()

        # Handle special logic preparation
        control = self._logic_handler.prepare_control_data(control, self._data)

        # Update local state optimistically
        now = time.time()
        for k, v in control.items():
            self._recent_controls[k] = (v, now)

        # Send control
        self._controller.send_control(control, current_status=self._data)

        # Trigger update to reflect optimistic state
        self._on_device_update(control)

    def refresh_status(self, query: Optional[dict] = None):
        self._controller.refresh_status(query)
