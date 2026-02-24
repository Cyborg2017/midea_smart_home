import logging
from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_DEVICE_ID, CONF_DEVICE_TYPE, CONF_SN, CONF_SN8, DOMAIN
from .coordinator import MideaCoordinator
from .device_mapping import get_device_mapping
from .entity import MideaBaseEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entry_data = hass.data[DOMAIN][entry.entry_id]
    entities = []
    
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
        device_name = data.get("device_name", f"Midea Device {device_id}")
        
        device_type_int = int(device_type, 16) if isinstance(device_type, str) else device_type
        
        device_mapping = get_device_mapping(device_type_int, sn8)
        entities_config = device_mapping.get("entities", {})
        rationale = device_mapping.get("rationale", ["off", "on"])
        
        switch_config = entities_config.get(Platform.SWITCH, {})
        if switch_config:
            for switch_id, config in switch_config.items():
                translation_key = config.get("translation_key")
                switch_rationale = config.get("rationale", rationale)
                condition = config.get("condition")
                entities.append(
                    MideaSwitchEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        switch_id, translation_key, switch_rationale, condition
                    )
                )
    
    async_add_entities(entities)

class MideaSwitchEntity(MideaBaseEntity, SwitchEntity):
    _attr_device_class = SwitchDeviceClass.SWITCH
    
    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        switch_id: str,
        translation_key: str = None,
        rationale: list = None,
        condition: dict = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, switch_id)
        self._switch_id = switch_id
        self._attr_translation_key = translation_key or switch_id
        self._rationale = rationale or ["off", "on"]
        self._condition = condition
    
    def _check_condition(self) -> bool:
        if not self._condition:
            return True
        
        data = self.coordinator.data or {}
        
        if "not" in self._condition:
            attrs = self._condition["not"]
            for attr in attrs:
                value = data.get(attr)
                if value:
                    return False
            return True
        
        if "eq" in self._condition:
            attr, expected_value = self._condition["eq"]
            actual_value = data.get(attr)
            return actual_value == expected_value
        
        return True
    
    @property
    def available(self) -> bool:
        return super().available and self._check_condition()
    
    @property
    def is_on(self) -> bool:
        data = self.coordinator.data or {}
        value = data.get(self._switch_id)
        if value is None:
            return False
        
        try:
            return bool(self._rationale.index(value))
        except ValueError:
            if isinstance(value, bool):
                return value
            elif isinstance(value, int) or value in ['0', '1']:
                return bool(int(value))
            elif isinstance(value, str):
                return value in ["on", "open", "1", "true", "True"]
        return False
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        on_value = self._rationale[1] if len(self._rationale) > 1 else "on"
        await self.coordinator.async_set_control(self._switch_id, on_value)
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        off_value = self._rationale[0] if self._rationale else "off"
        await self.coordinator.async_set_control(self._switch_id, off_value)
