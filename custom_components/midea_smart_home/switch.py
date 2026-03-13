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
                entities.append(
                    MideaSwitchEntity(
                        coordinator, device_id, device_type, sn, sn8, device_name,
                        switch_id, translation_key, switch_rationale, condition, model
                    )
                )

    async_add_entities(entities)


class MideaSwitchEntity(MideaBaseEntity, SwitchEntity):
    _attr_device_class = SwitchDeviceClass.SWITCH

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
        model: str = None,
    ):
        super().__init__(coordinator, device_id, device_type, sn, sn8, device_name, switch_id, model)
        self._switch_id = switch_id
        self._attr_translation_key = translation_key or switch_id
        self._rationale = rationale or ["off", "on"]
        self._condition = condition
        self._attr_unique_id = f"switch.midea_{device_id}_{switch_id}"
        self.entity_id = f"switch.midea_{device_id}_{switch_id}"

    @property
    def available(self) -> bool:
        return super().available and self._check_condition(self._condition)

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
        return self._get_status_on_off(self._switch_id)

    async def _async_set_status_on_off(self, attribute_key: str, turn_on: bool) -> None:
        value = self._rationale[int(turn_on)]
        await self.coordinator.async_set_control(attribute_key, value)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._async_set_status_on_off(self._switch_id, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._async_set_status_on_off(self._switch_id, False)
