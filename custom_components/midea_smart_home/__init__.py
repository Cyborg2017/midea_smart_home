import logging
import os
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import device_registry
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_CATEGORY,
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
    CONF_ROOM_NAME,
    CONF_SN,
    CONF_SN8,
    CONF_TOKEN,
    DEFAULT_PORT,
    DEVICE_TYPES,
    DOMAIN,
    PLATFORMS,
    LUA_COMMON_PATH,
    LUA_CUSTOM_PATH,
    ProtocolVersion,
)
from .config_flow import get_lua_custom_path, get_lua_file_path
from .coordinator import MideaCoordinator
from .midea_lib.device import MideaDevice
from .midea_lib.lua import write_file, ensure_lua_files
from .device_mapping import get_device_mapping

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.data.setdefault(DOMAIN, {})

    lua_path = hass.config.path(LUA_COMMON_PATH)
    os.makedirs(lua_path, exist_ok=True)

    cjson, bit, cjson_lua, bit_lua = await hass.async_add_executor_job(
        ensure_lua_files, lua_path
    )

    if not os.path.exists(cjson):
        success = await hass.async_add_executor_job(write_file, cjson, cjson_lua)
        if success:
            _LOGGER.info("Created cjson.lua at %s", cjson)

    if not os.path.exists(bit):
        success = await hass.async_add_executor_job(write_file, bit, bit_lua)
        if success:
            _LOGGER.info("Created bit.lua at %s", bit)

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})

    devices = entry.data.get("devices", [])
    if not devices:
        devices = [entry.data]

    language = hass.config.language or "en"

    async def init_single_device(device_data: dict) -> dict | None:
        device_id = device_data[CONF_DEVICE_ID]
        ip_address = device_data.get(CONF_IP, "")
        port = device_data.get(CONF_PORT, DEFAULT_PORT)
        token = device_data.get(CONF_TOKEN, "")
        key = device_data.get(CONF_KEY, "")
        lua_file = device_data.get(CONF_LUA_FILE, "")
        sn = device_data.get(CONF_SN, "")
        sn8 = device_data.get(CONF_SN8, "")
        model = device_data.get(CONF_PRODUCT_MODEL, "")
        device_type = device_data.get(CONF_DEVICE_TYPE)
        device_type_int = int(device_type, 16) if isinstance(device_type, str) else 0

        # Priority: use custom Lua file from integration's lua folder if it exists,
        # otherwise fall back to the cloud-downloaded file (new name, then old name for compatibility)
        component_dir = str(Path(__file__).parent)
        custom_lua_path = get_lua_custom_path(component_dir, device_type_int, sn8)
        storage_lua_path_new = get_lua_file_path(hass.config.config_dir, device_id, device_type_int, sn8)
        # Legacy naming with device_id prefix (for backward compatibility)
        legacy_storage_dir = Path(hass.config.config_dir) / ".storage" / DOMAIN / "lua_devices"
        if sn8:
            legacy_storage_path = legacy_storage_dir / f"{device_id}_T0x{hex(device_type_int)[2:].upper()}_{sn8}.lua"
        else:
            legacy_storage_path = legacy_storage_dir / f"{device_id}_T0x{hex(device_type_int)[2:].upper()}.lua"

        lua_file = ""
        for path, source in [
            (custom_lua_path, "custom"),
            (storage_lua_path_new, "storage (new)"),
            (legacy_storage_path, "storage (legacy)"),
        ]:
            if path.exists():
                lua_file = str(path)
                _LOGGER.info("Using Lua file from %s: %s", source, lua_file)
                break

        if not lua_file:
            entry_lua = device_data.get(CONF_LUA_FILE, "")
            if entry_lua and Path(entry_lua).exists():
                lua_file = entry_lua
                _LOGGER.info("Using Lua file from entry data: %s", lua_file)

        if not lua_file:
            _LOGGER.warning(
                "No Lua file found for device %s (type=0x%s, sn8=%s), "
                "checked: %s, %s, %s",
                device_id, hex(device_type_int)[2:].upper(), sn8,
                custom_lua_path, storage_lua_path_new, legacy_storage_path
            )

        device_name = device_data.get(CONF_DEVICE_NAME, "")
        if not device_name:
            device_name = DEVICE_TYPES.get(device_type_int, f"Device {device_type}")

        room_name = device_data.get(CONF_ROOM_NAME, "")
        area = room_name

        category = device_data.get(CONF_CATEGORY, "")
        protocol = device_data.get(CONF_PROTOCOL, ProtocolVersion.V3)

        lua_common_dir = str(Path(hass.config.config_dir) / LUA_COMMON_PATH)

        device_mapping = get_device_mapping(device_type_int, model, sn8, category)
        calculate_config = device_mapping.get("calculate", {})
        centralized = list(device_mapping.get("centralized", []))
        default_values = dict(device_mapping.get("default_values", {}))
        initial_query = device_mapping.get("initial_query")
        polling_query = device_mapping.get("polling_query")
        # Check if polling is supported (based on existence of polling_query)
        enable_polling = polling_query is not None and isinstance(polling_query, list) and len(polling_query) > 0
        # Get polling settings from device data (user configurable via Options)
        polling_enabled = device_data.get("polling_enabled", True)  # Default to enabled
        polling_interval = device_data.get("polling_interval", 30)
        # Only enable polling if both device_mapping supports it AND user has enabled it
        effective_polling = enable_polling and polling_enabled
        _LOGGER.debug(
            "Device %s: polling_supported=%s, polling_interval=%d, polling_query=%s",
            device_id,
            enable_polling,
            polling_interval,
            polling_query
        )

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

        def init_device():
            device = MideaDevice(
                device_id=device_id,
                device_type=device_type_int,
                ip_address=ip_address,
                port=port,
                token=token,
                key=key,
                protocol=protocol,
                model=device_data.get(CONF_PRODUCT_MODEL, ""),
                subtype=0,
                sn=sn,
                sn8=sn8,
                lua_file=lua_file,
                lua_common_dir=lua_common_dir,
                device_name=device_name,
                calculate_config=calculate_config,
                centralized=centralized,
                default_values=default_values,
                category=category,
                enable_polling=effective_polling,
                polling_interval=polling_interval,
                initial_query=initial_query,
                polling_query=polling_query,
            )
            device.open()
            import time
            for _ in range(10):
                if device.available:
                    break
                time.sleep(0.5)
            return device

        try:
            device = await hass.async_add_executor_job(init_device)

            if not device.available:
                _LOGGER.warning("Device %s failed to connect after 5 seconds, will retry in background", device_id)

            coordinator = MideaCoordinator(
                hass,
                device,
                device_name,
                area,
            )

            import asyncio
            if initial_query and isinstance(initial_query, list):
                for item in initial_query:
                    if isinstance(item, dict):
                        if len(item) == 0:
                            device.refresh_status({})
                        elif len(item) == 1:
                            key = list(item.keys())[0]
                            device.refresh_status({"query_type": key})
                    elif isinstance(item, set) and len(item) == 1:
                        key = list(item)[0]
                        device.refresh_status({"query_type": key})
                    await asyncio.sleep(0.3)
            else:
                device.refresh_status()

            if device.available:
                for _ in range(10):
                    if coordinator.data is not None:
                        break
                    await asyncio.sleep(0.3)

                if coordinator.data is None:
                    _LOGGER.warning("Device %s did not receive initial data after 3 seconds, will retry in background", device_id)

            return {
                "coordinator": coordinator,
                "device": device,
                CONF_DEVICE_ID: device_id,
                CONF_DEVICE_TYPE: device_type,
                CONF_SN8: sn8,
                CONF_SN: sn,
                CONF_PRODUCT_MODEL: device_data.get(CONF_PRODUCT_MODEL, ""),
                CONF_MODEL_NUMBER: device_data.get(CONF_MODEL_NUMBER, ""),
                CONF_DEVICE_NAME: device_name,
                CONF_PROTOCOL: protocol,
                CONF_CATEGORY: category,
            }
        except Exception as e:
            _LOGGER.error("Failed to initialize device %s: %s", device_id, e)
            return None

    import asyncio

    tasks = [init_single_device(device_data) for device_data in devices]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            _LOGGER.error("Error initializing device %d: %s", i, result)
        elif result is not None:
            device_id = result[CONF_DEVICE_ID]
            hass.data[DOMAIN][entry.entry_id][str(device_id)] = result

    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except (ValueError, KeyError, OSError) as e:
        _LOGGER.error("Failed to set up platforms: %s", e)
        return False

    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        entry_data = hass.data[DOMAIN].pop(entry.entry_id, {})
        for device_id_str, data in entry_data.items():
            coordinator = data.get("coordinator")
            if coordinator:
                coordinator.deactivate()
            device = data.get("device")
            if device:
                device.close()
    return unload_ok

async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)

async def async_remove_config_entry_device(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    device_entry: device_registry.DeviceEntry
) -> bool:
    """Remove a device from the config entry."""
    device_id = None
    for identifier in device_entry.identifiers:
        if identifier[0] == DOMAIN:
            device_id = identifier[1]
            break

    if device_id is None:
        _LOGGER.error("Device identifier not found for removal")
        return False

    entry_data = hass.data[DOMAIN].get(config_entry.entry_id, {})
    device_data = entry_data.get(str(device_id))

    if device_data:
        device = device_data.get("device")
        if device:
            device.close()
        entry_data.pop(str(device_id), None)

    new_devices = [
        d for d in config_entry.data.get("devices", [])
        if str(d.get(CONF_DEVICE_ID)) != str(device_id)
    ]

    new_data = dict(config_entry.data)
    new_data["devices"] = new_devices

    hass.config_entries.async_update_entry(
        config_entry,
        data=new_data,
    )

    _LOGGER.info("Removed device %s from config entry", device_id)
    return True
