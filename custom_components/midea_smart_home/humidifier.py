import logging
from typing import Any

from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import MideaCoordinator
from .entity import MideaBaseEntity, iter_midea_device_configs

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entities = []

    for coordinator, device_id, device_type, sn, sn8, device_name, model, device_mapping in iter_midea_device_configs(
        hass, entry
    ):
        entities_config = device_mapping.get("entities", {})
        humidifier_config = entities_config.get(Platform.HUMIDIFIER, {})

        if humidifier_config:
            for humidifier_id, config in humidifier_config.items():
                entities.append(
                    MideaHumidifierEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        humidifier_id, config, model
                    )
                )

    async_add_entities(entities)


class MideaHumidifierEntity(MideaBaseEntity, HumidifierEntity):
    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        humidifier_id: str,
        config: dict,
        model: str = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, humidifier_id, model)
        self._humidifier_id = humidifier_id
        self._config = config
        self._attr_unique_id = f"humidifier.midea_{device_id}_{humidifier_id}"
        self.entity_id = f"humidifier.midea_{device_id}_{humidifier_id}"
        self._attr_translation_key = config.get("translation_key", humidifier_id)
        self._key_power = config.get("power")
        self._key_target_humidity = config.get("target_humidity")
        self._key_current_humidity = config.get("current_humidity")
        self._key_mode = config.get("mode")
        self._key_modes = config.get("modes", {})
        self._min_humidity = config.get("min_humidity", 30)
        self._max_humidity = config.get("max_humidity", 80)

        if self._key_modes:
            self._attr_supported_features = HumidifierEntityFeature.MODES

    @property
    def device_class(self):
        return self._config.get("device_class", HumidifierDeviceClass.HUMIDIFIER)

    @property
    def min_humidity(self) -> int:
        return self._min_humidity

    @property
    def max_humidity(self) -> int:
        return self._max_humidity

    @property
    def is_on(self):
        if not self._key_power:
            return False
        return self._get_status_on_off(self._key_power)

    @property
    def target_humidity(self):
        if not self._key_target_humidity:
            return None
        value = self._get_nested_value(self._key_target_humidity)
        if value is not None:
            try:
                return int(value)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def current_humidity(self):
        if not self._key_current_humidity:
            return None
        value = self._get_nested_value(self._key_current_humidity)
        if value is not None:
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return None
        return None

    @property
    def mode(self):
        if not self._key_mode:
            return None
        data = self.coordinator.data or {}
        return data.get(self._key_mode)

    @property
    def available_modes(self):
        if self._key_modes:
            return list(self._key_modes.keys())
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        if self._key_power:
            await self.coordinator.async_set_control(self._key_power, "on")

    async def async_turn_off(self, **kwargs: Any) -> None:
        if self._key_power:
            await self.coordinator.async_set_control(self._key_power, "off")

    async def async_set_humidity(self, humidity: int) -> None:
        if self._key_target_humidity:
            await self.coordinator.async_set_control(self._key_target_humidity, humidity)

    async def async_set_mode(self, mode: str) -> None:
        if self._key_modes and mode in self._key_modes:
            mode_config = self._key_modes[mode]
            if isinstance(mode_config, dict):
                await self.coordinator.async_set_control(mode_config)
            else:
                await self.coordinator.async_set_control(self._key_mode, mode)
