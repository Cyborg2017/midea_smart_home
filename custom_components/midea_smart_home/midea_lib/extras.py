"""Midea Smart Home Extra Logic Handler."""

import logging
import time
from typing import Any, Optional

_LOGGER = logging.getLogger(__name__)

_DISHWASHER_COMPOSITE_KEYS = {
    "mode",
    "wash_region",
    "additional",
    "more_dry",
    "door_auto_open",
    "work_status",
}

_DISHWASHER_PENDING_KEYS = (
    "mode",
    "wash_region",
    "additional",
    "more_dry",
    "door_auto_open",
)


class DeviceLogicHandler:
    def __init__(self, device_type: int, device_name: str):
        self.device_type = device_type
        self.device_name = device_name

    def adjust_control_status(self, data: dict, running_status: str) -> None:
        control_status = "start" if running_status == "start" else "pause"
        control_status_key = "db_control_status" if self.device_type == 0xD9 else "control_status"
        data[control_status_key] = control_status

    def adjust_work_switch(self, data: dict) -> None:
        if "work_status" in data:
            work_status = data["work_status"]
            if work_status == "cancel":
                data["work_switch"] = 0
            elif work_status in ("cooking", "keep_warm"):
                data["work_switch"] = 2

    def apply_special_handling(
        self,
        data: dict,
        recent_controls: dict,
        control_timeout: float,
        is_control: bool = False,
        control_attrs: dict = None
    ) -> None:
        if self.device_type == 0xD9:
            if "db_running_status" in data:
                self.adjust_control_status(data, data["db_running_status"])

        elif self.device_type == 0xE1:
            self._apply_dishwasher_pending_state(data, recent_controls, control_timeout)

        elif self.device_type in [0xDA, 0xDB, 0xDC]:
            if "running_status" in data:
                self.adjust_control_status(data, data["running_status"])

        elif self.device_type == 0xEA:
            self.adjust_work_switch(data)

    def prepare_control_data(self, control: dict, current_data: dict = None) -> dict:
        """Prepare control data with device-specific requirements."""
        if self.device_type == 0xD9:
            control["bucket"] = "db"
            if "db_location" not in control and current_data and "db_location" in current_data:
                control["db_location"] = current_data["db_location"]
        elif self.device_type == 0xE1:
            control = self._prepare_dishwasher_control(control, current_data)
        return control

    def _prepare_dishwasher_control(
        self,
        control: dict,
        current_data: dict | None = None,
    ) -> dict:
        if not any(key in control for key in _DISHWASHER_COMPOSITE_KEYS):
            return control

        current_data = current_data or {}
        prepared = control.copy()

        if "mode" in prepared:
            prepared.setdefault("wash_region", 3)
            prepared.setdefault("additional", 0)

        if "mode" not in prepared:
            prepared["mode"] = self._normalize_dishwasher_mode(current_data.get("mode"))

        if "work_status" not in prepared:
            prepared["work_status"] = self._normalize_dishwasher_work_status(
                current_data.get("work_status")
            )

        if "wash_region" not in prepared:
            prepared["wash_region"] = self._normalize_dishwasher_int(
                current_data.get("wash_region"), 3
            )

        if "additional" not in prepared:
            prepared["additional"] = self._normalize_dishwasher_int(
                current_data.get("additional"), 0
            )

        if "more_dry" not in prepared:
            prepared["more_dry"] = self._normalize_dishwasher_int(
                current_data.get("more_dry"), 0
            )

        if "door_auto_open" not in prepared:
            prepared["door_auto_open"] = self._normalize_dishwasher_int(
                current_data.get("door_auto_open"), 0
            )

        return prepared

    def _normalize_dishwasher_work_status(self, value: Any) -> str:
        if value in {"cancel", "work", "order"}:
            return value
        if value in {"power_on", "power_off", "cancel_order"}:
            return "cancel"
        return "cancel"

    def _normalize_dishwasher_mode(self, value: Any) -> str:
        if isinstance(value, str) and value:
            return value
        return "neutral_gear"

    def _normalize_dishwasher_int(self, value: Any, default: int) -> int:
        if isinstance(value, bool):
            return int(value)
        if value is None:
            return default
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _apply_dishwasher_pending_state(
        self,
        data: dict,
        recent_controls: dict,
        control_timeout: float,
    ) -> None:
        work_status = data.get("work_status")
        mode = data.get("mode")

        # The local protocol reports pre-start selections as cancel + neutral_gear.
        # Keep recent user selections visible in HA until the device reports a real running state.
        if work_status not in {"cancel", "power_off"} or mode != "neutral_gear":
            return

        for key in _DISHWASHER_PENDING_KEYS:
            recent = recent_controls.get(key)
            if not recent:
                continue

            value, timestamp = recent
            if timestamp is None:
                continue

            # Device.py cleans expired controls after this hook, so re-check here.
            if time.time() - timestamp >= control_timeout:
                continue

            if key == "mode" and value == "neutral_gear":
                continue

            data[key] = value
