import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
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
    """Set up binary sensor entities for Midea devices."""
    entities = []

    for coordinator, device_id, device_type, sn, sn8, device_name, model, device_mapping in iter_midea_device_configs(hass, entry):
        entities.append(
            MideaDeviceStatusSensorEntity(
                coordinator, device_id, device_type, sn, sn8, device_name, model
            )
        )
        entities_config = device_mapping.get("entities", {})
        binary_sensor_config = entities_config.get(Platform.BINARY_SENSOR, {})

        if binary_sensor_config:
            for sensor_id, config in binary_sensor_config.items():
                device_class = config.get("device_class")
                translation_key = config.get("translation_key")
                on_values = config.get("on_value", [])
                off_values = config.get("off_value", [])
                entities.append(
                    MideaBinarySensorEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        sensor_id, device_class, translation_key, on_values, off_values, model
                    )
                )

    async_add_entities(entities)


class MideaDeviceStatusSensorEntity(MideaBaseEntity, BinarySensorEntity):
    """Device status binary sensor showing connectivity and all device attributes."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_translation_key = "device_status"

    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        model: str = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, "device_status", model)
        self._attr_unique_id = f"binary_sensor.midea_{device_id}_device_status"
        self.entity_id = f"binary_sensor.midea_{device_id}_device_status"

    @property
    def is_on(self) -> bool:
        """Return if the device is connected."""
        return self.coordinator.last_update_success

    @property
    def icon(self) -> str:
        """Return the icon."""
        if self.is_on:
            return "mdi:devices"
        return "mdi:devices-off"

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes with all device data."""
        data = self.coordinator.data or {}
        device_type_int = int(self._device_type, 16) if isinstance(self._device_type, str) else 0
        device_type_str = f"T0x{device_type_int:02X}" if device_type_int else self._device_type
        attributes = {
            "device_id": str(self._device_id),
            "sn": self._sn,
            "sn8": self._sn8,
            "model": self._model,
            "device_type": device_type_str,
        }

        other_attrs = {}
        for key, value in data.items():
            if value is not None:
                if isinstance(value, (str, int, float, bool)):
                    other_attrs[key] = value
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_value is not None and isinstance(sub_value, (str, int, float, bool)):
                            other_attrs[f"{key}_{sub_key}"] = sub_value

        for key in sorted(other_attrs.keys()):
            attributes[key] = other_attrs[key]

        return attributes


class MideaBinarySensorEntity(MideaBaseEntity, BinarySensorEntity):
    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        sensor_id: str,
        device_class: str = None,
        translation_key: str = None,
        on_values: list = None,
        off_values: list = None,
        model: str = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, sensor_id, model)
        self._sensor_id = sensor_id
        self._on_values = on_values or []
        self._off_values = off_values or []
        if device_class:
            try:
                self._attr_device_class = BinarySensorDeviceClass(device_class)
            except ValueError:
                pass
        self._attr_translation_key = translation_key or sensor_id
        self._attr_unique_id = f"binary_sensor.midea_{device_id}_{sensor_id}"
        self.entity_id = f"binary_sensor.midea_{device_id}_{sensor_id}"

    @property
    def is_on(self) -> bool | None:
        """Return if the binary sensor is on."""
        if not self.available:
            return False

        data = self.coordinator.data or {}
        value = data.get(self._sensor_id)

        if self._on_values and value in self._on_values:
            return True
        if self._off_values and value in self._off_values:
            return False

        if isinstance(value, bool):
            return value
        return value == 1 or value == "on" or value == "true"
