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

from .const import CONF_DEVICE_ID, CONF_DEVICE_NAME, CONF_DEVICE_TYPE, CONF_SN, CONF_SN8, CONF_PRODUCT_MODEL, DOMAIN
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
        model = data.get(CONF_PRODUCT_MODEL, "")
        device_name = data.get(CONF_DEVICE_NAME, f"Midea Device {device_id}")
        device_type_int = int(device_type, 16) if isinstance(device_type, str) else device_type
        device_mapping = get_device_mapping(device_type_int, sn8)
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
        self.entity_id = f"climate.midea_{device_id}_{entity_key}"

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
        if self._key_current_temperature is not None:
            value = self._get_nested_value(self._key_current_temperature)
            if value is not None:
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None
        return None

    @property
    def target_temperature(self) -> Optional[float]:
        if self._key_target_temperature is not None:
            value = self._get_nested_value(self._key_target_temperature)
            if value is not None:
                try:
                    return float(value)
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
            await self._async_set_control(self._key_target_temperature, int(temperature))

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if self._key_hvac_modes is not None:
            mode_config = self._key_hvac_modes.get(hvac_mode)
            if mode_config:
                await self._async_set_multiple_controls(mode_config)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if self._key_preset_modes is not None:
            preset_config = self._key_preset_modes.get(preset_mode)
            if preset_config:
                await self._async_set_multiple_controls(preset_config)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        if self._key_fan_modes is not None:
            fan_config = self._key_fan_modes.get(fan_mode)
            if fan_config:
                await self._async_set_multiple_controls(fan_config)

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        if self._key_swing_modes is not None:
            swing_config = self._key_swing_modes.get(swing_mode)
            if swing_config:
                await self._async_set_multiple_controls(swing_config)

    async def async_turn_aux_heat_on(self) -> None:
        if self._aux_heat is not None:
            await self._async_set_control(self._aux_heat, self._rationale[1] if len(self._rationale) > 1 else "on")

    async def async_turn_aux_heat_off(self) -> None:
        if self._aux_heat is not None:
            await self._async_set_control(self._aux_heat, self._rationale[0] if self._rationale else "off")

    async def async_turn_on(self) -> None:
        if self._key_power is not None:
            await self._async_set_control(self._key_power, self._rationale[1])

    async def async_turn_off(self) -> None:
        if self._key_power is not None:
            await self._async_set_control(self._key_power, self._rationale[0])
