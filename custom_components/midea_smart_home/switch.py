import logging
from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MideaCoordinator
from .entity import MideaBaseEntity, iter_midea_device_configs

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entities = []

    for coordinator, device_id, device_type, sn, sn8, device_name, model, device_mapping in iter_midea_device_configs(hass, entry):
        entities_config = device_mapping.get("entities", {})
        rationale = device_mapping.get("rationale", ["off", "on"])
        switch_config = entities_config.get(Platform.SWITCH, {})

        if switch_config:
            for switch_id, config in switch_config.items():
                translation_key = config.get("translation_key")
                switch_rationale = config.get("rationale", rationale)
                condition = config.get("condition")
                command = config.get("command")
                include_current = config.get("include_current")
                defer_update = config.get("defer_update", False)
                pending_commands = config.get("pending_commands", [])
                work_status_key = config.get("work_status_key")
                start_command = config.get("start_command")
                stop_command = config.get("stop_command")
                entities.append(
                    MideaSwitchEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        switch_id, translation_key, switch_rationale, condition, command, include_current, model,
                        defer_update, pending_commands, work_status_key, start_command, stop_command
                    )
                )

    async_add_entities(entities)


class MideaSwitchEntity(MideaBaseEntity, SwitchEntity):
    _attr_device_class = SwitchDeviceClass.SWITCH
    # Class-level storage for deferred commands per device
    _pending_commands: dict[int, dict[str, dict]] = {}

    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        switch_id: str,
        translation_key: str = None,
        rationale: list = None,
        condition: dict = None,
        command: dict = None,
        include_current: list = None,
        model: str = None,
        defer_update: bool = False,
        pending_commands: list[str] = None,
        work_status_key: str = None,
        start_command: dict = None,
        stop_command: dict = None,
    ):
        config = {"translation_key": translation_key} if translation_key else {}
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, switch_id, model,
            platform_name="switch", config=config, rationale=rationale, condition=condition
        )
        self._switch_id = switch_id
        self._command = command
        self._include_current = include_current or []
        self._defer_update = defer_update
        self._pending_commands_list = pending_commands or []
        self._work_status_key = work_status_key
        self._start_command = start_command
        self._stop_command = stop_command
        # Initialize pending commands storage for this device if not exists
        if self._device_id not in MideaSwitchEntity._pending_commands:
            MideaSwitchEntity._pending_commands[self._device_id] = {}

    def _get_status_on_off(self, attribute_key: str) -> bool:
        data = self.coordinator.data or {}
        status = data.get(attribute_key)
        if status is None:
            return False
        try:
            return bool(self._rationale.index(status))
        except ValueError:
            if isinstance(status, int) or status in ['0', '1']:
                return int(status) != 0
            _LOGGER.warning(
                "The value of attribute %s ('%s') is not in rationale %s",
                attribute_key, status, self._rationale
            )
        return False

    @property
    def is_on(self) -> bool:
        # If work_status_key is configured, use it to determine switch state
        if self._work_status_key:
            data = self.coordinator.data or {}
            work_status = data.get(self._work_status_key)
            # Check if work_status indicates "working" state
            return work_status == "work" or work_status == 8
        return self._get_status_on_off(self._switch_id)

    async def _async_set_status_on_off(self, attribute_key: str, turn_on: bool) -> None:
        # Handle deferred update mode (dish_wash switch)
        if self._defer_update:
            merged_command = {}
            if turn_on and self._start_command:
                merged_command.update(self._start_command)
            elif not turn_on and self._stop_command:
                merged_command.update(self._stop_command)

            # If turning on, merge pending commands from specified entities
            if turn_on and self._pending_commands_list:
                from .select import MideaSelectEntity
                for pending_id in self._pending_commands_list:
                    pending = MideaSelectEntity._pending_commands[self._device_id].get(pending_id, {})
                    for key, value in pending.items():
                        if key not in merged_command:
                            merged_command[key] = value
                # Clear pending commands after use
                MideaSwitchEntity._pending_commands[self._device_id] = {}

            if merged_command:
                await self.coordinator.async_set_control(merged_command)
            return

        # Original logic for non-defer switches
        value = self._rationale[int(turn_on)]
        merged_command = {}
        if isinstance(self._command, dict):
            merged_command.update(self._command)
        merged_command[attribute_key] = value

        for attr in self._include_current:
            current_value = self._get_nested_value(attr)
            if current_value is not None:
                merged_command[attr] = current_value

        await self.coordinator.async_set_control(merged_command)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._async_set_status_on_off(self._switch_id, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._async_set_status_on_off(self._switch_id, False)
