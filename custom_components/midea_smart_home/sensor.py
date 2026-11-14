import logging
from typing import Any, Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    EntityCategory,
    Platform,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CONNECTION_TYPE,
    CONNECTION_TYPE_BADGES,
    CONNECTION_TYPE_LAN,
    DOMAIN,
)
from .coordinator import MideaCoordinator
from .entity import MideaBaseEntity, iter_midea_device_configs
from .sensor_stats import CLOUD_STATS_SENSORS

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
                state_class = config.get("state_class")
                suggested_display_precision = config.get("suggested_display_precision")
                options = config.get("options")
                entities.append(
                    MideaSensorEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        sensor_id, name, device_class, unit, state_class, model,
                        suggested_display_precision, options, config
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

        device_runtime = hass.data.get(DOMAIN, {}).get(entry.entry_id, {}).get(
            str(device_id), {}
        )
        stats_coordinator = (
            device_runtime.get("cloud_stats_coordinator")
            if isinstance(device_runtime, dict)
            else None
        )
        device_type_int = (
            int(device_type, 16) if isinstance(device_type, str) else device_type
        )
        if stats_coordinator is not None:
            connection_type = device_runtime.get(
                CONF_CONNECTION_TYPE, CONNECTION_TYPE_LAN
            )
            for config in CLOUD_STATS_SENSORS.get(device_type_int, []):
                entities.append(
                    MideaCloudStatsSensor(
                        stats_coordinator, device_id, device_type, sn, device_name,
                        model, connection_type, config
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
        state_class: Optional[SensorStateClass] = None,
        model: str = None,
        suggested_display_precision: Optional[int] = None,
        options: Optional[list] = None,
        config: dict = None,
    ):
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, sensor_id, model,
            platform_name="sensor", config=config or {}
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


class MideaCloudStatsSensor(CoordinatorEntity, SensorEntity):
    """Sensor backed by the independent cloud statistics coordinator."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator,
        device_id: int,
        device_type: str,
        sn: str,
        device_name: str,
        model: str,
        connection_type: str,
        config: dict,
    ):
        super().__init__(coordinator)
        self._stat_key = config["key"]
        self._attr_unique_id = f"sensor.midea_{device_id}_{self._stat_key}"
        self.entity_id = f"sensor.midea_{device_id}_{self._stat_key}"
        self._attr_translation_key = config.get("translation_key", self._stat_key)
        self._attr_device_class = config.get("device_class")
        self._attr_state_class = config.get("state_class")
        self._attr_native_unit_of_measurement = config.get("unit")
        self._attr_suggested_display_precision = config.get("precision")
        self._attr_icon = config.get("icon")

        device_type_int = (
            int(device_type, 16) if isinstance(device_type, str) else device_type
        )
        model_display = model if model else f"T0x{device_type_int:02X}"
        badge = CONNECTION_TYPE_BADGES.get(connection_type)
        if badge and not model_display.endswith(f"| {badge}"):
            model_display = f"{model_display} | {badge}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(device_id))},
            name=device_name,
            manufacturer="Midea",
            model=model_display,
            serial_number=sn,
            configuration_url="https://github.com/Cyborg2017/midea_smart_home",
        )

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def native_value(self) -> Optional[Any]:
        data = self.coordinator.data or {}
        return data.get(self._stat_key)
