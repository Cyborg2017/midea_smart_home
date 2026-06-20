import logging
from typing import Any

from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityFeature,
    HumidifierAction,
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
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, humidifier_id, model,
            platform_name="humidifier", config=config
        )
        self._humidifier_id = humidifier_id
        self._key_power = self._config.get("power")
        self._key_target_humidity = self._config.get("target_humidity")
        self._key_current_humidity = self._config.get("current_humidity")
        self._key_external_humidity = "external_humidity_sensor"
        self._key_mode = self._config.get("mode")
        self._key_modes = self._config.get("modes", {})
        self._min_humidity = self._config.get("min_humidity", 30)
        self._max_humidity = self._config.get("max_humidity", 80)
        self._target_humidity_step = self._config.get("target_humidity_step", 1)

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
    def target_humidity_step(self) -> int:
        return self._target_humidity_step

    @property
    def action(self) -> HumidifierAction:
        if not self.is_on:
            return HumidifierAction.OFF
        current = self.current_humidity
        target = self.target_humidity
        if current is None or target is None:
            return HumidifierAction.IDLE
        dc = self.device_class
        if dc == HumidifierDeviceClass.DEHUMIDIFIER and current > target:
            return HumidifierAction.DRYING
        if dc == HumidifierDeviceClass.HUMIDIFIER and current < target:
            return HumidifierAction.HUMIDIFYING
        return HumidifierAction.IDLE

    @property
    def is_on(self):
        if not self._key_power:
            return False
        value = self._get_nested_value(self._key_power)
        rationale = self._config.get("rationale")
        if isinstance(rationale, list) and len(rationale) > 1:
            return value == rationale[1]
        if isinstance(rationale, list) and rationale:
            return value in rationale
        return self._is_on(value)

    @property
    def target_humidity(self):
        if not self._key_target_humidity:
            return None
        value = self._get_nested_value(self._key_target_humidity)
        if value is None:
            return None
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            return None
        if int_value < self._min_humidity or int_value > self._max_humidity:
            return None
        return int_value

    @property
    def current_humidity(self):
        external_entity_id = self._get_nested_value(self._key_external_humidity)
        if external_entity_id and isinstance(external_entity_id, str) and external_entity_id.strip():
            state = self.hass.states.get(external_entity_id.strip())
            if state and state.state not in ("unknown", "unavailable", None):
                try:
                    return int(float(state.state))
                except (ValueError, TypeError):
                    pass
            return None
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
        if not self._key_mode or not self._key_modes:
            return None
        data = self.coordinator.data or {}
        for mode_key, mode_config in self._key_modes.items():
            if not isinstance(mode_config, dict):
                continue
            match = True
            for attr, expected in mode_config.items():
                actual = data.get(attr)
                if actual != expected:
                    match = False
                    break
            if match:
                return mode_key
        return None

    @property
    def available_modes(self):
        if self._key_modes:
            return list(self._key_modes.keys())
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        if self._key_power:
            rationale = self._config.get("rationale")
            if isinstance(rationale, list) and len(rationale) > 1:
                await self.coordinator.async_set_control(self._key_power, rationale[1])
            else:
                await self.coordinator.async_set_control(self._key_power, "on")

    async def async_turn_off(self, **kwargs: Any) -> None:
        if self._key_power:
            rationale = self._config.get("rationale")
            if isinstance(rationale, list) and len(rationale) > 0:
                await self.coordinator.async_set_control(self._key_power, rationale[0])
            else:
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
