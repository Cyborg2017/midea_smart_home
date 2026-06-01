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
_SKIP_KEYS = frozenset({'data_type', 'bucket', 'category', 'version'})


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
        self._pending_poll_location: Optional[int] = None
        self._skip_initial_refresh: bool = False
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

    def update_all(self, status: dict[str, Any], poll_location: Optional[int] = None) -> None:
        _LOGGER.debug("[%s] Status update: %s", self._device_id, status)
        for update in self._updates:
            try:
                update(status, poll_location=poll_location)
            except Exception as e:
                _LOGGER.error("[%s] Error in update callback: %s", self._device_id, e)

    def set_available(self, available: bool = True) -> None:
        self._available = available
        self.update_all({"available": self.available})

    def set_skip_initial_refresh(self, skip: bool = True) -> None:
        self._skip_initial_refresh = skip

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
            if self._connection_errors > 100:
                self._connection_errors = 100
            try:
                self._retry_delay = min(
                    INITIAL_RETRY_DELAY * (RETRY_MULTIPLIER ** self._connection_errors),
                    MAX_RETRY_DELAY
                )
            except OverflowError:
                self._retry_delay = MAX_RETRY_DELAY

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
                                poll_location = self._pending_poll_location
                                self._pending_poll_location = None
                                self.update_all(status, poll_location=poll_location)
            return True
        except Exception as e:
            _LOGGER.error("[%s] Error parsing message: %s", self._device_id, e)
            return False

    def refresh_status(self, query: Optional[dict] = None) -> None:
        query_hex = self._codec.build_query(query)
        if query_hex:
            self._send_message(query_hex, query=True)

    def send_poll_query(self, location: int) -> None:
        self._pending_poll_location = location
        query = {"query_type": "db", "db_location": location}
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
        while self._is_run:
            if self._sock is not None:
                break
            if self._connect_internal():
                _LOGGER.info("[%s] Connection established, querying status", self._device_id)
                self.set_available(True)
                if not self._skip_initial_refresh:
                    self.refresh_status()
                break
            self._close_socket()
            _LOGGER.warning("[%s] Unable to connect, sleep %.1f seconds (errors: %d)", self._device_id, self._retry_delay, self._connection_errors)
            time.sleep(self._retry_delay)

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
        enable_polling: bool = False,
        polling_interval: int = 1,
        initial_query: Optional[list] = None,
        polling_query: Optional[list] = None,
    ):
        self._device_id = device_id
        self._device_type = device_type
        self._default_values = default_values or {}
        self._centralized = list(centralized) if isinstance(centralized, (list, tuple, set)) else []
        self._enable_polling = enable_polling
        # Ensure polling_interval is between 1 and 30 seconds
        self._polling_interval = max(1, min(30, int(polling_interval)))
        # Store initial_query for initial status queries
        self._initial_query = initial_query or []
        # Store polling_query for periodic polling
        self._polling_query = polling_query or []

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
        self._last_available_time: float = 0.0
        self._pending_unavailable = False
        self._unavailable_delay = 5.0
        self._unavailable_timer: Optional[threading.Timer] = None
        self._recent_controls = {}  # {attr: (value, timestamp)}
        self._control_timeout = 5.0
        self._control_hold = 5.0 if self._centralized else 1.0
        self._callbacks = []
        self._poll_thread: Optional[threading.Thread] = None
        self._poll_run = False
        self._attribute_poll_thread: Optional[threading.Thread] = None
        self._attribute_poll_run = False

        # Register controller update callback
        self._controller.register_update(self._on_device_update)

        if device_type == 0xD9:
            self._controller.set_skip_initial_refresh(True)
            self._start_poll_thread()
        elif self._enable_polling:
            self._start_attribute_poll_thread()

    @property
    def device_id(self):
        return self._device_id

    @property
    def available(self):
        return self._available

    def _mark_unavailable(self):
        """Called by timer after unavailable_delay to mark device as unavailable."""
        if self._pending_unavailable and not self._available:
            return
        if self._pending_unavailable:
            self._available = False
            self._pending_unavailable = False
            self._notify_update()

    @property
    def data(self):
        return self._data

    @property
    def controller(self):
        return self._controller

    def open(self):
        self._controller.open()

    def close(self):
        if self._unavailable_timer is not None:
            self._unavailable_timer.cancel()
            self._unavailable_timer = None
        self._stop_poll_thread()
        self._stop_attribute_poll_thread()
        self._controller.close()

    def _start_poll_thread(self):
        if self._poll_thread is not None:
            return
        self._poll_run = True
        self._poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._poll_thread.start()

    def _stop_poll_thread(self):
        self._poll_run = False
        if self._poll_thread is not None:
            self._poll_thread.join(timeout=2.0)
            self._poll_thread = None

    def _poll_loop(self):
        while self._poll_run:
            if self._controller.connected:
                try:
                    interval = 0.5 if self._data.get('db_power') else 1.0
                    self._controller.send_poll_query(1)
                    time.sleep(interval)
                    if not self._poll_run:
                        break
                    self._controller.send_poll_query(2)
                    time.sleep(interval)
                except Exception as e:
                    _LOGGER.debug("[%s] Poll query error: %s", self._device_id, e)
            else:
                time.sleep(1.0)

    def _start_attribute_poll_thread(self):
        """Start polling thread for specific attributes."""
        if self._attribute_poll_thread is not None:
            return
        self._attribute_poll_run = True
        _LOGGER.info(
            "[%s] Starting attribute poll thread: polling enabled, interval=%ds",
            self._device_id,
            self._polling_interval
        )
        self._attribute_poll_thread = threading.Thread(target=self._attribute_poll_loop, daemon=True)
        self._attribute_poll_thread.start()

    def _stop_attribute_poll_thread(self):
        """Stop attribute polling thread."""
        self._attribute_poll_run = False
        if self._attribute_poll_thread is not None:
            self._attribute_poll_thread.join(timeout=2.0)
            self._attribute_poll_thread = None

    def _attribute_poll_loop(self):
        """Poll loop for enabled polling devices."""
        import time as time_module
        poll_count = 0
        query_index = 0  # Track which query to execute next

        while self._attribute_poll_run:
            if self._controller.connected:
                try:
                    # Log every 10 polls
                    if poll_count % 10 == 0:
                        _LOGGER.info(
                            "[%s] Polling device status (interval=%ds, poll_count=%d)",
                            self._device_id,
                            self._polling_interval,
                            poll_count
                        )

                    # Execute queries from polling_query in sequence
                    if self._polling_query:
                        # Get current query configuration
                        query_config = self._polling_query[query_index % len(self._polling_query)]

                        # Build query parameters based on config
                        query_params = {}
                        if isinstance(query_config, dict):
                            if len(query_config) == 0:
                                # Empty dict means full status query
                                query_params = {}
                            elif len(query_config) == 1:
                                # Single key means query_type (may contain comma-separated values)
                                key = list(query_config.keys())[0]
                                # Remove spaces around commas for compatibility: "light, sound" → "light,sound"
                                key = ",".join([k.strip() for k in key.split(",")]) if "," in key else key
                                query_params = {"query_type": key}
                        elif isinstance(query_config, set) and len(query_config) == 1:
                            # Set with single element means query_type (may contain comma-separated values)
                            key = list(query_config)[0]
                            # Remove spaces around commas for compatibility
                            key = ",".join([k.strip() for k in key.split(",")]) if "," in key else key
                            query_params = {"query_type": key}

                        # Execute the query
                        self.refresh_status(query_params)

                        # Move to next query in sequence
                        query_index += 1

                        # Wait 0.5 seconds between queries within the same cycle
                        if query_index % len(self._polling_query) != 0:
                            time.sleep(0.5)
                        else:
                            # After completing a full cycle, wait for the remaining interval
                            cycle_time = len(self._polling_query) * 0.5
                            remaining_time = max(0, self._polling_interval - cycle_time)
                            if remaining_time > 0:
                                time.sleep(remaining_time)
                    else:
                        # Fallback to full status query if no polling_query defined
                        self.refresh_status()
                        time.sleep(self._polling_interval)

                    poll_count += 1

                except Exception as e:
                    _LOGGER.debug("[%s] Attribute poll error: %s", self._device_id, e)
                    time.sleep(5.0)
            else:
                time.sleep(1.0)

    def register_update(self, callback):
        self._callbacks.append(callback)

    def _on_device_update(self, status: dict, poll_location: Optional[int] = None):
        """Handle updates from the controller."""
        notify = False
        if "available" in status:
            if status["available"]:
                # Cancel any pending unavailable timer
                if self._unavailable_timer is not None:
                    self._unavailable_timer.cancel()
                    self._unavailable_timer = None
                if not self._available:
                    self._available = True
                    notify = True
                if self._pending_unavailable:
                    self._pending_unavailable = False
                    notify = True
                self._last_available_time = time.time()
            else:
                if not self._pending_unavailable:
                    self._pending_unavailable = True
                    self._last_available_time = time.time()
                    # Schedule a timer to mark unavailable after the delay
                    if self._unavailable_timer is not None:
                        self._unavailable_timer.cancel()
                    self._unavailable_timer = threading.Timer(
                        self._unavailable_delay, self._mark_unavailable
                    )
                    self._unavailable_timer.daemon = True
                    self._unavailable_timer.start()
            if notify:
                self._notify_update()
            return

        self._last_available_time = time.time()
        if self._pending_unavailable:
            self._pending_unavailable = False
            # Cancel any pending unavailable timer since we received data
            if self._unavailable_timer is not None:
                self._unavailable_timer.cancel()
                self._unavailable_timer = None
            self._available = True

        if self._device_type == 0xD9:
            if poll_location is None:
                return

            data_type = status.get('data_type')
            if data_type != '03db':
                return

            db_location = status.get("db_location")
            if db_location not in (1, 2) or db_location != poll_location:
                return

            db_position = status.get('db_position')
            suffix = "_l" if db_location == 1 else "_r"
            poll_keys = (
                "db_detergent_needed", "db_remain_time", "db_progress",
                "db_running_status", "db_error_code"
            )

            new_data = self._data.copy()
            updated_keys = []

            if db_position == 1:
                for key, value in status.items():
                    if key not in _SKIP_KEYS:
                        new_data[key] = value
                        updated_keys.append(key)

            for key in poll_keys:
                if key in status:
                    new_data[key + suffix] = status[key]
                    updated_keys.append(key + suffix)

            if self._logic_handler.apply_special_handling_for_poll(new_data, suffix, status):
                self._data = new_data
                if updated_keys:
                    self._notify_update()
            return

        # Merge with existing data
        new_data = self._data.copy()
        new_data.update(status)

        # Apply logic handler special handling
        self._logic_handler.apply_special_handling(
            new_data,
            self._recent_controls,
            self._control_timeout
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
