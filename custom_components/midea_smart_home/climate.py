import logging
from typing import Any, Optional

from homeassistant.components.climate import (
    ATTR_HVAC_MODE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction,
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
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, entity_key, model,
            platform_name="climate", config=config, rationale=rationale, condition=config.get("condition")
        )
        self._device_type = int(self._device_type, 16) if isinstance(self._device_type, str) else self._device_type

        self._key_power = self._config.get("power")
        self._key_hvac_modes = self._config.get("hvac_modes")
        self._key_preset_modes = self._config.get("preset_modes")
        self._key_fan_modes = self._config.get("fan_modes")
        self._key_swing_modes = self._config.get("swing_modes")
        self._key_target_temperature = self._config.get("target_temperature")
        self._key_current_temperature = self._config.get("current_temperature")
        self._key_current_humidity = self._config.get("current_humidity")
        self._key_min_temp = self._config.get("min_temp", 16)
        self._key_max_temp = self._config.get("max_temp", 30)
        self._aux_heat = self._config.get("aux_heat")

        self._fan_modes_grouped = False
        self._fan_modes_config = {}

        self._attr_temperature_unit = self._config.get("temperature_unit", UnitOfTemperature.CELSIUS)
        self._attr_precision = self._config.get("precision", 1.0)
        self._attr_target_temperature_step = self._config.get("precision", 1.0)
        self._attr_min_temp = float(self._key_min_temp)
        self._attr_max_temp = float(self._key_max_temp)

        self._setup_supported_features()
        self._setup_modes()

    @property
    def is_bath_heater(self) -> bool:
        return self._device_type == 0x26

    def _needs_full_control_for_mode(self, preset_mode: str) -> bool:
        """Check if device requires full control parameters for given preset mode.

        Automatic detection based on configuration structure:
        - If fan_modes has grouped structure (preset_mode as top-level key)
        - And preset_mode exists in both fan_modes and swing_modes
        - Then requires full control (mode + speed + direction)

        This eliminates the need for manual 'special_bath_heater' configuration.
        """
        if not self.is_bath_heater:
            return False

        # Auto-detect: check if fan_modes has preset-mode-based grouping
        if not self._fan_modes_grouped:
            return False

        # Check if current mode has both fan_modes and swing_modes configured
        has_fan_config = preset_mode in self._fan_modes_config
        has_swing_config = preset_mode in self._key_swing_modes if isinstance(self._key_swing_modes, dict) else False

        return has_fan_config and has_swing_config

    def _build_full_control_command(self, preset_mode: str, speed_key: str = None,
                                     dir_key: str = None, speed_value = None,
                                     dir_value = None) -> dict:
        """Build full control command with mode + speed + direction.

        Args:
            preset_mode: Current preset mode (e.g., 'blowing')
            speed_key: Speed attribute key (e.g., 'blowing_speed')
            dir_key: Direction attribute key (e.g., 'blowing_direction')
            speed_value: Speed value to set
            dir_value: Direction value to set

        Returns:
            Control command dict with full parameters
        """
        # Get default values if not provided
        if speed_key and speed_value is None:
            default_speed, _ = self._get_default_speed_and_direction(speed_key, dir_key)
            speed_value = default_speed

        if dir_key and dir_value is None:
            _, default_dir = self._get_default_speed_and_direction(speed_key, dir_key)
            dir_value = default_dir

        # Build full control command
        control = {"mode": preset_mode}
        if speed_key and speed_value is not None:
            control[speed_key] = speed_value
        if dir_key and dir_value is not None:
            control[dir_key] = dir_value

        return control

    def _get_default_speed_and_direction(self, speed_key: str, dir_key: str) -> tuple:
        """Get default speed and direction values from config or use fallback values"""
        # Get default speed from config
        fan_mode_config = self._fan_modes_config.get("blowing") if self._fan_modes_grouped else None
        default_speed = 30  # Fallback default
        if fan_mode_config:
            options = fan_mode_config.get("options")
            if options:
                first_option = next(iter(options.values()), None)
                if first_option:
                    if isinstance(first_option, dict):
                        default_speed = first_option.get(speed_key, default_speed)
                    else:
                        default_speed = first_option

        # Get default direction from config
        swing_mode_config = self._key_swing_modes.get("blowing") if isinstance(self._key_swing_modes, dict) else None
        default_direction = 90  # Fallback default
        if swing_mode_config:
            options = swing_mode_config.get("options")
            if options:
                first_option = next(iter(options.values()), None)
                if first_option:
                    if isinstance(first_option, dict):
                        default_direction = first_option.get(dir_key, default_direction)
                    else:
                        default_direction = first_option

        return default_speed, default_direction

    def _safe_convert_to_float(self, value) -> Optional[float]:
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

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
            # Check if this is grouped mode (for bath heaters)
            if self.is_bath_heater and isinstance(self._key_fan_modes, dict):
                # Check if first level keys are all preset modes and values contain "options"
                first_key = next(iter(self._key_fan_modes), None)
                if first_key and first_key in (self._attr_preset_modes or []):
                    # Grouped mode
                    self._fan_modes_grouped = True
                    self._fan_modes_config = self._key_fan_modes
                    # Take the first mode's options keys as the fan modes list (assuming all grouped modes have consistent options)
                    first_mode_config = self._key_fan_modes.get(first_key)
                    if first_mode_config and isinstance(first_mode_config, dict) and "options" in first_mode_config:
                        self._attr_fan_modes = list(first_mode_config["options"].keys())
                    else:
                        self._attr_fan_modes = []
                else:
                    self._attr_fan_modes = list(self._key_fan_modes.keys())
            else:
                self._attr_fan_modes = list(self._key_fan_modes.keys())

        if self._key_swing_modes is not None:
            if self.is_bath_heater and isinstance(self._key_swing_modes, dict):
                first_mode = next(iter(self._key_swing_modes.values()), None)
                if first_mode and isinstance(first_mode, dict) and "options" in first_mode:
                    self._attr_swing_modes = list(first_mode["options"].keys())
                else:
                    self._attr_swing_modes = list(self._key_swing_modes.keys())
            else:
                self._attr_swing_modes = list(self._key_swing_modes.keys())

    @property
    def hvac_mode(self) -> HVACMode:
        if self._key_hvac_modes is not None:
            if self.is_bath_heater:
                return self._get_bath_heater_hvac_mode()
            return self._dict_get_selected(self._key_hvac_modes, HVACMode.OFF)

        data = self.coordinator.data or {}
        power = data.get(self._key_power, 0)
        if self._is_off(power):
            return HVACMode.OFF
        return HVACMode.HEAT

    def _get_bath_heater_hvac_mode(self) -> HVACMode:
        data = self.coordinator.data or {}
        current_mode = data.get("mode")

        if current_mode == "close_all":
            return HVACMode.OFF

        mode_mapping = {
            "heating": HVACMode.HEAT,
            "bath": HVACMode.HEAT,
            "drying": HVACMode.DRY,
            "ventilation": HVACMode.AUTO,
            "blowing": HVACMode.FAN_ONLY,
        }

        return mode_mapping.get(current_mode, HVACMode.AUTO)

    @property
    def current_temperature(self) -> Optional[float]:
        if isinstance(self._key_current_temperature, list):
            temp_int = self._get_nested_value(self._key_current_temperature[0])
            tem_dec = self._get_nested_value(self._key_current_temperature[1])
            if temp_int is not None and tem_dec is not None:
                t_int = self._safe_convert_to_float(temp_int)
                t_dec = self._safe_convert_to_float(tem_dec)
                if t_int is not None and t_dec is not None:
                    return t_int + t_dec
                return None
            return None

        return self._safe_convert_to_float(
            self._get_nested_value(self._key_current_temperature)
        )

    @property
    def current_humidity(self) -> Optional[float]:
        if self._key_current_humidity is None:
            return None
        return self._safe_convert_to_float(
            self._get_nested_value(self._key_current_humidity)
        )

    @property
    def target_temperature(self) -> Optional[float]:
        if isinstance(self._key_target_temperature, dict):
            if self.is_bath_heater:
                return self._get_bath_heater_target_temp()
            return None

        if isinstance(self._key_target_temperature, list):
            return self._get_target_temp_from_list()

        return self._safe_convert_to_float(
            self._get_nested_value(self._key_target_temperature)
        )

    def _get_bath_heater_target_temp(self) -> Optional[float]:
        current_mode = self.preset_mode
        key = self._key_target_temperature.get(current_mode)

        if not key:
            return None

        return self._safe_convert_to_float(
            self._get_nested_value(key)
        )

    def _get_target_temp_from_list(self) -> Optional[float]:
        if len(self._key_target_temperature) == 1:
            return self._safe_convert_to_float(
                self._get_nested_value(self._key_target_temperature[0])
            )

        try:
            temp_int = self._get_nested_value(self._key_target_temperature[0])
            tem_dec = self._get_nested_value(self._key_target_temperature[1])
        except IndexError as e:
            _LOGGER.error(
                "target_temperature list index error: _key_target_temperature=%s, len=%d",
                self._key_target_temperature,
                len(self._key_target_temperature)
            )
            return None

        if temp_int is not None and tem_dec is not None:
            t_int = self._safe_convert_to_float(temp_int)
            t_dec = self._safe_convert_to_float(tem_dec)
            if t_int is not None and t_dec is not None:
                return t_int + t_dec
            return None
        return None

    @property
    def preset_mode(self) -> Optional[str]:
        if self._key_preset_modes is not None:
            return self._dict_get_selected(self._key_preset_modes)
        return None

    @property
    def fan_mode(self) -> Optional[str]:
        if self._key_fan_modes is None:
            return None

        if self._fan_modes_grouped:
            # Grouped mode: select corresponding configuration based on current preset mode
            current_mode = self.preset_mode
            if current_mode is None:
                return None
            mode_config = self._fan_modes_config.get(current_mode)
            if not (mode_config and isinstance(mode_config, dict)):
                return None
            speed_key = mode_config.get("key")
            options = mode_config.get("options")
            if not speed_key or not options:
                return None
            current_value = self._get_nested_value(speed_key)
            if current_value is None:
                return None
            # Match fan mode
            for option_key, option_config in options.items():
                if isinstance(option_config, dict):
                    if any(str(v) == str(current_value) for v in option_config.values()):
                        return option_key
                elif str(option_config) == str(current_value):
                    return option_key
            return None
        else:
            # Flat mode (original logic)
            return self._dict_get_selected(self._key_fan_modes)

    @property
    def swing_mode(self) -> Optional[str]:
        if self._key_swing_modes is None:
            return None

        if not (self.is_bath_heater and isinstance(self._key_swing_modes, dict)):
            return self._dict_get_selected(self._key_swing_modes)

        return self._get_bath_heater_swing_mode()

    def _get_bath_heater_swing_mode(self) -> Optional[str]:
        current_mode = self.preset_mode
        mode_config = self._key_swing_modes.get(current_mode)

        if not (mode_config and isinstance(mode_config, dict)):
            return self._dict_get_selected(self._key_swing_modes)

        direction_key = mode_config.get("key")
        options = mode_config.get("options")

        if not (direction_key and options):
            return self._dict_get_selected(self._key_swing_modes)

        current_value = self._get_nested_value(direction_key)
        if current_value is None:
            return None

        return self._match_swing_option(options, str(current_value))

    def _match_swing_option(self, options: dict, current_value: str) -> Optional[str]:
        for option_key, option_config in options.items():
            if isinstance(option_config, dict):
                if any(str(attr_value) == current_value for attr_value in option_config.values()):
                    return option_key
            elif str(option_config) == current_value:
                return option_key
        return None

    @property
    def is_aux_heat(self) -> bool:
        if self._aux_heat is not None:
            value = self._get_nested_value(self._aux_heat)
            return self._is_on(value)
        return False

    @property
    def hvac_action(self) -> HVACAction:
        if self.hvac_mode == HVACMode.OFF:
            return HVACAction.OFF

        current_mode = self.hvac_mode
        if current_mode == HVACMode.FAN_ONLY:
            return HVACAction.FAN
        elif current_mode == HVACMode.DRY:
            return HVACAction.DRYING

        # Get current and target temperatures
        current_temp = self.current_temperature
        target_temp = self.target_temperature

        # If we have both temperatures, use them to determine action
        if current_temp is not None and target_temp is not None:
            if current_mode == HVACMode.HEAT:
                # Heating if current temp is below target
                if current_temp < target_temp:
                    return HVACAction.HEATING
                else:
                    return HVACAction.IDLE
            elif current_mode == HVACMode.COOL:
                # Cooling if current temp is above target
                if current_temp > target_temp:
                    return HVACAction.COOLING
                else:
                    return HVACAction.IDLE
            elif current_mode == HVACMode.AUTO:
                # In auto mode, determine based on temperature difference
                # Assuming a small hysteresis of 1 degree
                if current_temp < target_temp - 0.5:
                    return HVACAction.HEATING
                elif current_temp > target_temp + 0.5:
                    return HVACAction.COOLING
                else:
                    return HVACAction.IDLE

        # Fallback to mode-based determination if temperature data is unavailable
        if current_mode == HVACMode.HEAT:
            return HVACAction.HEATING
        elif current_mode == HVACMode.COOL:
            return HVACAction.COOLING
        else:
            return HVACAction.IDLE

    async def async_set_temperature(self, **kwargs: Any) -> None:
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        hvac_mode = kwargs.get(ATTR_HVAC_MODE)
        if hvac_mode is not None:
            await self.async_set_hvac_mode(hvac_mode)

        if self._key_target_temperature is not None:
            if isinstance(self._key_target_temperature, dict):
                if self.is_bath_heater:
                    current_mode = self.preset_mode
                    target_key = self._key_target_temperature.get(current_mode)
                    if target_key:
                        await self.coordinator.async_set_control(target_key, int(temperature))
            elif isinstance(self._key_target_temperature, list) and len(self._key_target_temperature) == 2:
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
            if self.is_bath_heater and hvac_mode != HVACMode.OFF:
                return
            mode_config = self._key_hvac_modes.get(hvac_mode)
            if mode_config:
                await self.coordinator.async_set_controls(mode_config)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if self._key_preset_modes is None:
            return
        preset_config = self._key_preset_modes.get(preset_mode)
        if not preset_config:
            return

        # Use unified control builder if device needs full control
        if self._needs_full_control_for_mode(preset_mode):
            # Get speed and direction configuration
            fan_mode_config = self._fan_modes_config.get(preset_mode)
            speed_key = fan_mode_config.get("key") if fan_mode_config else None

            swing_mode_config = self._key_swing_modes.get(preset_mode) if isinstance(self._key_swing_modes, dict) else None
            dir_key = swing_mode_config.get("key") if swing_mode_config else None

            # Get current values
            data = self.coordinator.data or {}
            current_speed = data.get(speed_key) if speed_key else None
            current_direction = data.get(dir_key) if dir_key else None

            # Build and send full control command
            full_control = self._build_full_control_command(
                preset_mode=preset_mode,
                speed_key=speed_key,
                dir_key=dir_key,
                speed_value=current_speed,
                dir_value=current_direction
            )
            await self.coordinator.async_set_controls(full_control)
        else:
            await self.coordinator.async_set_controls(preset_config)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        if self._key_fan_modes is None:
            return

        if self._fan_modes_grouped:
            # Grouped mode: find corresponding options based on current preset mode
            current_mode = self.preset_mode
            if current_mode is None:
                _LOGGER.warning("Cannot set fan mode: preset_mode is None")
                return
            mode_config = self._fan_modes_config.get(current_mode)
            if not (mode_config and isinstance(mode_config, dict)):
                _LOGGER.warning("No fan config for preset mode %s", current_mode)
                return
            options = mode_config.get("options")
            if not options:
                return
            fan_config = options.get(fan_mode)
            if not fan_config:
                _LOGGER.warning("Fan mode %s not found for preset %s", fan_mode, current_mode)
                return

            # Use unified control builder if device needs full control
            if self._needs_full_control_for_mode(current_mode):
                speed_key = mode_config.get("key")
                if not speed_key:
                    _LOGGER.warning("No speed key found for fan mode config")
                    return
                speed_value = fan_config.get(speed_key)
                if speed_value is None:
                    _LOGGER.warning("No speed value found in fan config")
                    return

                # Get direction configuration
                swing_mode_config = self._key_swing_modes.get(current_mode) if isinstance(self._key_swing_modes, dict) else None
                dir_key = swing_mode_config.get("key") if swing_mode_config else None

                # Get current direction
                data = self.coordinator.data or {}
                current_direction = data.get(dir_key) if dir_key else None

                # Build and send full control command
                full_control = self._build_full_control_command(
                    preset_mode=current_mode,
                    speed_key=speed_key,
                    dir_key=dir_key,
                    speed_value=speed_value,
                    dir_value=current_direction
                )
                await self.coordinator.async_set_controls(full_control)
            else:
                await self.coordinator.async_set_controls(fan_config)
        else:
            # Flat mode (original logic)
            fan_config = self._key_fan_modes.get(fan_mode)
            if fan_config:
                await self.coordinator.async_set_controls(fan_config)

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        if self._key_swing_modes is None:
            return

        if not isinstance(self._key_swing_modes, dict):
            swing_config = self._key_swing_modes.get(swing_mode)
            if swing_config:
                await self.coordinator.async_set_controls(swing_config)
            return

        if self.is_bath_heater:
            await self._set_bath_heater_swing_mode(swing_mode)
            return

        swing_config = self._key_swing_modes.get(swing_mode)
        if swing_config:
            await self.coordinator.async_set_controls(swing_config)

    async def _set_bath_heater_swing_mode(self, swing_mode: str) -> None:
        current_mode = self.preset_mode
        mode_config = self._key_swing_modes.get(current_mode)

        if not (mode_config and isinstance(mode_config, dict)):
            return

        options = mode_config.get("options")
        if not options:
            return

        swing_config = options.get(swing_mode)
        if not swing_config:
            return

        # Use unified control builder if device needs full control
        if self._needs_full_control_for_mode(current_mode):
            # Get speed configuration
            fan_mode_config = self._fan_modes_config.get(current_mode) if self._fan_modes_grouped else None
            speed_key = fan_mode_config.get("key") if fan_mode_config else None

            # Get direction key and value
            dir_key = mode_config.get("key")
            if not dir_key:
                _LOGGER.warning("No direction key found for swing mode config")
                return
            dir_value = swing_config.get(dir_key)
            if dir_value is None:
                _LOGGER.warning("No direction value found in swing config")
                return

            # Get current speed
            data = self.coordinator.data or {}
            current_speed = data.get(speed_key) if speed_key else None

            # Build and send full control command
            full_control = self._build_full_control_command(
                preset_mode=current_mode,
                speed_key=speed_key,
                dir_key=dir_key,
                speed_value=current_speed,
                dir_value=dir_value
            )
            await self.coordinator.async_set_controls(full_control)
        else:
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
