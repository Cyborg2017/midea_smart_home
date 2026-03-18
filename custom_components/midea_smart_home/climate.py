import logging
from typing import Any, Optional

from homeassistant.components.climate import (
    ATTR_HVAC_MODE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature, Platform
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
        rationale = device_mapping.get("rationale", ["off", "on"])
        climate_config = entities_config.get(Platform.CLIMATE, {})

        if climate_config:
            for climate_key, config in climate_config.items():
                entities.append(
                    MideaClimateEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        climate_key, config, rationale, model
                    )
                )

    async_add_entities(entities)


class MideaClimateEntity(MideaBaseEntity, ClimateEntity):
    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        entity_key: str,
        config: dict,
        rationale: list,
        model: str = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, entity_key, model)
        self._config = config
        self._rationale = rationale
        self._attr_unique_id = f"climate.midea_{device_id}_{entity_key}"

        self._key_power = self._config.get("power")
        self._key_hvac_modes = self._config.get("hvac_modes")
        self._key_preset_modes = self._config.get("preset_modes")
        self._key_fan_modes = self._config.get("fan_modes")
        self._key_swing_modes = self._config.get("swing_modes")
        self._key_target_temperature = self._config.get("target_temperature")
        self._key_current_temperature = self._config.get("current_temperature")
        self._key_min_temp = self._config.get("min_temp", 16)
        self._key_max_temp = self._config.get("max_temp", 30)
        self._aux_heat = self._config.get("aux_heat")
        self._condition = config.get("condition")

        self._attr_translation_key = config.get("translation_key", entity_key)
        self._attr_temperature_unit = self._config.get("temperature_unit", UnitOfTemperature.CELSIUS)
        self._attr_precision = self._config.get("precision", 1.0)
        self._attr_target_temperature_step = self._config.get("precision", 1.0)
        self._attr_min_temp = float(self._key_min_temp)
        self._attr_max_temp = float(self._key_max_temp)

        self._setup_supported_features()
        self._setup_modes()

    @property
    def available(self) -> bool:
        return super().available and self._check_condition(self._condition)

    def _setup_supported_features(self):
        features = ClimateEntityFeature(0)
        features |= ClimateEntityFeature.TURN_ON
        features |= ClimateEntityFeature.TURN_OFF
        if self._key_target_temperature is not None:
            features |= ClimateEntityFeature.TARGET_TEMPERATURE
        if self._key_preset_modes is not None:
            features |= ClimateEntityFeature.PRESET_MODE
        if self._key_fan_modes is not None:
            features |= ClimateEntityFeature.FAN_MODE
        if self._key_swing_modes is not None:
            features |= ClimateEntityFeature.SWING_MODE
        if self._aux_heat is not None and hasattr(ClimateEntityFeature, 'AUX_HEAT'):
            features |= ClimateEntityFeature.AUX_HEAT
        self._attr_supported_features = features

    def _setup_modes(self):
        if self._key_hvac_modes is not None:
            self._attr_hvac_modes = list(self._key_hvac_modes.keys())
        else:
            self._attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]

        if self._key_preset_modes is not None:
            self._attr_preset_modes = list(self._key_preset_modes.keys())

        if self._key_fan_modes is not None:
            self._attr_fan_modes = list(self._key_fan_modes.keys())

        if self._key_swing_modes is not None:
            self._attr_swing_modes = list(self._key_swing_modes.keys())

    @property
    def hvac_mode(self) -> HVACMode:
        if self._key_hvac_modes is not None:
            return self._dict_get_selected(self._key_hvac_modes, HVACMode.OFF)

        data = self.coordinator.data or {}
        power = data.get(self._key_power, 0)
        if self._is_off(power):
            return HVACMode.OFF
        return HVACMode.HEAT

    @property
    def current_temperature(self) -> Optional[float]:
        if isinstance(self._key_current_temperature, list):
            temp_int = self._get_nested_value(self._key_current_temperature[0])
            tem_dec = self._get_nested_value(self._key_current_temperature[1])
            if temp_int is not None and tem_dec is not None:
                try:
                    return float(temp_int) + float(tem_dec)
                except (ValueError, TypeError):
                    return None
            return None
        else:
            temp = self._get_nested_value(self._key_current_temperature)
            if temp is not None:
                try:
                    return float(temp)
                except (ValueError, TypeError):
                    return None
            return None

    @property
    def target_temperature(self) -> Optional[float]:
        if isinstance(self._key_target_temperature, list):
            if len(self._key_target_temperature) == 1:
                temp = self._get_nested_value(self._key_target_temperature[0])
                if temp is not None:
                    try:
                        return float(temp)
                    except (ValueError, TypeError):
                        return None
                return None
            try:
                temp_int = self._get_nested_value(self._key_target_temperature[0])
                tem_dec = self._get_nested_value(self._key_target_temperature[1])
            except IndexError:
                _LOGGER.error(
                    "target_temperature list index error: _key_target_temperature=%s, len=%d",
                    self._key_target_temperature,
                    len(self._key_target_temperature)
                )
                return None
            if temp_int is not None and tem_dec is not None:
                try:
                    return float(temp_int) + float(tem_dec)
                except (ValueError, TypeError):
                    return None
            return None
        else:
            temp = self._get_nested_value(self._key_target_temperature)
            if temp is not None:
                try:
                    return float(temp)
                except (ValueError, TypeError):
                    return None
            return None

    @property
    def preset_mode(self) -> Optional[str]:
        if self._key_preset_modes is not None:
            return self._dict_get_selected(self._key_preset_modes)
        return None

    @property
    def fan_mode(self) -> Optional[str]:
        if self._key_fan_modes is not None:
            return self._dict_get_selected(self._key_fan_modes)
        return None

    @property
    def swing_mode(self) -> Optional[str]:
        if self._key_swing_modes is not None:
            return self._dict_get_selected(self._key_swing_modes)
        return None

    @property
    def is_aux_heat(self) -> bool:
        if self._aux_heat is not None:
            value = self._get_nested_value(self._aux_heat)
            return self._is_on(value)
        return False

    async def async_set_temperature(self, **kwargs: Any) -> None:
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        hvac_mode = kwargs.get(ATTR_HVAC_MODE)
        if hvac_mode is not None:
            await self.async_set_hvac_mode(hvac_mode)

        if self._key_target_temperature is not None:
            if isinstance(self._key_target_temperature, list) and len(self._key_target_temperature) == 2:
                temp_int = int(temperature)
                temp_decimal = temperature - temp_int
                new_status = {
                    self._key_target_temperature[0]: temp_int,
                    self._key_target_temperature[1]: temp_decimal
                }
                await self.coordinator.async_set_control(new_status)
            else:
                target_key = self._key_target_temperature[0] if isinstance(self._key_target_temperature, list) else self._key_target_temperature
                await self.coordinator.async_set_control(target_key, int(temperature))

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if self._key_hvac_modes is not None:
            mode_config = self._key_hvac_modes.get(hvac_mode)
            if mode_config:
                await self.coordinator.async_set_controls(mode_config)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if self._key_preset_modes is not None:
            preset_config = self._key_preset_modes.get(preset_mode)
            if preset_config:
                await self.coordinator.async_set_controls(preset_config)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        if self._key_fan_modes is not None:
            fan_config = self._key_fan_modes.get(fan_mode)
            if fan_config:
                await self.coordinator.async_set_controls(fan_config)

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        if self._key_swing_modes is not None:
            swing_config = self._key_swing_modes.get(swing_mode)
            if swing_config:
                await self.coordinator.async_set_controls(swing_config)

    async def async_turn_aux_heat_on(self) -> None:
        if self._aux_heat is not None:
            await self.coordinator.async_set_control(self._aux_heat, self._rationale[1] if len(self._rationale) > 1 else "on")

    async def async_turn_aux_heat_off(self) -> None:
        if self._aux_heat is not None:
            await self.coordinator.async_set_control(self._aux_heat, self._rationale[0] if self._rationale else "off")

    async def async_turn_on(self) -> None:
        if self._key_power is not None:
            await self.coordinator.async_set_control(self._key_power, self._rationale[1])

    async def async_turn_off(self) -> None:
        if self._key_power is not None:
            await self.coordinator.async_set_control(self._key_power, self._rationale[0])
