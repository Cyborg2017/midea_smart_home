"""Midea Smart Home Extra Logic Handler."""

import logging
from typing import Any, Optional

_LOGGER = logging.getLogger(__name__)


class DeviceLogicHandler:
    def __init__(self, device_type: int, device_name: str):
        self.device_type = device_type
        self.device_name = device_name
        self._last_standby_status: Any = None
        self._last_high_float_type: Any = None

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

        elif self.device_type == 0x9C:
            self.adjust_b3_function_control(data)

        elif self.device_type == 0xED:
            self.adjust_standby_status_for_wash(data)
            self.adjust_high_float_type_when_filter_on(data)

    def apply_special_handling_for_poll(self, data: dict, suffix: str, raw_status: dict = None) -> bool:
        """Apply special handling for poll data with suffix (_l or _r).

        Only process the specific bucket's data (left or right),
        do not affect the other bucket's data.

        Returns:
            True if data should be processed, False if data should be skipped.
        """
        if self.device_type != 0xD9:
            return True

        status_key = f"db_running_status{suffix}"
        progress_key = f"db_progress{suffix}"
        remain_time_key = f"db_remain_time{suffix}"

        if status_key not in data:
            return True

        running_status = data[status_key]

        if running_status == "end" and not self._validate_end_status(raw_status):
            return False

        # Handle common (non-suffixed) fields from the first poll response
        if raw_status and raw_status.get('db_position') == 1:
            if "db_running_status" in data:
                self.adjust_control_status(data, data["db_running_status"])
            self.process_progress(data, "db_running_status", "db_progress")
            self._adjust_db_running_status_for_power_off(data)
            self._adjust_db_remain_time(data)

        # Handle suffixed progress for the specific bucket
        if progress_key in data:
            if running_status != "start":
                data[progress_key] = "idle"
            else:
                self.process_progress(data, status_key, progress_key)

        # Handle suffixed remain time for the specific bucket
        if remain_time_key in data:
            self._adjust_remain_time_by_status(data, remain_time_key, running_status)

        # Calculate db_remain_time_long as max of left and right remain times
        self._calculate_db_remain_time_long(data)

        return True

    def _validate_end_status(self, raw_status: dict) -> bool:
        """Validate that an 'end' running status is legitimate.

        Checks that progress is 0 and remain_time <= 1 to filter out
        false 'end' signals from the device.

        Returns:
            True if the end status is valid, False otherwise.
        """
        if not raw_status:
            return False
        raw_progress = raw_status.get("db_progress")
        raw_remain_time = raw_status.get("db_remain_time")
        if raw_progress is None or raw_remain_time is None:
            return False
        try:
            if isinstance(raw_progress, str):
                raw_progress = int(raw_progress, 16) if raw_progress.startswith("0x") else int(raw_progress)
            if raw_progress != 0:
                return False
        except (ValueError, TypeError):
            return False
        try:
            if isinstance(raw_remain_time, str):
                raw_remain_time = int(raw_remain_time, 16) if raw_remain_time.startswith("0x") else int(raw_remain_time)
            if raw_remain_time > 1:
                return False
        except (ValueError, TypeError):
            return False
        return True

    @staticmethod
    def _adjust_remain_time_by_status(data: dict, remain_time_key: str, running_status: str) -> None:
        """Adjust remain time based on running status for any key prefix."""
        if running_status == "start":
            return
        elif running_status == "end":
            data[remain_time_key] = 0
        else:
            data[remain_time_key] = None

    @staticmethod
    def _calculate_db_remain_time_long(data: dict) -> None:
        """Calculate db_remain_time_long as max of left and right remain times.

        Rules:
        - If both are unknown (None), result is unknown
        - If one is unknown and other has value, result is the value
        - If both have values, result is the maximum
        """
        remain_l = data.get("db_remain_time_l")
        remain_r = data.get("db_remain_time_r")

        if remain_l is None and remain_r is None:
            data["db_remain_time_long"] = None
        elif remain_l is None:
            data["db_remain_time_long"] = remain_r
        elif remain_r is None:
            data["db_remain_time_long"] = remain_l
        else:
            data["db_remain_time_long"] = max(remain_l, remain_r)

    def _adjust_db_running_status_for_power_off(self, data: dict) -> None:
        db_power = data.get("db_power")
        if db_power == "off" or db_power == 0:
            if "db_running_status" in data:
                data["db_running_status"] = "standby"

    def _adjust_remain_time(self, data: dict) -> None:
        if "remain_time" in data and "running_status" in data:
            self._adjust_remain_time_by_status(data, "remain_time", data["running_status"])

    def _adjust_db_remain_time(self, data: dict) -> None:
        if "db_remain_time" in data and "db_running_status" in data:
            self._adjust_remain_time_by_status(data, "db_remain_time", data["db_running_status"])

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

    def adjust_b3_function_control(self, data: dict) -> None:
        """For T0x9C devices, map b3_upstair_status to b3_function_control."""
        if "b3_upstair_status" not in data:
            return

        status_map = {
            "power_off": 1,
            "uperization": 2,
            "drying": 4,
        }
        mapped = status_map.get(data["b3_upstair_status"])
        if mapped is not None:
            data["b3_function_control"] = mapped

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

    def adjust_high_float_type_when_filter_on(self, data: dict) -> None:
        """For T0xED devices, adjust high_float_type when filter is on.

        When the device reports both high_float_type and filter attributes,
        and filter is 'on', keep the previous high_float_type value instead
        of updating it with the new (possibly invalid) device value.
        Other attributes are not affected.
        """
        if self.device_type != 0xED:
            return

        if "high_float_type" not in data or "filter" not in data:
            return

        filter_value = data.get("filter")
        if filter_value == "on" or filter_value == 1:
            if self._last_high_float_type is not None:
                data["high_float_type"] = self._last_high_float_type
        else:
            self._last_high_float_type = data.get("high_float_type")
