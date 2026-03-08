import asyncio
import json
import logging
import re
import ast
import time
from typing import Any, Optional, Union

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .device import DeviceController

_LOGGER = logging.getLogger(__name__)

StatusDict = dict[str, Union[str, int, float, bool, None]]
ControlValue = Union[str, int, float, bool, None]


class MideaCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Midea Smart Home devices.
    
    This class manages data updates and control commands for Midea devices.
    All updates are received via push from the device background thread.
    """
    
    def __init__(
        self,
        hass: HomeAssistant,
        controller: DeviceController,
        device_name: str,
        calculate_config: Optional[dict] = None,
        centralized: Optional[list] = None,
        default_values: Optional[dict] = None,
        device_type: int = 0,
        **kwargs,
    ):
        self.controller = controller
        self.device_name = device_name
        self.calculate_config = calculate_config or {}
        self.centralized = centralized or []
        self.default_values = default_values or {}
        self.device_type = device_type
        
        self._control_lock = asyncio.Lock()
        self._db_location = 1
        self._db_location_selection = "left"
        self._last_db_position = 1
        self._recent_controls = {}
        self._control_timeout = 1
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"Midea Smart Home {device_name}",
            update_interval=None,
        )
        
        controller.register_update(self._device_update_callback)
    
    def _device_update_callback(self, status: dict[str, Any]) -> None:
        if not self.hass or self.hass.is_stopping:
            return
        
        self.hass.add_job(self._async_device_update, status)
    
    @callback
    async def _async_device_update(self, status: dict[str, Any]) -> None:
        update_start_time = time.time()
        if "available" in status and len(status) == 1:
            self.async_update_listeners()
            return
        
        current_time = time.time()
        for attr in list(self._recent_controls.keys()):
            value, timestamp = self._recent_controls[attr]
            if current_time - timestamp < self._control_timeout:
                if attr in status:
                    del status[attr]
            else:
                del self._recent_controls[attr]
        
        new_data = self.data.copy() if self.data else {}
        new_data.update(status)
        
        new_data = self._apply_default_values(new_data)
        new_data = self._apply_calculations(new_data)
        
        self._apply_special_handling(new_data)
        
        self.async_set_updated_data(new_data)
        _LOGGER.debug("[DeviceType:%s] HA update completed at %.3f, elapsed %.3f seconds", 
                      hex(self.device_type), time.time(), time.time() - update_start_time)

    def _evaluate_expression(self, expression: str, data: dict) -> Union[str, int, float, bool, None]:
        def replace_var(match):
            var_name = match.group(1)
            if var_name in data:
                return str(data[var_name])
            return "0"
        
        if re.fullmatch(r'\[[a-zA-Z_][a-zA-Z0-9_]*\]', expression):
            var_name = expression[1:-1]
            return data.get(var_name)
        
        result_expr = re.sub(r'\[([a-zA-Z_][a-zA-Z0-9_]*)\]', replace_var, expression)
        
        preserve_functions = ['float', 'int', 'str', 'bool']
        result_expr = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', 
                           lambda m: str(data[m.group(1)]) if m.group(1) in data and m.group(1) not in preserve_functions else m.group(1), 
                           result_expr)
        
        dangerous_patterns = ['__', 'import', 'exec', 'eval', 'compile', 'open', 'file', 'input']
        for pattern in dangerous_patterns:
            if pattern in result_expr.lower():
                _LOGGER.warning("Dangerous pattern '%s' detected in expression: %s", pattern, expression)
                return None
        
        try:
            allowed_names = {"float": float, "int": int, "str": str, "abs": abs, "round": round, "min": min, "max": max}
            node = ast.parse(result_expr, mode='eval')
            
            for node_type in ast.walk(node):
                if isinstance(node_type, (ast.Call, ast.Attribute, ast.Subscript)):
                    if isinstance(node_type, ast.Attribute):
                        if node_type.attr.startswith('_'):
                            _LOGGER.warning("Access to private attribute '%s' denied", node_type.attr)
                            return None
            
            return eval(compile(node, '<string>', 'eval'), {"__builtins__": {}}, allowed_names)
        except (SyntaxError, ValueError, TypeError, NameError, AttributeError) as e:
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
        control_status = "start" if running_status == "start" else "pause"
        control_status_key = "db_control_status" if self.device_type == 0xD9 else "control_status"
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
                current_time = time.time()
                if "db_control_status" not in [attr for attr, (_, timestamp) in self._recent_controls.items() if current_time - timestamp < self._control_timeout]:
                    if "db_running_status" in data:
                        self._adjust_control_status(data, data["db_running_status"])
        
        elif self.device_type in [0xDA, 0xDB, 0xDC]:
            current_time = time.time()
            if "control_status" not in [attr for attr, (_, timestamp) in self._recent_controls.items() if current_time - timestamp < self._control_timeout]:
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
        return self.data or {}

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
                    
                    current_status = self.data.copy() if self.data else {}
                    await self.hass.async_add_executor_job(
                        self.controller.set_control, full_control, None, current_status
                    )
                else:
                    current_status = self.data.copy() if self.data else {}
                    
                    if self.device_type == 0xD9:
                        control["bucket"] = "db"
                        control["db_location"] = self._db_location
                    
                    self._apply_special_handling(control, is_control=True, control_attrs=control)
                    
                    await self.hass.async_add_executor_job(
                        self.controller.set_control, control, None, current_status
                    )
                
                for attr_name, val in control.items():
                    if attr_name not in ["bucket", "db_location"]:
                        new_data[attr_name] = val
                
                if self.device_type == 0xD9:
                    new_data["db_location"] = self._db_location
                    new_data["db_location_selection"] = self._db_location_selection

                current_time = time.time()
                for attr_name, val in control.items():
                    if attr_name not in ["bucket", "db_location"]:
                        self._recent_controls[attr_name] = (val, current_time)
                
                self.async_set_updated_data(new_data)
                
            except (socket.error, OSError, ValueError, json.JSONDecodeError, TypeError) as e:
                _LOGGER.error("[%s] Control command execution failed: %s", self.device_name, e)
        
        return self.data
    
    async def async_set_controls(self, controls: dict[str, ControlValue]) -> StatusDict:
        for attr, value in controls.items():
            await self.async_set_control(attr, value)
        return self.data
