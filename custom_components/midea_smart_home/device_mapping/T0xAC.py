from homeassistant.const import Platform, PERCENTAGE, UnitOfTemperature, PRECISION_HALVES, PRECISION_WHOLE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
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
                    "min_temp": 17,
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
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "outdoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
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
                    "min_temp": 17,
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
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
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
                    "min_temp": 17,
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
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "total_elec_value": {
                    "device_class": SensorDeviceClass.ENERGY,
                    "unit_of_measurement": "kWh",
                    "state_class": SensorStateClass.TOTAL_INCREASING
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
                    "min_temp": 17,
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
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
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
                    "min_temp": 17,
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
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "total_elec_value": {
                    "device_class": SensorDeviceClass.ENERGY,
                    "unit_of_measurement": "kWh",
                    "state_class": SensorStateClass.TOTAL_INCREASING
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
        "centralized": ["buzzer"],
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
                    "native_unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "native_unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "new_wind_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "native_unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
