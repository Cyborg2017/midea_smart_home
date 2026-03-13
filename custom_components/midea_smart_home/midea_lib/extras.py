"""Midea Smart Home Extra Logic Handler."""

import logging
from typing import Any, Optional

_LOGGER = logging.getLogger(__name__)


class DeviceLogicHandler:
    def __init__(self, device_type: int, device_name: str):
        self.device_type = device_type
        self.device_name = device_name

    def adjust_control_status(self, data: dict, running_status: str) -> None:
        control_status = "start" if running_status == "start" else "pause"
        control_status_key = "db_control_status" if self.device_type == 0xD9 else "control_status"
        data[control_status_key] = control_status

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

        elif self.device_type in [0xDA, 0xDB, 0xDC]:
            if "running_status" in data:
                self.adjust_control_status(data, data["running_status"])

    def prepare_control_data(self, control: dict, current_data: dict = None) -> dict:
        """Prepare control data with device-specific requirements."""
        if self.device_type == 0xD9:
            control["bucket"] = "db"
            if "db_location" not in control and current_data and "db_location" in current_data:
                control["db_location"] = current_data["db_location"]
        return control
