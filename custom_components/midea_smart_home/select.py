import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONNECTION_TYPE_CLOUD_V2
from .coordinator import MideaCoordinator
from .entity import MideaBaseEntity, iter_midea_device_configs, async_load_state_labels

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
                condition = config.get("condition")
                status_key = config.get("status_key")
                ignore_values = config.get("ignore_values")
                include_current = config.get("include_current")
                if isinstance(options, dict):
                    option_list = list(options.keys())
                else:
                    option_list = options
                entities.append(
                    MideaSelectEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        select_id, option_list, options, command, condition, status_key,
                        ignore_values, include_current, model, config
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
        options: list,
        options_map: dict,
        command: dict | None,
        condition: dict = None,
        status_key: str = None,
        ignore_values: list = None,
        include_current: list = None,
        model: str = None,
        config: dict = None,
    ):
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, select_id, model,
            platform_name="select", config=config or {}, condition=condition
        )
        self._select_id = select_id
        # Raw option values as declared in the mapping (may be ints for
        # cloud_v2 Thing properties); display options are their strings.
        self._raw_options = list(options) if options else []
        self._options_map = options_map
        self._command = command
        self._status_key = status_key
        self._ignore_values = ignore_values or []
        self._include_current = include_current or []
        self._options_translation_keys = (config or {}).get("options_translation_keys")
        if isinstance(self._options_map, dict):
            self._attr_options = [str(o) for o in self._raw_options]
        else:
            self._attr_options = [str(o) for o in self._raw_options]
        self._last_option: str | None = None

    async def async_added_to_hass(self) -> None:
        """Replace option display labels with translated text once loaded."""
        await super().async_added_to_hass()
        keys = self._options_translation_keys
        if not (
            keys
            and self._raw_options
            and len(keys) == len(self._raw_options)
        ):
            return
        labels = await async_load_state_labels(
            self.hass, "select", self._config.get("translation_key")
        )
        if not labels:
            return
        self._attr_options = [labels.get(key, key) for key in keys]
        self.async_write_ha_state()

    def _is_ignored_value(self, value: Any) -> bool:
        if value is None:
            return False
        for ignore_val in self._ignore_values:
            if value == ignore_val:
                return True
            try:
                if isinstance(ignore_val, (int, float)) and isinstance(value, (int, float)):
                    if value == ignore_val:
                        return True
                elif str(value) == str(ignore_val):
                    return True
            except (TypeError, ValueError):
                pass
        return False

    def _dict_get_selected_for_select(self) -> tuple[str | None, bool]:
        if not isinstance(self._options_map, dict):
            return None, False

        if self._status_key:
            current_value = self._get_nested_value(self._status_key)
            if current_value is not None:
                if self._is_ignored_value(current_value):
                    return None, True
                for mode, status in self._options_map.items():
                    extracted = self._extract_deepest_value(status)
                    if extracted == current_value:
                        return mode, False
            return None, False

        for mode, status in self._options_map.items():
            match = True
            for attr, value in status.items():
                state_value = self._get_nested_value(attr)
                if state_value is None:
                    match = False
                    break
                if self._is_ignored_value(state_value):
                    return None, True
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
                return mode, False
        return None, False

    def _extract_deepest_value(self, config: dict) -> Any:
        for value in config.values():
            if isinstance(value, dict):
                return self._extract_deepest_value(value)
            return value
        return None

    def _match_raw_option(self, value: Any) -> str | None:
        """Return the display option whose raw value equals value."""
        for idx, raw in enumerate(self._raw_options):
            if str(raw) == str(value):
                return self._attr_options[idx]
        return None

    @property
    def current_option(self) -> str | None:
        if isinstance(self._options_map, dict):
            matched, ignored = self._dict_get_selected_for_select()
            if matched is not None:
                self._last_option = matched
                return matched
            if ignored:
                return self._last_option

        data = self.coordinator.data or {}
        value = data.get(self._select_id)

        if value is not None:
            if self._is_ignored_value(value):
                return self._last_option
            # Raw value match first (cloud_v2 Thing values may be ints).
            matched = self._match_raw_option(value)
            if matched is not None:
                self._last_option = matched
                return matched
            if isinstance(value, str):
                if value in self._attr_options:
                    self._last_option = value
                    return value
                try:
                    index = int(value)
                    if 0 <= index < len(self._attr_options):
                        self._last_option = self._attr_options[index]
                        return self._attr_options[index]
                except (TypeError, ValueError):
                    pass
            elif isinstance(value, int):
                if 0 <= value < len(self._attr_options):
                    self._last_option = self._attr_options[value]
                    return self._attr_options[value]

        return self._last_option

    async def async_select_option(self, option: str) -> None:
        if option not in self._attr_options:
            return

        self._last_option = option

        merged_command = {}

        if isinstance(self._options_map, dict) and option in self._options_map:
            option_value = self._options_map[option]
            if isinstance(option_value, dict):
                merged_command.update(option_value)

        if self._command and isinstance(self._command, dict):
            merged_command.update(self._command)

        for attr in self._include_current:
            current_value = self._get_nested_value(attr)
            if current_value is not None:
                merged_command[attr] = current_value

        if merged_command:
            await self.coordinator.async_set_control(merged_command)
            return

        if not isinstance(self._options_map, dict) and self._connection_type == CONNECTION_TYPE_CLOUD_V2:
            # Map the display option back to the raw declared value
            # (e.g. int Thing property values for cloud_v2 devices).
            idx = self._attr_options.index(option)
            if 0 <= idx < len(self._raw_options):
                await self.coordinator.async_set_control(self._select_id, self._raw_options[idx])
                return

        index = self._attr_options.index(option)
        await self.coordinator.async_set_control(self._select_id, index)
