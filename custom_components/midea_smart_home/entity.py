from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MideaCoordinator


class MideaBaseEntity(CoordinatorEntity[MideaCoordinator]):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        entity_key: str,
    ) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_type = device_type
        self._sn = sn
        self._sn8 = sn8
        self._entity_key = entity_key

        device_type_int = int(device_type, 16) if isinstance(device_type, str) else 0
        device_type_code = f"T0x{device_type_int:02X}" if device_type_int else device_type

        device_display_name = f"{device_name} ({sn8})" if sn8 else device_name

        self._attr_unique_id = f"{DOMAIN}_{device_id}_{entity_key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(device_id))},
            name=device_display_name,
            manufacturer="Midea",
            model=sn8 if sn8 else device_type_code,
            serial_number=sn,
        )

    def _get_nested_value(self, key):
        data = self.coordinator.data or {}
        if isinstance(key, list):
            value = data
            for k in key:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return None
            return value
        return data.get(key)

    def _dict_get_selected(self, config_dict, default=None):
        data = self.coordinator.data or {}
        for mode, mode_config in config_dict.items():
            if isinstance(mode_config, dict):
                match = True
                for key, value in mode_config.items():
                    current_value = self._get_nested_value(key)
                    if current_value != value:
                        match = False
                        break
                if match:
                    return mode
        return default if default is not None else list(config_dict.keys())[0] if config_dict else None

    def _is_off(self, value):
        if isinstance(value, bool):
            return not value
        elif isinstance(value, int):
            return value == 0
        elif isinstance(value, str):
            return value in ["off", "0", "false", "False"]
        return True

    def _is_on(self, value):
        return not self._is_off(value)

    def _get_status_on_off(self, key):
        if key is None:
            return False
        value = self._get_nested_value(key)
        return self._is_on(value)

    def _check_condition(self, condition=None) -> bool:
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

    async def _async_set_control(self, attr: str, value) -> None:
        await self.coordinator.async_set_control(attr, value)

    async def _async_set_multiple_controls(self, controls: dict) -> None:
        for attr, value in controls.items():
            await self._async_set_control(attr, value)

    async def _async_set_status_on_off(self, key, on_off: bool, rationale: list = None):
        if key is None:
            return
        rationale = rationale or getattr(self, '_rationale', ["off", "on"])
        value = rationale[1] if on_off else rationale[0]
        await self._async_set_control(key, value)
