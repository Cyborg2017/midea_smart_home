import logging
from typing import Any, Union

from homeassistant.components.persistent_notification import async_create, async_dismiss
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .midea_lib.device import MideaDevice

_LOGGER = logging.getLogger(__name__)

StatusDict = dict[str, Union[str, int, float, bool, None]]
ControlValue = Union[str, int, float, bool, None]

OFFLINE_DEVICES_KEY = "offline_devices"
NOTIFICATION_ID = "midea_smart_home_device_status"

_translations_cache: dict[str, dict] = {}

def _get_translations(language: str) -> dict:
    """Get notification translations for the given language."""
    if language.startswith("zh"):
        lang_code = "zh-Hans"
    else:
        lang_code = "en"

    if lang_code in _translations_cache:
        return _translations_cache[lang_code]

    translations = {
        "en": {
            "offline_title": "⚠️ Midea Smart Home Device Offline",
            "online_title": "✅ Midea Smart Home Device Online",
            "offline_header": "🔴 **The following devices are offline:**",
            "online_header": "🟢 **Device is back online:**",
            "offline_item": "- {name} ({device_id}, {ip}{area})",
            "online_item": "- {name} ({device_id}, {ip}{area})",
            "offline_hint": "💡 Tip: Please check if the devices are powered on and the network connection is normal.",
        },
        "zh-Hans": {
            "offline_title": "⚠️ Midea Smart Home 设备离线通知",
            "online_title": "✅ Midea Smart Home 设备上线通知",
            "offline_header": "🔴 **以下设备已离线：**",
            "online_header": "🟢 **设备已重新上线：**",
            "offline_item": "- {name}（{device_id}, {ip}{area}）",
            "online_item": "- {name}（{device_id}, {ip}{area}）",
            "offline_hint": "💡 提示：请检查设备是否开机或网络连接是否正常。",
        },
    }

    result = translations.get(lang_code, translations["en"])
    _translations_cache[lang_code] = result
    return result

def _get_text(key: str, language: str) -> str:
    """Get translated text."""
    translations = _get_translations(language)
    return translations.get(key, key)

def _get_offline_devices(hass: HomeAssistant) -> dict[str, dict]:
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if OFFLINE_DEVICES_KEY not in hass.data[DOMAIN]:
        hass.data[DOMAIN][OFFLINE_DEVICES_KEY] = {}
    return hass.data[DOMAIN][OFFLINE_DEVICES_KEY]

def async_update_device_status_notification(hass: HomeAssistant, device_id: str, device_name: str, ip: str, is_online: bool, area: str = "") -> None:
    offline_devices = _get_offline_devices(hass)
    language = hass.config.language or "en"

    if is_online:
        if device_id in offline_devices:
            del offline_devices[device_id]
            area_text = f", {area}" if area else ""
            online_msg = (
                _get_text("online_header", language) + "\n\n" +
                _get_text("online_item", language).format(name=device_name, device_id=device_id, ip=ip, area=area_text)
            )
            async_create(
                hass,
                online_msg,
                title=_get_text("online_title", language),
                notification_id=f"{NOTIFICATION_ID}_online_{device_id}",
            )
    else:
        offline_devices[device_id] = {"name": device_name, "ip": ip, "area": area}

    if offline_devices:
        lines = []
        for device_id, info in offline_devices.items():
            area_text = f", {info['area']}" if info.get('area') else ""
            lines.append(_get_text("offline_item", language).format(name=info["name"], device_id=device_id, ip=info["ip"], area=area_text))
        message = (
            _get_text("offline_header", language) + "\n\n" +
            "\n".join(lines) + "\n\n" +
            _get_text("offline_hint", language)
        )
        async_create(
            hass,
            message,
            title=_get_text("offline_title", language),
            notification_id=NOTIFICATION_ID,
        )
    else:
        async_dismiss(hass, NOTIFICATION_ID)


class MideaCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Midea Smart Home devices.

    This class bridges Home Assistant and the MideaDevice library.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        device: MideaDevice,
        device_name: str,
        area: str = "",
        config_entry: ConfigEntry | None = None,
    ):
        self.device = device
        self.device_name = device_name
        self.area = area
        self.device_type = device.device_id
        self.config_entry = config_entry
        self._was_available: bool | None = None
        self._initialized: bool = False
        self._active: bool = True

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

    def deactivate(self) -> None:
        """Deactivate this coordinator to stop processing callbacks."""
        self._active = False

    def _device_update_callback(self) -> None:
        """Handle device data updates."""
        if not self.hass or self.hass.is_stopping or not self._active:
            return

        self._check_availability_change()

        self.hass.loop.call_soon_threadsafe(
            self.async_set_updated_data, self.device.data
        )

    def _check_availability_change(self) -> None:
        """Check if device availability changed and send notifications."""
        current_available = self.device.available

        if self._was_available is None:
            self._was_available = current_available
            _LOGGER.info("Device %s: INIT available=%s", self.device.device_id, current_available)
            return

        if not self._initialized:
            if current_available:
                self._initialized = True
                _LOGGER.info("Device %s: INITIALIZED (was=%s, now online)", self.device.device_id, self._was_available)
            if self._was_available is not None and current_available != self._was_available:
                _LOGGER.info("Device %s: CHANGE during init %s->%s, sending notification!", self.device.device_id, self._was_available, current_available)
                self._was_available = current_available
                self.hass.loop.call_soon_threadsafe(self._async_send_notification, current_available)
            else:
                self._was_available = current_available
            return

        if current_available == self._was_available:
            return

        _LOGGER.info("Device %s: CHANGE %s->%s, sending notification!", self.device.device_id, self._was_available, current_available)
        self._was_available = current_available
        self.hass.loop.call_soon_threadsafe(self._async_send_notification, current_available)

    @callback
    def _async_send_notification(self, is_online: bool) -> None:
        """Send notification for device availability change."""
        # Check per-entry notification switches (default True for backward compatibility)
        entry_data = self.config_entry.data if self.config_entry else {}
        if is_online:
            if not entry_data.get("notify_online", True):
                _LOGGER.debug("Online notification suppressed for device %s (disabled by config)", self.device.device_id)
                return
        else:
            if not entry_data.get("notify_offline", True):
                _LOGGER.debug("Offline notification suppressed for device %s (disabled by config)", self.device.device_id)
                return

        _LOGGER.info(">>> SENDING notification for device %s: is_online=%s <<<", self.device.device_id, is_online)
        async_update_device_status_notification(
            self.hass,
            str(self.device.device_id),
            self.device_name,
            self.device.controller.ip,
            is_online,
            self.area,
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
            await self.hass.async_add_executor_job(self.device.set_attributes, attr)
        else:
            await self.hass.async_add_executor_job(self.device.set_attribute, attr, value)

        return self.device.data

    async def async_set_controls(self, controls: dict[str, ControlValue]) -> StatusDict:
        """Send multiple control commands."""
        return await self.async_set_control(controls)
