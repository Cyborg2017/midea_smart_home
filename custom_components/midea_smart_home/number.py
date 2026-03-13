import logging

from homeassistant.components.number import NumberEntity
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
        number_config = entities_config.get(Platform.NUMBER, {})

        if number_config:
            for number_id, config in number_config.items():
                entities.append(
                    MideaNumberEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        number_id, config, model
                    )
                )

    async_add_entities(entities)


class MideaNumberEntity(MideaBaseEntity, NumberEntity):
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
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, entity_key, model)
        self._config = config
        self._attr_translation_key = config.get("translation_key", entity_key)
        self._attr_native_min_value = config.get("min", 0.0)
        self._attr_native_max_value = config.get("max", 100.0)
        self._attr_native_step = config.get("step", 1.0)
        self._attr_mode = config.get("mode", "auto")
        self._attr_unique_id = f"number.midea_{device_id}_{entity_key}"
        self.entity_id = f"number.midea_{device_id}_{entity_key}"
        self._condition = config.get("condition")

        if "unit_of_measurement" in config:
            self._attr_native_unit_of_measurement = config["unit_of_measurement"]

        if "device_class" in config:
            self._attr_device_class = config["device_class"]

    @property
    def available(self) -> bool:
        return super().available and self._check_condition(self._condition)

    @property
    def native_value(self) -> float | None:
        if not self.coordinator.data:
            return None
        value = self.coordinator.data.get(self._entity_key)

        if value is None:
            return None

        try:
            return float(value)
        except (ValueError, TypeError):
            _LOGGER.warning("Failed to convert value '%s' to float for number entity %s", value, self._entity_key)
            return None

    async def async_set_native_value(self, value: float) -> None:
        command = self._config.get("command")

        if command and isinstance(command, dict):
            merged_command = {}
            for key, val in command.items():
                if isinstance(val, str) and "{value}" in val:
                    merged_command[key] = val.replace("{value}", str(int(value)))
                else:
                    merged_command[key] = val
            await self.coordinator.async_set_control(merged_command)
        else:
            await self.coordinator.async_set_control(self._entity_key, int(value))
