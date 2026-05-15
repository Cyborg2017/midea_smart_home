from homeassistant.const import Platform, PERCENTAGE
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
                "auto_rinse": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "dry": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "auto_deodorization": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light_sensor": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "auto_eco": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sedentary_remind": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "foam_shield": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.BUTTON: {
                "stop": {
                    "command": {"stop": "stop"}
                }
            },
            Platform.SELECT: {
                "clean_mode": {
                    "options": {
                        "off": {"clean_mode": "invalid"},
                        "rear_wash": {"clean_mode": "normal"},
                        "feminine_wash": {"clean_mode": "woman"},
                        "nozzle_clean": {"clean_mode": "maintain"}
                    }
                },
                "dry_gear": {
                     "options": {
                        "off": {"dry_gear": 0},
                        "low": {"dry_gear": 1},
                        "medium": {"dry_gear": 2},
                        "high": {"dry_gear": 3}
                    }
                },
                "water_gear": {
                     "options": {
                        "off": {"water_gear": 0},
                        "low": {"water_gear": 1},
                        "medium_low": {"water_gear": 2},
                        "medium": {"water_gear": 3},
                        "medium_high": {"water_gear": 4},
                        "high": {"water_gear": 5}
                    }
                },
                "seat_gear": {
                    "options": {
                        "off": {"seat_gear": 0},
                        "low": {"seat_gear": 1},
                        "medium_low": {"seat_gear": 2},
                        "medium": {"seat_gear": 3},
                        "medium_high": {"seat_gear": 4},
                        "high": {"seat_gear": 5}
                    }
                },
                "rinse_volume": {
                    "options": {
                        "full": {"rinse_volume": "full"},
                        "half": {"rinse_volume": "half"},
                        "off": {"rinse_volume": "invalid"}
                    }
                },
                "injector_position_normal": {
                    "options": {
                        "off": {"injector_position_normal": 0},
                        "rear": {"injector_position_normal": 1},
                        "mid_rear": {"injector_position_normal": 2},
                        "middle": {"injector_position_normal": 3},
                        "mid_front": {"injector_position_normal": 4},
                        "front": {"injector_position_normal": 5}
                    }
                },
                "injector_position_woman": {
                    "options": {
                        "off": {"injector_position_woman": 0},
                        "rear": {"injector_position_woman": 1},
                        "mid_rear": {"injector_position_woman": 2},
                        "middle": {"injector_position_woman": 3},
                        "mid_front": {"injector_position_woman": 4},
                        "front": {"injector_position_woman": 5}
                    }
                },
                "water_pressure_normal": {
                    "options": {
                        "off": {"water_pressure_normal": 0},
                        "low": {"water_pressure_normal": 1},
                        "medium_low": {"water_pressure_normal": 2},
                        "medium": {"water_pressure_normal": 3},
                        "medium_high": {"water_pressure_normal": 4},
                        "high": {"water_pressure_normal": 5}
                    }
                },
                "water_pressure_woman": {
                    "options": {
                        "off": {"water_pressure_woman": 0},
                        "low": {"water_pressure_woman": 1},
                        "medium_low": {"water_pressure_woman": 2},
                        "medium": {"water_pressure_woman": 3},
                        "medium_high": {"water_pressure_woman": 4},
                        "high": {"water_pressure_woman": 5}
                    }
                },
            },
            Platform.SENSOR: {
                "filter_use_per": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            },
            Platform.BINARY_SENSOR: {
                "on_seat": {
                    "device_class": BinarySensorDeviceClass.OCCUPANCY
                },
                "flip_status": {
                    "device_class": BinarySensorDeviceClass.OPENING
                }
            }
        }
    }
}
