import logging
from typing import Any, Optional

from homeassistant.components.water_heater import WaterHeaterEntity, WaterHeaterEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform,
    ATTR_TEMPERATURE,
    UnitOfTemperature,
)
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
        water_heater_config = entities_config.get(Platform.WATER_HEATER, {})

        if water_heater_config:
            for water_heater_key, config in water_heater_config.items():
                entities.append(
                    MideaWaterHeaterEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        water_heater_key, config, rationale, model
                    )
                )

    async_add_entities(entities)


class MideaWaterHeaterEntity(MideaBaseEntity, WaterHeaterEntity):
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
        self._attr_unique_id = f"water_heater.midea_{device_id}_{entity_key}"
        self.entity_id = f"water_heater.midea_{device_id}_{entity_key}"

        self._key_power = self._config.get("power")
        self._key_operation_list = self._config.get("operation_list")
        self._key_min_temp = self._config.get("min_temp", 30)
        self._key_max_temp = self._config.get("max_temp", 75)
        self._key_current_temperature = self._config.get("current_temperature")
        self._key_target_temperature = self._config.get("target_temperature")

        self._attr_translation_key = config.get("translation_key", entity_key)
        self._attr_temperature_unit = self._config.get("temperature_unit", UnitOfTemperature.CELSIUS)
        self._attr_precision = self._config.get("precision", 1.0)
        self._attr_target_temperature_step = self._config.get("precision", 1.0)
        self._attr_min_temp = float(self._key_min_temp)
        self._attr_max_temp = float(self._key_max_temp)

    @property
    def supported_features(self):
        features = WaterHeaterEntityFeature(0)
        if hasattr(WaterHeaterEntityFeature, 'ON_OFF'):
            features |= WaterHeaterEntityFeature.ON_OFF
        if self._key_target_temperature is not None:
            features |= WaterHeaterEntityFeature.TARGET_TEMPERATURE
        if self._key_operation_list is not None:
            features |= WaterHeaterEntityFeature.OPERATION_MODE
        return features

    @property
    def operation_list(self):
        if self._key_operation_list:
            return list(self._key_operation_list.keys())
        return None

    @property
    def current_operation(self):
        if self._key_operation_list:
            return self._dict_get_selected(self._key_operation_list)
        return None

    @property
    def current_temperature(self):
        if self._key_current_temperature is not None:
            value = self._get_nested_value(self._key_current_temperature)
            if value is not None:
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None
        return None

    @property
    def target_temperature(self):
        if self._key_target_temperature is not None:
            if isinstance(self._key_target_temperature, list):
                temp_int = self._get_nested_value(self._key_target_temperature[0])
                temp_dec = self._get_nested_value(self._key_target_temperature[1])
                if temp_int is not None and temp_dec is not None:
                    try:
                        return float(temp_int) + float(temp_dec)
                    except (ValueError, TypeError):
                        return None
                return None
            else:
                value = self._get_nested_value(self._key_target_temperature)
                if value is not None:
                    try:
                        return float(value)
                    except (ValueError, TypeError):
                        return None
        return None

    @property
    def min_temp(self):
        if isinstance(self._key_min_temp, str):
            value = self._get_nested_value(self._key_min_temp)
            if value is not None:
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None
        else:
            try:
                return float(self._key_min_temp)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def max_temp(self):
        if isinstance(self._key_max_temp, str):
            value = self._get_nested_value(self._key_max_temp)
            if value is not None:
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None
        else:
            try:
                return float(self._key_max_temp)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def target_temperature_low(self):
        return self.min_temp

    @property
    def target_temperature_high(self):
        return self.max_temp

    @property
    def is_on(self) -> bool:
        return self._get_status_on_off(self._key_power)

    async def async_turn_on(self):
        await self._async_set_status_on_off(self._key_power, True)

    async def async_turn_off(self):
        await self._async_set_status_on_off(self._key_power, False)

    async def async_set_temperature(self, **kwargs):
        if ATTR_TEMPERATURE not in kwargs:
            return
        temperature = kwargs.get(ATTR_TEMPERATURE)
        temp_int, temp_dec = divmod(temperature, 1)
        temp_int = int(temp_int)
        new_status = {}
        if isinstance(self._key_target_temperature, list):
            new_status[self._key_target_temperature[0]] = temp_int
            new_status[self._key_target_temperature[1]] = temp_dec
        else:
            new_status[self._key_target_temperature] = temperature
        await self.coordinator.async_set_controls(new_status)

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        if self._key_operation_list is not None:
            new_status = self._key_operation_list.get(operation_mode)
            if new_status:
                await self.coordinator.async_set_controls(new_status)
