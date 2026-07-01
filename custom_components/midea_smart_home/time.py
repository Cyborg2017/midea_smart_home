import logging
import math
from datetime import time, datetime, timedelta

from homeassistant.components.time import TimeEntity
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
        time_config = entities_config.get(Platform.TIME, {})

        if time_config:
            for time_id, config in time_config.items():
                entities.append(
                    MideaTimeEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        time_id, config, model
                    )
                )

    async_add_entities(entities)


class MideaTimeEntity(MideaBaseEntity, TimeEntity):
    """Time entity that can work with either absolute or relative time."""

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
        model: str = None,
    ):
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, entity_key, model,
            platform_name="time", config=config, condition=config.get("condition")
        )
        self._target_keys = config.get("target_keys", {})
        self._translation_key = config.get("translation_key")
        # Determine time mode:
        # - "direct": device receives absolute time directly (user input -> device)
        # - "convert": device receives relative time/duration (user input -> convert to duration -> device)
        self._time_mode = config.get("time_mode", "convert")
        # Check if using single duration field or separate hour/minute fields
        self._use_duration = "duration" in self._target_keys

    @property
    def native_value(self) -> time | None:
        """Return the current time value."""
        if not self.coordinator.data:
            return None

        if self._use_duration:
            # Single duration field mode
            duration_minutes = self.coordinator.data.get(self._target_keys.get("duration"))
            
            if duration_minutes is None:
                return None
            
            try:
                duration_minutes = int(duration_minutes)
                
                # Check if timer is not set (duration is 0)
                if duration_minutes == 0:
                    return None
                
                if self._time_mode == "convert":
                    # Device uses relative time: convert duration to target time
                    now = datetime.now()
                    target_time = now + timedelta(minutes=duration_minutes)
                    # Return time without seconds and microseconds
                    return time(hour=target_time.hour, minute=target_time.minute)
                else:
                    # Device uses absolute time: convert duration to time format
                    hours = duration_minutes // 60
                    minutes = duration_minutes % 60
                    return time(hour=min(hours, 23), minute=min(minutes, 59))
            except (ValueError, TypeError):
                _LOGGER.warning("Failed to convert duration value for entity %s", self._entity_key)
                return None
        else:
            # Separate hour/minute fields mode
            hours = self.coordinator.data.get(self._target_keys.get("hour"))
            minutes = self.coordinator.data.get(self._target_keys.get("minute"))

            if hours is None or minutes is None:
                return None

            try:
                hours = int(hours)
                minutes = int(minutes)
                
                # Check if timer is not set (both hours and minutes are 0)
                if hours == 0 and minutes == 0:
                    return None

                if self._time_mode == "convert":
                    # Device uses relative time: convert absolute time to duration
                    # User input 15:30 -> convert to "how long from now" -> send to device
                    now = datetime.now()
                    target_time = now + timedelta(hours=hours, minutes=minutes)
                    # Return time without seconds and microseconds
                    return time(hour=target_time.hour, minute=target_time.minute)
                else:
                    # Device uses absolute time: directly show the time value
                    # User input 15:30 -> show 15:30 -> send 15:30 to device
                    return time(hour=min(hours, 23), minute=min(minutes, 59))
            except (ValueError, TypeError):
                _LOGGER.warning("Failed to convert time values for entity %s", self._entity_key)
                return None

    async def async_set_value(self, value: time) -> None:
        """Set the time value."""
        try:
            now = datetime.now()
            
            # Get command configuration if exists
            command_config = self._config.get("command", {})

            if self._use_duration:
                # Single duration field mode
                if "duration" not in self._target_keys:
                    _LOGGER.error("Missing 'duration' key in target_keys for entity %s", self._entity_key)
                    return
                
                if self._time_mode == "convert":
                    # Convert target time to duration
                    target_datetime = datetime.combine(now.date(), value)
                    time_diff = target_datetime - now

                    # Handle case where target time is earlier than current time (next day)
                    if time_diff.total_seconds() < 0:
                        time_diff += timedelta(hours=24)

                    # Use ceiling to ensure we reach the target time
                    total_minutes = math.ceil(time_diff.total_seconds() / 60)

                    command = {
                        self._target_keys["duration"]: total_minutes,
                        **command_config  # Merge with additional command config
                    }
                else:
                    # Direct mode: convert time to duration
                    total_minutes = value.hour * 60 + value.minute
 
                    command = {
                        self._target_keys["duration"]: total_minutes,
                        **command_config
                    }
            else:
                # Separate hour/minute fields mode
                if "hour" not in self._target_keys or "minute" not in self._target_keys:
                    _LOGGER.error("Missing 'hour' or 'minute' key in target_keys for entity %s", self._entity_key)
                    return
                
                if self._time_mode == "convert":
                    # Device uses relative time: convert user's target time to duration
                    # User inputs 15:30, calculate how long from now, send duration to device
                    target_datetime = datetime.combine(now.date(), value)
                    time_diff = target_datetime - now

                    # Handle case where target time is earlier than current time (next day)
                    if time_diff.total_seconds() < 0:
                        time_diff += timedelta(hours=24)

                    # Use ceiling to ensure we reach the target time
                    total_seconds = math.ceil(time_diff.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60

                else:
                    # Device uses absolute time: directly send the time value
                    # User inputs 15:30, send 15:30 (hour=15, minute=30) to device
                    hours = value.hour
                    minutes = value.minute

                # Send to device
                command = {
                    self._target_keys["hour"]: hours,
                    self._target_keys["minute"]: minutes,
                    **command_config
                }

            await self.coordinator.async_set_control(command)
            
        except Exception as e:
            _LOGGER.error("Failed to set time value for entity %s: %s", self._entity_key, str(e))
            raise
