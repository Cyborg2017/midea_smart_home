import logging
from typing import Any, Optional

from homeassistant.components.light import LightEntity, LightEntityFeature, ColorMode
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
        rationale = device_mapping.get("rationale", ["off", "on"])
        light_config = entities_config.get(Platform.LIGHT, {})

        if light_config:
            for light_key, config in light_config.items():
                light_rationale = config.get("rationale", rationale)
                entities.append(
                    MideaLightEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        light_key, config, light_rationale, model
                    )
                )

    async_add_entities(entities)


class MideaLightEntity(MideaBaseEntity, LightEntity):
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
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, entity_key, model,
            platform_name="light", config=config, rationale=rationale
        )

        self._key_power = self._config.get("power")
        self._key_preset_modes = self._config.get("preset_modes")
        self._key_brightness = self._config.get("brightness")
        self._key_color_temp = self._config.get("color_temp")
        self._command = self._config.get("command")

        # cloud_v2 Thing-style light: raw thing keys for power/brightness and
        # int scene indices for effects.
        self._thing_light = "power_key" in self._config
        self._key_power = self._key_power or self._config.get("power_key")
        self._key_effect = self._config.get("effect_key")
        self._scenes = list(self._config.get("scenes") or [])
        self._scene_translation_keys = list(
            self._config.get("scenes_translation_keys") or []
        )
        if self._thing_light and self._scenes:
            self._key_brightness = self._config.get("brightness_key")
        # display label -> scene index; label defaults to the translation key
        if len(self._scene_translation_keys) == len(self._scenes):
            self._scene_by_label = dict(zip(self._scene_translation_keys, self._scenes))
            self._label_by_scene = dict(zip(self._scenes, self._scene_translation_keys))
        else:
            self._scene_by_label = {str(s): s for s in self._scenes}
            self._label_by_scene = {s: str(s) for s in self._scenes}

        self._brightness_is_range = False
        self._brightness_min = 0
        self._brightness_max = 255
        self._brightness_key = "brightness"

        if self._key_brightness:
            if isinstance(self._key_brightness, list) and len(self._key_brightness) == 2:
                if isinstance(self._key_brightness[0], (int, float)) and isinstance(self._key_brightness[1], (int, float)):
                    self._brightness_is_range = True
                    self._brightness_min = self._key_brightness[0]
                    self._brightness_max = self._key_brightness[1]
            elif isinstance(self._key_brightness, dict):
                for key, value in self._key_brightness.items():
                    if isinstance(value, list) and len(value) == 2:
                        if isinstance(value[0], (int, float)) and isinstance(value[1], (int, float)):
                            self._brightness_is_range = True
                            self._brightness_min = value[0]
                            self._brightness_max = value[1]
                            self._brightness_key = key
                            break

        self._color_temp_is_range = False
        self._color_temp_min = 2700
        self._color_temp_max = 6500
        self._color_temp_key = "color_temp"
        self._color_temp_device_range = [1, 100]

        if self._key_color_temp:
            if isinstance(self._key_color_temp, dict):
                if "kelvin_range" in self._key_color_temp and "device_range" in self._key_color_temp:
                    kelvin_range = self._key_color_temp["kelvin_range"]
                    device_range = self._key_color_temp["device_range"]
                    if (
                        isinstance(kelvin_range, list)
                        and len(kelvin_range) == 2
                        and isinstance(device_range, list)
                        and len(device_range) == 2
                    ):
                        self._color_temp_is_range = True
                        self._color_temp_min = kelvin_range[0]
                        self._color_temp_max = kelvin_range[1]
                        self._color_temp_device_range = device_range
                        self._color_temp_key = "color_temp"
                else:
                    for key, value in self._key_color_temp.items():
                        if isinstance(value, dict):
                            if "kelvin_range" in value and "device_range" in value:
                                kelvin_range = value["kelvin_range"]
                                device_range = value["device_range"]
                                if (
                                    isinstance(kelvin_range, list)
                                    and len(kelvin_range) == 2
                                    and isinstance(device_range, list)
                                    and len(device_range) == 2
                                ):
                                    self._color_temp_is_range = True
                                    self._color_temp_min = kelvin_range[0]
                                    self._color_temp_max = kelvin_range[1]
                                    self._color_temp_device_range = device_range
                                    self._color_temp_key = key
                                    break

    @property
    def supported_features(self):
        features = LightEntityFeature(0)
        if self._thing_light and self._scenes:
            features |= LightEntityFeature.EFFECT
        if self._key_preset_modes is not None and len(self._key_preset_modes) > 0:
            features |= LightEntityFeature.EFFECT
        return features

    @property
    def supported_color_modes(self):
        modes = set()
        if self._thing_light and self._key_brightness:
            modes.add(ColorMode.BRIGHTNESS)
        elif self._brightness_is_range and self._color_temp_is_range:
            modes.add(ColorMode.COLOR_TEMP)
        elif self._brightness_is_range:
            modes.add(ColorMode.BRIGHTNESS)
        elif self._color_temp_is_range:
            modes.add(ColorMode.COLOR_TEMP)
        else:
            modes.add(ColorMode.ONOFF)
        return modes

    @property
    def color_mode(self):
        if self._thing_light and self._key_brightness:
            return ColorMode.BRIGHTNESS
        if self._brightness_is_range and self._color_temp_is_range:
            return ColorMode.COLOR_TEMP
        elif self._brightness_is_range:
            return ColorMode.BRIGHTNESS
        elif self._color_temp_is_range:
            return ColorMode.COLOR_TEMP
        return ColorMode.ONOFF

    async def async_added_to_hass(self) -> None:
        """Load translated effect scene labels once the entity is added."""
        await super().async_added_to_hass()
        if not (self._thing_light and self._scenes and self._scene_translation_keys):
            return
        if len(self._scene_translation_keys) != len(self._scenes):
            return
        # Light effect states live under state_attributes.effect.state
        translations = await self._load_effect_labels()
        if not translations:
            return
        self._scene_by_label = {}
        self._label_by_scene = {}
        for key, scene in zip(self._scene_translation_keys, self._scenes):
            label = translations.get(key, key)
            self._scene_by_label[label] = scene
            self._label_by_scene[scene] = label
        self.async_write_ha_state()

    async def _load_effect_labels(self) -> dict[str, str]:
        """Load entity.light.<key>.state_attributes.effect.state labels."""
        from homeassistant.helpers.translation import async_get_translations
        from .const import DOMAIN

        translation_key = self._config.get("translation_key")
        if not translation_key:
            return {}
        translations = await async_get_translations(
            self.hass, self.hass.config.language, "entity", {DOMAIN}
        )
        prefix = (
            f"component.{DOMAIN}.entity.light.{translation_key}"
            ".state_attributes.effect.state."
        )
        return {
            key[len(prefix):]: value
            for key, value in translations.items()
            if key.startswith(prefix)
        }

    @property
    def is_on(self) -> bool:
        if self._key_power is None:
            return False
        value = self._get_nested_value(self._key_power)
        if value is None:
            return False
        if self._thing_light:
            # cloud_v2 power properties are real booleans
            return bool(value)
        try:
            return bool(self._rationale.index(value))
        except ValueError:
            # When rationale is defined but the value is not in it,
            # the light should be considered off (not on).
            # This handles the case where multiple lights share the same
            # power key with different rationale values (e.g., light_mode).
            return False

    @property
    def effect_list(self):
        if self._thing_light:
            return list(self._scene_by_label.keys()) if self._scenes else None
        if self._key_preset_modes:
            return list(self._key_preset_modes.keys())
        return None

    @property
    def effect(self):
        if self._thing_light:
            if not (self._scenes and self._key_effect):
                return None
            value = self._get_nested_value(self._key_effect)
            if value is None:
                return None
            try:
                return self._label_by_scene.get(int(value))
            except (ValueError, TypeError):
                return None
        if self._key_preset_modes:
            return self._dict_get_selected(self._key_preset_modes)
        return None

    @property
    def brightness(self):
        if self._thing_light:
            if not self._key_brightness:
                return None
            value = self._get_nested_value(self._key_brightness)
            if value is None:
                return None
            try:
                device_value = int(value)
            except (ValueError, TypeError):
                return None
            # Device range 1-100 -> HA 1-255
            return max(1, min(255, round(device_value * 255 / 100)))
        if not self._brightness_is_range:
            return None

        brightness_value = self._get_nested_value(self._brightness_key)
        if brightness_value is not None:
            try:
                brightness_value = int(brightness_value)
            except (ValueError, TypeError):
                return None
        if brightness_value is not None:
            if self._brightness_min == 0 and self._brightness_max == 255:
                return max(1, min(255, brightness_value))
            else:
                device_range = self._brightness_max - self._brightness_min
                if device_range > 0:
                    ha_brightness = round((brightness_value - self._brightness_min) * 255 / device_range)
                    return max(1, min(255, ha_brightness))
        return None

    @property
    def color_temp_kelvin(self):
        if not self._color_temp_is_range:
            return None

        color_temp_value = self._get_nested_value(self._color_temp_key)
        if color_temp_value is not None:
            try:
                device_value = int(color_temp_value)
                device_min, device_max = self._color_temp_device_range

                kelvin_range = self._color_temp_max - self._color_temp_min
                if kelvin_range > 0:
                    device_range = device_max - device_min
                    if device_range > 0:
                        normalized = (device_value - device_min) / device_range
                        ha_color_temp = self._color_temp_min + normalized * kelvin_range
                        return round(ha_color_temp)
                    else:
                        return self._color_temp_min
                else:
                    return self._color_temp_min
            except (ValueError, TypeError):
                return None
        return None

    @property
    def min_color_temp_kelvin(self):
        if self._color_temp_is_range:
            return self._color_temp_min
        return None

    @property
    def max_color_temp_kelvin(self):
        if self._color_temp_is_range:
            return self._color_temp_max
        return None

    async def async_turn_on(
            self,
            brightness: int | None = None,
            brightness_pct: int | None = None,
            percentage: int | None = None,
            color_temp_kelvin: int | None = None,
            effect: str | None = None,
            preset_mode: str | None = None,
            **kwargs,
    ):
        new_status = {}

        if self._thing_light:
            # cloud_v2: power bool, brightness 1-100, effect scene index
            if not self.is_on:
                await self.coordinator.async_set_controls({self._key_power: True})
            if effect is not None and self._key_effect:
                scene = self._scene_by_label.get(effect)
                if scene is not None:
                    new_status[self._key_effect] = scene
            target_brightness = None
            if brightness is not None:
                target_brightness = brightness
            elif brightness_pct is not None:
                target_brightness = round(brightness_pct * 255 / 100)
            elif percentage is not None:
                target_brightness = round(percentage * 255 / 100)
            if target_brightness is not None and self._key_brightness:
                device_value = max(1, min(100, round(target_brightness * 100 / 255)))
                new_status[self._key_brightness] = device_value
            for key, value in new_status.items():
                await self.coordinator.async_set_controls({key: value})
            return

        if effect is not None and self._key_preset_modes is not None:
            effect_config = self._key_preset_modes.get(effect, {})
            new_status.update(effect_config)

        target_brightness = None
        if brightness is not None:
            target_brightness = brightness
        elif brightness_pct is not None:
            target_brightness = round(brightness_pct * 255 / 100)
        elif percentage is not None:
            target_brightness = round(percentage * 255 / 100)

        if target_brightness is not None and self._key_brightness and self._brightness_is_range:
            target_brightness = max(0, min(255, target_brightness))

            if self._brightness_min == 0 and self._brightness_max == 255:
                device_brightness = target_brightness
            else:
                device_range = self._brightness_max - self._brightness_min
                if device_range > 0:
                    device_brightness = round(self._brightness_min + (target_brightness / 255.0) * device_range)
                    device_brightness = max(self._brightness_min, min(self._brightness_max, device_brightness))
                else:
                    return
            new_status[self._brightness_key] = device_brightness

        if color_temp_kelvin is not None and self._color_temp_is_range:
            ha_color_temp = max(self._color_temp_min, min(self._color_temp_max, color_temp_kelvin))

            device_min, device_max = self._color_temp_device_range

            kelvin_range = self._color_temp_max - self._color_temp_min
            if kelvin_range > 0:
                device_range = device_max - device_min
                if device_range > 0:
                    normalized = (ha_color_temp - self._color_temp_min) / kelvin_range
                    device_value = round(device_min + normalized * device_range)
                    device_value = max(device_min, min(device_max, device_value))
                else:
                    device_value = device_min
            else:
                device_value = device_min

            new_status[self._color_temp_key] = str(device_value)

        # Split controls into individual commands to ensure each takes effect.
        is_currently_on = self.is_on

        # Step 1: If light is off, send power-on first as a separate command
        if self._key_power and not is_currently_on:
            power_cmd = {self._key_power: self._rationale[1]}
            if self._command and isinstance(self._command, dict):
                power_cmd = {**self._command, **power_cmd}
            await self.coordinator.async_set_controls(power_cmd)

        # Step 2: Send each remaining property as an individual command
        if new_status:
            for key, value in new_status.items():
                cmd = {key: value}
                if self._command and isinstance(self._command, dict):
                    cmd = {**self._command, **cmd}
                await self.coordinator.async_set_controls(cmd)

    async def async_turn_off(self):
        if self._thing_light:
            if self._key_power:
                await self.coordinator.async_set_controls({self._key_power: False})
            return
        if self._key_power:
            new_status = {self._key_power: self._rationale[0]}
            if self._command and isinstance(self._command, dict):
                merged = dict(self._command)
                merged.update(new_status)
                new_status = merged
            await self.coordinator.async_set_controls(new_status)
