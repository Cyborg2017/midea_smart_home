"""Midea Smart Home Extra Logic Handler."""

import logging
from typing import Any, Optional

_LOGGER = logging.getLogger(__name__)


class DeviceLogicHandler:
    def __init__(self, device_type: int, device_name: str):
        self.device_type = device_type
        self.device_name = device_name
        self._last_standby_status: Any = None

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

    def adjust_ac_mode(self, data: dict) -> None:
        if "mode" in data:
            power = data.get("power")
            if power == "off" or power == 0:
                data["mode"] = "idle"

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
            self.process_progress(data, "db_running_status", "db_progress")
            self._adjust_db_running_status_for_power_off(data)
            self._adjust_db_remain_time(data)

        elif self.device_type in [0xDA, 0xDB, 0xDC]:
            if "running_status" in data:
                self.adjust_control_status(data, data["running_status"])
            self.process_progress(data, "running_status", "progress")
            self._adjust_remain_time(data)

        elif self.device_type == 0xEA:
            self.adjust_work_switch(data)

        elif self.device_type == 0xAC:
            self.adjust_ac_mode(data)

        elif self.device_type == 0xED:
            self.adjust_standby_status_for_wash(data)

    def _adjust_db_running_status_for_power_off(self, data: dict) -> None:
        db_power = data.get("db_power")
        if db_power == "off" or db_power == 0:
            if "db_running_status" in data:
                data["db_running_status"] = "standby"

    def _adjust_remain_time(self, data: dict) -> None:
        if "remain_time" not in data or "running_status" not in data:
            return
        running_status = data["running_status"]
        if running_status == "start":
            return
        elif running_status == "end":
            data["remain_time"] = 0
        else:
            data["remain_time"] = None

    def _adjust_db_remain_time(self, data: dict) -> None:
        if "db_remain_time" not in data or "db_running_status" not in data:
            return
        running_status = data["db_running_status"]
        if running_status == "start":
            return
        elif running_status == "end":
            data["db_remain_time"] = 0
        else:
            data["db_remain_time"] = None

    def process_progress(self, data: dict, status_key: str, progress_key: str) -> None:
        """Process progress sensor special logic"""
        if progress_key not in data:
            return

        running_status = data.get(status_key)
        if running_status != "start":
            data[progress_key] = "idle"
            return

        value = data[progress_key]
        try:
            if isinstance(value, str):
                value = int(value, 16) if value.startswith("0x") else int(value)

            calculated_value = 0
            if value > 0:
                calculated_value = (value & -value).bit_length()
        except (ValueError, TypeError):
            if isinstance(value, str):
                return
            calculated_value = -1

        if self.device_type == 0xDA:
            progress_map = {
                0: "idle",
                1: "spin",
                2: "rinse",
                3: "wash",
                4: "weight",
                5: "unknown",
                6: "dry",
                7: "soak",
            }
        elif self.device_type == 0xDC:
            progress_map = {
                0: "idle",
                1: "dry",
                2: "anti-wrinkle",
                3: "cold_air",
            }
        else:
            progress_map = {
                0: "idle",
                1: "spin",
                2: "rinse",
                3: "wash",
                4: "pre-wash",
                5: "dry",
                6: "weight",
                7: "spin_high",
                8: "unknown",
            }
        data[progress_key] = progress_map.get(calculated_value, "unknown")

    def prepare_control_data(self, control: dict, current_data: dict = None) -> dict:
        """Prepare control data with device-specific requirements."""
        if self.device_type == 0xD9:
            control["bucket"] = "db"
            if "db_location" not in control and current_data and "db_location" in current_data:
                control["db_location"] = current_data["db_location"]
        return control

    def adjust_standby_status_for_wash(self, data: dict) -> None:
        """For T0xED devices, prevent standby_status update when wash is on."""
        if self.device_type != 0xED:
            return

        if "standby_status" not in data or "wash" not in data:
            return

        wash_status = data.get("wash")
        if wash_status == "on" or wash_status == 1:
            if self._last_standby_status is not None:
                data["standby_status"] = self._last_standby_status
        else:
            self._last_standby_status = data.get("standby_status")
