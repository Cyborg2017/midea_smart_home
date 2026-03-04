from typing import Any, Optional, Union

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MideaCoordinator, ControlValue


class MideaBaseEntity(CoordinatorEntity[MideaCoordinator]):
    _attr_has_entity_name = True
    
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        
        if not self.coordinator.controller.connected:
            return False
            
        data = self.coordinator.data
        if data is None:
            return False
            
        return True

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
    ) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_type = device_type
        self._sn = sn
        self._sn8 = sn8
        self._entity_key = entity_key
        self._model = model

        device_type_int = int(device_type, 16) if isinstance(device_type, str) else 0
        device_type_code = f"T0x{device_type_int:02X}" if device_type_int else device_type

        if model:
            device_display_name = f"{device_name} ( {model} )"
            model_display = model
        elif sn8:
            device_display_name = f"{device_name} ( {device_type_code} | {sn8} )"
            model_display = device_type_code
        else:
            device_display_name = device_name
            model_display = device_type_code

        self._attr_unique_id = f"midea_{device_id}_{entity_key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(device_id))},
            name=device_display_name,
            manufacturer="Midea",
            model=model_display,
            serial_number=sn,
        )

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

    async def _async_set_control(
        self,
        attr: str,
        value: ControlValue
    ) -> None:
        await self.coordinator.async_set_control(attr, value)

    async def _async_set_multiple_controls(
        self,
        controls: dict[str, ControlValue]
    ) -> None:
        for attr, value in controls.items():
            await self._async_set_control(attr, value)

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
        await self._async_set_control(key, value)
