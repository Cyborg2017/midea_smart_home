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
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
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
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
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
    "38129929": {
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
                    "command": {
                        "protocol_v": 2
                    },
                    "options": {
                        "baby_clothes": {"program": "water_cotton"},
                        "big": {"program": "big"},
                        "blue_oxygen_color_protect": {"program": 164},
                        "clean_stains": {"program": "clean_stains"},
                        "cold_wash": {"program": "water_cold_wash"},
                        "cotton": {"program": "new_water_cotton"},
                        "deep_ssp": {"program": 163},
                        "down_jacket": {"program": "down_jacket"},
                        "eco": {"program": "water_eco"},
                        "enzyme": {"program": "enzyme"},
                        "fast_wash": {"program": "fast_wash"},
                        "fast_wash_30": {"program": "fast_wash_30"},
                        "fiber": {"program": "water_fiber"},
                        "intelligent": {"program": "water_intelligent"},
                        "jacket": {"program": "jacket"},
                        "jean": {"program": "jean"},
                        "mixed_wash": {"program": "water_mixed_wash"},
                        "new_clothes_wash": {"program": "new_clothes_wash"},
                        "no_channeling_color": {"program": "no_channeling_color"},
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
                        "steam_sterilize_wash": {"program": "steam_sterilize_wash"},
                        "steep": {"program": "water_steep"},
                        "summer_wash": {"program": "summer_wash"},
                        "underwear": {"program": "water_underwear"},
                        "white_clothes_clean": {"program": "white_clothes_clean"},
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
                    "translation_key": "stains_38129929",
                    "command": {
                        "protocol_v": 2
                    },
                    "options": {
                        "off": {"stains": "0"},
                        "grass": {"stains": "1"},
                        "coffee": {"stains": "5"},
                        "lipstick": {"stains": "4"},
                        "wine": {"stains": "6"},
                        "mud": {"stains": "2"},
                        "blood": {"stains": "3"}
                    }
                },
                "fresh_anion_switch": {
                    "translation_key": "fresh_anion_switch_38129929",
                    "command": {
                        "protocol_v": 2
                    },
                    "options": {
                        "off": {
                            "fresh_anion_switch": "off",
                            "wind_dispel": "0"
                        },
                        "on": {
                            "fresh_anion_switch": "on",
                            "wind_dispel": "1"
                        }
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
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
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
    "385L0830": {
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
                    "command": {
                        "protocol_v": 2
                    },
                    "options": {
                        "underwear": {"program": 262},
                        "underpants": {"program": 160},
                        "blood_stain_wash": {"program": 209},
                        "fast_wash": {"program": "fast_wash"},
                        "single_dehytration": {"program": "single_dehytration"},
                        "single_drying": {"program": "single_drying"},
                        "ssp": {"program": "water_ssp"},
                        "enzyme": {"program": 77},
                        "girl_underwear": {"program": 259},
                        "nursing_underwear": {"program": 260},
                        "sports_underwear": {"program": 261},
                        "secretion_wash": {"program": 210},
                        "socks": {"program": 161},
                        "cold_wash": {"program": "cold_wash"},
                        "new_clothes_wash": {"program": "new_clothes_wash"},
                        "steep": {"program": "steep"},
                        "rinsing_dehydration": {"program": "rinsing_dehydration"},
                        "strong_wash": {"program": 231},
                        "underwear_dry": {"program": 214},
                        "underpants_dry": {"program": 215},
                        "socks_dry": {"program": 263},
                        "mixed_dry": {"program": 166},
                        "refresh_deodorize": {"program": 138},
                        "hot_wind_dry": {"program": 189},
                        "detergent_box_clean": {"program": 264}
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
                "dryer": {
                    "command": {
                        "protocol_v": 2
                    },
                    "options": {
                        "off": {"dryer": "0"},
                        "auto": {
                            "dryer": "3",
                            "fresh_anion_switch": "off",
                            "wind_dispel": "0"
                        },
                        "timer_60": {
                            "dryer": "5",
                            "fresh_anion_switch": "off",
                            "wind_dispel": "0"
                        },
                        "timer_90": {
                            "dryer": "6",
                            "fresh_anion_switch": "off",
                            "wind_dispel": "0"
                        },
                        "timer_120": {
                            "dryer": "7",
                            "fresh_anion_switch": "off",
                            "wind_dispel": "0"
                        },
                        "timer_180": {
                            "dryer": "11",
                            "fresh_anion_switch": "off",
                            "wind_dispel": "0"
                        }
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
                "fresh_anion_switch": {
                    "translation_key": "fresh_anion_switch",
                    "command": {
                        "protocol_v": 2
                    },
                    "condition": {
                        "eq": ["dryer", "0"]
                    },
                    "options": {
                        "off": {
                            "fresh_anion_switch": "off",
                            "wind_dispel": "0"
                        },
                        "on": {
                            "dryer": "0",
                            "fresh_anion_switch": "on",
                            "wind_dispel": "1"
                        }
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
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
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
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
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
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
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
