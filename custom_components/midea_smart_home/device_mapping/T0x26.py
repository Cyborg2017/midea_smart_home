from homeassistant.const import Platform, UnitOfTemperature, PERCENTAGE, PRECISION_WHOLE, UnitOfTime
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.CLIMATE: {
                "bath_heater": {
                    "translation_key": "bath_heater",
                    "power": "mode",
                    "hvac_modes": {
                        "off": {"mode": "close_all"}
                    },
                    "preset_modes": {
                        "close": {"mode": "close_all"},
                        "heating": {"mode": "heating"},
                        "bath": {"mode": "bath"},
                        "ventilation": {"mode": "ventilation"},
                        "drying": {"mode": "drying"},
                        "blowing": {"mode": "blowing"}
                    },
                    "target_temperature": {
                        "heating": "heating_temperature",
                        "bath": "bath_temperature"
                    },
                    "current_temperature": "current_temperature",
                    "swing_modes": {
                        "heating": {
                            "key": "heating_direction",
                            "options": {
                                "60": {"heating_direction": "60"},
                                "70": {"heating_direction": "70"},
                                "80": {"heating_direction": "80"},
                                "90": {"heating_direction": "90"},
                                "100": {"heating_direction": "100"},
                                "110": {"heating_direction": "110"},
                                "120": {"heating_direction": "120"},
                                "swing": {"heating_direction": "253"}
                            }
                        },
                        "bath": {
                            "key": "bath_direction",
                            "options": {
                                "60": {"bath_direction": "60"},
                                "70": {"bath_direction": "70"},
                                "80": {"bath_direction": "80"},
                                "90": {"bath_direction": "90"},
                                "100": {"bath_direction": "100"},
                                "110": {"bath_direction": "110"},
                                "120": {"bath_direction": "120"},
                                "swing": {"bath_direction": "253"}
                            }
                        },
                        "ventilation": {
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
                        },
                        "drying": {
                            "key": "drying_direction",
                            "options": {
                                "60": {"drying_direction": "60"},
                                "70": {"drying_direction": "70"},
                                "80": {"drying_direction": "80"},
                                "90": {"drying_direction": "90"},
                                "100": {"drying_direction": "100"},
                                "110": {"drying_direction": "110"},
                                "120": {"drying_direction": "120"},
                                "swing": {"drying_direction": "253"}
                            }
                        }
                    },
                    "min_temp": 30,
                    "max_temp": 42,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.LIGHT: {
                "main_light": {
                    "power": "light_mode",
                    "brightness": {"main_light_brightness": [10, 100]},
                    "rationale": ["close_all", "main_light"]
                },
                "night_light": {
                    "power": "light_mode",
                    "brightness": {"night_light_brightness": [5, 30]},
                    "rationale": ["close_all", "night_light"]
                }
            },
            Platform.SWITCH: {
                "radar_induction_enable": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "wifi_led_enable": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.NUMBER: {
                "radar_induction_closing_time": {
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            },
            Platform.SENSOR: {
                "night_light_brightness": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "main_light_brightness": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "current_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                }
            },
            Platform.BINARY_SENSOR: {
                "current_radar_status": {
                    "device_class": BinarySensorDeviceClass.OCCUPANCY
                }
            }
        }
    },
    "default_bath_heater": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.CLIMATE: {
                "bath_heater": {
                    "translation_key": "bath_heater",
                    "power": "mode",
                    "hvac_modes": {
                        "off": {"mode": "close_all"}
                    },
                    "preset_modes": {
                        "close": {"mode": "close_all"},
                        "heating": {"mode": "heating"},
                        "bath": {"mode": "bath"},
                        "ventilation": {"mode": "ventilation"},
                        "drying": {"mode": "drying"},
                        "blowing": {"mode": "blowing"}
                    },
                    "target_temperature": {
                        "heating": "heating_temperature",
                        "bath": "bath_temperature"
                    },
                    "current_temperature": "current_temperature",
                    "swing_modes": {
                        "heating": {
                            "key": "heating_direction",
                            "options": {
                                "60": {"heating_direction": "60"},
                                "70": {"heating_direction": "70"},
                                "80": {"heating_direction": "80"},
                                "90": {"heating_direction": "90"},
                                "100": {"heating_direction": "100"},
                                "110": {"heating_direction": "110"},
                                "120": {"heating_direction": "120"},
                                "swing": {"heating_direction": "253"}
                            }
                        },
                        "bath": {
                            "key": "bath_direction",
                            "options": {
                                "60": {"bath_direction": "60"},
                                "70": {"bath_direction": "70"},
                                "80": {"bath_direction": "80"},
                                "90": {"bath_direction": "90"},
                                "100": {"bath_direction": "100"},
                                "110": {"bath_direction": "110"},
                                "120": {"bath_direction": "120"},
                                "swing": {"bath_direction": "253"}
                            }
                        },
                        "ventilation": {
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
                        },
                        "drying": {
                            "key": "drying_direction",
                            "options": {
                                "60": {"drying_direction": "60"},
                                "70": {"drying_direction": "70"},
                                "80": {"drying_direction": "80"},
                                "90": {"drying_direction": "90"},
                                "100": {"drying_direction": "100"},
                                "110": {"drying_direction": "110"},
                                "120": {"drying_direction": "120"},
                                "swing": {"drying_direction": "253"}
                            }
                        }
                    },
                    "min_temp": 30,
                    "max_temp": 42,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.LIGHT: {
                "main_light": {
                    "power": "light_mode",
                    "brightness": {"main_light_brightness": [10, 100]},
                    "rationale": ["close_all", "main_light"]
                },
                "night_light": {
                    "power": "light_mode",
                    "brightness": {"night_light_brightness": [5, 30]},
                    "rationale": ["close_all", "night_light"]
                }
            },
            Platform.SWITCH: {
                "radar_induction_enable": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "wifi_led_enable": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.NUMBER: {
                "radar_induction_closing_time": {
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            },
            Platform.SENSOR: {
                "night_light_brightness": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "main_light_brightness": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "current_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                }
            },
            Platform.BINARY_SENSOR: {
                "current_radar_status": {
                    "device_class": BinarySensorDeviceClass.OCCUPANCY
                }
            }
        }
    }
}
