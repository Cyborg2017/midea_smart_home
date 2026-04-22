from homeassistant.const import Platform, UnitOfTime
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
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
    }
}
