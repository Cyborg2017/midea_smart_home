"""Midea device setup and validation helpers."""
import logging
import socket
import time
from typing import Optional, Tuple

from .device import DeviceController
from .lua import MideaCodec
from .exceptions import CannotAuthenticate

_LOGGER = logging.getLogger(__name__)

async def validate_device(
    hass,
    device_id: int,
    ip_address: str,
    port: int,
    token: str,
    key: str,
    lua_file: str,
    protocol: int,
    sn: str = "",
    sn8: str = "",
    device_type: int = 0
) -> Tuple[bool, Optional[str]]:
    """Validate device connection and authentication.

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    # 1. Test socket connection
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = await hass.async_add_executor_job(
            sock.connect_ex, (ip_address, port)
        )
        sock.close()
        if result != 0:
            return False, "cannot_connect"
    except Exception as e:
        _LOGGER.error("[setup] socket connect failed: ip=%s port=%s error=%s", ip_address, port, e)
        return False, "cannot_connect"

    # 2. Test authentication and protocol
    try:
        from ..const import LUA_COMMON_PATH
        from pathlib import Path
        from ..device_mapping import get_device_mapping

        lua_common_dir = Path(hass.config.config_dir) / LUA_COMMON_PATH

        # Init controls (e.g. lock off) used as a fallback to fetch full
        # status when the initial status query returns no data
        initial_control = get_device_mapping(device_type, "", sn8, "").get("initial_control")

        def _test_connection():
            codec = MideaCodec(lua_file, str(lua_common_dir), sn=sn, subtype=0, device_type=device_type, sn8=sn8)
            controller = DeviceController(
                device_id=device_id,
                ip_address=ip_address,
                port=port,
                token=token,
                key=key,
                codec=codec,
                protocol=protocol,
            )

            got_status = False

            def status_callback(status, poll_location=None):
                nonlocal got_status
                # Ignore availability-only updates (e.g. {"available":
                # false} after a connection error) and metadata-only
                # payloads (e.g. {"version": 0}); require real status
                # data parsed from the device reply
                if status and set(status) - {"available", "version"}:
                    got_status = True

            controller.register_update(status_callback)

            try:
                controller.open()
                start = time.time()
                while not controller.available and (time.time() - start < 10):
                    time.sleep(0.5)

                if not controller.available:
                    return False, "cannot_connect"

                # Try to get status
                controller.refresh_status()

                # Wait for status
                start = time.time()
                while not got_status and (time.time() - start < 5):
                    time.sleep(0.5)

                # Fallback: if the init query returned no data, send init
                # controls (e.g. lock off) to fetch full status
                if not got_status and initial_control:
                    for control in initial_control:
                        if isinstance(control, dict) and control:
                            controller.send_control(control, current_status={})
                            time.sleep(0.3)
                    start = time.time()
                    while not got_status and (time.time() - start < 5):
                        time.sleep(0.5)

                if not got_status:
                    return False, "lua_error"

                return True, None
            finally:
                controller.close()
                if controller.is_alive():
                    controller.join(timeout=3.0)
                    if controller.is_alive():
                        _LOGGER.warning(
                            "[setup] controller thread did not stop within 3s: device_id=%s",
                            device_id,
                        )

        return await hass.async_add_executor_job(_test_connection)

    except Exception as e:
        _LOGGER.error("[setup] device validation failed: device_id=%s error=%s", device_id, e)
        return False, "unknown"
