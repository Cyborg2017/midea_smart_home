import logging

from homeassistant.components.fan import FanEntity, FanEntityFeature
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
        fan_config = entities_config.get(Platform.FAN, {})

        if fan_config:
            for fan_id, config in fan_config.items():
                entities.append(
                    MideaFanEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        fan_id, config, model
                    )
                )

    async_add_entities(entities)


class MideaFanEntity(MideaBaseEntity, FanEntity):
    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        fan_id: str,
        config: dict,
        model: str = None,
    ):
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, fan_id, model,
            platform_name="fan", config=config
        )
        self._fan_id = fan_id
        self._key_power = self._config.get("power")
        self._power_rationale = self._config.get("rationale")
        self._key_preset_modes = self._config.get("preset_modes", {})
        speeds_config = self._config.get("speeds", [])
        self._key_oscillate = self._config.get("oscillate")
        self._key_directions = self._config.get("directions", {})

        if isinstance(speeds_config, list) and len(speeds_config) > 0:
            if isinstance(speeds_config[0], dict) and "key" in speeds_config[0]:
                key_name = speeds_config[0]["key"]
                value_range = speeds_config[0].get("value", [1, 100])
                if isinstance(value_range, list) and len(value_range) == 2:
                    start, end = value_range[0], value_range[1]
                    self._key_speeds = [{key_name: str(i)} for i in range(start, end + 1)]
                else:
                    self._key_speeds = speeds_config
            else:
                self._key_speeds = speeds_config
        else:
            self._key_speeds = speeds_config

        self._attr_speed_count = len(self._key_speeds) if self._key_speeds else 0
        self._current_speeds = self._key_speeds

    @property
    def supported_features(self):
        features = FanEntityFeature(0)
        features |= FanEntityFeature.TURN_ON
        features |= FanEntityFeature.TURN_OFF
        if self._key_preset_modes:
            features |= FanEntityFeature.PRESET_MODE
        if self._current_speeds:
            features |= FanEntityFeature.SET_SPEED
        if self._key_oscillate:
            features |= FanEntityFeature.OSCILLATE
        if self._key_directions:
            features |= FanEntityFeature.DIRECTION
        return features

    @property
    def is_on(self) -> bool:
        return self._get_status_on_off(self._key_power)

    @property
    def preset_modes(self):
        if not self._key_preset_modes:
            return None
        return list(self._key_preset_modes.keys())

    @property
    def preset_mode(self):
        if not self._key_preset_modes:
            return None

        current_mode = self._dict_get_selected(self._key_preset_modes)

        if current_mode:
            mode_config = self._key_preset_modes.get(current_mode, {})
            if "speeds" in mode_config:
                self._current_speeds = mode_config["speeds"]
                self._attr_speed_count = len(self._current_speeds)
            else:
                self._current_speeds = self._key_speeds
                self._attr_speed_count = len(self._current_speeds) if self._current_speeds else 0

        return current_mode

    @property
    def speed_count(self):
        current_mode = self._dict_get_selected(self._key_preset_modes)
        if current_mode:
            mode_config = self._key_preset_modes.get(current_mode, {})
            if "speeds" in mode_config:
                return len(mode_config["speeds"])
        return len(self._key_speeds) if self._key_speeds else 0

    @property
    def percentage(self):
        if not self.is_on:
            return 0

        index = self._list_get_selected(self._current_speeds)
        if index is None:
            return 0

        if self._attr_speed_count == 0:
            return 0
        if self._attr_speed_count == 1:
            return 100

        return round((index + 1) * 100 / self._attr_speed_count)

    @property
    def oscillating(self):
        return self._get_status_on_off(self._key_oscillate)

    @property
    def current_direction(self):
        return self._dict_get_selected(self._key_directions)

    async def async_turn_on(
            self,
            percentage: int | None = None,
            preset_mode: str | None = None,
            **kwargs,
    ):
        new_status = {}
        if preset_mode is not None and self._key_preset_modes:
            mode_config = self._key_preset_modes.get(preset_mode, {})
            if mode_config:
                new_status = {k: v for k, v in mode_config.items() if k != "speeds"}

                if "speeds" in mode_config:
                    self._current_speeds = mode_config["speeds"]
                    self._attr_speed_count = len(self._current_speeds)
                    if len(self._current_speeds) >= 1:
                        new_status.update(self._current_speeds[0])
                else:
                    self._current_speeds = self._key_speeds
                    self._attr_speed_count = len(self._current_speeds) if self._current_speeds else 0

        if percentage is not None and self._current_speeds:
            if percentage == 0:
                await self.async_turn_off()
                return

            index = self._get_speed_index_from_percentage(percentage)
            if index >= 0:
                new_status.update(self._current_speeds[index])

        await self._async_set_status_on_off(self._key_power, True, rationale=self._power_rationale)
        if new_status:
            await self.coordinator.async_set_controls(new_status)

    async def async_turn_off(self):
        await self._async_set_status_on_off(self._key_power, False, rationale=self._power_rationale)

    async def async_set_percentage(self, percentage: int):
        if not self._current_speeds:
            return

        if percentage == 0:
            await self.async_turn_off()
            return

        if not self.is_on:
            await self._async_set_status_on_off(self._key_power, True, rationale=self._power_rationale)

        index = self._get_speed_index_from_percentage(percentage)
        if index >= 0:
            new_status = self._current_speeds[index]
            await self.coordinator.async_set_controls(new_status)

    async def async_set_preset_mode(self, preset_mode: str):
        if not self._key_preset_modes:
            return

        mode_config = self._key_preset_modes.get(preset_mode, {})
        if mode_config:
            if not self.is_on:
                await self._async_set_status_on_off(self._key_power, True, rationale=self._power_rationale)

            if "speeds" in mode_config:
                self._current_speeds = mode_config["speeds"]
                self._attr_speed_count = len(self._current_speeds)
            else:
                self._current_speeds = self._key_speeds
                self._attr_speed_count = len(self._current_speeds) if self._current_speeds else 0

            new_status = {k: v for k, v in mode_config.items() if k != "speeds"}

            if "speeds" in mode_config and len(mode_config["speeds"]) >= 1:
                new_status.update(mode_config["speeds"][0])

            await self.coordinator.async_set_controls(new_status)

    async def async_oscillate(self, oscillating: bool):
        if self.oscillating != oscillating:
            await self._async_set_status_on_off(self._key_oscillate, oscillating)

    async def async_set_direction(self, direction: str):
        if not self._key_directions:
            return
        new_status = self._key_directions.get(direction)
        if new_status:
            await self.coordinator.async_set_controls(new_status)

    def _list_get_selected(self, options_list: list):
        if not options_list:
            return None
        data = self.coordinator.data or {}
        for i, value in enumerate(options_list):
            if isinstance(value, dict):
                match = True
                for k, v in value.items():
                    if data.get(k) != v:
                        match = False
                        break
                if match:
                    return i
        return None

    def _get_speed_index_from_percentage(self, percentage: int) -> int:
        """Convert percentage to speed index (0-based)."""
        if not self._current_speeds or self._attr_speed_count == 0:
            return -1
        if self._attr_speed_count == 1:
            return 0
        index = round(percentage * self._attr_speed_count / 100) - 1
        return max(0, min(index, self._attr_speed_count - 1))
