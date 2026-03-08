import logging
from typing import Any, Optional

from homeassistant.components.light import LightEntity, LightEntityFeature, ColorMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
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
        light_config = entities_config.get(Platform.LIGHT, {})

        if light_config:
            for light_key, config in light_config.items():
                entities.append(
                    MideaLightEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        light_key, config, rationale, model
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
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, entity_key, model)
        self._config = config
        self._rationale = rationale
        self._attr_unique_id = f"light.midea_{device_id}_{entity_key}"
        self.entity_id = f"light.midea_{device_id}_{entity_key}"

        self._key_power = self._config.get("power")
        self._key_preset_modes = self._config.get("preset_modes")
        self._key_brightness = self._config.get("brightness")
        self._key_color_temp = self._config.get("color_temp")

        self._attr_translation_key = config.get("translation_key", entity_key)

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
        if self._key_preset_modes is not None and len(self._key_preset_modes) > 0:
            features |= LightEntityFeature.EFFECT
        return features

    @property
    def supported_color_modes(self):
        modes = set()
        if self._brightness_is_range and self._color_temp_is_range:
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
        if self._brightness_is_range and self._color_temp_is_range:
            return ColorMode.COLOR_TEMP
        elif self._brightness_is_range:
            return ColorMode.BRIGHTNESS
        elif self._color_temp_is_range:
            return ColorMode.COLOR_TEMP
        return ColorMode.ONOFF

    @property
    def is_on(self) -> bool:
        return self._get_status_on_off(self._key_power)

    @property
    def effect_list(self):
        if self._key_preset_modes:
            return list(self._key_preset_modes.keys())
        return None

    @property
    def effect(self):
        if self._key_preset_modes:
            return self._dict_get_selected(self._key_preset_modes)
        return None

    @property
    def brightness(self):
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

        await self._async_set_status_on_off(self._key_power, True)
        if new_status:
            await self.coordinator.async_set_controls(new_status)

    async def async_turn_off(self):
        await self._async_set_status_on_off(self._key_power, False)
