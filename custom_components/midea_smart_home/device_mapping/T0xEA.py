from homeassistant.const import Platform, UnitOfTemperature, UnitOfTime
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "calculate": {
            "get": [
                {
                    "lvalue": "[remain_time]",
                    "rvalue": "[left_time_hour] * 60 + [left_time_min]"
                },
                {
                    "lvalue": "[warming_time]",
                    "rvalue": "[warm_time_hour] * 60 + [warm_time_min]"
                }
            ],
            "set": {
            }
        },
        "entities": {
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "stop": {"work_switch": 0},
                        "firewood_rice": {"mode": "firewood_rice", "work_switch": 2},
                        "warm_porridge": {"mode": 125, "work_switch": 2},
                        "rice_porridge": {"work_mode": 142, "work_switch": 2},
                        "double_layer_cook": {"work_mode": 143, "work_switch": 2},
                        "coarse_rice": {"mode": "coarse_rice", "work_switch": 2},
                        "cook_soup": {"mode": "cook_soup", "work_switch": 2},
                        "stewing": {"mode": "stewing", "work_switch": 2},
                        "keep_warm": {"mode": "keep_warm", "work_switch": 2}
                    }
                },
                "rice_type": {
                    "options": {
                        "none": {"rice_type": "none"},
                        "northeast": {"rice_type": "northeast"},
                        "longrain": {"rice_type": "longrain"},
                        "fragrant": {"rice_type": "fragrant"},
                        "five": {"rice_type": "five"}
                    }
                }
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "warming_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "top_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "bottom_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
            }
        }
    },
    "default_rice_cooker": {
        "rationale": ["off", "on"],
        "calculate": {
            "get": [
                {
                    "lvalue": "[remain_time]",
                    "rvalue": "[left_time_hour] * 60 + [left_time_min]"
                },
                {
                    "lvalue": "[warming_time]",
                    "rvalue": "[warm_time_hour] * 60 + [warm_time_min]"
                }
            ],
            "set": {
            }
        },
        "entities": {
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "stop": {"work_switch": 0},
                        "firewood_rice": {"mode": "firewood_rice", "work_switch": 2},
                        "warm_porridge": {"mode": 125, "work_switch": 2},
                        "rice_porridge": {"work_mode": 142, "work_switch": 2},
                        "double_layer_cook": {"work_mode": 143, "work_switch": 2},
                        "coarse_rice": {"mode": "coarse_rice", "work_switch": 2},
                        "cook_soup": {"mode": "cook_soup", "work_switch": 2},
                        "stewing": {"mode": "stewing", "work_switch": 2},
                        "keep_warm": {"mode": "keep_warm", "work_switch": 2}
                    }
                },
                "rice_type": {
                    "options": {
                        "none": {"rice_type": "none"},
                        "northeast": {"rice_type": "northeast"},
                        "longrain": {"rice_type": "longrain"},
                        "fragrant": {"rice_type": "fragrant"},
                        "five": {"rice_type": "five"}
                    }
                }
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "warming_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "top_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "bottom_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
            }
        }
    }
}
