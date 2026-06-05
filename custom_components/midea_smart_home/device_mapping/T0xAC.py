from homeassistant.const import Platform, PERCENTAGE, UnitOfTemperature, PRECISION_HALVES, PRECISION_WHOLE, UnitOfTime, UnitOfPower, UnitOfEnergy
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"no_wind_sense"},
            {"prevent_straight_wind"},
            {"prevent_super_cool"},
            {"wind_swing_lr_angle"},
            {"wind_swing_ud_angle"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "centralized": ["buzzer"],
        "calculate":{
            "get": [
                {
                    "lvalue": "[screen_display]",
                    "rvalue": "[screen_display_now]"
                },
            ],
            "set": []
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off",
                            "comfort_power_save": "off"
                        },
                        "eco": {"eco": "on"},
                        "comfort": {"comfort_power_save": "on"}
                    },
                    "swing_modes": {
                        "off": {"wind_swing_lr": "off", "wind_swing_ud": "off"},
                        "both": {"wind_swing_lr": "on", "wind_swing_ud": "on"},
                        "horizontal": {"wind_swing_lr": "on", "wind_swing_ud": "off"},
                        "vertical": {"wind_swing_lr": "off", "wind_swing_ud": "on"},
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.FAN: {
                "fresh_air_fan": {
                    "power": "fresh_air",
                    "speeds": list({"fresh_air": "on", "fresh_air_fan_speed": value + 1} for value in range(0, 100)),
                    "preset_modes": {
                        "low": {"fresh_air": "on", "fresh_air_fan_speed": 40},
                        "mid": {"fresh_air": "on", "fresh_air_fan_speed": 60},
                        "high": {"fresh_air": "on", "fresh_air_fan_speed": 80},
                        "strong": {"fresh_air": "on", "fresh_air_fan_speed": 100}
                    }
                }
            },
            Platform.SELECT: {
                "wind_swing_ud_angle": {
                    "options": {
                        "off": {"wind_swing_ud_angle": 0},
                        "top": {"wind_swing_ud_angle": 1},
                        "upper": {"wind_swing_ud_angle": 25},
                        "middle": {"wind_swing_ud_angle": 50},
                        "lower": {"wind_swing_ud_angle": 75},
                        "bottom": {"wind_swing_ud_angle": 100}
                    }
                },
                "wind_swing_lr_angle": {
                    "options": {
                        "off": {"wind_swing_lr_angle": 0},
                        "leftmost": {"wind_swing_lr_angle": 1},
                        "left": {"wind_swing_lr_angle": 25},
                        "middle": {"wind_swing_lr_angle": 50},
                        "right": {"wind_swing_lr_angle": 75},
                        "rightmost": {"wind_swing_lr_angle": 100}
                    }
                },
                "no_wind_sense": {
                    "options": {
                        "off": {"no_wind_sense": 0},
                        "up_down_no_wind": {"no_wind_sense": 1},
                        "up_no_wind": {"no_wind_sense": 2},
                        "down_no_wind": {"no_wind_sense": 3},
                    }
                },
                "wind_around": {
                    "options": {
                        "off": {"wind_around": "off"},
                        "up": {"wind_around": "on", "wind_around_ud": 1},
                        "down": {"wind_around": "on", "wind_around_ud": 2}
                    }
                },
                "prevent_straight_wind": {
                    "options": {
                        "off": {"prevent_straight_wind": 1},
                        "up": {"prevent_straight_wind": 2, "prevent_straight_wind_lr": 2},
                        "down": {"prevent_straight_wind": 2, "prevent_straight_wind_lr": 3}
                    }
                },
                "ptc": {
                    "options": {
                        "off": {"ptc": "off"},
                        "mode_1": {"ptc": "on", "ptc_default_rule": 1},
                        "mode_2": {"ptc": "on", "ptc_default_rule": 0}
                    }
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "default_value": "on",
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "display_on_off"
                },
                "prevent_straight_wind": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [1, 2]
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "light_sensitive": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 3]
                },
                "power_saving": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_floor_air_conditioner": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"prevent_super_cool"},
            {"wind_swing_lr_angle"},
            {"wind_swing_ud_angle"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "centralized": ["buzzer"],
        "calculate":{
            "get": [
                {
                    "lvalue": "[screen_display]",
                    "rvalue": "[screen_display_now]"
                },
            ],
            "set": []
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off"
                        },
                        "eco": {"eco": "on"}
                    },
                    "swing_modes": {
                        "off": {"wind_swing_lr": "off", "wind_swing_ud": "off"},
                        "both": {"wind_swing_lr": "on", "wind_swing_ud": "on"},
                        "horizontal": {"wind_swing_lr": "on", "wind_swing_ud": "off"},
                        "vertical": {"wind_swing_lr": "off", "wind_swing_ud": "on"},
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SELECT: {
                "wind_swing_ud_angle": {
                    "options": {
                        "off": {"wind_swing_ud_angle": 0},
                        "top": {"wind_swing_ud_angle": 1},
                        "upper": {"wind_swing_ud_angle": 25},
                        "middle": {"wind_swing_ud_angle": 50},
                        "lower": {"wind_swing_ud_angle": 75},
                        "bottom": {"wind_swing_ud_angle": 100}
                    }
                },
                "wind_swing_lr_angle": {
                    "options": {
                        "off": {"wind_swing_lr_angle": 0},
                        "leftmost": {"wind_swing_lr_angle": 1},
                        "left": {"wind_swing_lr_angle": 25},
                        "middle": {"wind_swing_lr_angle": 50},
                        "right": {"wind_swing_lr_angle": 75},
                        "rightmost": {"wind_swing_lr_angle": 100}
                    }
                },
                "no_wind_sense": {
                    "options": {
                        "off": {"no_wind_sense": 0},
                        "up_down_no_wind": {"no_wind_sense": 1},
                        "up_no_wind": {"no_wind_sense": 2},
                        "down_no_wind": {"no_wind_sense": 3},
                    }
                },
                "wind_around": {
                    "options": {
                        "off": {"wind_around": "off"},
                        "up": {"wind_around": "on", "wind_around_ud": 1},
                        "down": {"wind_around": "on", "wind_around_ud": 2}
                    }
                },
                "prevent_straight_wind": {
                    "options": {
                        "off": {"prevent_straight_wind": 1},
                        "up": {"prevent_straight_wind": 2, "prevent_straight_wind_lr": 2},
                        "down": {"prevent_straight_wind": 2, "prevent_straight_wind_lr": 3}
                    }
                },
                "ptc": {
                    "options": {
                        "off": {"ptc": "off"},
                        "mode_1": {"ptc": "on", "ptc_default_rule": 1},
                        "mode_2": {"ptc": "on", "ptc_default_rule": 0}
                    }
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "default_value": "on",
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "display_on_off"
                },
                "prevent_straight_wind": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [1, 2]
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "light_sensitive": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 3]
                },
                "power_saving": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "22259041": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"prevent_super_cool"},
            {"wind_swing_lr_angle"},
            {"wind_swing_ud_angle"},
            {"fresh_air"},
            {"fresh_filter_time_use"},
            {"fresh_air_fan_speed"},
            {"fresh_air_mode_two"},
            {"inner_purifier"},
            {"inner_purifier_fan_speed"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "centralized": ["buzzer"],
        "calculate":{
            "get": [
                {
                    "lvalue": "[screen_display]",
                    "rvalue": "[screen_display_now]"
                },
            ],
            "set": []
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off"
                        },
                        "eco": {"eco": "on"}
                    },
                    "swing_modes": {
                        "off": {"wind_swing_lr": "off", "wind_swing_ud": "off"},
                        "both": {"wind_swing_lr": "on", "wind_swing_ud": "on"},
                        "horizontal": {"wind_swing_lr": "on", "wind_swing_ud": "off"},
                        "vertical": {"wind_swing_lr": "off", "wind_swing_ud": "on"},
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.FAN: {
                "fresh_air_fan": {
                    "power": "fresh_air",
                    "speeds": list({"fresh_air": "on","fresh_air_fan_speed": value + 1} for value in range(0, 100)),
                    "preset_modes": {
                        "low": {"fresh_air": "on", "fresh_air_fan_speed": 40},
                        "mid": {"fresh_air": "on", "fresh_air_fan_speed": 60},
                        "high": {"fresh_air": "on", "fresh_air_fan_speed": 80},
                        "strong": {"fresh_air": "on", "fresh_air_fan_speed": 100}
                    }
                },
                "inner_purifier_fan": {
                    "power": "inner_purifier",
                    "speeds": list({"inner_purifier": "on","inner_purifier_fan_speed": value + 1} for value in range(0, 100)),
                    "preset_modes": {
                        "low": {"inner_purifier": "on", "inner_purifier_fan_speed": 40},
                        "mid": {"inner_purifier": "on", "inner_purifier_fan_speed": 60},
                        "high": {"inner_purifier": "on", "inner_purifier_fan_speed": 80},
                        "strong": {"inner_purifier": "on", "inner_purifier_fan_speed": 100}
                    }
                }
            },
            Platform.SELECT: {
                "wind_swing_ud_angle": {
                    "options": {
                        "off": {"wind_swing_ud_angle": 0},
                        "top": {"wind_swing_ud_angle": 1},
                        "upper": {"wind_swing_ud_angle": 25},
                        "middle": {"wind_swing_ud_angle": 50},
                        "lower": {"wind_swing_ud_angle": 75},
                        "bottom": {"wind_swing_ud_angle": 100}
                    }
                },
                "wind_swing_lr_angle": {
                    "options": {
                        "off": {"wind_swing_lr_angle": 0},
                        "leftmost": {"wind_swing_lr_angle": 1},
                        "left": {"wind_swing_lr_angle": 25},
                        "middle": {"wind_swing_lr_angle": 50},
                        "right": {"wind_swing_lr_angle": 75},
                        "rightmost": {"wind_swing_lr_angle": 100}
                    }
                },
                "fresh_air_mode_two": {
                    "options": {
                        "outside": {"fresh_air_mode_two": 0},
                        "inside": {"fresh_air_mode_two": 8}
                    }
                }
            },
            Platform.SWITCH: {
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "default_value": "on",
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "display_on_off"
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "fresh_filter_time_use": {
                    "state_class": SensorStateClass.MEASUREMENT,
                    "unit_of_measurement": UnitOfTime.HOURS
                }
            }
        }
    },
    "22011719": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"wind_swing_lr_angle"},
            {"wind_swing_ud_angle"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "centralized": ["buzzer"],
        "calculate":{
            "get": [
                {
                    "lvalue": "[screen_display]",
                    "rvalue": "[screen_display_now]"
                },
            ],
            "set": []
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "swing_modes": {
                        "off": {"wind_swing_lr": "off", "wind_swing_ud": "off"},
                        "both": {"wind_swing_lr": "on", "wind_swing_ud": "on"},
                        "horizontal": {"wind_swing_lr": "on", "wind_swing_ud": "off"},
                        "vertical": {"wind_swing_lr": "off", "wind_swing_ud": "on"},
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SELECT: {
                "wind_swing_ud_angle": {
                    "options": {
                        "off": {"wind_swing_ud_angle": 0},
                        "top": {"wind_swing_ud_angle": 1},
                        "upper": {"wind_swing_ud_angle": 25},
                        "middle": {"wind_swing_ud_angle": 50},
                        "lower": {"wind_swing_ud_angle": 75},
                        "bottom": {"wind_swing_ud_angle": 100}
                    }
                },
                "wind_swing_lr_angle": {
                    "options": {
                        "off": {"wind_swing_lr_angle": 0},
                        "leftmost": {"wind_swing_lr_angle": 1},
                        "left": {"wind_swing_lr_angle": 25},
                        "middle": {"wind_swing_lr_angle": 50},
                        "right": {"wind_swing_lr_angle": 75},
                        "rightmost": {"wind_swing_lr_angle": 100}
                    }
                }
            },
            Platform.SWITCH: {
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "default_value": "on",
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "display_on_off"
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_wall_air_conditioner": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"no_wind_sense"},
            {"prevent_straight_wind"},
            {"prevent_super_cool"},
            {"wind_swing_lr_angle"},
            {"wind_swing_ud_angle"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "centralized": ["buzzer"],
        "calculate":{
            "get": [
                {
                    "lvalue": "[screen_display]",
                    "rvalue": "[screen_display_now]"
                },
            ],
            "set": []
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off",
                            "comfort_power_save": "off"
                        },
                        "eco": {"eco": "on"},
                        "comfort": {"comfort_power_save": "on"}
                    },
                    "swing_modes": {
                        "off": {"wind_swing_lr": "off", "wind_swing_ud": "off"},
                        "both": {"wind_swing_lr": "on", "wind_swing_ud": "on"},
                        "horizontal": {"wind_swing_lr": "on", "wind_swing_ud": "off"},
                        "vertical": {"wind_swing_lr": "off", "wind_swing_ud": "on"},
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.FAN: {
                "fresh_air_fan": {
                    "power": "fresh_air",
                    "speeds": list({"fresh_air": "on", "fresh_air_fan_speed": value + 1} for value in range(0, 100)),
                    "preset_modes": {
                        "low": {"fresh_air": "on", "fresh_air_fan_speed": 40},
                        "mid": {"fresh_air": "on", "fresh_air_fan_speed": 60},
                        "high": {"fresh_air": "on", "fresh_air_fan_speed": 80},
                        "strong": {"fresh_air": "on", "fresh_air_fan_speed": 100}
                    }
                }
            },
            Platform.SELECT: {
                "wind_swing_ud_angle": {
                    "options": {
                        "off": {"wind_swing_ud_angle": 0},
                        "top": {"wind_swing_ud_angle": 1},
                        "upper": {"wind_swing_ud_angle": 25},
                        "middle": {"wind_swing_ud_angle": 50},
                        "lower": {"wind_swing_ud_angle": 75},
                        "bottom": {"wind_swing_ud_angle": 100}
                    }
                },
                "wind_swing_lr_angle": {
                    "options": {
                        "off": {"wind_swing_lr_angle": 0},
                        "leftmost": {"wind_swing_lr_angle": 1},
                        "left": {"wind_swing_lr_angle": 25},
                        "middle": {"wind_swing_lr_angle": 50},
                        "right": {"wind_swing_lr_angle": 75},
                        "rightmost": {"wind_swing_lr_angle": 100}
                    }
                },
                "no_wind_sense": {
                    "options": {
                        "off": {"no_wind_sense": 0},
                        "up_down_no_wind": {"no_wind_sense": 1},
                        "up_no_wind": {"no_wind_sense": 2},
                        "down_no_wind": {"no_wind_sense": 3},
                    }
                },
                "wind_around": {
                    "options": {
                        "off": {"wind_around": "off"},
                        "up": {"wind_around": "on", "wind_around_ud": 1},
                        "down": {"wind_around": "on", "wind_around_ud": 2}
                    }
                },
                "prevent_straight_wind": {
                    "options": {
                        "off": {"prevent_straight_wind": 1},
                        "up": {"prevent_straight_wind": 2, "prevent_straight_wind_lr": 2},
                        "down": {"prevent_straight_wind": 2, "prevent_straight_wind_lr": 3}
                    }
                },
                "ptc": {
                    "options": {
                        "off": {"ptc": "off"},
                        "mode_1": {"ptc": "on", "ptc_default_rule": 1},
                        "mode_2": {"ptc": "on", "ptc_default_rule": 0}
                    }
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "default_value": "on",
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "display_on_off"
                },
                "prevent_straight_wind": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [1, 2]
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "light_sensitive": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 3]
                },
                "power_saving": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "22019053": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"no_wind_sense"},
            {"prevent_straight_wind"},
            {"prevent_super_cool"},
            {"wind_swing_lr_angle"},
            {"wind_swing_ud_angle"},
            {"fresh_air"},
            {"fresh_filter_time_use"},
            {"fresh_air_fan_speed"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "centralized": ["buzzer"],
        "calculate":{
            "get": [
                {
                    "lvalue": "[screen_display]",
                    "rvalue": "[screen_display_now]"
                },
            ],
            "set": []
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off",
                            "comfort_power_save": "off"
                        },
                        "eco": {"eco": "on"},
                        "comfort": {"comfort_power_save": "on"}
                    },
                    "swing_modes": {
                        "off": {"wind_swing_lr": "off", "wind_swing_ud": "off"},
                        "both": {"wind_swing_lr": "on", "wind_swing_ud": "on"},
                        "horizontal": {"wind_swing_lr": "on", "wind_swing_ud": "off"},
                        "vertical": {"wind_swing_lr": "off", "wind_swing_ud": "on"},
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.FAN: {
                "fresh_air_fan": {
                    "power": "fresh_air",
                    "speeds": list({"fresh_air": "on", "fresh_air_fan_speed": value + 1} for value in range(0, 100)),
                    "preset_modes": {
                        "low": {"fresh_air": "on", "fresh_air_fan_speed": 40},
                        "mid": {"fresh_air": "on", "fresh_air_fan_speed": 60},
                        "high": {"fresh_air": "on", "fresh_air_fan_speed": 80},
                        "strong": {"fresh_air": "on", "fresh_air_fan_speed": 100}
                    }
                }
            },
            Platform.SELECT: {
                "wind_swing_ud_angle": {
                    "options": {
                        "off": {"wind_swing_ud_angle": 0},
                        "top": {"wind_swing_ud_angle": 1},
                        "upper": {"wind_swing_ud_angle": 25},
                        "middle": {"wind_swing_ud_angle": 50},
                        "lower": {"wind_swing_ud_angle": 75},
                        "bottom": {"wind_swing_ud_angle": 100}
                    }
                },
                "wind_swing_lr_angle": {
                    "options": {
                        "off": {"wind_swing_lr_angle": 0},
                        "leftmost": {"wind_swing_lr_angle": 1},
                        "left": {"wind_swing_lr_angle": 25},
                        "middle": {"wind_swing_lr_angle": 50},
                        "right": {"wind_swing_lr_angle": 75},
                        "rightmost": {"wind_swing_lr_angle": 100}
                    }
                },
                "no_wind_sense": {
                    "options": {
                        "off": {"no_wind_sense": 0},
                        "up_down_no_wind": {"no_wind_sense": 1},
                        "up_no_wind": {"no_wind_sense": 2},
                        "down_no_wind": {"no_wind_sense": 3},
                    }
                }
            },
            Platform.SWITCH: {
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "default_value": "on",
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "display_on_off"
                },
                "prevent_straight_wind": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [1, 2]
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
               "fresh_filter_time_use": {
                    "state_class": SensorStateClass.MEASUREMENT,
                    "unit_of_measurement": UnitOfTime.HOURS
                }
            }
        }
    },
    ("22013201", "22013129"): {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"prevent_straight_wind"},
            {"prevent_super_cool"},
            {"wind_swing_lr_angle"},
            {"wind_swing_ud_angle"},
            {"temperature"},
            {"group_data_one"},
            {"group_data_four"},
            {"group_data_five"}
        ],
        "polling_query": [
            {"temperature"},
            {"group_data_one"},
            {"group_data_four"},
            {"group_data_five"}
        ],
        "centralized": ["buzzer"],
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {"cool_power_saving": 0},
                        "eco": {"cool_power_saving": 1}
                    },
                    "swing_modes": {
                        "off": {"wind_swing_lr": "off", "wind_swing_ud": "off"},
                        "both": {"wind_swing_lr": "on", "wind_swing_ud": "on"},
                        "horizontal": {"wind_swing_lr": "on", "wind_swing_ud": "off"},
                        "vertical": {"wind_swing_lr": "off", "wind_swing_ud": "on"},
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "current_humidity": "indoor_humidity",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SELECT: {
                "wind_swing_ud_angle": {
                    "options": {
                        "off": {"wind_swing_ud_angle": 0},
                        "top": {"wind_swing_ud_angle": 1},
                        "upper": {"wind_swing_ud_angle": 25},
                        "middle": {"wind_swing_ud_angle": 50},
                        "lower": {"wind_swing_ud_angle": 75},
                        "bottom": {"wind_swing_ud_angle": 100}
                    }
                },
                "wind_swing_lr_angle": {
                    "options": {
                        "off": {"wind_swing_lr_angle": 0},
                        "leftmost": {"wind_swing_lr_angle": 1},
                        "left": {"wind_swing_lr_angle": 25},
                        "middle": {"wind_swing_lr_angle": 50},
                        "right": {"wind_swing_lr_angle": 75},
                        "rightmost": {"wind_swing_lr_angle": 100}
                    }
                },
                "wind_around": {
                    "options": {
                        "off": {"wind_around": "off"},
                        "up": {"wind_around": "on", "wind_around_ud": 1},
                        "down": {"wind_around": "on", "wind_around_ud": 2}
                    }
                },
                "prevent_straight_wind": {
                    "options": {
                        "off": {"prevent_straight_wind": 1},
                        "up": {"prevent_straight_wind": 2, "prevent_straight_wind_lr": 2},
                        "down": {"prevent_straight_wind": 2, "prevent_straight_wind_lr": 3}
                    }
                },
                "ptc": {
                    "options": {
                        "off": {"ptc": "off"},
                        "mode_1": {"ptc": "on", "ptc_default_rule": 1},
                        "mode_2": {"ptc": "on", "ptc_default_rule": 0}
                    }
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "default_value": "on"
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 100],
                    "translation_key": "display_on_off"
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light_sensitive": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 3]
                },
                "power_saving": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "indoor_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "current_time_power": {
                    "device_class": SensorDeviceClass.POWER,
                    "unit_of_measurement": UnitOfPower.KILO_WATT,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "suggested_display_precision": 1
                },
                "total_power_consumption": {
                    "device_class": SensorDeviceClass.ENERGY,
                    "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
                    "state_class": SensorStateClass.TOTAL_INCREASING,
                    "suggested_display_precision": 1,
                    "translation_key": "total_elec_value"
                }
            }
        }
    },
    ("22040055", "22040023", "22040053"): {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"prevent_straight_wind"},
            {"prevent_super_cool"},
            {"wind_swing_lr_angle"},
            {"wind_swing_ud_angle"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "centralized": ["buzzer"],
        "calculate":{
            "get": [
                {
                    "lvalue": "[screen_display]",
                    "rvalue": "[screen_display_now]"
                },
            ],
            "set": []
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off",
                            "comfort_power_save": "off"
                        },
                        "eco": {"eco": "on"},
                        "comfort": {"comfort_power_save": "on"}
                    },
                    "swing_modes": {
                        "off": {"wind_swing_lr": "off", "wind_swing_ud": "off"},
                        "both": {"wind_swing_lr": "on", "wind_swing_ud": "on"},
                        "horizontal": {"wind_swing_lr": "on", "wind_swing_ud": "off"},
                        "vertical": {"wind_swing_lr": "off", "wind_swing_ud": "on"},
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES
                }
            },
            Platform.SELECT: {
                "wind_swing_ud_angle": {
                    "options": {
                        "off": {"wind_swing_ud_angle": 0},
                        "top": {"wind_swing_ud_angle": 1},
                        "upper": {"wind_swing_ud_angle": 25},
                        "middle": {"wind_swing_ud_angle": 50},
                        "lower": {"wind_swing_ud_angle": 75},
                        "bottom": {"wind_swing_ud_angle": 100}
                    }
                },
                "wind_swing_lr_angle": {
                    "options": {
                        "off": {"wind_swing_lr_angle": 0},
                        "leftmost": {"wind_swing_lr_angle": 1},
                        "left": {"wind_swing_lr_angle": 25},
                        "middle": {"wind_swing_lr_angle": 50},
                        "right": {"wind_swing_lr_angle": 75},
                        "rightmost": {"wind_swing_lr_angle": 100}
                    }
                }
            },
            Platform.SWITCH: {
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "default_value": "on",
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "display_on_off"
                },
                "prevent_straight_wind": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [1, 2]
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_central_air_conditioner": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"indoor_temperature"},
            {"prevent_super_cool"},
            {"run_status"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "calculate": {
            "get": [
                {
                    "lvalue": "[total_elec_value]",
                    "rvalue": "float([total_elec]) / 1000"
                },
            ],
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off",
                            "cool_power_saving": 0,
                            "strong_wind": "off"
                        },
                        "eco": {"eco": "on", "cool_power_saving": 1},
                        "boost": {"strong_wind": "on"}
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SWITCH: {
                "fengguan_remove_odor": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                },
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "follow_body_sense": {
                    "options": {
                        "on": {"follow_body_sense": "on", "follow_body_sense_enable": 1},
                        "off": {"follow_body_sense": "off", "follow_body_sense_enable": 1},
                    }
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "total_elec_value": {
                    "device_class": SensorDeviceClass.ENERGY,
                    "unit_of_measurement": "kWh",
                    "state_class": SensorStateClass.TOTAL_INCREASING
                }
            }
        }
    },
    ("22396505", "22396521", "22396525", "22396533"): {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"indoor_temperature"},
            {"indoor_humidity"},
            {"prevent_super_cool"},
            {"run_status"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {"strong_wind": "off"},
                        "boost": {"strong_wind": "on"}
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "ac_dry"
                }
            },
            Platform.SELECT: {
                "follow_body_sense": {
                    "options": {
                        "on": {"follow_body_sense": "on", "follow_body_sense_enable": 1},
                        "off": {"follow_body_sense": "off", "follow_body_sense_enable": 1},
                    }
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "indoor_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_humidity"
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "22396517": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"indoor_temperature"},
            {"indoor_humidity"},
            {"no_wind_sense"},
            {"prevent_super_cool"},
            {"run_status"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {"strong_wind": "off"},
                        "boost": {"strong_wind": "on"}
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "ac_dry"
                },
                "no_wind_sense": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SELECT: {
                "follow_body_sense": {
                    "options": {
                        "on": {"follow_body_sense": "on", "follow_body_sense_enable": 1},
                        "off": {"follow_body_sense": "off", "follow_body_sense_enable": 1},
                    }
                },
                "up_down_wind_direction": {
                    "options": {
                        "auto": {"up_down_wind_direction": 0, "wind_swing_ud": "on"},
                        "top": {"up_down_wind_direction": 1, "wind_swing_ud": "off"},
                        "upper": {"up_down_wind_direction": 3, "wind_swing_ud": "off"},
                        "middle": {"up_down_wind_direction": 5, "wind_swing_ud": "off"},
                        "lower": {"up_down_wind_direction": 7, "wind_swing_ud": "off"},
                        "bottom": {"up_down_wind_direction": 9, "wind_swing_ud": "off"}
                    },
                    "translation_key": "wind_swing_ud_angle"
                },
                "left_right_wind_direction": {
                    "options": {
                        "auto": {"left_right_wind_direction": 0, "wind_swing_lr": "on"},
                        "leftmost": {"left_right_wind_direction": 1, "wind_swing_lr": "off"},
                        "left": {"left_right_wind_direction": 3, "wind_swing_lr": "off"},
                        "middle": {"left_right_wind_direction": 5, "wind_swing_lr": "off"},
                        "right": {"left_right_wind_direction": 7, "wind_swing_lr": "off"},
                        "rightmost": {"left_right_wind_direction": 9, "wind_swing_lr": "off"}
                    },
                    "translation_key": "wind_swing_lr_angle"
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "indoor_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_humidity"
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "23096245": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"indoor_temperature"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "23096653": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"indoor_temperature"},
            {"run_status"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "calculate": {
            "get": [
                {
                    "lvalue": "[total_elec_value]",
                    "rvalue": "float([total_elec]) / 1000"
                },
            ],
        },
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off",
                            "cool_power_saving": 0,
                            "strong_wind": "off"
                        },
                        "eco": {"eco": "on", "cool_power_saving": 1},
                        "boost": {"strong_wind": "on"}
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SWITCH: {
                "fengguan_remove_odor": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                },
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "follow_body_sense": {
                    "options": {
                        "on": {"follow_body_sense": "on", "follow_body_sense_enable": 1},
                        "off": {"follow_body_sense": "off", "follow_body_sense_enable": 1},
                    }
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "total_elec_value": {
                    "device_class": SensorDeviceClass.ENERGY,
                    "unit_of_measurement": "kWh",
                    "state_class": SensorStateClass.TOTAL_INCREASING
                }
            }
        }
    },
    ("22396399", "22396403", "22396405"): {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"indoor_temperature"},
            {"outdoor_temperature"},
            {"prevent_super_cool"},
            {"run_status"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "auto": {"power": "on", "mode": "auto"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "preset_modes": {
                        "none": {
                            "strong_wind": "off"
                        },
                        "boost": {"strong_wind": "on"}
                    },
                    "fan_modes": {
                        "20": {"wind_speed": 20},
                        "40": {"wind_speed": 40},
                        "60": {"wind_speed": 60},
                        "80": {"wind_speed": 80},
                        "100": {"wind_speed": 100},
                        "102": {"wind_speed": 102}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 16,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "prevent_super_cool": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "ac_dry"
                }
            },
            Platform.SELECT: {
                "follow_body_sense": {
                    "options": {
                        "on": {"follow_body_sense": "on", "follow_body_sense_enable": 1},
                        "off": {"follow_body_sense": "off", "follow_body_sense_enable": 1}
                    }
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "outdoor_temperature"
                }
            }
        }
    },
    "default_central_fresh_air": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"fresh_air_mode"},
            {"fresh_filter_time"},
            {"indoor_temperature"},
            {"new_wind_humidity"},
            {"run_status"},
            {"wind_strength"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "entities": {
            Platform.FAN: {
                "fan": {
                    "translation_key": "fresh_air_fan",
                    "power": "new_wind_machine",
                    "speeds": list({"fresh_air_fan_speed": value + 1} for value in range(0, 100)),
                    "preset_modes": {
                        "heat_exchange": {
                            "fresh_air_mode": 1,
                            "exhaust_strength": 0,
                            "wind_strength": 0
                        },
                        "smooth_in": {
                            "fresh_air_mode": 2,
                            "exhaust_strength": 0,
                            "wind_strength": 0
                        },
                        "rough_in": {
                            "fresh_air_mode": 2,
                            "exhaust_strength": 0,
                            "wind_strength": 1
                        },
                        "smooth_out": {
                            "fresh_air_mode": 3,
                            "exhaust_strength": 0,
                            "wind_strength": 0
                        },
                        "rough_out": {
                            "fresh_air_mode": 3,
                            "exhaust_strength": 1,
                            "wind_strength": 0
                        },
                        "auto": {
                            "fresh_air_mode": 4,
                            "exhaust_strength": 0,
                            "wind_strength": 0
                        },
                        "innercycle": {
                            "fresh_air_mode": 5,
                            "exhaust_strength": 0,
                            "wind_strength": 0
                        },
                    }
                }
            },
            Platform.SWITCH: {
                "fresh_air_remove_odor": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                }
            },
            Platform.SENSOR: {
                "fresh_filter_time": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "new_wind_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_central_miniaturized_fresh_air": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"fresh_air_mode"},
            {"fresh_filter_time"},
            {"indoor_temperature"},
            {"run_status"}
        ],
        "polling_query": [
            {"indoor_temperature"}
        ],
        "entities": {
            Platform.SWITCH: {
                "new_wind_machine": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "power"
                },
                "fresh_air_remove_odor": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                }
            },
            Platform.FAN: {
                "intake_fan": {
                    "power": "new_wind_machine_intake_switch",
                    "rationale": [0, 1],
                    "speeds": list({"fresh_air_intake_fan_speed": value + 1} for value in range(0, 100))
                },
                "exhaust_fan": {
                    "power": "new_wind_machine_exhaust_switch",
                    "rationale": [0, 1],
                    "speeds": list({"fresh_air_exhaust_fan_speed": value + 1} for value in range(0, 100))
                }
            },
            Platform.SELECT: {
                "fresh_air_mode": {
                    "options": {
                        "heat_exchange": {
                            "fresh_air_mode": 1
                        },
                        "strong": {
                            "fresh_air_mode": 7
                        },
                        "vacation": {
                            "fresh_air_mode": 8
                        },
                        "auto": {
                            "fresh_air_mode": 4
                        }
                    }
                }
            },
            Platform.SENSOR: {
                "fresh_filter_time": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
