import json
import logging
import socket
from pathlib import Path
from typing import Any

import lupa.lua51
import voluptuous as vol
from aiohttp import ClientSession
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_ACCOUNT,
    CONF_CATEGORY,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_HOME_NAME,
    CONF_IP,
    CONF_KEY,
    CONF_LUA_FILE,
    CONF_MANUFACTURER_CODE,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_ROOM_NAME,
    CONF_SERVER,
    CONF_SN,
    CONF_SN8,
    CONF_PRODUCT_MODEL,
    CONF_MODEL_NUMBER,
    CONF_TOKEN,
    DEFAULT_PORT,
    DEVICE_TYPES,
    DOMAIN,
    JSON_FILES_PATH,
    LUA_COMMON_PATH,
    LUA_CUSTOM_PATH,
    LUA_DEVICE_PATH,
    ProtocolVersion,
)
from .midea_lib.packet_builder import PacketBuilder
from .midea_lib.discovery import discover_devices, DISCOVERY_TIMEOUT
from .midea_lib.lua import write_file, decrypt_lua_code, ensure_lua_files
from .midea_lib.setup import validate_device
from .midea_lib.cloud import download_lua_file, SUPPORTED_CLOUDS

_LOGGER = logging.getLogger(__name__)

CLOUD_SERVERS = {
    1: "美的美居",
    2: "MSmart Home",
    3: "Midea Air",
    4: "NetHome Plus",
    5: "Ariston Clima",
}

CLOUD_KEY_TO_NAME = {
    1: "Meiju Cloud",
    2: "SmartHome",
    3: "Midea Air",
    4: "NetHome Plus",
    5: "Ariston Clima",
}

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_ACCOUNT): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Required(CONF_SERVER, default=1): vol.In(CLOUD_SERVERS),
    vol.Optional("scan_address", default="auto"): str,
})

def get_lua_storage_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / LUA_DEVICE_PATH

def get_lua_common_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / LUA_COMMON_PATH

def get_lua_custom_path(component_dir: str, device_type: int, sn8: str = "") -> Path:
    """Get path for custom Lua file in integration's lua folder.

    Custom Lua files are named T0x{device_type}_{sn8}.lua (without device_id).
    """
    if sn8:
        return Path(component_dir) / LUA_CUSTOM_PATH / f"T0x{hex(device_type)[2:].upper()}_{sn8}.lua"
    return Path(component_dir) / LUA_CUSTOM_PATH / f"T0x{hex(device_type)[2:].upper()}.lua"

def get_lua_file_path(hass_config_dir: str, device_id: int, device_type: int, sn8: str = "") -> Path:
    """Get path for cloud-downloaded Lua file in .storage directory."""
    if sn8:
        return get_lua_storage_path(hass_config_dir) / f"T0x{hex(device_type)[2:].upper()}_{sn8}.lua"
    return get_lua_storage_path(hass_config_dir) / f"T0x{hex(device_type)[2:].upper()}.lua"

def get_json_files_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / JSON_FILES_PATH

def get_device_json_path(hass_config_dir: str, device_id: int, device_type: int, sn8: str = "") -> Path:
    if sn8:
        return get_json_files_path(hass_config_dir) / f"T0x{hex(device_type)[2:].upper()}_{sn8}.json"
    return get_json_files_path(hass_config_dir) / f"T0x{hex(device_type)[2:].upper()}.json"


class MideaSmartHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._discovered_devices: dict = {}
        self._selected_devices: list = []
        self._current_device_index: int = 0
        self._devices_data: list = []
        self._account: str = None
        self._password: str = None
        self._cloud_name: str = "Meiju Cloud"
        self._scan_address: str = "auto"
        self._session: ClientSession = None
        self._preset_cloud = None
        self._user_cloud = None
        self._existing_entry: config_entries.ConfigEntry | None = None
        self._cloud_devices: dict = {}

    async def _cleanup_session(self):
        if self._session:
            await self._session.close()
            self._session = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors = {}

        if user_input is not None:
            self._account = user_input.get(CONF_ACCOUNT)
            self._password = user_input.get(CONF_PASSWORD)
            self._scan_address = user_input.get("scan_address", "auto")
            cloud_server_key = user_input.get(CONF_SERVER, 1)
            self._cloud_name = CLOUD_KEY_TO_NAME.get(cloud_server_key, "Meiju Cloud")

            existing_entries = self.hass.config_entries.async_entries(DOMAIN)
            for entry in existing_entries:
                entry_account = entry.data.get(CONF_ACCOUNT)
                if entry_account == self._account:
                    self._existing_entry = entry
                    self._devices_data = list(entry.data.get("devices", []))
                    break

            return await self.async_step_discover()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "note": "Please enter Meiju Cloud account and password to download device Lua files"
            },
        )

    async def async_step_discover(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        self._discovered_devices = await self.hass.async_add_executor_job(
            discover_devices, DISCOVERY_TIMEOUT, self._scan_address
        )

        if not self._discovered_devices:
            return self.async_show_form(
                step_id="discover",
                errors={"base": "no_devices_found"},
                description_placeholders={"note": "No devices found in LAN"},
            )

        existing_device_ids = {d.get(CONF_DEVICE_ID) for d in self._devices_data}
        self._discovered_devices = {
            did: info for did, info in self._discovered_devices.items()
            if did not in existing_device_ids
        }

        if not self._discovered_devices:
            return self.async_show_form(
                step_id="discover",
                errors={"base": "all_devices_added"},
                description_placeholders={"note": "All discovered devices have already been added"},
            )

        if self._session is None:
            self._session = ClientSession()

            try:
                from .midea_lib.cloud import get_midea_cloud, get_preset_account_cloud

                preset = get_preset_account_cloud()
                self._preset_cloud = get_midea_cloud(
                    cloud_name=preset["cloud_name"],
                    session=self._session,
                    account=preset["username"],
                    password=preset["password"],
                )

                if not await self._preset_cloud.login():
                    _LOGGER.warning("Preset cloud login failed")

                self._user_cloud = get_midea_cloud(
                    cloud_name=self._cloud_name,
                    session=self._session,
                    account=self._account,
                    password=self._password,
                )

                if not await self._user_cloud.login():
                    _LOGGER.warning("User account login failed")
                    await self._cleanup_session()
                    return self.async_abort(reason="auth_failed")

                _LOGGER.info("Cloud login success with %s", self._cloud_name)

                self._cloud_devices = await self._user_cloud.list_appliances(home_id=None) or {}
                _LOGGER.info("Cloud devices list: %s", self._cloud_devices)

                lua_common_dir = get_lua_common_path(self.hass.config.config_dir)
                await self._download_common_lua_files(lua_common_dir)

            except (json.JSONDecodeError, OSError) as err:
                _LOGGER.error("Failed to login to cloud: %s", err)
                await self._cleanup_session()
                return self.async_abort(reason="auth_failed")

        return await self.async_step_select_device()

    async def async_step_select_device(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        device_options = {}

        for did, info in self._discovered_devices.items():
            cloud_device = self._cloud_devices.get(did, {})
            device_name = cloud_device.get("name", DEVICE_TYPES.get(info[CONF_DEVICE_TYPE], f"T0x{info[CONF_DEVICE_TYPE]:02X}"))
            device_options[str(did)] = f"{device_name} ( {info[CONF_IP]} )"

        return self.async_show_menu(
            step_id="select_device",
            menu_options=["select_device_continue", "select_device_rescan"],
            description_placeholders={
                "device_count": str(len(device_options)),
            },
        )

    async def async_step_select_device_continue(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        device_options = {}

        for did, info in self._discovered_devices.items():
            cloud_device = self._cloud_devices.get(did, {})
            device_name = cloud_device.get("name", DEVICE_TYPES.get(info[CONF_DEVICE_TYPE], f"T0x{info[CONF_DEVICE_TYPE]:02X}"))
            device_options[str(did)] = f"{device_name} ( {info[CONF_IP]} )"

        if user_input is not None:
            selected = user_input.get("devices", [])
            if selected:
                self._selected_devices = [
                    self._discovered_devices[int(did)]
                    for did in selected
                ]
                self._current_device_index = 0
                return await self.async_step_get_token()

        all_device_ids = list(device_options.keys())
        return self.async_show_form(
            step_id="select_device_continue",
            data_schema=vol.Schema({
                vol.Required(
                    "devices",
                    description={"suggested_value": all_device_ids}
                ): cv.multi_select(device_options),
            }),
        )

    async def async_step_select_device_rescan(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        return await self.async_step_discover()

    def _save_device_to_json(self, device_data: dict):
        """Save device data to JSON file."""
        try:
            json_dir = get_json_files_path(self.hass.config.config_dir)
            json_dir.mkdir(parents=True, exist_ok=True)

            device_id = device_data.get(CONF_DEVICE_ID)
            device_type_str = device_data.get(CONF_DEVICE_TYPE)
            sn8 = device_data.get(CONF_SN8, "")

            if not device_id or not device_type_str:
                return

            # Convert device_type from string to integer
            try:
                device_type = int(device_type_str, 16)
            except ValueError:
                _LOGGER.error("Invalid device type format: %s", device_type_str)
                return

            json_path = get_device_json_path(self.hass.config.config_dir, device_id, device_type, sn8)

            # Read existing data if file exists
            existing_data = {}
            if json_path.exists():
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                except (json.JSONDecodeError, OSError) as e:
                    _LOGGER.error("Failed to read existing JSON file: %s", e)

            # Update with new data
            existing_data.update(device_data)

            # Write back to file
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            _LOGGER.info("Saved device data to JSON file: %s", json_path)
        except (json.JSONEncodeError, OSError) as e:
            _LOGGER.error("Failed to save device data to JSON file: %s", e)

    async def _validate_token_key(
        self,
        device_id: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
    ) -> bool:
        """Validate token/key by attempting V3 authentication handshake.

        Returns True if authentication succeeds.
        """
        if not token or not key:
            return False

        def _try_auth():
            try:
                from .midea_lib.security import LocalSecurity
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((ip_address, port))
                security = LocalSecurity()
                handshake = security.encode_8370(bytes.fromhex(token), 0x0)
                sock.send(handshake)
                response = sock.recv(256)
                sock.close()
                if len(response) < 72:
                    _LOGGER.debug(
                        "[%s] Token/key validation failed: response too short (%d bytes): %s",
                        device_id, len(response), response.hex(),
                    )
                    return False
                auth_data = response[8:72]
                security.tcp_key(auth_data, bytes.fromhex(key))
                _LOGGER.debug("[%s] Token/key validation passed", device_id)
                return True
            except Exception as e:
                _LOGGER.debug("[%s] Token/key validation error: %s", device_id, e)
                return False

        return await self.hass.async_add_executor_job(_try_auth)

    async def _acquire_validated_token_key(
        self,
        device_id: int,
        ip_address: str,
        port: int,
        protocol: int,
    ) -> tuple:
        """Get validated token/key with fallback chain.

        Tries preset cloud first, validates, falls back to user cloud.
        Returns (token, key, source) tuple.
        """
        is_v3 = protocol == ProtocolVersion.V3
        if not is_v3:
            return "", "", "not_needed"

        # Step 1: Try preset cloud
        if self._preset_cloud:
            try:
                keys = await self._preset_cloud.get_cloud_keys(device_id)
                if keys:
                    method = list(keys.keys())[0]
                    token = keys[method]["token"]
                    key = keys[method]["key"]
                    _LOGGER.info("Got token/key from preset cloud for device %s", device_id)
                    if await self._validate_token_key(device_id, ip_address, port, token, key):
                        return token, key, "preset_cloud"
                    _LOGGER.warning(
                        "Preset cloud token/key invalid for device %s, will try user cloud",
                        device_id,
                    )
            except Exception as e:
                _LOGGER.warning("Preset cloud get_cloud_keys error for device %s: %s", device_id, e)

        # Step 2: Fallback to user's own cloud account
        if self._user_cloud:
            try:
                keys = await self._user_cloud.get_cloud_keys(device_id)
                if keys:
                    method = list(keys.keys())[0]
                    token = keys[method]["token"]
                    key = keys[method]["key"]
                    _LOGGER.info("Got token/key from user cloud for device %s", device_id)
                    if await self._validate_token_key(device_id, ip_address, port, token, key):
                        return token, key, "user_cloud"
                    _LOGGER.warning("User cloud token/key also invalid for device %s", device_id)
            except Exception as e:
                _LOGGER.warning("User cloud get_cloud_keys error for device %s: %s", device_id, e)

        # Step 3: All failed, return empty for manual input
        _LOGGER.warning("No valid token/key found for device %s, manual input required", device_id)
        return "", "", "manual"

    async def async_step_get_token(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if self._current_device_index >= len(self._selected_devices):
            await self._cleanup_session()

            if self._devices_data:
                if self._existing_entry:
                    existing_data = dict(self._existing_entry.data)
                    old_device_ids = {d.get(CONF_DEVICE_ID) for d in existing_data.get("devices", [])}

                    existing_data["devices"] = self._devices_data
                    if CONF_ACCOUNT not in existing_data:
                        existing_data[CONF_ACCOUNT] = self._account
                        existing_data[CONF_PASSWORD] = self._password

                    self.hass.config_entries.async_update_entry(
                        self._existing_entry,
                        data=existing_data,
                    )

                    import asyncio

                    async def reload_in_background():
                        try:
                            await self.hass.config_entries.async_reload(self._existing_entry.entry_id)
                            _LOGGER.info("Background reload completed successfully")
                        except Exception as e:
                            _LOGGER.error("Background reload failed: %s", e)

                    asyncio.create_task(reload_in_background())

                    return self.async_abort(reason="devices_added_background")

                first_device_id = self._devices_data[0].get(CONF_DEVICE_ID) if self._devices_data else None
                first_cloud_device = self._cloud_devices.get(first_device_id, {}) if first_device_id else {}
                home_name = first_cloud_device.get("home_name", "")

                return self.async_create_entry(
                    title=f"Midea | {self._account} | {home_name}" if home_name else f"Midea | {self._account}",
                    data={
                        "devices": self._devices_data,
                        CONF_ACCOUNT: self._account,
                        CONF_PASSWORD: self._password,
                        CONF_SERVER: self._cloud_name,
                    },
                )
            return self.async_abort(reason="no_devices")

        current_device = self._selected_devices[self._current_device_index]
        device_id = current_device[CONF_DEVICE_ID]
        protocol = current_device.get(CONF_PROTOCOL, ProtocolVersion.V3)

        # Ensure protocol has a valid value (V1, V2, or V3), default to V3 if None
        if protocol is None:
            protocol = ProtocolVersion.V3
        is_v3 = protocol == ProtocolVersion.V3

        if user_input is not None:
            lua_file = user_input.get(CONF_LUA_FILE, "")
            token = user_input.get(CONF_TOKEN, "")
            key = user_input.get(CONF_KEY, "")
            device_type = current_device.get(CONF_DEVICE_TYPE)
            sn = current_device.get(CONF_SN, "")
            sn8 = current_device.get(CONF_SN8, "")

            if not lua_file or (is_v3 and (not token or not key)):
                return self._show_token_form(
                    current_device, device_id, protocol, token, key, lua_file,
                    error="Please fill in all required fields" if is_v3 else "Please enter Lua file path"
                )

            from .midea_lib.device import MideaCodec, DeviceController
            lua_common_dir = Path(self.hass.config.config_dir) / LUA_COMMON_PATH
            ip_address = current_device[CONF_IP]

            valid, error_msg = await validate_device(
                self.hass,
                device_id,
                ip_address,
                DEFAULT_PORT,
                token,
                key,
                lua_file,
                protocol,
                sn=sn,
                sn8=sn8,
                device_type=device_type
            )

            if not valid:
                return self._show_token_form(
                    current_device, device_id, protocol, token, key, lua_file,
                    error=error_msg
                )

            device_data = {
                CONF_DEVICE_ID: device_id,
                CONF_IP: current_device[CONF_IP],
                CONF_PORT: DEFAULT_PORT,
                CONF_DEVICE_TYPE: hex(current_device.get(CONF_DEVICE_TYPE)),
                CONF_SN: sn,
                CONF_SN8: sn8,
                CONF_PRODUCT_MODEL: current_device.get(CONF_PRODUCT_MODEL, ""),
                CONF_MODEL_NUMBER: current_device.get(CONF_MODEL_NUMBER, ""),
                CONF_DEVICE_NAME: current_device.get(CONF_DEVICE_NAME, ""),
                CONF_MANUFACTURER_CODE: current_device.get(CONF_MANUFACTURER_CODE, "0000"),
                CONF_CATEGORY: current_device.get(CONF_CATEGORY, ""),
                CONF_TOKEN: token if is_v3 else "",
                CONF_KEY: key if is_v3 else "",
                CONF_LUA_FILE: lua_file,
                CONF_PROTOCOL: protocol,
                CONF_HOME_NAME: current_device.get(CONF_HOME_NAME, ""),
                CONF_ROOM_NAME: current_device.get(CONF_ROOM_NAME, ""),
            }

            existing_index = next(
                (i for i, d in enumerate(self._devices_data) if d.get(CONF_DEVICE_ID) == device_id),
                None
            )
            if existing_index is not None:
                self._devices_data[existing_index] = device_data
            else:
                self._devices_data.append(device_data)

            await self.hass.async_add_executor_job(self._save_device_to_json, device_data)

            self._current_device_index += 1
            return await self.async_step_get_token()

        token = None
        key = None
        lua_file = None

        try:
            ip_address = current_device[CONF_IP]
            token, key, key_source = await self._acquire_validated_token_key(
                device_id, ip_address, DEFAULT_PORT, protocol,
            )
            if token and key:
                _LOGGER.info("Using token/key from %s for device %s", key_source, device_id)

            if self._user_cloud:
                cloud_device = self._cloud_devices.get(device_id, {})

                if cloud_device:
                    current_device[CONF_SN] = cloud_device.get("sn") or current_device.get(CONF_SN, "")
                    current_device[CONF_SN8] = cloud_device.get("sn8") or current_device.get(CONF_SN8, "")
                    current_device[CONF_PRODUCT_MODEL] = cloud_device.get("model") or current_device.get(CONF_PRODUCT_MODEL, "")
                    current_device[CONF_MODEL_NUMBER] = cloud_device.get("model_number") or current_device.get(CONF_MODEL_NUMBER, "")
                    current_device[CONF_DEVICE_NAME] = cloud_device.get("name") or current_device.get(CONF_DEVICE_NAME, "")
                    current_device[CONF_MANUFACTURER_CODE] = cloud_device.get("manufacturer_code") or current_device.get(CONF_MANUFACTURER_CODE, "0000")
                    current_device[CONF_CATEGORY] = cloud_device.get("category") or current_device.get(CONF_CATEGORY, "")
                    current_device[CONF_HOME_NAME] = cloud_device.get("home_name", "")
                    current_device[CONF_ROOM_NAME] = cloud_device.get("room_name", "")

                sn = current_device.get(CONF_SN, "")
                sn8 = current_device.get(CONF_SN8, "")
                model_number = current_device.get(CONF_MODEL_NUMBER)
                device_type = current_device.get(CONF_DEVICE_TYPE)
                manufacturer_code = current_device.get(CONF_MANUFACTURER_CODE, sn[:4] or "0000")

                lua_storage_dir = get_lua_storage_path(self.hass.config.config_dir)
                lua_storage_dir.mkdir(parents=True, exist_ok=True)

                success, downloaded_lua = await download_lua_file(
                    self.hass,
                    self._user_cloud._access_token,
                    sn,
                    device_type,
                    manufacturer_code,
                    model_number,
                    self._cloud_name,
                )

                if success:
                    if sn8:
                        lua_file_path = lua_storage_dir / f"T0x{hex(device_type)[2:].upper()}_{sn8}.lua"
                    else:
                        lua_file_path = lua_storage_dir / f"T0x{hex(device_type)[2:].upper()}.lua"

                    await self.hass.async_add_executor_job(write_file, lua_file_path, downloaded_lua)
                    lua_file = str(lua_file_path)
                    _LOGGER.info("Downloaded Lua file to %s", lua_file)

        except (socket.error, OSError, ValueError, json.JSONDecodeError) as err:
            _LOGGER.error("Failed to get token/key or lua: %s", err)

        device_type = current_device.get(CONF_DEVICE_TYPE)
        sn8 = current_device.get(CONF_SN8, "")
        lua_file_path = get_lua_file_path(self.hass.config.config_dir, device_id, device_type, sn8)

        if not lua_file and lua_file_path.exists():
            lua_file = str(lua_file_path)

        return self._show_token_form(
            current_device, device_id, protocol, token or "", key or "", lua_file or ""
        )

    def _show_token_form(
        self,
        current_device: dict,
        device_id: int,
        protocol: int,
        token: str,
        key: str,
        lua_file: str,
        error: str = ""
    ) -> FlowResult:
        is_v3 = protocol == ProtocolVersion.V3
        device_type = current_device.get(CONF_DEVICE_TYPE)
        sn8 = current_device.get(CONF_SN8, "")

        protocol_name = f"V{protocol}"
        device_name = current_device.get(CONF_DEVICE_NAME, "")
        if not device_name:
            device_name = DEVICE_TYPES.get(device_type, f"Device {device_type}")
        model = current_device.get(CONF_PRODUCT_MODEL, "")

        if is_v3:
            data_schema = vol.Schema({
                vol.Required(CONF_TOKEN, default=token): str,
                vol.Required(CONF_KEY, default=key): str,
                vol.Required(CONF_LUA_FILE, default=lua_file): str,
            })
        else:
            data_schema = vol.Schema({
                vol.Optional(CONF_TOKEN, default=token): str,
                vol.Optional(CONF_KEY, default=key): str,
                vol.Required(CONF_LUA_FILE, default=lua_file): str,
            })

        return self.async_show_form(
            step_id="get_token",
            data_schema=data_schema,
            errors={"base": "lua_error"} if error else None,
            description_placeholders={
                "device_name": device_name,
                "device_model": model if model else "Unknown",
                "device_id": str(device_id),
                "ip_address": current_device[CONF_IP],
                "sn8": sn8 if sn8 else "Unknown",
                "protocol_version": protocol_name,
                "error": f"\n{error}" if error else "",
                "progress": f"({self._current_device_index + 1}/{len(self._selected_devices)})",
                "token_required": "Required" if is_v3 else "Optional (Not needed for V1/V2)",
                "key_required": "Required" if is_v3 else "Optional (Not needed for V1/V2)",
            },
        )

    async def _download_common_lua_files(
        self, storage_dir: Path
    ) -> bool:
        try:
            storage_dir.mkdir(parents=True, exist_ok=True)

            cjson_path, bit_path, cjson_lua, bit_lua = await self.hass.async_add_executor_job(
                ensure_lua_files, str(storage_dir)
            )

            files_to_check = [
                (Path(cjson_path), cjson_lua),
                (Path(bit_path), bit_lua),
            ]

            for file_path, content in files_to_check:
                if file_path.exists():
                    _LOGGER.info("Common Lua file already exists: %s", file_path)
                    continue

                success = await self.hass.async_add_executor_job(
                    write_file, file_path, content
                )
                if success:
                    _LOGGER.info("Created common Lua file: %s", file_path.name)

            return True
        except OSError as err:
            _LOGGER.error("Failed to create common Lua files: %s", err)
            return False

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        return MideaSmartHomeOptionsFlowHandler(config_entry)


class MideaSmartHomeOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self._config_entry = config_entry
        self._account = config_entry.data.get(CONF_ACCOUNT, "")
        self._password = config_entry.data.get(CONF_PASSWORD, "")
        self._cloud_name = config_entry.data.get(CONF_SERVER, "Meiju Cloud")
        self._discovered_devices: dict = {}
        self._selected_devices: list = []
        self._current_device_index: int = 0
        self._devices_data: list = list(config_entry.data.get("devices", []))
        self._session: ClientSession = None
        self._preset_cloud = None
        self._user_cloud = None
        self._cloud_devices: dict = {}

    async def _validate_token_key(
        self,
        device_id: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
    ) -> bool:
        """Validate token/key by attempting V3 authentication handshake.

        Returns True if authentication succeeds.
        """
        if not token or not key:
            return False

        def _try_auth():
            try:
                from .midea_lib.security import LocalSecurity
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((ip_address, port))
                security = LocalSecurity()
                handshake = security.encode_8370(bytes.fromhex(token), 0x0)
                sock.send(handshake)
                response = sock.recv(256)
                sock.close()
                if len(response) < 72:
                    _LOGGER.debug(
                        "[%s] Token/key validation failed: response too short (%d bytes): %s",
                        device_id, len(response), response.hex(),
                    )
                    return False
                auth_data = response[8:72]
                security.tcp_key(auth_data, bytes.fromhex(key))
                _LOGGER.debug("[%s] Token/key validation passed", device_id)
                return True
            except Exception as e:
                _LOGGER.debug("[%s] Token/key validation error: %s", device_id, e)
                return False

        return await self.hass.async_add_executor_job(_try_auth)

    async def _acquire_validated_token_key(
        self,
        device_id: int,
        ip_address: str,
        port: int,
        protocol: int,
    ) -> tuple:
        """Get validated token/key with fallback chain.

        Tries preset cloud first, validates, falls back to user cloud.
        Returns (token, key, source) tuple.
        """
        is_v3 = protocol == ProtocolVersion.V3
        if not is_v3:
            return "", "", "not_needed"

        # Step 1: Try preset cloud
        if self._preset_cloud:
            try:
                keys = await self._preset_cloud.get_cloud_keys(device_id)
                if keys:
                    method = list(keys.keys())[0]
                    token = keys[method]["token"]
                    key = keys[method]["key"]
                    _LOGGER.info("Got token/key from preset cloud for device %s", device_id)
                    if await self._validate_token_key(device_id, ip_address, port, token, key):
                        return token, key, "preset_cloud"
                    _LOGGER.warning(
                        "Preset cloud token/key invalid for device %s, will try user cloud",
                        device_id,
                    )
            except Exception as e:
                _LOGGER.warning("Preset cloud get_cloud_keys error for device %s: %s", device_id, e)

        # Step 2: Fallback to user's own cloud account
        if self._user_cloud:
            try:
                keys = await self._user_cloud.get_cloud_keys(device_id)
                if keys:
                    method = list(keys.keys())[0]
                    token = keys[method]["token"]
                    key = keys[method]["key"]
                    _LOGGER.info("Got token/key from user cloud for device %s", device_id)
                    if await self._validate_token_key(device_id, ip_address, port, token, key):
                        return token, key, "user_cloud"
                    _LOGGER.warning("User cloud token/key also invalid for device %s", device_id)
            except Exception as e:
                _LOGGER.warning("User cloud get_cloud_keys error for device %s: %s", device_id, e)

        # Step 3: All failed, return empty for manual input
        _LOGGER.warning("No valid token/key found for device %s, manual input required", device_id)
        return "", "", "manual"

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        return self.async_show_menu(
            step_id="init",
            menu_options=["add_device", "update_account", "sync_cloud", "clear_cache", "configure_polling"],
        )

    async def async_step_add_device(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            scan_address = user_input.get("scan_address", "auto")
            return await self._discover_devices(scan_address)

        return self.async_show_form(
            step_id="add_device",
            data_schema=vol.Schema({
                vol.Optional("scan_address", default="auto"): str,
            }),
        )

    async def _discover_devices(self, scan_address: str = "auto") -> FlowResult:
        self._discovered_devices = await self.hass.async_add_executor_job(
            discover_devices, DISCOVERY_TIMEOUT, scan_address
        )

        if not self._discovered_devices:
            return self.async_show_form(
                step_id="add_device",
                errors={"base": "no_devices_found"},
                description_placeholders={"note": "No devices found in LAN"},
            )

        existing_device_ids = {d.get(CONF_DEVICE_ID) for d in self._devices_data}
        self._discovered_devices = {
            did: info for did, info in self._discovered_devices.items()
            if did not in existing_device_ids
        }

        if not self._discovered_devices:
            return self.async_show_form(
                step_id="add_device",
                errors={"base": "all_devices_added"},
                description_placeholders={"note": "All discovered devices have already been added"},
            )

        if self._session is None:
            self._session = ClientSession()

            try:
                from .midea_lib.cloud import get_midea_cloud, get_preset_account_cloud

                preset = get_preset_account_cloud()
                self._preset_cloud = get_midea_cloud(
                    cloud_name=preset["cloud_name"],
                    session=self._session,
                    account=preset["username"],
                    password=preset["password"],
                )

                if not await self._preset_cloud.login():
                    _LOGGER.warning("Preset cloud login failed")

                if self._account and self._password:
                    self._user_cloud = get_midea_cloud(
                        cloud_name=self._cloud_name,
                        session=self._session,
                        account=self._account,
                        password=self._password,
                    )

                    if not await self._user_cloud.login():
                        _LOGGER.warning("User account login failed")

                    _LOGGER.info("Cloud login success")
                    self._cloud_devices = await self._user_cloud.list_appliances(home_id=None) or {}
                    _LOGGER.info("Cloud devices list: %s", self._cloud_devices)

                lua_common_dir = get_lua_common_path(self.hass.config.config_dir)
                await self._download_common_lua_files(lua_common_dir)

            except (json.JSONDecodeError, OSError) as err:
                _LOGGER.error("Failed to login to cloud: %s", err)
                await self._cleanup_session()

        return await self.async_step_select_device_option()

    async def async_step_select_device_option(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        device_options = {}

        for did, info in self._discovered_devices.items():
            cloud_device = self._cloud_devices.get(did, {})
            device_name = cloud_device.get("name", DEVICE_TYPES.get(info[CONF_DEVICE_TYPE], f"T0x{info[CONF_DEVICE_TYPE]:02X}"))
            device_options[str(did)] = f"{device_name} ( {info[CONF_IP]} )"

        return self.async_show_menu(
            step_id="select_device_option",
            menu_options=["select_device_continue_option", "select_device_rescan_option"],
            description_placeholders={
                "device_count": str(len(device_options)),
            },
        )

    async def async_step_select_device_continue_option(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        device_options = {}

        for did, info in self._discovered_devices.items():
            cloud_device = self._cloud_devices.get(did, {})
            device_name = cloud_device.get("name", DEVICE_TYPES.get(info[CONF_DEVICE_TYPE], f"T0x{info[CONF_DEVICE_TYPE]:02X}"))
            device_options[str(did)] = f"{device_name} ( {info[CONF_IP]} )"

        if user_input is not None:
            selected = user_input.get("devices", [])
            if selected:
                self._selected_devices = [
                    self._discovered_devices[int(did)]
                    for did in selected
                ]
                self._current_device_index = 0
                return await self.async_step_get_token_option()

        all_device_ids = list(device_options.keys())
        return self.async_show_form(
            step_id="select_device_continue_option",
            data_schema=vol.Schema({
                vol.Required(
                    "devices",
                    description={"suggested_value": all_device_ids}
                ): cv.multi_select(device_options),
            }),
        )

    async def async_step_select_device_rescan_option(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        return await self._discover_devices()

    async def async_step_get_token_option(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if self._current_device_index >= len(self._selected_devices):
            await self._cleanup_session()

            if self._devices_data:
                new_data = dict(self._config_entry.data)
                old_device_ids = {d.get(CONF_DEVICE_ID) for d in new_data.get("devices", [])}

                new_data["devices"] = self._devices_data
                self.hass.config_entries.async_update_entry(
                    self._config_entry,
                    data=new_data,
                )

                import asyncio

                async def reload_in_background():
                    try:
                        await self.hass.config_entries.async_reload(self._config_entry.entry_id)
                        _LOGGER.info("Background reload completed successfully")
                    except Exception as e:
                        _LOGGER.error("Background reload failed: %s", e)

                asyncio.create_task(reload_in_background())

                return self.async_create_entry(title="", data={})
            return self.async_abort(reason="no_devices")

        current_device = self._selected_devices[self._current_device_index]
        device_id = current_device[CONF_DEVICE_ID]
        protocol = current_device.get(CONF_PROTOCOL, ProtocolVersion.V3)

        if protocol is None:
            protocol = ProtocolVersion.V3
        is_v3 = protocol == ProtocolVersion.V3

        if user_input is not None:
            lua_file = user_input.get(CONF_LUA_FILE, "")
            token = user_input.get(CONF_TOKEN, "")
            key = user_input.get(CONF_KEY, "")
            device_type = current_device.get(CONF_DEVICE_TYPE)
            sn = current_device.get(CONF_SN, "")
            sn8 = current_device.get(CONF_SN8, "")

            if not lua_file or (is_v3 and (not token or not key)):
                return self._show_token_form_option(
                    current_device, device_id, protocol, token, key, lua_file,
                    error="Please fill in all required fields" if is_v3 else "Please enter Lua file path"
                )

            from .midea_lib.device import MideaCodec, DeviceController
            lua_common_dir = Path(self.hass.config.config_dir) / LUA_COMMON_PATH
            ip_address = current_device[CONF_IP]

            valid, error_msg = await validate_device(
                self.hass,
                device_id,
                ip_address,
                DEFAULT_PORT,
                token,
                key,
                lua_file,
                protocol,
                sn=sn,
                sn8=sn8,
                device_type=device_type
            )

            if not valid:
                return self._show_token_form_option(
                    current_device, device_id, protocol, token, key, lua_file,
                    error=error_msg
                )

            device_data = {
                CONF_DEVICE_ID: device_id,
                CONF_IP: current_device[CONF_IP],
                CONF_PORT: DEFAULT_PORT,
                CONF_DEVICE_TYPE: hex(current_device.get(CONF_DEVICE_TYPE)),
                CONF_SN: sn,
                CONF_SN8: sn8,
                CONF_PRODUCT_MODEL: current_device.get(CONF_PRODUCT_MODEL, ""),
                CONF_MODEL_NUMBER: current_device.get(CONF_MODEL_NUMBER, ""),
                CONF_DEVICE_NAME: current_device.get(CONF_DEVICE_NAME, ""),
                CONF_MANUFACTURER_CODE: current_device.get(CONF_MANUFACTURER_CODE, "0000"),
                CONF_CATEGORY: current_device.get(CONF_CATEGORY, ""),
                CONF_TOKEN: token if is_v3 else "",
                CONF_KEY: key if is_v3 else "",
                CONF_LUA_FILE: lua_file,
                CONF_PROTOCOL: protocol,
                CONF_HOME_NAME: current_device.get(CONF_HOME_NAME, ""),
                CONF_ROOM_NAME: current_device.get(CONF_ROOM_NAME, ""),
            }

            existing_index = next(
                (i for i, d in enumerate(self._devices_data) if d.get(CONF_DEVICE_ID) == device_id),
                None
            )
            if existing_index is not None:
                self._devices_data[existing_index] = device_data
            else:
                self._devices_data.append(device_data)

            await self.hass.async_add_executor_job(self._save_device_to_json, device_data)

            self._current_device_index += 1
            return await self.async_step_get_token_option()

        token = None
        key = None
        lua_file = None

        try:
            ip_address = current_device[CONF_IP]
            token, key, key_source = await self._acquire_validated_token_key(
                device_id, ip_address, DEFAULT_PORT, protocol,
            )
            if token and key:
                _LOGGER.info("Using token/key from %s for device %s", key_source, device_id)

            if self._user_cloud:
                cloud_device = self._cloud_devices.get(device_id, {})

                if cloud_device:
                    current_device[CONF_SN] = cloud_device.get("sn") or current_device.get(CONF_SN, "")
                    current_device[CONF_SN8] = cloud_device.get("sn8") or current_device.get(CONF_SN8, "")
                    current_device[CONF_PRODUCT_MODEL] = cloud_device.get("model") or current_device.get(CONF_PRODUCT_MODEL, "")
                    current_device[CONF_MODEL_NUMBER] = cloud_device.get("model_number") or current_device.get(CONF_MODEL_NUMBER, "")
                    current_device[CONF_DEVICE_NAME] = cloud_device.get("name") or current_device.get(CONF_DEVICE_NAME, "")
                    current_device[CONF_MANUFACTURER_CODE] = cloud_device.get("manufacturer_code") or current_device.get(CONF_MANUFACTURER_CODE, "0000")
                    current_device[CONF_CATEGORY] = cloud_device.get("category") or current_device.get(CONF_CATEGORY, "")

                sn = current_device.get(CONF_SN, "")
                sn8 = current_device.get(CONF_SN8, "")
                model_number = current_device.get(CONF_MODEL_NUMBER)
                device_type = current_device.get(CONF_DEVICE_TYPE)
                manufacturer_code = current_device.get(CONF_MANUFACTURER_CODE, sn[:4] or "0000")

                lua_storage_dir = get_lua_storage_path(self.hass.config.config_dir)
                lua_storage_dir.mkdir(parents=True, exist_ok=True)

                success, downloaded_lua = await download_lua_file(
                    self.hass,
                    self._user_cloud._access_token,
                    sn,
                    device_type,
                    manufacturer_code,
                    model_number,
                    self._cloud_name,
                )

                if success:
                    if sn8:
                        lua_file_path = lua_storage_dir / f"T0x{hex(device_type)[2:].upper()}_{sn8}.lua"
                    else:
                        lua_file_path = lua_storage_dir / f"T0x{hex(device_type)[2:].upper()}.lua"

                    await self.hass.async_add_executor_job(write_file, lua_file_path, downloaded_lua)
                    lua_file = str(lua_file_path)
                    _LOGGER.info("Downloaded Lua file to %s", lua_file)

        except (socket.error, OSError, ValueError, json.JSONDecodeError) as err:
            _LOGGER.error("Failed to get token/key or lua: %s", err)

        device_type = current_device.get(CONF_DEVICE_TYPE)
        sn8 = current_device.get(CONF_SN8, "")
        lua_file_path = get_lua_file_path(self.hass.config.config_dir, device_id, device_type, sn8)

        if not lua_file and lua_file_path.exists():
            lua_file = str(lua_file_path)

        return self._show_token_form_option(
            current_device, device_id, protocol, token or "", key or "", lua_file or ""
        )

    def _show_token_form_option(
        self,
        current_device: dict,
        device_id: int,
        protocol: int,
        token: str,
        key: str,
        lua_file: str,
        error: str = ""
    ) -> FlowResult:
        is_v3 = protocol == ProtocolVersion.V3
        device_type = current_device.get(CONF_DEVICE_TYPE)
        sn8 = current_device.get(CONF_SN8, "")

        protocol_name = f"V{protocol}"
        device_name = current_device.get(CONF_DEVICE_NAME, "")
        if not device_name:
            device_name = DEVICE_TYPES.get(device_type, f"Device {device_type}")
        model = current_device.get(CONF_PRODUCT_MODEL, "")

        if is_v3:
            data_schema = vol.Schema({
                vol.Required(CONF_TOKEN, default=token): str,
                vol.Required(CONF_KEY, default=key): str,
                vol.Required(CONF_LUA_FILE, default=lua_file): str,
            })
        else:
            data_schema = vol.Schema({
                vol.Optional(CONF_TOKEN, default=token): str,
                vol.Optional(CONF_KEY, default=key): str,
                vol.Required(CONF_LUA_FILE, default=lua_file): str,
            })

        return self.async_show_form(
            step_id="get_token_option",
            data_schema=data_schema,
            errors={"base": "lua_error"} if error else None,
            description_placeholders={
                "device_name": device_name,
                "device_model": model if model else "Unknown",
                "device_id": str(device_id),
                "ip_address": current_device[CONF_IP],
                "sn8": sn8 if sn8 else "Unknown",
                "protocol_version": protocol_name,
                "error": f"\n{error}" if error else "",
                "progress": f"({self._current_device_index + 1}/{len(self._selected_devices)})",
                "token_required": "Required" if is_v3 else "Optional (Not needed for V1/V2)",
                "key_required": "Required" if is_v3 else "Optional (Not needed for V1/V2)",
            },
        )

    async def _cleanup_session(self):
        if self._session:
            await self._session.close()
            self._session = None

    def _save_device_to_json(self, device_data: dict):
        try:
            json_dir = get_json_files_path(self.hass.config.config_dir)
            json_dir.mkdir(parents=True, exist_ok=True)

            device_id = device_data.get(CONF_DEVICE_ID)
            device_type_str = device_data.get(CONF_DEVICE_TYPE)
            sn8 = device_data.get(CONF_SN8, "")

            if not device_id or not device_type_str:
                return

            try:
                device_type = int(device_type_str, 16)
            except ValueError:
                _LOGGER.error("Invalid device type format: %s", device_type_str)
                return

            json_path = get_device_json_path(self.hass.config.config_dir, device_id, device_type, sn8)

            existing_data = {}
            if json_path.exists():
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                except (json.JSONDecodeError, OSError) as e:
                    _LOGGER.error("Failed to read existing JSON file: %s", e)

            existing_data.update(device_data)

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            _LOGGER.info("Saved device data to JSON file: %s", json_path)
        except (json.JSONEncodeError, OSError) as e:
            _LOGGER.error("Failed to save device data to JSON file: %s", e)

    async def _download_common_lua_files(
        self, storage_dir: Path
    ) -> bool:
        try:
            storage_dir.mkdir(parents=True, exist_ok=True)

            cjson_path, bit_path, cjson_lua, bit_lua = await self.hass.async_add_executor_job(
                ensure_lua_files, str(storage_dir)
            )

            files_to_check = [
                (Path(cjson_path), cjson_lua),
                (Path(bit_path), bit_lua),
            ]

            for file_path, content in files_to_check:
                if file_path.exists():
                    _LOGGER.info("Common Lua file already exists: %s", file_path)
                    continue

                success = await self.hass.async_add_executor_job(
                    write_file, file_path, content
                )
                if success:
                    _LOGGER.info("Created common Lua file: %s", file_path.name)

            return True
        except OSError as err:
            _LOGGER.error("Failed to create common Lua files: %s", err)
            return False

    async def async_step_update_account(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            new_data = dict(self._config_entry.data)
            if user_input.get(CONF_ACCOUNT):
                new_data[CONF_ACCOUNT] = user_input[CONF_ACCOUNT]
            if user_input.get(CONF_PASSWORD):
                new_data[CONF_PASSWORD] = user_input[CONF_PASSWORD]
            cloud_server_key = user_input.get(CONF_SERVER, None)
            if cloud_server_key is not None:
                new_data[CONF_SERVER] = CLOUD_KEY_TO_NAME.get(cloud_server_key, self._cloud_name)

            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data=new_data,
            )
            return self.async_create_entry(title="", data={})

        current_cloud_key = next(
            (k for k, v in CLOUD_KEY_TO_NAME.items() if v == self._cloud_name),
            1,
        )

        return self.async_show_form(
            step_id="update_account",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_ACCOUNT,
                    default=self._account,
                ): str,
                vol.Optional(
                    CONF_PASSWORD,
                    default=self._password,
                ): str,
                vol.Optional(
                    CONF_SERVER,
                    default=current_cloud_key,
                ): vol.In(CLOUD_SERVERS),
            }),
        )

    async def async_step_sync_cloud(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            new_data = dict(self._config_entry.data)

            if not self._account or not self._password:
                return self.async_show_form(
                    step_id="sync_cloud",
                    errors={"base": "no_account_password"},
                )

            devices = new_data.get("devices", [])
            devices, home_name = await self._refresh_cloud_device_info(devices)
            new_data["devices"] = devices
            new_title = f"Midea | {self._account} | {home_name}" if home_name else f"Midea | {self._account}"
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                title=new_title,
                data=new_data,
            )
            await self.hass.config_entries.async_reload(self._config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="sync_cloud",
        )

    async def async_step_clear_cache(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            storage_path = Path(self.hass.config.config_dir) / ".storage" / DOMAIN
            backup_path = Path(self.hass.config.config_dir) / ".storage" / f"{DOMAIN}-backup"

            if not storage_path.exists():
                return self.async_show_form(
                    step_id="clear_cache",
                    errors={"base": "no_cache_found"},
                )

            def _clear_cache():
                if backup_path.exists():
                    import shutil
                    shutil.rmtree(backup_path)
                storage_path.rename(backup_path)

            await self.hass.async_add_executor_job(_clear_cache)
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="clear_cache",
        )

    async def _refresh_cloud_device_info(self, devices: list) -> tuple[list, str]:
        """Refresh device info from cloud."""
        from .midea_lib.cloud import get_midea_cloud

        cloud_device_info = {}
        home_name = ""
        session = ClientSession()
        try:
            cloud = get_midea_cloud(
                cloud_name=self._cloud_name,
                session=session,
                account=self._account,
                password=self._password,
            )
            if await cloud.login():
                device_ids = [d.get(CONF_DEVICE_ID) for d in devices if d.get(CONF_DEVICE_ID)]
                cloud_devices = await cloud.list_appliances(home_id=None) or {}
                for device_id in device_ids:
                    if device_id in cloud_devices:
                        device = cloud_devices[device_id]
                        if not home_name:
                            home_name = device.get("home_name", "")
                        cloud_device_info[device_id] = {
                            CONF_SN: device.get("sn", ""),
                            CONF_SN8: device.get("sn8", ""),
                            CONF_PRODUCT_MODEL: device.get("model", ""),
                            CONF_MODEL_NUMBER: device.get("model_number", ""),
                            CONF_DEVICE_NAME: device.get("name", ""),
                            CONF_CATEGORY: device.get("category", ""),
                            CONF_HOME_NAME: device.get("home_name", ""),
                            CONF_ROOM_NAME: device.get("room_name", ""),
                        }
                _LOGGER.info("Refreshed device info from cloud for %d devices", len(cloud_device_info))
        except (socket.error, OSError, ValueError, json.JSONDecodeError) as err:
            _LOGGER.warning("Failed to refresh device info from cloud: %s", err)
        finally:
            await session.close()

        for device in devices:
            device_id = device.get(CONF_DEVICE_ID)
            if device_id in cloud_device_info:
                device.update(cloud_device_info[device_id])

        return devices, home_name

    async def async_step_configure_polling(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure polling interval for devices with polling_attributes."""
        from homeassistant.helpers import translation as ha_translation

        devices = self._devices_data

        # Get translations for current language
        current_language = self.hass.config.language or "en"
        translations = await ha_translation.async_get_translations(
            self.hass, current_language, "options", {DOMAIN}
        )

        def _translate(key: str, default: str) -> str:
            """Get translated string from translations dict."""
            full_key = f"options.step.configure_polling.data.{key}"
            for k in [full_key, f"component.{DOMAIN}.{full_key}"]:
                if k in translations:
                    return translations[k]
            return default

        # Find devices that have polling_attributes configured in their device_mapping
        from .device_mapping import get_device_mapping
        configurable_devices = []

        # Define polling options: disabled and intervals in seconds
        polling_options = {
            "disabled": _translate("option_disabled", "off"),
            "1": _translate("option_1s", "1s"),
            "2": _translate("option_2s", "2s"),
            "3": _translate("option_3s", "3s"),
            "4": _translate("option_4s", "4s"),
            "5": _translate("option_5s", "5s"),
            "10": _translate("option_10s", "10s"),
            "15": _translate("option_15s", "15s"),
            "20": _translate("option_20s", "20s"),
            "25": _translate("option_25s", "25s"),
            "30": _translate("option_30s", "30s"),
        }

        for device in devices:
            device_id = device.get(CONF_DEVICE_ID)
            device_type_str = device.get(CONF_DEVICE_TYPE, "0")
            model = device.get(CONF_PRODUCT_MODEL, "")
            sn8 = device.get(CONF_SN8, "")
            category = device.get(CONF_CATEGORY, "")

            try:
                device_type_int = int(device_type_str, 16) if isinstance(device_type_str, str) else 0
            except ValueError:
                device_type_int = 0

            device_mapping = get_device_mapping(device_type_int, model, sn8, category)
            polling_query = device_mapping.get("polling_query")
            # Check if device supports polling (based on existence of polling_query)
            enable_polling = polling_query is not None and isinstance(polling_query, list) and len(polling_query) > 0

            if enable_polling:
                device_name = device.get(CONF_DEVICE_NAME, f"Device {device_id}")
                current_interval = device.get("polling_interval", 30)
                polling_enabled = device.get("polling_enabled", True)

                # Determine current selection based on enabled status and interval
                if not polling_enabled:
                    current_selection = "disabled"
                else:
                    current_selection = str(current_interval)

                configurable_devices.append({
                    "device_id": device_id,
                    "device_name": device_name,
                    "current_selection": current_selection,
                })

        if not configurable_devices:
            return self.async_show_form(
                step_id="configure_polling",
                errors={"base": "no_configurable_devices"},
                description_placeholders={"note": "No devices with polling attributes found"}
            )

        # Build form schema with Select dropdown for each device
        schema_dict = {}
        device_name_count = {}
        device_info_lines = []

        polling_status_label = _translate("polling_status_label", "Polling: {status}")

        for i, device_info in enumerate(configurable_devices, 1):
            device_id = device_info["device_id"]
            device_name = device_info["device_name"]
            current_selection = device_info["current_selection"]

            if device_name in device_name_count:
                device_name_count[device_name] += 1
                base_key = f"{device_name}_{device_name_count[device_name]}"
            else:
                device_name_count[device_name] = 1
                base_key = device_name

            # Create a single Select dropdown instead of boolean + slider
            schema_dict[vol.Optional(base_key, default=current_selection)] = vol.In(polling_options)

            if not hasattr(self, '_polling_device_mapping'):
                self._polling_device_mapping = {}
            self._polling_device_mapping[base_key] = {
                'device_id': device_id,
                'device_name': device_name,
            }

            # Get display text for current selection
            selection_text = polling_options.get(current_selection, current_selection)
            device_info_lines.append(f"{i}. {device_name} ({device_id}) - {selection_text}")

        device_info_text = "\n".join(device_info_lines)
        placeholders = {
            "device_count": str(len(configurable_devices)),
            "device_info": device_info_text
        }

        if user_input is not None:
            # Update polling settings for selected devices
            import copy
            new_data = copy.deepcopy(dict(self._config_entry.data))
            updated = False

            devices_list = new_data.get("devices", [])

            # Use the mapping to find which device corresponds to each field
            for base_key, device_info in getattr(self, '_polling_device_mapping', {}).items():
                device_id = device_info['device_id']

                # Find the device in devices list
                for device in devices_list:
                    if device.get(CONF_DEVICE_ID) == device_id:
                        # Get selected value from dropdown
                        if base_key in user_input:
                            selected_value = user_input[base_key]

                            if selected_value == "disabled":
                                # Polling disabled
                                device["polling_enabled"] = False
                                _LOGGER.debug(
                                    "Disabled polling for device %s (%s)",
                                    device_info['device_name'],
                                    device_id
                                )
                            else:
                                # Polling enabled with specific interval
                                try:
                                    interval = int(selected_value)
                                    device["polling_enabled"] = True
                                    device["polling_interval"] = interval
                                    _LOGGER.debug(
                                        "Set polling interval for device %s (%s) to %d seconds",
                                        device_info['device_name'],
                                        device_id,
                                        interval
                                    )
                                except (ValueError, TypeError):
                                    _LOGGER.warning(
                                        "Invalid polling value '%s' for device %s (%s)",
                                        selected_value,
                                        device_info['device_name'],
                                        device_id
                                    )

                            updated = True
                        break

            # Always update the entry to ensure changes are saved
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data=new_data,
            )

            _LOGGER.info("Polling configuration saved, updated=%s", updated)

            if updated:
                # Reload to apply changes
                await self.hass.config_entries.async_reload(self._config_entry.entry_id)

            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="configure_polling",
            data_schema=vol.Schema(schema_dict),
            description_placeholders=placeholders,
            last_step=False,
        )
