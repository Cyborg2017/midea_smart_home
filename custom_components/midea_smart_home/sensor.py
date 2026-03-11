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

from .const import DOMAIN
from .coordinator import MideaCoordinator
from .entity import MideaBaseEntity, iter_midea_device_configs

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entities = []

    for coordinator, device_id, device_type, sn, sn8, device_name, model, device_mapping in iter_midea_device_configs(hass, entry):
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
                        sensor_id, name, device_class, unit, translation_key, state_class, model
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
        model: str = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, sensor_id, model)
        self._sensor_id = sensor_id
        self._attr_translation_key = translation_key or sensor_id

        if device_class and isinstance(device_class, str):
            try:
                device_class = SensorDeviceClass(device_class)
            except ValueError:
                device_class = None

        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = f"sensor.midea_{device_id}_{sensor_id}"
        self.entity_id = f"sensor.midea_{device_id}_{sensor_id}"

        if state_class is not None:
            if isinstance(state_class, str):
                try:
                    state_class = SensorStateClass(state_class)
                except ValueError:
                    state_class = None
            self._attr_state_class = state_class
        elif device_class == SensorDeviceClass.ENUM:
            self._attr_state_class = None
        elif device_class == SensorDeviceClass.ENERGY:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif device_class in (SensorDeviceClass.TEMPERATURE, SensorDeviceClass.HUMIDITY,
                              SensorDeviceClass.PRESSURE, SensorDeviceClass.POWER,
                              SensorDeviceClass.CURRENT, SensorDeviceClass.VOLTAGE):
            self._attr_state_class = SensorStateClass.MEASUREMENT
        else:
            self._attr_state_class = None

    @property
    def native_value(self) -> Optional[Any]:
        """Return the state of the sensor."""
        if not self.available:
            return None

        data = self.coordinator.data or {}
        value = data.get(self._sensor_id)

        if value is None or value == "":
            return None

        return value
