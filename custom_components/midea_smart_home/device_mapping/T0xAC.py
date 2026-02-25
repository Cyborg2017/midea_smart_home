from homeassistant.const import Platform, UnitOfTemperature, PRECISION_HALVES
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "queries": [{}, {"query_type": "prevent_straight_wind"}, {"query_type": "prevent_super_cool"},
                    {"query_type": "wind_swing_ud_angle"}, {"query_type": "wind_swing_lr_angle"}, {"query_type": "no_wind_sense"}], 
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
                "thermostat": {
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
                        "silent": {"wind_speed": 20},
                        "low": {"wind_speed": 40},
                        "medium": {"wind_speed": 60},
                        "high": {"wind_speed": 80},
                        "full": {"wind_speed": 100},
                        "auto": {"wind_speed": 102}
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
                    "translation_key": "voice"
                },
                "screen_display": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "screen_close",
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
                    "translation_key": "aux_heat",
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
    "23096653": {
        "rationale": ["off", "on"],
        "queries": [{}, {"query_type":"run_status"}, {"query_type":"indoor_humidity"}, {"query_type":"indoor_temperature"}],
        "calculate": {
            "get": [
                {
                    "lvalue": "[total_elec_value]",
                    "rvalue": "float([total_elec]) / 1000"
                },
            ],
        },
        "centralized": [],
        "entities": {
            Platform.CLIMATE: {
                "thermostat": {
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
                        "silent": {"wind_speed": 20},
                        "low": {"wind_speed": 40},
                        "medium": {"wind_speed": 60},
                        "high": {"wind_speed": 80},
                        "full": {"wind_speed": 100},
                        "auto": {"wind_speed": 102}
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
                    "translation_key": "disinfect",
                },
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ptc": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "aux_heat",
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
    }
}
