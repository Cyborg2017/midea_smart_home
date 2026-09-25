from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "centralized": [
            "work_mode",
            "pre_heat",
            "steam_quantity",
            "temperature",
            "work_hour",
            "work_minute",
            "work_second"
        ],
        "initial_query": [{}],
        "polling_query": [{}],
        "calculate": {
            "get": [
                {
                    "lvalue": "[work_time]",
                    "rvalue": "[work_second] + 60 * [work_minute] + 3600 * [work_hour]"
                },
                {
                    "lvalue": "[set_time]",
                    "rvalue": "[second_set] + 60 * [minute_set] + 3600 * [hour_set]"
                },
                {
                    "lvalue": "[appoint_time]",
                    "rvalue": "[appoint_second] + 60 * [appoint_minute] + 3600 * [appoint_hour]"
                }
            ],
            "set": [
            ]
        },
        "entities": {
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.NUMBER: {
                "temperature": {
                    "min": 0,
                    "max": 250,
                    "step": 5,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                },
                "work_hour": {
                    "min": 0,
                    "max": 23,
                    "step": 1,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTime.HOURS,
                },
                "work_minute": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTime.MINUTES,
                }
            },
            Platform.SWITCH: {
                "pre_heat": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["off", "work"]
                }
            },
            Platform.SELECT: {
                "steam_quantity": {
                    "options": {
                        "off": {"steam_quantity": 0},
                        "low": {"steam_quantity": 1},
                        "middle": {"steam_quantity": 2},
                        "high": {"steam_quantity": 3}
                    }
                },
                "work_mode": {
                    "translation_key": "steam_oven_mode",
                    "options": {
                        "pure_steam": {"work_mode": "pure_steam"},
                        "steam_hot_wind_tube_fan": {"work_mode": "steam_hot_wind_tube_fan"},
                        "double_tube": {"work_mode": "double_tube"},
                        "double_tube_fan": {"work_mode": "double_tube_fan"},
                        "hot_wind_tube_fan": {"work_mode": "hot_wind_tube_fan"},
                        "underside_tube": {"work_mode": "underside_tube"},
                        "above_inside_tube": {"work_mode": "above_inside_tube"},
                        "above_inside_outside_tube": {"work_mode": "above_inside_outside_tube"},
                        "above_inside_outside_tube_fan": {"work_mode": "above_inside_outside_tube_fan"},
                        "zymosis": {"work_mode": "zymosis"},
                        "scale_clean": {"work_mode": "scale_clean"},
                        "none": {"work_mode": "ff"}
                    }
                },
                "work_status": {
                    "options": {
                        "standby": {"work_status": "standby"},
                        "work": {"work_status": "work"},
                        "pause": {"work_status": "pause"}
                    }
                }
            },
            Platform.BINARY_SENSOR: {
                "door_open": {
                    "device_class": BinarySensorDeviceClass.DOOR
                }
            },
            Platform.SENSOR: {
                "appoint_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "appointment_time"
                },
                "cur_temperature_above": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "execute": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "set_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "stepnum": {
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "totalstep": {
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "water_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_mode": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_steam_oven": {
        "rationale": ["off", "on"],
        "centralized": [
            "work_mode",
            "pre_heat",
            "steam_quantity",
            "temperature",
            "work_hour",
            "work_minute",
            "work_second"
        ],
        "initial_query": [{}],
        "polling_query": [{}],
        "calculate": {
            "get": [
                {
                    "lvalue": "[work_time]",
                    "rvalue": "[work_second] + 60 * [work_minute] + 3600 * [work_hour]"
                },
                {
                    "lvalue": "[set_time]",
                    "rvalue": "[second_set] + 60 * [minute_set] + 3600 * [hour_set]"
                },
                {
                    "lvalue": "[appoint_time]",
                    "rvalue": "[appoint_second] + 60 * [appoint_minute] + 3600 * [appoint_hour]"
                }
            ],
            "set": [
            ]
        },
        "entities": {
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.NUMBER: {
                "temperature": {
                    "min": 0,
                    "max": 250,
                    "step": 5,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTemperature.CELSIUS
                },
                "work_hour": {
                    "min": 0,
                    "max": 23,
                    "step": 1,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTime.HOURS,
                },
                "work_minute": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTime.MINUTES,
                }
            },
            Platform.SWITCH: {
                "pre_heat": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["off", "work"]
                }
            },
            Platform.SELECT: {
                "steam_quantity": {
                    "options": {
                        "off": {"steam_quantity": 0},
                        "low": {"steam_quantity": 1},
                        "middle": {"steam_quantity": 2},
                        "high": {"steam_quantity": 3}
                    }
                },
                "work_mode": {
                    "translation_key": "steam_oven_mode",
                    "options": {
                        "pure_steam": {"work_mode": "pure_steam"},
                        "steam_hot_wind_tube_fan": {"work_mode": "steam_hot_wind_tube_fan"},
                        "double_tube": {"work_mode": "double_tube"},
                        "double_tube_fan": {"work_mode": "double_tube_fan"},
                        "hot_wind_tube_fan": {"work_mode": "hot_wind_tube_fan"},
                        "underside_tube": {"work_mode": "underside_tube"},
                        "above_inside_tube": {"work_mode": "above_inside_tube"},
                        "above_inside_outside_tube": {"work_mode": "above_inside_outside_tube"},
                        "above_inside_outside_tube_fan": {"work_mode": "above_inside_outside_tube_fan"},
                        "zymosis": {"work_mode": "zymosis"},
                        "scale_clean": {"work_mode": "scale_clean"},
                        "none": {"work_mode": "ff"}
                    }
                },
                "work_status": {
                    "options": {
                        "standby": {"work_status": "standby"},
                        "work": {"work_status": "work"},
                        "pause": {"work_status": "pause"}
                    }
                }
            },
            Platform.BINARY_SENSOR: {
                "door_open": {
                    "device_class": BinarySensorDeviceClass.DOOR
                }
            },
            Platform.SENSOR: {
                "appoint_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "appointment_time"
                },
                "cur_temperature_above": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "execute": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "set_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "stepnum": {
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "totalstep": {
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "water_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_mode": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "70000663": {
        "rationale": ["off", "on"],
        "centralized": [
            "work_mode",
            "pre_heat",
            "steam_quantity",
            "temperature",
            "work_hour",
            "work_minute",
            "work_second"
        ],
        "initial_query": [{}],
        "polling_query": [{}],
        "calculate": {
            "get": [
                {
                    "lvalue": "[work_time]",
                    "rvalue": "[work_second] + 60 * [work_minute] + 3600 * [work_hour]"
                },
                {
                    "lvalue": "[set_time]",
                    "rvalue": "[second_set] + 60 * [minute_set] + 3600 * [hour_set]"
                },
                {
                    "lvalue": "[appoint_time]",
                    "rvalue": "[appoint_second] + 60 * [appoint_minute] + 3600 * [appoint_hour]"
                }
            ],
            "set": [
            ]
        },
        "entities": {
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.NUMBER: {
                "temperature": {
                    "min": 0,
                    "max": 250,
                    "step": 5,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                },
                "work_hour": {
                    "min": 0,
                    "max": 23,
                    "step": 1,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTime.HOURS,
                },
                "work_minute": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTime.MINUTES,
                }
            },
            Platform.SWITCH: {
                "pre_heat": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SELECT: {
                "steam_quantity": {
                    "options": {
                        "off": {"steam_quantity": 0},
                        "low": {"steam_quantity": 1},
                        "middle": {"steam_quantity": 2},
                        "high": {"steam_quantity": 3}
                    }
                },
                "work_mode": {
                    "translation_key": "steam_oven_mode",
                    "options": {
                        "pure_steam": {"work_mode": "pure_steam"},
                        "steam_hot_wind_tube_fan": {"work_mode": "steam_hot_wind_tube_fan"},
                        "double_tube": {"work_mode": "double_tube"},
                        "double_tube_fan": {"work_mode": "double_tube_fan"},
                        "hot_wind_tube_fan": {"work_mode": "hot_wind_tube_fan"},
                        "underside_tube": {"work_mode": "underside_tube"},
                        "above_inside_tube": {"work_mode": "above_inside_tube"},
                        "above_inside_outside_tube": {"work_mode": "above_inside_outside_tube"},
                        "above_inside_outside_tube_fan": {"work_mode": "above_inside_outside_tube_fan"},
                        "zymosis": {"work_mode": "zymosis"},
                        "scale_clean": {"work_mode": "scale_clean"},
                        "none": {"work_mode": "ff"}
                    }
                },
                "work_status": {
                    "options": {
                        "standby": {"work_status": "standby"},
                        "work": {"work_status": "work"},
                        "pause": {"work_status": "pause"}
                    }
                }
            },
            Platform.BINARY_SENSOR: {
                "door_open": {
                    "device_class": BinarySensorDeviceClass.DOOR
                }
            },
            Platform.SENSOR: {
                "appoint_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "appointment_time"
                },
                "cur_temperature_above": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "execute": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "set_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "stepnum": {
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "totalstep": {
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "water_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_mode": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
