import logging
from typing import Any, Union

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .midea_lib.device import MideaDevice

_LOGGER = logging.getLogger(__name__)

StatusDict = dict[str, Union[str, int, float, bool, None]]
ControlValue = Union[str, int, float, bool, None]


class MideaCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Midea Smart Home devices.

    This class bridges Home Assistant and the MideaDevice library.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        device: MideaDevice,
        device_name: str,
    ):
        self.device = device
        self.device_name = device_name
        self.device_type = device.device_id # Use device_id or type as needed, mainly for logging

        super().__init__(
            hass,
            _LOGGER,
            name=f"Midea Smart Home {device_name}",
            update_interval=None,
        )

        device.register_update(self._device_update_callback)

    @property
    def controller(self):
        """Return the device controller."""
        return self.device.controller

    def _device_update_callback(self) -> None:
        """Handle device data updates."""
        if not self.hass or self.hass.is_stopping:
            return
            
        # The device update callback is called from a separate thread.
        # We need to schedule the update on the event loop.
        self.hass.loop.call_soon_threadsafe(
            self.async_set_updated_data, self.device.data
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Return the current data."""
        return self.device.data or {}

    async def async_set_control(
        self,
        attr: str | dict,
        value: ControlValue = None
    ) -> StatusDict:
        """Send control command to the device."""
        if isinstance(attr, dict):
            controls = attr
        else:
            controls = {attr: value}

        # Use asyncio.to_thread to run the blocking socket operation in a separate thread
        # MideaDevice.set_attribute handles the logic and sending
        for k, v in controls.items():
            await self.hass.async_add_executor_job(self.device.set_attribute, k, v)
            
        return self.device.data

    async def async_set_controls(self, controls: dict[str, ControlValue]) -> StatusDict:
        """Send multiple control commands."""
        return await self.async_set_control(controls)
