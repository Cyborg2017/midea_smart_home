import logging
from typing import Any, Optional

from homeassistant.components.sensor import (
    EntityCategory,
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
                suggested_display_precision = config.get("suggested_display_precision")
                options = config.get("options")
                entities.append(
                    MideaSensorEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        sensor_id, name, device_class, unit, translation_key, state_class, model,
                        suggested_display_precision, options
                    )
                )

        ip_address = None
        if hasattr(coordinator.device, 'controller') and hasattr(coordinator.device.controller, 'ip'):
            ip_address = coordinator.device.controller.ip
        elif hasattr(coordinator.device, 'ip_address'):
            ip_address = coordinator.device.ip_address

        if ip_address:
            entities.append(
                MideaLanIPEntity(
                    coordinator, device_id, device_type, sn, sn8, device_name,
                    model, ip_address
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
        suggested_display_precision: Optional[int] = None,
        options: Optional[list] = None,
    ):
        config = {"translation_key": translation_key} if translation_key else {}
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, sensor_id, model,
            platform_name="sensor", config=config
        )
        self._sensor_id = sensor_id

        if options is not None:
            self._attr_options = options

        if device_class and isinstance(device_class, str):
            try:
                device_class = SensorDeviceClass(device_class)
            except ValueError:
                device_class = None

        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_suggested_display_precision = suggested_display_precision

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


class MideaLanIPEntity(MideaBaseEntity, SensorEntity):

    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        model: str,
        ip_address: str,
    ):
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, "lan_ip", model,
            platform_name="sensor", config={"translation_key": "lan_ip"}
        )
        self._ip_address = ip_address
        self._attr_device_class = None
        self._attr_native_unit_of_measurement = None
        self._attr_state_class = None
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> Optional[str]:
        """Return the LAN IP address."""
        if not self.coordinator.device or not self.coordinator.device.available:
            return None

        if hasattr(self.coordinator.device, 'controller') and hasattr(self.coordinator.device.controller, 'ip'):
            return self.coordinator.device.controller.ip
        elif hasattr(self.coordinator.device, 'ip_address'):
            return self.coordinator.device.ip_address

        return self._ip_address
