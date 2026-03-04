import asyncio
import json
import logging
import re
import socket
import ast
from datetime import timedelta
from typing import Any, Optional, Union

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .device import DeviceController

_LOGGER = logging.getLogger(__name__)

StatusDict = dict[str, Union[str, int, float, bool, None]]
ControlValue = Union[str, int, float, bool, None]


class MideaCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(
        self,
        hass: HomeAssistant,
        controller: DeviceController,
        device_name: str,
        update_interval: float = 1.0,
        calculate_config: Optional[dict] = None,
        queries: Optional[list] = None,
        centralized: Optional[list] = None,
        default_values: Optional[dict] = None,
        device_type: int = 0,
    ):
        self.controller = controller
        self.device_name = device_name
        self.calculate_config = calculate_config or {}
        self.queries = queries or [{}]
        self.centralized = centralized or []
        self.default_values = default_values or {}
        self.device_type = device_type
        
        self._control_lock = asyncio.Lock()
        self._db_location = 1
        self._db_location_selection = "left"
        self._last_db_position = 1
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"Midea Smart Home {device_name}",
            update_interval=timedelta(seconds=update_interval),
        )

    def _evaluate_expression(self, expression: str, data: dict) -> Union[str, int, float, bool, None]:
        def replace_var(match):
            var_name = match.group(1)
            if var_name in data:
                return str(data[var_name])
            return "0"
        
        result_expr = re.sub(r'\[([a-zA-Z_][a-zA-Z0-9_]*)\]', replace_var, expression)
        
        preserve_functions = ['float', 'int', 'str', 'bool']
        result_expr = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', 
                           lambda m: str(data[m.group(1)]) if m.group(1) in data and m.group(1) not in preserve_functions else m.group(1), 
                           result_expr)
        
        try:
            allowed_names = {"float": float, "int": int, "str": str}
            node = ast.parse(result_expr, mode='eval')
            return eval(compile(node, '<string>', 'eval'), {"__builtins__": {}}, allowed_names)
        except (SyntaxError, ValueError, TypeError, NameError) as e:
            _LOGGER.warning("Failed to evaluate expression '%s': %s", expression, e)
            return None

    def _apply_calculations(self, data: dict) -> dict:
        if not data:
            return data
        
        get_calculations = self.calculate_config.get("get", [])
        for calc in get_calculations:
            lvalue = calc.get("lvalue")
            rvalue = calc.get("rvalue")
            if lvalue and rvalue:
                result = self._evaluate_expression(rvalue, data)
                if result is not None:
                    if lvalue.startswith('[') and lvalue.endswith(']'):
                        actual_lvalue = lvalue[1:-1]
                    else:
                        actual_lvalue = lvalue
                    data[actual_lvalue] = result
        
        return data

    def _apply_default_values(self, data: dict) -> dict:
        for attr, default_value in self.default_values.items():
            if attr not in data or data[attr] is None:
                data[attr] = default_value
        return data
    
    def _adjust_control_status(self, data: dict, running_status: str) -> None:
        if running_status == "start":
            control_status = "start"
        else:
            control_status = "pause"
        
        if self.device_type == 0xD9:
            control_status_key = "db_control_status"
        elif self.device_type in [0xDA, 0xDB, 0xDC]:
            control_status_key = "control_status"
        else:
            control_status_key = "control_status"
        
        data[control_status_key] = control_status
    
    def _apply_special_handling(self, data: dict, is_control: bool = False, control_attrs: dict = None) -> None:
        if self.device_type == 0xD9:
            if is_control and control_attrs:
                if "db_control_status" in control_attrs:
                    if control_attrs["db_control_status"] == "start":
                        data["db_control_status"] = "start"
                    else:
                        data["db_control_status"] = "pause"
            else:
                if "db_running_status" in data:
                    self._adjust_control_status(data, data["db_running_status"])
        
        elif self.device_type in [0xDA, 0xDB, 0xDC]:
            if "running_status" in data:
                self._adjust_control_status(data, data["running_status"])

    def _is_valid_data_type(self, data: dict) -> bool:
        if self.device_type != 0xD9:
            return True
        
        data_type = data.get("data_type", "")
        
        if data_type == "03db":
            return True
        
        if data_type:
            _LOGGER.debug("[%s] Ignoring data_type: %s", self.device_name, data_type)
            return False
        
        return True

    def _handle_t0xd9_db_location_selection(self, status: dict, value: str) -> None:
        if value == "left":
            status["db_location"] = 1
            self._db_location = 1
            self._db_location_selection = "left"
        elif value == "right":
            status["db_location"] = 2
            self._db_location = 2
            self._db_location_selection = "right"

    def _adjust_t0xd9_db_location_based_on_position(self, status: dict = None) -> int:
        db_position = self.data.get("db_position", 1) if self.data else 1
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

    def _sync_t0xd9_location_selection(self, location: int) -> None:
        if location == 1:
            self._db_location_selection = "left"
        elif location == 2:
            self._db_location_selection = "right"

    async def _async_update_data(self) -> dict[str, Any]:
        if self._control_lock.locked():
            return self.data
  
        try:
            all_data = {}
            
            for query in self.queries:
                actual_query = query.copy() if isinstance(query, dict) else query
                
                if self.device_type == 0xD9 and isinstance(actual_query, dict):
                    actual_query["db_location"] = self._db_location
                
                try:
                    data = await self.hass.async_add_executor_job(
                        self.controller.get_status, actual_query
                    )
                    if data:
                        if not self._is_valid_data_type(data):
                            continue
                        all_data.update(data)
                except (socket.error, OSError, ValueError, json.JSONDecodeError) as e:
                    _LOGGER.error("Error getting status for query %s: %s", query, e)
            
            if self.device_type == 0xD9 and all_data:
                data_type = all_data.get("data_type", "")
                
                if data_type == "03db":
                    db_position = all_data.get("db_position", 1)
                    
                    if db_position == 1:
                        self._last_db_position = 1
                    
                    elif db_position == 0 and self._last_db_position == 1:
                        _LOGGER.info(
                            "[%s] 03db: db_position changed from 1 to 0, switching bucket location",
                            self.device_name
                        )
                        
                        if self._db_location == 1:
                            self._db_location = 2
                            self._db_location_selection = "right"
                        else:
                            self._db_location = 1
                            self._db_location_selection = "left"
                        
                        self._last_db_position = 0
                        
                        _LOGGER.info(
                            "[%s] Switched to db_location=%d, querying new status",
                            self.device_name, self._db_location
                        )
                        
                        retry_query = {"db_location": self._db_location}
                        retry_data = await self.hass.async_add_executor_job(
                            self.controller.get_status, retry_query
                        )
                        if retry_data and self._is_valid_data_type(retry_data):
                            all_data.update(retry_data)
                            _LOGGER.info(
                                "[%s] Updated status after bucket switch",
                                self.device_name
                            )
                
                all_data["db_location"] = self._db_location
                all_data["db_location_selection"] = self._db_location_selection
            
            if self.data:
                for attr, old_value in self.data.items():
                    if old_value is not None:
                        if attr not in all_data or all_data[attr] is None:
                            all_data[attr] = old_value
            
            if not all_data:
                _LOGGER.warning("No data received from device %s, attempting to reconnect", self.device_name)
                await self.hass.async_add_executor_job(self.controller.connect)
                
                for query in self.queries:
                    actual_query = query.copy() if isinstance(query, dict) else query
                    
                    if self.device_type == 0xD9 and isinstance(actual_query, dict):
                        actual_query["db_location"] = self._db_location
                    
                    try:
                        data = await self.hass.async_add_executor_job(
                            self.controller.get_status, actual_query
                        )
                        if data:
                            if not self._is_valid_data_type(data):
                                continue
                            all_data.update(data)
                    except (socket.error, OSError, ValueError, json.JSONDecodeError) as e:
                        _LOGGER.error("Retry failed for query %s: %s", query, e)
                        
                if not all_data:
                    raise UpdateFailed("No data received from device after retry")
            
            result = self._apply_default_values(all_data)
            result = self._apply_calculations(result)
            
            self._apply_special_handling(result)
            
            return result
        except UpdateFailed:
            raise
        except (socket.error, OSError, ValueError, json.JSONDecodeError, TypeError) as e:
            raise UpdateFailed(f"Failed to update device status: {e}") from e

    async def async_set_control(
        self,
        attr: str | dict,
        value: ControlValue = None
    ) -> StatusDict:
        if isinstance(attr, dict):
            control = attr
        else:
            control = {attr: value}
            
        async with self._control_lock:
            try:
                new_data = self.data.copy() if self.data else {}
                
                if self.device_type == 0xD9:
                    if "db_location_selection" in control:
                        self._handle_t0xd9_db_location_selection(new_data, control["db_location_selection"])
                    else:
                        self._adjust_t0xd9_db_location_based_on_position(new_data)
                
                if self.centralized:
                    full_control = {}
                    for attr_name in self.centralized:
                        if attr_name in self.data and self.data[attr_name] is not None:
                            full_control[attr_name] = self.data[attr_name]
                        elif attr_name in self.default_values:
                            full_control[attr_name] = self.default_values[attr_name]
                    full_control.update(control)
                    
                    if self.device_type == 0xD9:
                        full_control["bucket"] = "db"
                        full_control["db_location"] = self._db_location
                    
                    self._apply_special_handling(full_control, is_control=True, control_attrs=control)
                    
                    response = await self.hass.async_add_executor_job(
                        self.controller.set_control, full_control
                    )
                    
                    for attr_name, val in control.items():
                        new_data[attr_name] = val
                    if response:
                        if self.device_type != 0xD9:
                            if self._is_valid_data_type(response):
                                for attr_name, val in response.items():
                                    if val is not None and attr_name not in self.centralized:
                                        new_data[attr_name] = val
                else:
                    current_status = self.data.copy() if self.data else {}
                    for attr_name, val in control.items():
                        single_control = {attr_name: val}
                        
                        if self.device_type == 0xD9:
                            single_control["bucket"] = "db"
                            single_control["db_location"] = self._db_location
                        
                        self._apply_special_handling(single_control, is_control=True, control_attrs=single_control)
                        
                        response = await self.hass.async_add_executor_job(
                            self.controller.set_control, single_control, None, current_status
                        )
                        
                        current_status[attr_name] = val
                        new_data[attr_name] = val
                        
                if self.device_type == 0xD9:
                    new_data["db_location"] = self._db_location
                    new_data["db_location_selection"] = self._db_location_selection

                self.async_set_updated_data(new_data)
                
            except (socket.error, OSError, ValueError, json.JSONDecodeError, TypeError) as e:
                _LOGGER.error("Control command execution failed: %s", e)
                    
        return self.data

    async def async_set_controls(self, controls: dict[str, ControlValue]) -> StatusDict:
        return await self.async_set_control(controls)
