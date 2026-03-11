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
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_IP,
    CONF_KEY,
    CONF_LUA_FILE,
    CONF_MANUFACTURER_CODE,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_PROTOCOL,
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
    LUA_DEVICE_PATH,
    ProtocolVersion,
)
from .midea_lib.packet_builder import PacketBuilder
from .midea_lib.discovery import discover_devices, DISCOVERY_TIMEOUT
from .midea_lib.lua import write_file, decrypt_lua_code, ensure_lua_files
from .midea_lib.setup import validate_device
from .midea_lib.cloud import download_lua_file

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_ACCOUNT): str,
    vol.Required(CONF_PASSWORD): str,
})

def get_lua_storage_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / LUA_DEVICE_PATH

def get_lua_common_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / LUA_COMMON_PATH

def get_lua_file_path(hass_config_dir: str, device_id: int, device_type: int, sn8: str = "") -> Path:
    if sn8:
        return get_lua_storage_path(hass_config_dir) / f"{device_id}_T0x{hex(device_type)[2:].upper()}_{sn8}.lua"
    return get_lua_storage_path(hass_config_dir) / f"{device_id}_T0x{hex(device_type)[2:]}.lua"

def get_json_files_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / JSON_FILES_PATH

def get_device_json_path(hass_config_dir: str, device_id: int, device_type: int, sn8: str = "") -> Path:
    if sn8:
        return get_json_files_path(hass_config_dir) / f"{device_id}_T0x{hex(device_type)[2:].upper()}_{sn8}.json"
    return get_json_files_path(hass_config_dir) / f"{device_id}_T0x{hex(device_type)[2:]}.json"


class MideaSmartHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._discovered_devices: dict = {}
        self._selected_devices: list = []
        self._current_device_index: int = 0
        self._devices_data: list = []
        self._account: str = None
        self._password: str = None
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

            existing_entries = self.hass.config_entries.async_entries(DOMAIN)
            for entry in existing_entries:
                if entry.title == f"Midea | {self._account}":
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
            discover_devices, DISCOVERY_TIMEOUT
        )

        if not self._discovered_devices:
            return self.async_show_form(
                step_id="discover",
                errors={"base": "no_devices_found"},
                description_placeholders={"note": "No devices found in LAN"},
            )

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
                cloud_name="Meiju Cloud",
                session=self._session,
                account=self._account,
                password=self._password,
            )

            if not await self._user_cloud.login():
                _LOGGER.warning("User account login failed")
                await self._cleanup_session()
                return self.async_abort(reason="auth_failed")

            _LOGGER.info("Cloud login success")

            self._cloud_devices = await self._user_cloud.list_appliances(home_id=None) or {}
            _LOGGER.info("Cloud devices list: %s", self._cloud_devices)

            lua_common_dir = get_lua_common_path(self.hass.config.config_dir)
            await self._download_common_lua_files(lua_common_dir)

        except (json.JSONDecodeError, OSError) as err:
            _LOGGER.error("Failed to login to cloud: %s", err)
            await self._cleanup_session()
            return self.async_abort(reason="auth_failed")

        device_options = {}

        for did, info in self._discovered_devices.items():
            cloud_device = self._cloud_devices.get(did, {})
            device_name = cloud_device.get("name", DEVICE_TYPES.get(info[CONF_DEVICE_TYPE], f"T0x{info[CONF_DEVICE_TYPE]:02X}"))
            device_options[str(did)] = f"{device_name} ( {info[CONF_IP]} )"

        return self.async_show_form(
            step_id="select_device",
            data_schema=vol.Schema({
                vol.Required("devices"): cv.multi_select(device_options),
            }),
        )

    async def async_step_select_device(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is None:
            return self.async_abort(reason="no_devices_selected")

        selected = user_input.get("devices", [])
        if not selected:
            return self.async_abort(reason="no_devices_selected")

        self._selected_devices = [
            self._discovered_devices[int(did)]
            for did in selected
        ]
        self._current_device_index = 0

        return await self.async_step_get_token()

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

    async def async_step_get_token(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if self._current_device_index >= len(self._selected_devices):
            await self._cleanup_session()

            if self._devices_data:
                if self._existing_entry:
                    existing_data = dict(self._existing_entry.data)
                    existing_data["devices"] = self._devices_data
                    if CONF_ACCOUNT not in existing_data:
                        existing_data[CONF_ACCOUNT] = self._account
                        existing_data[CONF_PASSWORD] = self._password
                    self.hass.config_entries.async_update_entry(
                        self._existing_entry,
                        data=existing_data,
                    )
                    await self.hass.config_entries.async_reload(self._existing_entry.entry_id)
                    return self.async_abort(reason="devices_updated")
                return self.async_create_entry(
                    title=f"Midea | {self._account}",
                    data={
                        "devices": self._devices_data,
                        CONF_ACCOUNT: self._account,
                        CONF_PASSWORD: self._password,
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
                CONF_TOKEN: token if is_v3 else "",
                CONF_KEY: key if is_v3 else "",
                CONF_LUA_FILE: lua_file,
                CONF_PROTOCOL: protocol,
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
            if is_v3 and self._preset_cloud:
                keys = await self._preset_cloud.get_cloud_keys(device_id)
                if keys:
                    method = list(keys.keys())[0]
                    token = keys[method]["token"]
                    key = keys[method]["key"]
                    _LOGGER.info("Got token/key for device %s", device_id)

            if self._user_cloud:
                cloud_device = self._cloud_devices.get(device_id, {})

                if cloud_device:
                    current_device[CONF_SN] = cloud_device.get("sn") or current_device.get(CONF_SN, "")
                    current_device[CONF_SN8] = cloud_device.get("sn8") or current_device.get(CONF_SN8, "")
                    current_device[CONF_PRODUCT_MODEL] = cloud_device.get("model") or current_device.get(CONF_PRODUCT_MODEL, "")
                    current_device[CONF_MODEL_NUMBER] = cloud_device.get("model_number") or current_device.get(CONF_MODEL_NUMBER, "")
                    current_device[CONF_DEVICE_NAME] = cloud_device.get("name") or current_device.get(CONF_DEVICE_NAME, "")
                    current_device[CONF_MANUFACTURER_CODE] = cloud_device.get("manufacturer_code") or current_device.get(CONF_MANUFACTURER_CODE, "0000")

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
                    model_number
                )
                
                if success:
                    if sn8:
                        lua_file_path = lua_storage_dir / f"{device_id}_T0x{hex(device_type)[2:].upper()}_{sn8}.lua"
                    else:
                        lua_file_path = lua_storage_dir / f"{device_id}_T0x{hex(device_type)[2:]}.lua"
                    
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

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            new_data = dict(self._config_entry.data)

            account = user_input.get(CONF_ACCOUNT) or self._account
            password = user_input.get(CONF_PASSWORD) or self._password

            if user_input.get("refresh_cloud"):
                if account and password:
                    self._account = account
                    self._password = password
                    devices = new_data.get("devices", [])
                    devices = await self._refresh_cloud_device_info(devices)
                    new_data["devices"] = devices
                    new_data[CONF_ACCOUNT] = account
                    new_data[CONF_PASSWORD] = password
                    self.hass.config_entries.async_update_entry(
                        self._config_entry,
                        data=new_data,
                    )
                    return self.async_create_entry(title="", data={})
                return self.async_show_form(
                    step_id="init",
                    errors={"base": "no_account_password"},
                    description_placeholders={"note": "Please configure account and password first"},
                )

            if user_input.get(CONF_ACCOUNT):
                new_data[CONF_ACCOUNT] = user_input[CONF_ACCOUNT]
            if user_input.get(CONF_PASSWORD):
                new_data[CONF_PASSWORD] = user_input[CONF_PASSWORD]

            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data=new_data,
            )
            return self.async_create_entry(title="", data={})

        options = self._config_entry.options
        return self.async_show_form(
            step_id="init",
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
                    "refresh_cloud",
                    default=False,
                ): bool,
            }),
        )

    async def _refresh_cloud_device_info(self, devices: list) -> list:
        """Refresh device info from cloud."""
        from .midea_lib.cloud import get_midea_cloud

        cloud_device_info = {}
        session = ClientSession()
        try:
            cloud = get_midea_cloud(
                cloud_name="Meiju Cloud",
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
                        cloud_device_info[device_id] = {
                            CONF_SN: device.get("sn", ""),
                            CONF_SN8: device.get("sn8", ""),
                            CONF_PRODUCT_MODEL: device.get("model", ""),
                            CONF_MODEL_NUMBER: device.get("model_number", ""),
                            CONF_DEVICE_NAME: device.get("name", ""),
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

        return devices
