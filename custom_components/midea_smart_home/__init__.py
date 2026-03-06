import logging
import os
import base64
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import UpdateFailed
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_IP,
    CONF_KEY,
    CONF_LUA_FILE,
    CONF_PRODUCT_MODEL,
    CONF_MODEL_NUMBER,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_SN,
    CONF_SN8,
    CONF_TOKEN,
    DEFAULT_PORT,
    DEVICE_TYPES,
    DEVICE_TYPES_ZH,
    DOMAIN,
    PLATFORMS,
    CJSON_LUA,
    BIT_LUA,
    LUA_COMMON_PATH,
    ProtocolVersion,
)
from .coordinator import MideaCoordinator
from .device import DeviceController, MideaCodec
from .device_mapping import get_device_mapping, get_queries, get_centralized, get_default_values, get_respose

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

def _write_lua_file(file_path: str, content: str) -> bool:
    try:
        with open(file_path, "w", encoding="utf-8") as fp:
            fp.write(content)
        return True
    except PermissionError as e:
        _LOGGER.error("Failed to create %s: %s", file_path, e)
        return False

def _ensure_lua_files(lua_path: str) -> tuple:
    cjson = os.path.join(lua_path, "cjson.lua")
    bit = os.path.join(lua_path, "bit.lua")
    
    cjson_lua = base64.b64decode(CJSON_LUA.encode("utf-8")).decode("utf-8")
    bit_lua = base64.b64decode(BIT_LUA.encode("utf-8")).decode("utf-8")
    
    return cjson, bit, cjson_lua, bit_lua

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.data.setdefault(DOMAIN, {})
    
    lua_path = hass.config.path(LUA_COMMON_PATH)
    os.makedirs(lua_path, exist_ok=True)
    
    cjson, bit, cjson_lua, bit_lua = await hass.async_add_executor_job(
        _ensure_lua_files, lua_path
    )
    
    if not os.path.exists(cjson):
        success = await hass.async_add_executor_job(_write_lua_file, cjson, cjson_lua)
        if success:
            _LOGGER.info("Created cjson.lua at %s", cjson)
    
    if not os.path.exists(bit):
        success = await hass.async_add_executor_job(_write_lua_file, bit, bit_lua)
        if success:
            _LOGGER.info("Created bit.lua at %s", bit)

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})
    
    devices = entry.data.get("devices", [])
    if not devices:
        devices = [entry.data]
    
    update_interval = entry.options.get("update_interval", 1)
    language = hass.config.language or "en"
    
    for device_data in devices:
        device_id = device_data[CONF_DEVICE_ID]
        ip_address = device_data.get(CONF_IP, "")
        port = device_data.get(CONF_PORT, DEFAULT_PORT)
        token = device_data.get(CONF_TOKEN, "")
        key = device_data.get(CONF_KEY, "")
        lua_file = device_data.get(CONF_LUA_FILE, "")
        sn = device_data.get(CONF_SN, "")
        sn8 = device_data.get(CONF_SN8, "")
        device_type = device_data.get(CONF_DEVICE_TYPE)
        device_type_int = int(device_type, 16) if isinstance(device_type, str) else 0
        
        device_name = device_data.get(CONF_DEVICE_NAME, "")
        if not device_name:
            if language.startswith("zh"):
                device_name = DEVICE_TYPES_ZH.get(device_type_int, f"设备 {device_type}")
            else:
                device_name = DEVICE_TYPES.get(device_type_int, f"Device {device_type}")
        
        protocol = device_data.get(CONF_PROTOCOL, ProtocolVersion.V3)
        
        lua_common_dir = Path(hass.config.config_dir) / LUA_COMMON_PATH
        
        def init_device():
            codec = MideaCodec(lua_file, str(lua_common_dir), sn=sn, subtype=0, device_type=device_type_int, sn8=sn8)
            controller = DeviceController(
                device_id=device_id,
                ip_address=ip_address,
                port=port,
                token=token,
                key=key,
                codec=codec,
                protocol=protocol,
            )
            if controller.connect():
                return controller
            return None
        
        controller = await hass.async_add_executor_job(init_device)
        if not controller:
            _LOGGER.warning("Device %s initialization failed", device_id)
            continue
        
        device_mapping = get_device_mapping(device_type_int, sn8)
        calculate_config = device_mapping.get("calculate", {})
        queries = get_queries(device_type_int, sn8)
        centralized = get_centralized(device_type_int, sn8)
        default_values = get_default_values(device_type_int, sn8)
        respose = get_respose(device_type_int, sn8)

        entities_cfg = (device_mapping.get("entities") or {})
        for platform_cfg in entities_cfg.values():
            if not isinstance(platform_cfg, dict):
                continue
            for entity_key, ecfg in platform_cfg.items():
                if not isinstance(ecfg, dict):
                    continue
                if "default_value" in ecfg:
                    attr_name = ecfg.get("attribute", entity_key)
                    default_values[attr_name] = ecfg["default_value"]
        
        coordinator = MideaCoordinator(
            hass,
            controller,
            f"Device_{device_id}",
            update_interval=update_interval,
            calculate_config=calculate_config,
            queries=queries,
            centralized=centralized,
            default_values=default_values,
            device_type=device_type_int,
            respose=respose,
        )
        
        try:
            await coordinator.async_config_entry_first_refresh()
        except UpdateFailed as e:
            _LOGGER.error("Failed first refresh for device %s: %s", device_id, e)
            controller.close()
            continue
        
        hass.data[DOMAIN][entry.entry_id][str(device_id)] = {
            "coordinator": coordinator,
            "controller": controller,
            CONF_DEVICE_ID: device_id,
            CONF_DEVICE_TYPE: device_type,
            CONF_SN8: sn8,
            CONF_SN: sn,
            CONF_PRODUCT_MODEL: device_data.get(CONF_PRODUCT_MODEL, ""),
            CONF_MODEL_NUMBER: device_data.get(CONF_MODEL_NUMBER, ""),
            CONF_DEVICE_NAME: device_name,
            CONF_PROTOCOL: protocol,
        }
    
    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except (ValueError, KeyError, OSError) as e:
        _LOGGER.error("Failed to set up platforms: %s", e)
        return False
    
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        entry_data = hass.data[DOMAIN].pop(entry.entry_id)
        for device_id_str, data in entry_data.items():
            controller = data.get("controller")
            if controller:
                controller.close()
    return unload_ok

async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
