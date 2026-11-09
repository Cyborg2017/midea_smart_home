import logging

from homeassistant.components.button import ButtonEntity
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
        super().__init__(
            coordinator, device_id, device_type, sn, sn8, device_name, entity_key, model,
            platform_name="button", config=config
        )

    async def async_press(self) -> None:
        # cloud_v2 thing action (e.g. manual feed)
        action_code = self._config.get("action_code")
        if action_code:
            device = self.coordinator.device
            if hasattr(device, "trigger_thing_action"):
                await self.hass.async_add_executor_job(
                    device.trigger_thing_action,
                    self._config.get("module_code"),
                    action_code,
                    self._config.get("body") or {},
                )
                return
            _LOGGER.warning("[entity] device does not support thing actions: entity=%s", self._entity_key)
            return

        command = self._config.get("command")

        if command and isinstance(command, dict):
            await self.coordinator.async_set_control(command)
        else:
            _LOGGER.warning("[entity] button has no command: entity=%s", self._entity_key)
