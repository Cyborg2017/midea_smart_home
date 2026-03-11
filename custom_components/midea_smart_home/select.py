import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
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
        select_config = entities_config.get(Platform.SELECT, {})

        if select_config:
            for select_id, config in select_config.items():
                options = config.get("options", {})
                command = config.get("command")
                translation_key = config.get("translation_key")
                condition = config.get("condition")
                if isinstance(options, dict):
                    option_list = list(options.keys())
                else:
                    option_list = options
                entities.append(
                    MideaSelectEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        select_id, option_list, options, command, translation_key, condition, model
                    )
                )

    async_add_entities(entities)


class MideaSelectEntity(MideaBaseEntity, SelectEntity):
    def __init__(
        self,
        coordinator: MideaCoordinator,
        device_id: int,
        device_type: str,
        sn: str,
        sn8: str,
        device_name: str,
        select_id: str,
        options: list[str],
        options_map: dict,
        command: dict | None,
        translation_key: str = None,
        condition: dict = None,
        model: str = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, select_id, model)
        self._select_id = select_id
        self._options = options
        self._options_map = options_map
        self._command = command
        self._attr_translation_key = translation_key or select_id
        self._attr_options = options
        self._attr_unique_id = f"select.midea_{device_id}_{select_id}"
        self.entity_id = f"select.midea_{device_id}_{select_id}"
        self._last_option: str | None = None
        self._condition = condition

    @property
    def available(self) -> bool:
        return super().available and self._check_condition(self._condition)

    def _dict_get_selected_for_select(self) -> str | None:
        if not isinstance(self._options_map, dict):
            return None

        for mode, status in self._options_map.items():
            match = True
            for attr, value in status.items():
                state_value = self._get_nested_value(attr)
                if state_value is None:
                    match = False
                    break
                try:
                    if isinstance(value, int) and state_value != value:
                        match = False
                        break
                    elif isinstance(value, str) and str(state_value) != value:
                        match = False
                        break
                except (TypeError, ValueError):
                    match = False
                    break
            if match:
                return mode
        return None

    @property
    def current_option(self) -> str | None:
        if isinstance(self._options_map, dict):
            matched = self._dict_get_selected_for_select()
            if matched is not None:
                self._last_option = matched
                return matched

        data = self.coordinator.data or {}
        value = data.get(self._select_id)

        if value is not None:
            if isinstance(value, str):
                if value in self._options:
                    self._last_option = value
                    return value
                try:
                    index = int(value)
                    if 0 <= index < len(self._options):
                        self._last_option = self._options[index]
                        return self._options[index]
                except (TypeError, ValueError):
                    pass
            elif isinstance(value, int):
                if 0 <= value < len(self._options):
                    self._last_option = self._options[value]
                    return self._options[value]

        return self._last_option

    async def async_select_option(self, option: str) -> None:
        if option not in self._options:
            return

        self._last_option = option

        merged_command = {}

        if isinstance(self._options_map, dict) and option in self._options_map:
            option_value = self._options_map[option]
            if isinstance(option_value, dict):
                merged_command.update(option_value)

        if self._command and isinstance(self._command, dict):
            merged_command.update(self._command)

        if merged_command:
            await self.coordinator.async_set_control(merged_command)
        else:
            index = self._options.index(option)
            await self.coordinator.async_set_control(self._select_id, index)
