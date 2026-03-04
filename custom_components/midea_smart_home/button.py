import logging

from homeassistant.components.button import ButtonEntity
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
        button_config = entities_config.get(Platform.BUTTON, {})
        
        if button_config:
            for button_id, config in button_config.items():
                entities.append(
                    MideaButtonEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        button_id, config, model
                    )
                )
    
    async_add_entities(entities)


class MideaButtonEntity(MideaBaseEntity, ButtonEntity):
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
        self._attr_unique_id = f"button.midea_{device_id}_{entity_key}"
        self.entity_id = f"button.midea_{device_id}_{entity_key}"
    
    async def async_press(self) -> None:
        command = self._config.get("command")
        
        if command and isinstance(command, dict):
            await self.coordinator.async_set_control(command)
        else:
            _LOGGER.warning("Button %s has no command configured", self._entity_key)
