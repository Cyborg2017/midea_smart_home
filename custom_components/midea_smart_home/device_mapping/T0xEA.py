from custom_components.midea_smart_home.device_mapping._common import *

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
                }
            }
        }
    },
    "00000032": {
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
                },
                {
                    "lvalue": "[order_time]",
                    "rvalue": "[order_time_hour] * 60 + [order_time_min]"
                }
            ]
        },
        "entities": {
            Platform.SELECT: {
                "mode": {
                    "include_current": ["left_time_hour", "left_time_min"],
                    "options": {
                        "stop": {"work_status": "cancel"},
                        "luscious_rice": {"work_status": "cooking", "mode": "luscious_rice"},
                        "hot_fast_rice": {"work_status": "cooking", "mode": "hot_fast_rice"},
                        "boiling_congee": {"work_status": "cooking", "mode": "boiling_congee"},
                        "stewing": {"work_status": "cooking", "mode": "stewing"},
                        "heat_rice": {"work_status": "cooking", "mode": "heat_rice"},
                        "keep_warm": {"work_status": "cooking", "mode": "keep_warm"}
                    }
                },
                "order_mode": {
                    "include_current": ["order_time_hour", "order_time_min"],
                    "options": {
                        "stop": {"work_status": "cancel"},
                        "order_luscious_rice": {"work_status": "schedule", "mode": "luscious_rice"},
                        "order_boiling_congee": {"work_status": "schedule", "mode": "boiling_congee"},
                        "order_stewing": {"work_status": "schedule", "mode": "stewing"}
                    }
                },
                "rice_type": {
                    "options": {
                        "northeast": {"rice_type": "northeast"},
                        "longrain": {"rice_type": "longrain"},
                        "fragrant": {"rice_type": "fragrant"},
                        "five": {"rice_type": "five"}
                    }
                },
                "mouthfeel": {
                    "options": {
                        "soft": {"mouthfeel": "soft"},
                        "middle": {"mouthfeel": "middle"},
                        "hard": {"mouthfeel": "hard"}
                    }
                }
            },
            Platform.TIME: {
                "work_time": {
                    "target_keys": {
                        "hour": "left_time_hour",
                        "minute": "left_time_min"
                    },
                    "time_mode": "direct"
                }
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "mouthfeel": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "rice_type": {
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
                "order_time": {
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
                }
            }
        }
    }
}
