import logging

from homeassistant.components.number import NumberEntity
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
            await self.coordinator.async_set_control(self._entity_key, str(int(value)))
