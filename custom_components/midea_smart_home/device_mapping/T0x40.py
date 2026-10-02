from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.CLIMATE: {
                "cooling_fan": {
                    "power": "mode",
                    "hvac_modes": {
                        "off": {"mode": "close_all"}
                    },
                    "preset_modes": {
                        "close": {"mode": "close_all"},
                        "ventilation": {"mode": "ventilation"},
                        "blowing": {"mode": "blowing"}
                    },
                    "fan_modes": {
                        "ventilation": {
                            "key": "ventilation_speed",
                            "options": {
                                "silent": {"ventilation_speed": "20"},
                                "soft_wind": {"ventilation_speed": "40"},
                                "standard": {"ventilation_speed": "60"},
                                "strong": {"ventilation_speed": "80"},
                                "storm": {"ventilation_speed": "100"}
                            }
                        },
                        "blowing": {
                            "key": "blowing_speed",
                            "options": {
                                "silent": {"blowing_speed": "20"},
                                "soft_wind": {"blowing_speed": "40"},
                                "standard": {"blowing_speed": "60"},
                                "strong": {"blowing_speed": "80"},
                                "storm": {"blowing_speed": "100"}
                            }
                        }
                    },
                    "swing_modes": {
                        "ventilation": {
                            "key": "ventilation_direction",
                            "options": {
                                "60": {"ventilation_direction": "60"},
                                "70": {"ventilation_direction": "70"},
                                "80": {"ventilation_direction": "80"},
                                "90": {"ventilation_direction": "90"},
                                "100": {"ventilation_direction": "100"},
                                "110": {"ventilation_direction": "110"},
                                "120": {"ventilation_direction": "120"},
                                "swing": {"ventilation_direction": "253"}
                            }
                        },
                        "blowing": {
                            "key": "blowing_direction",
                            "options": {
                                "60": {"blowing_direction": "60"},
                                "70": {"blowing_direction": "70"},
                                "80": {"blowing_direction": "80"},
                                "90": {"blowing_direction": "90"},
                                "100": {"blowing_direction": "100"},
                                "110": {"blowing_direction": "110"},
                                "120": {"blowing_direction": "120"},
                                "swing": {"blowing_direction": "253"}
                            }
                        }
                    }
                }
            },
            Platform.LIGHT: {
                "main_light": {
                    "power": "light_mode",
                    "brightness": {"main_light_brightness": [10, 100]},
                    "rationale": ["close_all", "main_light"]
                }
            },
            Platform.SWITCH: {
                "smelly_enable": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.BINARY_SENSOR: {
                "smelly_trigger": {
                    "device_class": BinarySensorDeviceClass.OCCUPANCY
                }
            },
            Platform.SENSOR: {
                "current_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "smelly_level": {
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "smelly_threshold": {
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
