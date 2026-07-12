from homeassistant.components.humidifier import HumidifierDeviceClass
from homeassistant.const import Platform, PERCENTAGE, UnitOfTemperature
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "polling_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "entities": {
            Platform.LOCK: {
                "child_lock": {}
            },
            Platform.SWITCH: {
                "anion": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "wind_swing_ud": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "purifier": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "display_on_off"
                },
                "self_clean": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sound": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "buzzer"
                },
                "water_pump": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                }
            },
            Platform.TIME: {
                "power_on_timer": {
                    "target_keys": {
                        "duration": "power_on_time_value"
                    },
                    "time_mode": "convert",
                    "command": {"power_on_timer": "on"}
                },
                "power_off_timer": {
                    "target_keys": {
                        "duration": "power_off_time_value"
                    },
                    "time_mode": "convert",
                    "command": {"power_off_timer": "on"}
                }
            },
            Platform.BUTTON: {
                "cancel_power_on_off_timer": {
                    "command": {"power_on_timer": "off", "power_off_timer": "off"}
                }
            },
            Platform.HUMIDIFIER: {
                "dehumidifier": {
                    "device_class": HumidifierDeviceClass.DEHUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 35,
                    "max_humidity": 85,
                    "target_humidity_step": 5,
                    "mode": "mode",
                    "modes": {
                        "continuity": {"mode": "continuity"},
                        "dry_clothes": {"mode": "dry_clothes"},
                        "auto": {"mode": "auto"},
                        "eco": {"mode": "eco"},
                        "set": {"mode": "set"}
                    }
                }
            },
            Platform.TEXT: {
                "external_humidity_sensor": {}
            },
            Platform.SELECT: {
                "wind_speed": {
                    "options": {
                        "silent": {"wind_speed": 20},
                        "low": {"wind_speed": 40},
                        "comfort": {"wind_speed": 60},
                        "high": {"wind_speed": 80},
                        "strong": {"wind_speed": 100}
                    }
                }
            },
            Platform.SENSOR: {
                "water_full_level": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "default_dehumidifier": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "polling_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "entities": {
            Platform.LOCK: {
                "child_lock": {}
            },
            Platform.SWITCH: {
                "anion": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "wind_swing_ud": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "purifier": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "display_on_off"
                },
                "self_clean": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sound": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "buzzer"
                },
                "water_pump": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                }
            },
            Platform.TIME: {
                "power_on_timer": {
                    "target_keys": {
                        "duration": "power_on_time_value"
                    },
                    "time_mode": "convert",
                    "command": {"power_on_timer": "on"}
                },
                "power_off_timer": {
                    "target_keys": {
                        "duration": "power_off_time_value"
                    },
                    "time_mode": "convert",
                    "command": {"power_off_timer": "on"}
                }
            },
            Platform.BUTTON: {
                "cancel_power_on_off_timer": {
                    "command": {"power_on_timer": "off", "power_off_timer": "off"}
                }
            },
            Platform.HUMIDIFIER: {
                "dehumidifier": {
                    "device_class": HumidifierDeviceClass.DEHUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 35,
                    "max_humidity": 85,
                    "target_humidity_step": 5,
                    "mode": "mode",
                    "modes": {
                        "continuity": {"mode": "continuity"},
                        "dry_clothes": {"mode": "dry_clothes"},
                        "auto": {"mode": "auto"},
                        "eco": {"mode": "eco"},
                        "set": {"mode": "set"}
                    }
                }
            },
            Platform.TEXT: {
                "external_humidity_sensor": {}
            },
            Platform.SELECT: {
                "wind_speed": {
                    "options": {
                        "silent": {"wind_speed": 20},
                        "low": {"wind_speed": 40},
                        "comfort": {"wind_speed": 60},
                        "high": {"wind_speed": 80},
                        "strong": {"wind_speed": 100}
                    }
                }
            },
            Platform.SENSOR: {
                "water_full_level": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "20104032": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "polling_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "entities": {
            Platform.LOCK: {
                "child_lock": {}
            },
            Platform.SWITCH: {
                "anion": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "wind_swing_ud": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "purifier": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "display_on_off"
                },
                "self_clean": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sound": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "buzzer"
                }
            },
            Platform.TIME: {
                "power_on_timer": {
                    "target_keys": {
                        "duration": "power_on_time_value"
                    },
                    "time_mode": "convert",
                    "command": {"power_on_timer": "on"}
                },
                "power_off_timer": {
                    "target_keys": {
                        "duration": "power_off_time_value"
                    },
                    "time_mode": "convert",
                    "command": {"power_off_timer": "on"}
                }
            },
            Platform.BUTTON: {
                "cancel_power_on_off_timer": {
                    "command": {"power_on_timer": "off", "power_off_timer": "off"}
                }
            },
            Platform.HUMIDIFIER: {
                "dehumidifier": {
                    "device_class": HumidifierDeviceClass.DEHUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 35,
                    "max_humidity": 85,
                    "target_humidity_step": 5,
                    "mode": "mode",
                    "modes": {
                        "continuity": {"mode": "continuity"},
                        "dry_clothes": {"mode": "dry_clothes"},
                        "eco": {"mode": "eco"},
                        "set": {"mode": "set"}
                    }
                }
            },
            Platform.TEXT: {
                "external_humidity_sensor": {}
            },
            Platform.SELECT: {
                "wind_speed": {
                    "options": {
                        "silent": {"wind_speed": 20},
                        "comfort": {"wind_speed": 60},
                        "high": {"wind_speed": 80},
                        "strong": {"wind_speed": 100}
                    }
                }
            },
            Platform.SENSOR: {
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "20104036": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"light, sound"}
        ],
        "polling_query": [
            {},
            {"light, sound"}
        ],
        "entities": {
            Platform.SWITCH: {
                "anion": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "display_on_off"
                },
                "sound": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "buzzer"
                },
                "water_pump": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                }
            },
            Platform.TIME: {
                "power_on_timer": {
                    "target_keys": {
                        "duration": "power_on_time_value"
                    },
                    "time_mode": "convert",
                    "command": {"power_on_timer": "on"}
                },
                "power_off_timer": {
                    "target_keys": {
                        "duration": "power_off_time_value"
                    },
                    "time_mode": "convert",
                    "command": {"power_off_timer": "on"}
                }
            },
            Platform.BUTTON: {
                "cancel_power_on_off_timer": {
                    "command": {"power_on_timer": "off", "power_off_timer": "off"}
                }
            },
            Platform.HUMIDIFIER: {
                "dehumidifier": {
                    "device_class": HumidifierDeviceClass.DEHUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 35,
                    "max_humidity": 85,
                    "target_humidity_step": 5,
                    "mode": "mode",
                    "modes": {
                        "continuity": {"mode": "continuity"},
                        "dry_clothes": {"mode": "dry_clothes"},
                        "auto": {"mode": "auto"},
                        "set": {"mode": "set"}
                    }
                }
            },
            Platform.TEXT: {
                "external_humidity_sensor": {}
            },
            Platform.SELECT: {
                "wind_speed": {
                    "options": {
                        "low": {"wind_speed": 40},
                        "high": {"wind_speed": 80}
                    }
                }
            },
            Platform.SENSOR: {
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
