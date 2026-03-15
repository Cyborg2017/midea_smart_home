from homeassistant.const import Platform, UnitOfTime
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default_clothes_dryer": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "control_status": {
                    "rationale": ["pause", "start"]
                },
                "sterilize": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "prevent_wrinkle_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
            },
            Platform.BINARY_SENSOR: {
                "door_warn": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "translation_key": "door_opened"
                }
            },
            Platform.SELECT: {
                "program": {
                    "options": {
                        "baby_clothes": {"program": "baby_clothes"},
                        "bed_clothes": {"program": "bed_clothes"},
                        "cotton": {"program": "cotton"},
                        "dehumidification": {"program": "dehumidification"},
                        "down_jacket": {"program": "down_jacket"},
                        "fiber": {"program": "fiber"},
                        "fresh_air": {"program": "fresh_air"},
                        "jean": {"program": "jean"},
                        "mixed_wash": {"program": "mixed_wash"},
                        "outdoor": {"program": "outdoor"},
                        "quick_dry_20": {"program": "quick_dry_20"},
                        "shirt": {"program": "shirt"},
                        "sport_clothes": {"program": "sport_clothes"},
                        "towel": {"program": "towel"},
                        "underwear": {"program": "underwear"},
                        "warm_clothes": {"program": "warm_clothes"}
                    }
                },
                "intensity": {
                    "options": {
                        "off": {"intensity": "1"},
                        "10": {"intensity": "2"},
                        "20": {"intensity": "3"},
                        "30": {"intensity": "4"},
                        "40": {"intensity": "5"}
                    }
                }
            },
            Platform.SENSOR: {
                "running_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "progress": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "dry_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "38208347": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "control_status": {
                    "rationale": ["pause", "start"]
                },
                "sterilize": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "prevent_wrinkle_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "dry_night": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "nightly"
                }
            },
            Platform.BINARY_SENSOR: {
                "door_warn": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "translation_key": "door_opened"
                }
            },
            Platform.SELECT: {
                "program": {
                    "options": {
                        "mixed_wash": {"program": "mixed_wash"},
                        "small_piece_dry": {"program": "small_piece_dry"},
                        "down_jacket": {"program": "down_jacket"},
                        "fixed_time_dry": {"program": "fixed_time_dry"},
                        "cotton": {"program": "cotton"},
                        "baby_clothes": {"program": "baby_clothes"},
                        "shirt": {"program": "shirt"},
                        "towel": {"program": "towel"},
                        "sterilize": {"program": "sterilize"},
                        "quick_dry": {"program": "quick_dry"},
                        "sport_clothes": {"program": "sport_clothes"},
                        "underwear": {"program": 101},
                        "jean": {"program": "jean"},
                        "wool": {"program": "wool"},
                        "big": {"program": "big"},
                        "windbreaker": {"program": 123},
                        "windcoat": {"program": 60},
                        "silk": {"program": "silk"},
                        "uniforms": {"program": "uniforms"},
                        "fleece_blanket": {"program": 136},
                        "polar_fleece": {"program": 97}
                    }
                },
                "intensity": {
                    "options": {
                        "iron_now": {"intensity": "1"},
                        "wear_now": {"intensity": "2"},
                        "store": {"intensity": "3"}
                    }
                }
            },
            Platform.SENSOR: {
                "running_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "progress": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "dry_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "38207821": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "control_status": {
                    "rationale": ["pause", "start"]
                },
                "sterilize": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "multi_dimensional_sterilize",
                    "command_on": {
                        "protocol": "02dc",
                        "sterilize": 1
                    },
                    "command_off": {
                        "protocol": "02dc",
                        "sterilize": 0
                    }
                },
                "prevent_wrinkle_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "temperature_level": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "low_temp_dry"
                },
                "flash_dry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "quick_dry_switch"
                },
                "jet": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "six_d_air_flow_dry"
                },
                "dry_night": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "nightly"
                }
            },
            Platform.BINARY_SENSOR: {
                "door_warn": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "translation_key": "door_opened"
                }
            },
            Platform.SELECT: {
                "program": {
                    "options": {
                        "mixed_dry": {"program": "mixed_wash"},
                        "big_dry": {"program": "big_dry"},
                        "down_jacket": {"program": "down_jacket"},
                        "fixed_time_dry": {"program": "fixed_time_dry"},
                        "baby_clothes": {"program": "baby_clothes"},
                        "shirt": {"program": "shirt"},
                        "sterilize": {"program": "sterilize"},
                        "quick_dry_3kg": {"useCycleValue": 1, "program": 127},
                        "wool": {"program": "wool"},
                        "jacket": {"useCycleValue": 1, "program": 60},
                        "hot_air_dry": {"program": "hot_air_dry"},
                        "cold_air_fresh_air": {"program": "cold_air_fresh_air"},
                        "sterilize_remove_mite": {"useCycleValue": 1, "program": 83},
                        "sun_quilt": {"program": "sun_quilt"},
                        "steam_care": {"program": "steam_care"},
                        "jacket_care": {"useCycleValue": 1, "program": 81},
                        "silk": {"program": "silk"},
                        "shirt_care": {"useCycleValue": 1, "program": 68},
                        "trench_coat_care": {"useCycleValue": 1, "program": 67},
                        "small_piece_dry": {"program": "small_piece_dry"},
                        "quick_dry": {"program": "quick_dry"},
                        "cotton": {"program": "cotton"},
                        "towel": {"program": "towel"},
                        "jean": {"program": "jean"},
                        "trench_coat": {"useCycleValue": 1, "program": 123},
                        "steam_bucket_self_clean": {"program": "bucket_self_clean"},
                        "pet_remove_mite": {"useCycleValue": 1, "program": 82},
                        "woolen": {"useCycleValue": 1, "program": 121},
                        "wool_coat": {"useCycleValue": 1, "program": 78},
                        "seasonal_refresh": {"useCycleValue": 1, "program": 89}
                    }
                },
                "intensity": {
                    "translation_key": "dryness_level",
                    "options": {
                        "slightly_dry_for_ironing": {"intensity": 1},
                        "fully_dry_for_wearing": {"intensity": 2},
                        "extra_dry_for_storage": {"intensity": 3}
                    }
                },
                "wind_level": {
                    "options": {
                        "silent": {"wind_level": 1},
                        "gentle": {"wind_level": 2},
                        "strong": {"wind_level": 3}
                    }
                },
                "forget_no_worry_time": {
                    "options": {
                        "0h": {"forget_no_worry_time": 0},
                        "2h": {"forget_no_worry_time": 2},
                        "4h": {"forget_no_worry_time": 4},
                        "6h": {"forget_no_worry_time": 6},
                        "8h": {"forget_no_worry_time": 8}
                    }
                }
            },
            Platform.SENSOR: {
                "running_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "progress": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "dry_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
