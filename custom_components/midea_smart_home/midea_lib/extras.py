"""Midea Smart Home Extra Logic Handler."""

import logging
import time
from typing import Any, Optional

_LOGGER = logging.getLogger(__name__)

class DeviceLogicHandler:
    def __init__(self, device_type: int, device_name: str):
        self.device_type = device_type
        self.device_name = device_name

        # State variables moved from coordinator
        self._db_location = 1
        self._db_location_selection = "left"

    @property
    def db_location(self):
        return self._db_location

    @property
    def db_location_selection(self):
        return self._db_location_selection

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
            if is_control and control_attrs:
                if "db_control_status" in control_attrs:
                    if control_attrs["db_control_status"] == "start":
                        data["db_control_status"] = "start"
                    else:
                        data["db_control_status"] = "pause"
            else:
                current_time = time.time()
                # Check if db_control_status was recently controlled
                was_recently_controlled = "db_control_status" in [
                    attr for attr, (_, timestamp) in recent_controls.items()
                    if current_time - timestamp < control_timeout
                ]

                if not was_recently_controlled:
                    if "db_running_status" in data:
                        self.adjust_control_status(data, data["db_running_status"])

        elif self.device_type in [0xDA, 0xDB, 0xDC]:
            current_time = time.time()
            # Check if control_status was recently controlled
            was_recently_controlled = "control_status" in [
                attr for attr, (_, timestamp) in recent_controls.items()
                if current_time - timestamp < control_timeout
            ]

            if not was_recently_controlled:
                if "running_status" in data:
                    self.adjust_control_status(data, data["running_status"])


    def handle_t0xd9_db_location_selection(self, status: dict, value: str) -> None:
        if value == "left":
            status["db_location"] = 1
            self._db_location = 1
            self._db_location_selection = "left"
        elif value == "right":
            status["db_location"] = 2
            self._db_location = 2
            self._db_location_selection = "right"

    def adjust_t0xd9_db_location_based_on_position(self, current_data: Optional[dict], status: dict = None) -> int:
        db_position = current_data.get("db_position", 1) if current_data else 1
        current_location = self._db_location

        if db_position == 1:
            calculated_location = current_location
        elif db_position == 0:
            calculated_location = 2 if current_location == 1 else 1
        else:
            calculated_location = current_location

        if status is not None:
            status["db_location"] = calculated_location

        return calculated_location


    def prepare_control_data(self, control: dict) -> dict:
        """Prepare control data with device-specific requirements."""
        if self.device_type == 0xD9:
            control["bucket"] = "db"
            control["db_location"] = self.db_location
        return control

    def update_state_for_control(self, new_data: dict, control: dict, current_data: dict) -> None:
        """Update local state based on control command."""
        if self.device_type == 0xD9:
            if "db_location_selection" in control:
                self.handle_t0xd9_db_location_selection(new_data, control["db_location_selection"])
            else:
                self.adjust_t0xd9_db_location_based_on_position(current_data, new_data)

            new_data["db_location"] = self.db_location
            new_data["db_location_selection"] = self.db_location_selection
