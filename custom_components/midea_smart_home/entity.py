from typing import Any, Optional, Union, Generator

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CATEGORY,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_PRODUCT_MODEL,
    CONF_SN,
    CONF_SN8,
    DOMAIN,
)
from .coordinator import MideaCoordinator, ControlValue
from .device_mapping import get_device_mapping

def iter_midea_device_configs(
    hass: HomeAssistant, entry: ConfigEntry
) -> Generator[tuple[MideaCoordinator, int, str, str, str, str, str, dict], None, None]:
    entry_data = hass.data[DOMAIN][entry.entry_id]

    for device_id_str, data in entry_data.items():
        if device_id_str == "device_list":
            continue
        coordinator = data.get("coordinator")
        if not coordinator:
            continue
        device_id = data[CONF_DEVICE_ID]
        device_type = data[CONF_DEVICE_TYPE]
        sn8 = data.get(CONF_SN8, "")
        sn = data.get(CONF_SN, "")
        model = data.get(CONF_PRODUCT_MODEL, "")
        device_name = data.get(CONF_DEVICE_NAME, f"Midea Device {device_id}")
        category = data.get(CONF_CATEGORY, "")
        device_type_int = (
            int(device_type, 16) if isinstance(device_type, str) else device_type
        )
        device_mapping = get_device_mapping(device_type_int, model, sn8, category)
        yield coordinator, device_id, device_type, sn, sn8, device_name, model, device_mapping


class MideaBaseEntity(CoordinatorEntity[MideaCoordinator]):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        entity_key: str,
        model: Optional[str] = None,
        platform_name: Optional[str] = None,
        config: Optional[dict] = None,
        rationale: Optional[list] = None,
        condition: Optional[dict] = None,
    ) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_type = device_type
        self._sn = sn
        self._sn8 = sn8
        self._entity_key = entity_key
        self._model = model
        self._config = config or {}
        self._rationale = rationale or ["off", "on"]
        self._condition = condition

        device_type_int = int(device_type, 16) if isinstance(device_type, str) else 0
        device_type_code = f"T0x{device_type_int:02X}" if device_type_int else device_type

        device_display_name = device_name
        model_display = model if model else device_type_code

        self._attr_unique_id = f"{platform_name}.midea_{device_id}_{entity_key}" if platform_name else f"midea_{device_id}_{entity_key}"

        if platform_name:
            self.entity_id = f"{platform_name}.midea_{device_id}_{entity_key.lower()}"

        self._attr_translation_key = self._config.get("translation_key", entity_key)

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(device_id))},
            name=device_display_name,
            manufacturer="Midea",
            model=model_display,
            serial_number=sn,
            configuration_url="https://github.com/Cyborg2017/midea_smart_home",
        )

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success:
            return False

        if not self.coordinator.controller.available:
            return False

        data = self.coordinator.data
        if data is None:
            return False

        return self._check_condition(self._condition)

    def _get_nested_value(
        self,
        key: str | list[str]
    ) -> Union[str, int, float, bool, None]:
        data = self.coordinator.data or {}
        if isinstance(key, list):
            value: Any = data
            for k in key:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return None
            return value
        return data.get(key)

    def _dict_get_selected(
        self,
        config_dict: dict,
        default: Optional[str] = None
    ) -> Optional[str]:
        data = self.coordinator.data or {}
        status_key = config_dict.get("status_key")
        if status_key:
            current_value = self._get_nested_value(status_key)
            if current_value is not None:
                for mode, mode_config in config_dict.items():
                    if mode == "status_key":
                        continue
                    if isinstance(mode_config, dict):
                        extracted = self._extract_deepest_value(mode_config)
                        if extracted == current_value:
                            return mode
            if default is not None:
                return default
            if config_dict:
                for key in config_dict.keys():
                    if key != "status_key":
                        return key
            return None
        for mode, mode_config in config_dict.items():
            if isinstance(mode_config, dict):
                match = True
                for key, value in mode_config.items():
                    if key == "speeds":
                        continue
                    current_value = self._get_nested_value(key)
                    if current_value != value:
                        match = False
                        break
                if match:
                    return mode
        if default is not None:
            return default
        if config_dict:
            return list(config_dict.keys())[0]
        return None

    def _extract_deepest_value(self, config: dict) -> Any:
        for value in config.values():
            if isinstance(value, dict):
                return self._extract_deepest_value(value)
            return value
        return None

    def _is_off(self, value: Any) -> bool:
        if isinstance(value, bool):
            return not value
        if isinstance(value, int):
            return value == 0
        if isinstance(value, str):
            return value in ["off", "0", "false", "False"]
        return True

    def _is_on(self, value: Any) -> bool:
        return not self._is_off(value)

    def _get_status_on_off(self, key: Optional[str]) -> bool:
        if key is None:
            return False
        value = self._get_nested_value(key)
        return self._is_on(value)

    def _check_condition(self, condition: Optional[dict] = None) -> bool:
        condition = condition or getattr(self, '_condition', None)
        if not condition:
            return True

        data = self.coordinator.data or {}

        if "not" in condition:
            attrs = condition["not"]
            for attr in attrs:
                value = data.get(attr)
                if value:
                    return False
            return True

        if "eq" in condition:
            attr, expected_value = condition["eq"]
            actual_value = data.get(attr)
            return actual_value == expected_value

        return True

    async def _async_set_status_on_off(
        self,
        key: Optional[str],
        on_off: bool,
        rationale: Optional[list[str]] = None
    ) -> None:
        if key is None:
            return
        rationale = rationale or getattr(self, '_rationale', ["off", "on"])
        value = rationale[1] if on_off else rationale[0]
        await self.coordinator.async_set_control(key, value)
