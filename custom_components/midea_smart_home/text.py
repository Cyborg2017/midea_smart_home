import logging
from typing import Any

from homeassistant.components.text import TextEntity, TextMode
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
        text_config = entities_config.get(Platform.TEXT, {})

        if text_config:
            for text_id, config in text_config.items():
                entities.append(
                    MideaTextEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        text_id, config, model
                    )
                )

    async_add_entities(entities)


class MideaTextEntity(MideaBaseEntity, TextEntity):
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
            platform_name="text", config=config, condition=config.get("condition")
        )
        self._attr_native_min = config.get("min_length", 0)
        self._attr_native_max = config.get("max_length", 100)
        mode_str = config.get("mode", "text")
        self._attr_mode = getattr(TextMode, mode_str.upper(), TextMode.TEXT)
        self._attr_pattern = config.get("pattern", "^$|^[a-z][a-z0-9_]*\\.[a-z0-9_]+$")
        if "unit_of_measurement" in config:
            self._attr_native_unit_of_measurement = config["unit_of_measurement"]
        self._default = config.get("default", "")
        self._persist = config.get("persist", True)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data or {}
        value = data.get(self._entity_key)
        if value is not None and isinstance(value, str):
            return value
        return self._default or None

    async def async_set_value(self, value: str) -> None:
        await self.coordinator.async_set_control(self._entity_key, value)
