"""Midea device setup and validation helpers."""
import logging
import socket
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
        _LOGGER.error("Socket connect error: %s", e)
        return False, "cannot_connect"

    # 2. Test authentication and protocol
    try:
        from ..const import LUA_COMMON_PATH
        from pathlib import Path

        lua_common_dir = Path(hass.config.config_dir) / LUA_COMMON_PATH

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

            try:
                controller.open()
                import time
                start = time.time()
                while not controller.available and (time.time() - start < 10):
                    time.sleep(0.5)

                if not controller.available:
                    return False, "cannot_connect"

                # Try to get status
                controller.refresh_status()

                # Wait for status
                start = time.time()
                got_status = False

                def status_callback(status):
                    nonlocal got_status
                    got_status = True

                controller.register_update(status_callback)

                while not got_status and (time.time() - start < 10):
                    time.sleep(0.5)

                if not got_status:
                    return False, "lua_error"

                return True, None
            finally:
                controller.close()

        return await hass.async_add_executor_job(_test_connection)

    except Exception as e:
        _LOGGER.error("Validation error: %s", e)
        return False, "unknown"
