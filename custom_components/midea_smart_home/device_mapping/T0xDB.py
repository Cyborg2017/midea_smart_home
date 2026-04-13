from homeassistant.const import Platform, UnitOfTime
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default_front_load_washer": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.BINARY_SENSOR: {
                "door_opened": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                },
                "detergent_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                },
                "bucket_water_overheating": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "nightly": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "wind_dispel": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {"protocol_v": 2}
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "normal": {"mode": "normal"},
                        "factory_test": {"mode": "factory_test"},
                        "service": {"mode": "service"},
                        "normal_continus": {"mode": "normal_continus"}
                    }
                },
                "program": {
                    "options": {
                        "air_wash": {"program": "air_wash"},
                        "baby_clothes": {"program": "baby_clothes"},
                        "big": {"program": "big"},
                        "clean_stains": {"program": "clean_stains"},
                        "cold_wash": {"program": "cold_wash"},
                        "cotton": {"program": "cotton"},
                        "deep_ssp": {"program": "deep_ssp"},
                        "down_jacket": {"program": "down_jacket"},
                        "enzyme": {"program": "enzyme"},
                        "fast_wash": {"program": "fast_wash"},
                        "fast_wash_30": {"program": "fast_wash_30"},
                        "fiber": {"program": "fiber"},
                        "intelligent": {"program": "intelligent"},
                        "jacket": {"program": "jacket"},
                        "jean": {"program": "jean"},
                        "mixed_wash": {"program": "mixed_wash"},
                        "new_clothes_wash": {"program": "new_clothes_wash"},
                        "outdoor": {"program": "outdoor"},
                        "remove_mite_wash": {"program": "remove_mite_wash"},
                        "rinsing_dehydration": {"program": "rinsing_dehydration"},
                        "shirt": {"program": "shirt"},
                        "silk": {"program": "silk"},
                        "single_dehytration": {"program": "single_dehytration"},
                        "single_drying": {"program": "single_drying"},
                        "sport_clothes": {"program": "sport_clothes"},
                        "spring_autumn_wash": {"program": "spring_autumn_wash"},
                        "ssp": {"program": "ssp"},
                        "steam_sterilize_wash": {"program": "steam_sterilize_wash"},
                        "steep": {"program": "steep"},
                        "summer_wash": {"program": "summer_wash"},
                        "underwear": {"program": "underwear"},
                        "winter_wash": {"program": "wash"},
                        "wool": {"program": "wool"}
                    }
                },
                "dehydration_speed": {
                    "options": {
                        "no_spin": {"dehydration_speed": "0"},
                        "400rpm": {"dehydration_speed": "400"},
                        "600rpm": {"dehydration_speed": "600"},
                        "800rpm": {"dehydration_speed": "800"},
                        "1000rpm": {"dehydration_speed": "1000"},
                        "1200rpm": {"dehydration_speed": "1200"},
                        "1400rpm": {"dehydration_speed": "1400"}
                    }
                },
                "soak_count": {
                    "options": {
                        "1_time": {"soak_count": "1"},
                        "2_times": {"soak_count": "2"},
                        "3_times": {"soak_count": "3"},
                        "4_times": {"soak_count": "4"}
                    }
                },
                "water_level": {
                    "options": {
                        "auto": {"water_level": "auto"},
                        "l1": {"water_level": "low"},
                        "l2": {"water_level": "mid"},
                        "l3": {"water_level": "high"},
                        "l4": {"water_level": "4"}
                    }
                },
                "detergent": {
                    "options": {
                        "smart": {"detergent": "4"},
                        "off": {"detergent": "0"},
                        "l1": {"detergent": "1"},
                        "l2": {"detergent": "2"},
                        "l3": {"detergent": "3"},
                        "l4": {"detergent": "5"}
                    }
                },
                "temperature": {
                    "options": {
                        "cold_water": {"temperature": "0"},
                        "20c": {"temperature": "20"},
                        "30c": {"temperature": "30"},
                        "40c": {"temperature": "40"},
                        "60c": {"temperature": "60"},
                        "95c": {"temperature": "95"}
                    }
                },
                "stains": {
                    "options": {
                        "off": {"stains": "0"},
                        "sauce": {"stains": "83"},
                        "fruit": {"stains": "85"},
                        "makeup": {"stains": "84"}
                    }
                },
                "dryer": {
                    "options": {
                        "off": {"dryer": "0"},
                        "low_temp_dry": {"dryer": "3"},
                        "high_temp_dry": {"dryer": "1"},
                        "30_min": {"dryer": "4"},
                        "60_min": {"dryer": "5"},
                        "90_min": {"dryer": "6"},
                        "120_min": {"dryer": "7"},
                        "180_min": {"dryer": "11"}
                    }
                },
                "fresh_air_time": {
                    "options": {
                        "2_hours": {"fresh_air_time": 2},
                        "4_hours": {"fresh_air_time": 4},
                        "6_hours": {"fresh_air_time": 6},
                        "8_hours": {"fresh_air_time": 8}
                    },
                    "command": {"protocol_v": 2}
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
                "wash_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "dehydration_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "td10ve40": { # sn8: "38133671"
        "rationale": ["off", "on"],
        "entities": {
            Platform.BINARY_SENSOR: {
                "door_opened": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                },
                "detergent_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                },
                "bucket_water_overheating": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "nightly": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "wind_dispel": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {"protocol_v": 2}
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "normal": {"mode": "normal"},
                        "factory_test": {"mode": "factory_test"},
                        "service": {"mode": "service"},
                        "normal_continus": {"mode": "normal_continus"}
                    }
                },
                "program": {
                    "options": {
                        "air_wash": {"program": "air_wash"},
                        "baby_clothes": {"program": "water_cotton"},
                        "big": {"program": "big"},
                        "clean_stains": {"program": "clean_stains"},
                        "cold_wash": {"program": "water_cold_wash"},
                        "cotton": {"program": "new_water_cotton"},
                        "deep_ssp": {"program": 163},
                        "down_jacket": {"program": "down_jacket"},
                        "enzyme": {"program": "enzyme"},
                        "fast_wash": {"program": "fast_wash"},
                        "fast_wash_30": {"program": "fast_wash_30"},
                        "fiber": {"program": "water_fiber"},
                        "intelligent": {"program": "water_intelligent"},
                        "jacket": {"program": "jacket"},
                        "jean": {"program": "jean"},
                        "mixed_wash": {"program": "water_mixed_wash"},
                        "new_clothes_wash": {"program": "new_clothes_wash"},
                        "outdoor": {"program": "water_outdoor"},
                        "remove_mite_wash": {"program": "water_remove_mite_wash"},
                        "rinsing_dehydration": {"program": "rinsing_dehydration"},
                        "shirt": {"program": "fast_wash_60"},
                        "silk": {"program": "silk"},
                        "single_dehytration": {"program": "single_dehytration"},
                        "single_drying": {"program": "single_drying"},
                        "sport_clothes": {"program": "sport_clothes"},
                        "spring_autumn_wash": {"program": "spring_autumn_wash"},
                        "ssp": {"program": "water_ssp"},
                        "steam_sterilize_wash": {"program": "steam_sterilize_wash"},
                        "steep": {"program": "water_steep"},
                        "summer_wash": {"program": "summer_wash"},
                        "underwear": {"program": "water_underwear"},
                        "winter_wash": {"program": "winter_wash"},
                        "wool": {"program": "green_wool"}
                    }
                },
                "dehydration_speed": {
                    "options": {
                        "no_spin": {"dehydration_speed": "0"},
                        "400rpm": {"dehydration_speed": "400"},
                        "600rpm": {"dehydration_speed": "600"},
                        "800rpm": {"dehydration_speed": "800"},
                        "1000rpm": {"dehydration_speed": "1000"},
                        "1200rpm": {"dehydration_speed": "1200"},
                        "1400rpm": {"dehydration_speed": "1400"}
                    }
                },
                "soak_count": {
                    "options": {
                        "1_time": {"soak_count": "1"},
                        "2_times": {"soak_count": "2"},
                        "3_times": {"soak_count": "3"},
                        "4_times": {"soak_count": "4"}
                    }
                },
                "water_level": {
                    "options": {
                        "auto": {"water_level": "auto"},
                        "l1": {"water_level": "low"},
                        "l2": {"water_level": "mid"},
                        "l3": {"water_level": "high"},
                        "l4": {"water_level": "4"}
                    }
                },
                "detergent": {
                    "options": {
                        "smart": {"detergent": "4"},
                        "off": {"detergent": "0"},
                        "l1": {"detergent": "1"},
                        "l2": {"detergent": "2"},
                        "l3": {"detergent": "3"},
                        "l4": {"detergent": "5"}
                    }
                },
                "temperature": {
                    "options": {
                        "cold_water": {"temperature": "0"},
                        "20c": {"temperature": "20"},
                        "30c": {"temperature": "30"},
                        "40c": {"temperature": "40"},
                        "60c": {"temperature": "60"},
                        "95c": {"temperature": "95"}
                    }
                },
                "stains": {
                    "options": {
                        "off": {"stains": "0"},
                        "sauce": {"stains": "83"},
                        "fruit": {"stains": "85"},
                        "makeup": {"stains": "84"}
                    }
                },
                "dryer": {
                    "options": {
                        "off": {"dryer": "0"},
                        "low_temp_dry": {"dryer": "3"},
                        "high_temp_dry": {"dryer": "1"},
                        "30_min": {"dryer": "4"},
                        "60_min": {"dryer": "5"},
                        "90_min": {"dryer": "6"},
                        "120_min": {"dryer": "7"},
                        "180_min": {"dryer": "11"}
                    }
                },
                "fresh_air_time": {
                    "options": {
                        "2_hours": {"fresh_air_time": 2},
                        "4_hours": {"fresh_air_time": 4},
                        "6_hours": {"fresh_air_time": 6},
                        "8_hours": {"fresh_air_time": 8}
                    },
                    "command": {"protocol_v": 2}
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
                "wash_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "dehydration_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "tg10ve40": { # sn8: "38133671"
        "rationale": ["off", "on"],
        "entities": {
            Platform.BINARY_SENSOR: {
                "door_opened": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                },
                "detergent_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                },
                "bucket_water_overheating": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "nightly": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "wind_dispel": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {"protocol_v": 2}
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "normal": {"mode": "normal"},
                        "factory_test": {"mode": "factory_test"},
                        "service": {"mode": "service"},
                        "normal_continus": {"mode": "normal_continus"}
                    }
                },
                "program": {
                    "options": {
                        "baby_clothes": {"program": "water_cotton"},
                        "big": {"program": "big"},
                        "clean_stains": {"program": "clean_stains"},
                        "cold_wash": {"program": "water_cold_wash"},
                        "cotton": {"program": "new_water_cotton"},
                        "deep_ssp": {"program": 163},
                        "down_jacket": {"program": "down_jacket"},
                        "enzyme": {"program": "enzyme"},
                        "fast_wash": {"program": "fast_wash"},
                        "fast_wash_30": {"program": "fast_wash_30"},
                        "fiber": {"program": "water_fiber"},
                        "intelligent": {"program": "water_intelligent"},
                        "jacket": {"program": "jacket"},
                        "jean": {"program": "jean"},
                        "mixed_wash": {"program": "water_mixed_wash"},
                        "new_clothes_wash": {"program": "new_clothes_wash"},
                        "outdoor": {"program": "water_outdoor"},
                        "remove_mite_wash": {"program": "water_remove_mite_wash"},
                        "rinsing_dehydration": {"program": "rinsing_dehydration"},
                        "shirt": {"program": "fast_wash_60"},
                        "silk": {"program": "silk"},
                        "single_dehytration": {"program": "single_dehytration"},
                        "sport_clothes": {"program": "sport_clothes"},
                        "spring_autumn_wash": {"program": "spring_autumn_wash"},
                        "ssp": {"program": "water_ssp"},
                        "steam_sterilize_wash": {"program": "steam_sterilize_wash"},
                        "steep": {"program": "water_steep"},
                        "summer_wash": {"program": "summer_wash"},
                        "underwear": {"program": "water_underwear"},
                        "winter_wash": {"program": "winter_wash"},
                        "wool": {"program": "green_wool"}
                    }
                },
                "dehydration_speed": {
                    "options": {
                        "no_spin": {"dehydration_speed": "0"},
                        "400rpm": {"dehydration_speed": "400"},
                        "600rpm": {"dehydration_speed": "600"},
                        "800rpm": {"dehydration_speed": "800"},
                        "1000rpm": {"dehydration_speed": "1000"},
                        "1200rpm": {"dehydration_speed": "1200"},
                        "1400rpm": {"dehydration_speed": "1400"}
                    }
                },
                "soak_count": {
                    "options": {
                        "1_time": {"soak_count": "1"},
                        "2_times": {"soak_count": "2"},
                        "3_times": {"soak_count": "3"},
                        "4_times": {"soak_count": "4"}
                    }
                },
                "water_level": {
                    "options": {
                        "auto": {"water_level": "auto"},
                        "l1": {"water_level": "low"},
                        "l2": {"water_level": "mid"},
                        "l3": {"water_level": "high"},
                        "l4": {"water_level": "4"}
                    }
                },
                "detergent": {
                    "options": {
                        "smart": {"detergent": "4"},
                        "off": {"detergent": "0"},
                        "l1": {"detergent": "1"},
                        "l2": {"detergent": "2"},
                        "l3": {"detergent": "3"},
                        "l4": {"detergent": "5"}
                    }
                },
                "temperature": {
                    "options": {
                        "cold_water": {"temperature": "0"},
                        "20c": {"temperature": "20"},
                        "30c": {"temperature": "30"},
                        "40c": {"temperature": "40"},
                        "60c": {"temperature": "60"},
                        "95c": {"temperature": "95"}
                    }
                },
                "stains": {
                    "options": {
                        "off": {"stains": "0"},
                        "sauce": {"stains": "83"},
                        "fruit": {"stains": "85"},
                        "makeup": {"stains": "84"}
                    }
                },
                "fresh_air_time": {
                    "options": {
                        "2_hours": {"fresh_air_time": 2},
                        "4_hours": {"fresh_air_time": 4},
                        "6_hours": {"fresh_air_time": 6},
                        "8_hours": {"fresh_air_time": 8}
                    },
                    "command": {"protocol_v": 2}
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
                "wash_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "dehydration_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "38133671": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.BINARY_SENSOR: {
                "door_opened": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                },
                "detergent_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                },
                "bucket_water_overheating": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "nightly": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "wind_dispel": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {"protocol_v": 2}
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "normal": {"mode": "normal"},
                        "factory_test": {"mode": "factory_test"},
                        "service": {"mode": "service"},
                        "normal_continus": {"mode": "normal_continus"}
                    }
                },
                "program": {
                    "options": {
                        "air_wash": {"program": "air_wash"},
                        "baby_clothes": {"program": "water_cotton"},
                        "big": {"program": "big"},
                        "clean_stains": {"program": "clean_stains"},
                        "cold_wash": {"program": "water_cold_wash"},
                        "cotton": {"program": "new_water_cotton"},
                        "deep_ssp": {"program": 163},
                        "down_jacket": {"program": "down_jacket"},
                        "enzyme": {"program": "enzyme"},
                        "fast_wash": {"program": "fast_wash"},
                        "fast_wash_30": {"program": "fast_wash_30"},
                        "fiber": {"program": "water_fiber"},
                        "intelligent": {"program": "water_intelligent"},
                        "jacket": {"program": "jacket"},
                        "jean": {"program": "jean"},
                        "mixed_wash": {"program": "water_mixed_wash"},
                        "new_clothes_wash": {"program": "new_clothes_wash"},
                        "outdoor": {"program": "water_outdoor"},
                        "remove_mite_wash": {"program": "water_remove_mite_wash"},
                        "rinsing_dehydration": {"program": "rinsing_dehydration"},
                        "shirt": {"program": "fast_wash_60"},
                        "silk": {"program": "silk"},
                        "single_dehytration": {"program": "single_dehytration"},
                        "single_drying": {"program": "single_drying"},
                        "sport_clothes": {"program": "sport_clothes"},
                        "spring_autumn_wash": {"program": "spring_autumn_wash"},
                        "ssp": {"program": "water_ssp"},
                        "steam_sterilize_wash": {"program": "steam_sterilize_wash"},
                        "steep": {"program": "water_steep"},
                        "summer_wash": {"program": "summer_wash"},
                        "underwear": {"program": "water_underwear"},
                        "winter_wash": {"program": "winter_wash"},
                        "wool": {"program": "green_wool"}
                    }
                },
                "dehydration_speed": {
                    "options": {
                        "no_spin": {"dehydration_speed": "0"},
                        "400rpm": {"dehydration_speed": "400"},
                        "600rpm": {"dehydration_speed": "600"},
                        "800rpm": {"dehydration_speed": "800"},
                        "1000rpm": {"dehydration_speed": "1000"},
                        "1200rpm": {"dehydration_speed": "1200"},
                        "1400rpm": {"dehydration_speed": "1400"}
                    }
                },
                "soak_count": {
                    "options": {
                        "1_time": {"soak_count": "1"},
                        "2_times": {"soak_count": "2"},
                        "3_times": {"soak_count": "3"},
                        "4_times": {"soak_count": "4"}
                    }
                },
                "water_level": {
                    "options": {
                        "auto": {"water_level": "auto"},
                        "l1": {"water_level": "low"},
                        "l2": {"water_level": "mid"},
                        "l3": {"water_level": "high"},
                        "l4": {"water_level": "4"}
                    }
                },
                "detergent": {
                    "options": {
                        "smart": {"detergent": "4"},
                        "off": {"detergent": "0"},
                        "l1": {"detergent": "1"},
                        "l2": {"detergent": "2"},
                        "l3": {"detergent": "3"},
                        "l4": {"detergent": "5"}
                    }
                },
                "temperature": {
                    "options": {
                        "cold_water": {"temperature": "0"},
                        "20c": {"temperature": "20"},
                        "30c": {"temperature": "30"},
                        "40c": {"temperature": "40"},
                        "60c": {"temperature": "60"},
                        "95c": {"temperature": "95"}
                    }
                },
                "stains": {
                    "options": {
                        "off": {"stains": "0"},
                        "sauce": {"stains": "83"},
                        "fruit": {"stains": "85"},
                        "makeup": {"stains": "84"}
                    }
                },
                "dryer": {
                    "options": {
                        "off": {"dryer": "0"},
                        "low_temp_dry": {"dryer": "3"},
                        "high_temp_dry": {"dryer": "1"},
                        "30_min": {"dryer": "4"},
                        "60_min": {"dryer": "5"},
                        "90_min": {"dryer": "6"},
                        "120_min": {"dryer": "7"},
                        "180_min": {"dryer": "11"}
                    }
                },
                "fresh_air_time": {
                    "options": {
                        "2_hours": {"fresh_air_time": 2},
                        "4_hours": {"fresh_air_time": 4},
                        "6_hours": {"fresh_air_time": 6},
                        "8_hours": {"fresh_air_time": 8}
                    },
                    "command": {"protocol_v": 2}
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
                "wash_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "dehydration_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "38124584": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.BINARY_SENSOR: {
                "door_opened": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                },
                "detergent_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ultraviolet_lamp": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "wind_dispel": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {"protocol_v": 2}
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "normal": {"mode": "normal"},
                        "factory_test": {"mode": "factory_test"},
                        "service": {"mode": "service"},
                        "normal_continus": {"mode": "normal_continus"}
                    }
                },
                "program": {
                    "options": {
                        "big": {"program": "big"},
                        "down_jacket": {"program": "down_jacket"},
                        "eco": {"program": "eco"},
                        "fast_wash": {"program": "fast_wash"},
                        "jacket": {"program": "jacket"},
                        "mixed_wash": {"program": "water_mixed_wash"},
                        "rinsing_dehydration": {"program": "rinsing_dehydration"},
                        "single_dehytration": {"program": "single_dehytration"},
                        "steam_sterilize_wash": {"program": "steam_sterilize_wash"},
                        "baby_clothes": {"program": "baby_clothes"},
                        "fast_wash_30": {"program": "fast_wash_30"},
                        "intelligent": {"program": "intelligent"},
                        "shirt": {"program": "shirt"},
                        "remove_mite_wash": {"program": "remove_mite_wash"},
                        "ssp": {"program": "ssp"},
                        "steep": {"program": "steep"},
                        "underwear": {"program": "underwear"},
                        "wool": {"program": "wool"}
                    }
                },
                "dehydration_speed": {
                    "options": {
                        "no_spin": {"dehydration_speed": "0"},
                        "400rpm": {"dehydration_speed": "400"},
                        "600rpm": {"dehydration_speed": "600"},
                        "800rpm": {"dehydration_speed": "800"},
                        "1000rpm": {"dehydration_speed": "1000"},
                        "1200rpm": {"dehydration_speed": "1200"}
                    }
                },
                "soak_count": {
                    "options": {
                        "1_time": {"soak_count": "1"},
                        "2_times": {"soak_count": "2"},
                        "3_times": {"soak_count": "3"},
                        "4_times": {"soak_count": "4"}
                    }
                },
                "water_level": {
                    "options": {
                        "auto": {"water_level": "auto"},
                        "l1": {"water_level": "low"},
                        "l2": {"water_level": "mid"},
                        "l3": {"water_level": "high"},
                        "l4": {"water_level": "4"}
                    }
                },
                "detergent": {
                    "options": {
                        "smart": {"detergent": "4"},
                        "off": {"detergent": "0"},
                        "l1": {"detergent": "1"},
                        "l2": {"detergent": "2"},
                        "l3": {"detergent": "3"},
                        "l4": {"detergent": "5"}
                    }
                },
                "temperature": {
                    "options": {
                        "cold_water": {"temperature": "0"},
                        "20c": {"temperature": "20"},
                        "30c": {"temperature": "30"},
                        "40c": {"temperature": "40"},
                        "60c": {"temperature": "60"},
                        "95c": {"temperature": "95"}
                    }
                },
                "fresh_air_time": {
                    "options": {
                        "2_hours": {"fresh_air_time": 2},
                        "4_hours": {"fresh_air_time": 4},
                        "6_hours": {"fresh_air_time": 6},
                        "8_hours": {"fresh_air_time": 8}
                    },
                    "command": {"protocol_v": 2}
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
                "wash_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "dehydration_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "38132344": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.BINARY_SENSOR: {
                "door_opened": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                },
                "detergent_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                },
                "bucket_water_overheating": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "nightly": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "steam_wash": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "microbubble": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "wind_dispel": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {"protocol_v": 2}
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "normal": {"mode": "normal"},
                        "factory_test": {"mode": "factory_test"},
                        "service": {"mode": "service"},
                        "normal_continus": {"mode": "normal_continus"}
                    }
                },
                "program": {
                    "options": {
                        "baby_clothes": {"program": "water_cotton"},
                        "big": {"program": "big"},
                        "clean_stains": {"program": "clean_stains"},
                        "cold_wash": {"program": "water_cold_wash"},
                        "cotton": {"program": "new_water_cotton"},
                        "deep_ssp": {"program": 163},
                        "down_jacket": {"program": "down_jacket"},
                        "enzyme": {"program": "enzyme"},
                        "fast_wash": {"program": "fast_wash"},
                        "fast_wash_30": {"program": "fast_wash_30"},
                        "fiber": {"program": "water_fiber"},
                        "jacket": {"program": "jacket"},
                        "jean": {"program": "jean"},
                        "mixed_wash": {"program": "water_mixed_wash"},
                        "new_clothes_wash": {"program": "new_clothes_wash"},
                        "outdoor": {"program": "water_outdoor"},
                        "remove_mite_wash": {"program": "water_remove_mite_wash"},
                        "rinsing_dehydration": {"program": "rinsing_dehydration"},
                        "shirt": {"program": "fast_wash_60"},
                        "silk": {"program": "silk"},
                        "single_dehytration": {"program": "single_dehytration"},
                        "sport_clothes": {"program": "sport_clothes"},
                        "spring_autumn_wash": {"program": "spring_autumn_wash"},
                        "ssp": {"program": "water_ssp"},
                        "sterilize_wash": {"program": "sterilize_wash"},
                        "steep": {"program": "water_steep"},
                        "summer_wash": {"program": "summer_wash"},
                        "super_clean": {"program": 80},
                        "underwear": {"program": "water_underwear"},
                        "winter_wash": {"program": "winter_wash"},
                        "wool": {"program": "green_wool"}
                    }
                },
                "dehydration_speed": {
                    "options": {
                        "no_spin": {"dehydration_speed": "0"},
                        "400rpm": {"dehydration_speed": "400"},
                        "600rpm": {"dehydration_speed": "600"},
                        "800rpm": {"dehydration_speed": "800"},
                        "1000rpm": {"dehydration_speed": "1000"},
                        "1200rpm": {"dehydration_speed": "1200"},
                        "1400rpm": {"dehydration_speed": "1400"}
                    }
                },
                "soak_count": {
                    "options": {
                        "1_time": {"soak_count": "1"},
                        "2_times": {"soak_count": "2"},
                        "3_times": {"soak_count": "3"},
                        "4_times": {"soak_count": "4"}
                    }
                },
                "water_level": {
                    "options": {
                        "auto": {"water_level": "auto"},
                        "l1": {"water_level": "low"},
                        "l2": {"water_level": "mid"},
                        "l3": {"water_level": "high"},
                        "l4": {"water_level": "4"}
                    }
                },
                "detergent": {
                    "options": {
                        "smart": {"detergent": "4"},
                        "off": {"detergent": "0"},
                        "l1": {"detergent": "1"},
                        "l2": {"detergent": "2"},
                        "l3": {"detergent": "3"},
                        "l4": {"detergent": "5"}
                    }
                },
                "temperature": {
                    "options": {
                        "cold_water": {"temperature": "0"},
                        "20c": {"temperature": "20"},
                        "30c": {"temperature": "30"},
                        "40c": {"temperature": "40"},
                        "60c": {"temperature": "60"},
                        "95c": {"temperature": "95"}
                    }
                },
                "stains": {
                    "options": {
                        "off": {"stains": "0"},
                        "sauce": {"stains": "83"},
                        "fruit": {"stains": "85"},
                        "makeup": {"stains": "84"}
                    }
                },
                "fresh_air_time": {
                    "options": {
                        "2_hours": {"fresh_air_time": 2},
                        "4_hours": {"fresh_air_time": 4},
                        "6_hours": {"fresh_air_time": 6},
                        "8_hours": {"fresh_air_time": 8}
                    },
                    "command": {"protocol_v": 2}
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
                "wash_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "dehydration_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "38124077": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.BINARY_SENSOR: {
                "door_opened": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                },
                "detergent_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                },
                "softener_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                },
                "bucket_water_overheating": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "ultraviolet_lamp": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "microbubble": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
                "wind_dispel": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["0", "1"]
                },
                "cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {"protocol_v": 2}
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "normal": {"mode": "normal"},
                        "factory_test": {"mode": "factory_test"},
                        "service": {"mode": "service"},
                        "normal_continus": {"mode": "normal_continus"}
                    }
                },
                "program": {
                    "options": {
                        "fast_wash": {"program": "fast_wash"},
                        "mixed_wash": {"program": "water_mixed_wash"},
                        "single_dehytration": {"program": "single_dehytration"},
                        "rinsing_dehydration": {"program": "rinsing_dehydration"},
                        "down_jacket": {"program": "down_jacket"},
                        "big": {"program": "big"},
                        "cold_wash": {"program": "water_cold_wash"},
                        "wool": {"program": "wool"},
                        "remove_mite_wash": {"program": "water_remove_mite_wash"},
                        "ssp": {"program": "water_ssp"},
                        "intelligent": {"program": "water_intelligent"},
                        "steep": {"program": "water_steep"},
                        "fast_wash_30": {"program": "fast_wash_30"},
                        "cotton": {"program": "new_water_cotton"},
                        "baby_clothes": {"program": "water_cotton"},
                        "sterilize_wash": {"program": "sterilize_wash"},
                        "eco": {"program": "water_eco"},
                        "hanfu_spring_summer": {"program": "hanfu_spring_summer"},
                        "hanfu_autumn_winter": {"program": "hanfu_autumn_winter"}
                    }
                },
                "dehydration_speed": {
                    "options": {
                        "no_spin": {"dehydration_speed": "0"},
                        "400rpm": {"dehydration_speed": "400"},
                        "600rpm": {"dehydration_speed": "600"},
                        "800rpm": {"dehydration_speed": "800"},
                        "1000rpm": {"dehydration_speed": "1000"},
                        "1200rpm": {"dehydration_speed": "1200"}
                    }
                },
                "soak_count": {
                    "options": {
                        "1_time": {"soak_count": "1"},
                        "2_times": {"soak_count": "2"},
                        "3_times": {"soak_count": "3"},
                        "4_times": {"soak_count": "4"}
                    }
                },
                "water_level": {
                    "options": {
                        "auto": {"water_level": "auto"},
                        "l1": {"water_level": "low"},
                        "l2": {"water_level": "mid"},
                        "l3": {"water_level": "high"},
                        "l4": {"water_level": "4"}
                    }
                },
                "detergent": {
                    "options": {
                        "smart": {"detergent": "4"},
                        "off": {"detergent": "0"},
                        "l1": {"detergent": "1"},
                        "l2": {"detergent": "2"},
                        "l3": {"detergent": "3"},
                        "l4": {"detergent": "5"}
                    }
                },
                "softener": {
                    "options": {
                        "off": {"softener": "0"},
                        "auto": {"softener": "1"},
                        "l1": {"softener": "2"},
                        "l2": {"softener": "3"},
                        "l3": {"softener": "4"},
                        "l4": {"softener": "5"}
                    }
                },
                "temperature": {
                    "options": {
                        "cold_water": {"temperature": "0"},
                        "20c": {"temperature": "20"},
                        "30c": {"temperature": "30"},
                        "40c": {"temperature": "40"},
                        "60c": {"temperature": "60"},
                        "95c": {"temperature": "95"}
                    }
                },
                "fresh_air_time": {
                    "options": {
                        "2_hours": {"fresh_air_time": 2},
                        "4_hours": {"fresh_air_time": 4},
                        "6_hours": {"fresh_air_time": 6},
                        "8_hours": {"fresh_air_time": 8}
                    },
                    "command": {"protocol_v": 2}
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
                "wash_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "dehydration_time_value": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
