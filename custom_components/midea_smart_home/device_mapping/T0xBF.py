from homeassistant.const import Platform, UnitOfTime, UnitOfTemperature
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "centralized": [
            "work_mode",
            "fire_power",
            "pre_heat",
            "steam_quantity",
            "temperature",
            "work_hour",
            "work_minute",
            "work_second",
            "weight"
        ],
        "calculate": {
            "get": [
                {
                    "lvalue": "[work_time]",
                    "rvalue": "[work_second] + 60 * [work_minute] + 3600 * [work_hour]"
                },
                {
                    "lvalue": "[set_time]",
                    "rvalue": "[second_set] + 60 * [minute_set] + 3600 * [hour_set]"
                }
            ],
            "set": [
            ]
        },
        "entities": {
            Platform.SELECT: {
                "work_mode": {
                    "options": {
                        "microwave_1": {"work_mode": "microwave_1"},
                        "unfreeze_1": {"work_mode": "unfreeze_1"},
                        "pure_steam_2": {"work_mode": "pure_steam_2"},
                        "pure_steam_1": {"work_mode": "pure_steam_1"},
                        "pure_steam_7": {"work_mode": "pure_steam_7"},
                        "steam_hot_wind_tube_fan_2": {"work_mode": "steam_hot_wind_tube_fan_2"},
                        "pure_steam_5": {"work_mode": "pure_steam_5"},
                        "pure_preheat": {"work_mode": "pure_preheat"},
                        "upper_lower_tube": {"work_mode": "double_tube_1"},
                        "hot_wind_tube_fan_1": {"work_mode": "hot_wind_tube_fan_1"},
                        "double_tube_fan": {"work_mode": "double_tube_fan"},
                        "underside_tube_1": {"work_mode": "underside_tube_1"},
                        "above_inside_outside_tube": {"work_mode": "above_inside_outside_tube"},
                        "above_inside_outside_tube_fan": {"work_mode": "above_inside_outside_tube_fan"},
                        "underside_tube_hot_wind_tube_fan": {"work_mode": "underside_tube_hot_wind_tube_fan"},
                        "steam_hot_wind_tube_fan_1": {"work_mode": "steam_hot_wind_tube_fan_1"},
                        "pure_preheat_2": {"work_mode": "pure_preheat_2"},
                        "hot_wind_tube_fan_5": {"work_mode": "hot_wind_tube_fan_5"},
                        "warm": {"work_mode": "warm"},
                        "stop": {"work_status": "standby"},
                        "pause": {"work_status": "pause"},
                        "work": {"work_status": "work"},
                        "none": {"work_mode": "ff"}
                    }
                },
                "fire_power": {
                    "options": {
                        "100": {"fire_power": "fire_power_10"},
                        "80": {"fire_power": "fire_power_8"},
                        "50": {"fire_power": "fire_power_5"},
                        "30": {"fire_power": "fire_power_3"},
                        "10": {"fire_power": "fire_power_1"},
                        "none": {"fire_power": "fire_power_0"}
                    }
                },
                "pre_heat": {
                    "options": {
                        "off": {"pre_heat": "off"},
                        "on": {"pre_heat": "work"}
                    }
                },
                "steam_quantity": {
                    "options": {
                        "off": {"steam_quantity": 0},
                        "low": {"steam_quantity": 1},
                        "middle": {"steam_quantity": 2},
                        "high": {"steam_quantity": 3},
                    }
                }
            },
            Platform.NUMBER: {
                "temperature": {
                    "min": 0,
                    "max": 250,
                    "step": 5,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS
                },
                "work_hour": {
                    "min": 0,
                    "max": 23,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.HOURS
                },
                "work_minute": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                },
                "work_second": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.SECONDS
                },
                "weight": {
                    "min": 0,
                    "max": 2000,
                    "step": 100,
                    "unit_of_measurement": "g"
                }
            },
            Platform.BINARY_SENSOR: {
                "lack_water": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": [0, 1]
                },
                "door_open": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                },
                "change_water": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": [0, 1]
                }
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_temperature_above": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_temperature_underside": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "work_mode": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "fire_power": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "set_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_microwave_steam_oven": {
        "rationale": ["off", "on"],
        "centralized": [
            "work_mode",
            "fire_power",
            "pre_heat",
            "steam_quantity",
            "temperature",
            "work_hour",
            "work_minute",
            "work_second",
            "weight"
        ],
        "calculate": {
            "get": [
                {
                    "lvalue": "[work_time]",
                    "rvalue": "[work_second] + 60 * [work_minute] + 3600 * [work_hour]"
                },
                {
                    "lvalue": "[set_time]",
                    "rvalue": "[second_set] + 60 * [minute_set] + 3600 * [hour_set]"
                }
            ],
            "set": [
            ]
        },
        "entities": {
            Platform.SELECT: {
                "work_mode": {
                    "options": {
                        "microwave_1": {"work_mode": "microwave_1"},
                        "unfreeze_1": {"work_mode": "unfreeze_1"},
                        "pure_steam_2": {"work_mode": "pure_steam_2"},
                        "pure_steam_1": {"work_mode": "pure_steam_1"},
                        "pure_steam_7": {"work_mode": "pure_steam_7"},
                        "steam_hot_wind_tube_fan_2": {"work_mode": "steam_hot_wind_tube_fan_2"},
                        "pure_steam_5": {"work_mode": "pure_steam_5"},
                        "pure_preheat": {"work_mode": "pure_preheat"},
                        "upper_lower_tube": {"work_mode": "double_tube_1"},
                        "hot_wind_tube_fan_1": {"work_mode": "hot_wind_tube_fan_1"},
                        "double_tube_fan": {"work_mode": "double_tube_fan"},
                        "underside_tube_1": {"work_mode": "underside_tube_1"},
                        "above_inside_outside_tube": {"work_mode": "above_inside_outside_tube"},
                        "above_inside_outside_tube_fan": {"work_mode": "above_inside_outside_tube_fan"},
                        "underside_tube_hot_wind_tube_fan": {"work_mode": "underside_tube_hot_wind_tube_fan"},
                        "steam_hot_wind_tube_fan_1": {"work_mode": "steam_hot_wind_tube_fan_1"},
                        "pure_preheat_2": {"work_mode": "pure_preheat_2"},
                        "hot_wind_tube_fan_5": {"work_mode": "hot_wind_tube_fan_5"},
                        "warm": {"work_mode": "warm"},
                        "stop": {"work_status": "standby"},
                        "pause": {"work_status": "pause"},
                        "work": {"work_status": "work"},
                        "none": {"work_mode": "ff"}
                    }
                },
                "fire_power": {
                    "options": {
                        "100": {"fire_power": "fire_power_10"},
                        "80": {"fire_power": "fire_power_8"},
                        "50": {"fire_power": "fire_power_5"},
                        "30": {"fire_power": "fire_power_3"},
                        "10": {"fire_power": "fire_power_1"},
                        "none": {"fire_power": "fire_power_0"}
                    }
                },
                "pre_heat": {
                    "options": {
                        "off": {"pre_heat": "off"},
                        "on": {"pre_heat": "work"}
                    }
                },
                "steam_quantity": {
                    "options": {
                        "off": {"steam_quantity": 0},
                        "low": {"steam_quantity": 1},
                        "middle": {"steam_quantity": 2},
                        "high": {"steam_quantity": 3},
                    }
                }
            },
            Platform.NUMBER: {
                "temperature": {
                    "min": 0,
                    "max": 250,
                    "step": 5,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS
                },
                "work_hour": {
                    "min": 0,
                    "max": 23,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.HOURS
                },
                "work_minute": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                },
                "work_second": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.SECONDS
                },
                "weight": {
                    "min": 0,
                    "max": 2000,
                    "step": 100,
                    "unit_of_measurement": "g"
                }
            },
            Platform.BINARY_SENSOR: {
                "lack_water": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": [0, 1]
                },
                "door_open": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                },
                "change_water": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": [0, 1]
                }
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_temperature_above": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_temperature_underside": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "work_mode": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "fire_power": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "work_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "set_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
