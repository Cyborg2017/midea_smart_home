import logging
from typing import Any, Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
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
        
        sensor_config = entities_config.get(Platform.SENSOR, {})
        if sensor_config:
            for sensor_id, config in sensor_config.items():
                name = config.get("name", sensor_id)
                device_class = config.get("device_class")
                unit = config.get("unit_of_measurement")
                translation_key = config.get("translation_key")
                state_class = config.get("state_class")
                entities.append(
                    MideaSensorEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        sensor_id, name, device_class, unit, translation_key, state_class
                    )
                )
    
    async_add_entities(entities)

class MideaSensorEntity(MideaBaseEntity, SensorEntity):
    
    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        sensor_id: str,
        name: str,
        device_class: Optional[SensorDeviceClass],
        unit: str,
        translation_key: str = None,
        state_class: Optional[SensorStateClass] = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, sensor_id)
        self._sensor_id = sensor_id
        self._attr_translation_key = translation_key or sensor_id
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        
        if state_class is not None:
            self._attr_state_class = state_class
        elif device_class == SensorDeviceClass.ENUM:
            self._attr_state_class = None
        elif device_class == SensorDeviceClass.ENERGY:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        else:
            self._attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self) -> Optional[Any]:
        data = self.coordinator.data or {}
        return data.get(self._sensor_id)
