from homeassistant.const import Platform, UnitOfTime
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [
            {"db"}
        ],
        "entities": {
            Platform.BINARY_SENSOR: {
                "db_detergent_needed_l": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "db_detergent_needed_r": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                }
            },
            Platform.LOCK: {
                "db_baby_lock": {
                    "rationale": [0, 1],
                    "translation_key": "child_lock"
                }
            },
            Platform.SWITCH: {
                "db_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "power"
                },
                "db_control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                    "translation_key": "control_status"
                },
                "db_voice_not_disturb_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "nightly"
                },
                "db_cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "cycle_memory"
                }
            },
            Platform.SELECT: {
                "db_location": {
                    "options": {
                        "left": {"db_location": 1},
                        "right": {"db_location": 2}
                    }
                },
                "db_program": {
                    "options": {
                        "baby_clothes": {"db_program": "baby_clothes"},
                        "baby_clothes_dry": {"db_program": 151},
                        "clean_stains": {"db_program": "clean_stains"},
                        "cold_wash": {"db_program": "cold_wash"},
                        "cook_wash": {"db_program": "cook_wash"},
                        "fast_wash": {"db_program": 137},
                        "hot_wind_dry": {"db_program": 153},
                        "rinsing_dehydration": {"db_program": "rinsing_dehydration"},
                        "self_wash_5": {"db_program": "self_wash_5"},
                        "single_dehytration": {"db_program": "single_dehytration"},
                        "single_drying": {"db_program": "single_drying"},
                        "small_wash_dry": {"db_program": 138},
                        "socks": {"db_program": 148},
                        "standard": {"db_program": "standard"},
                        "underpants": {"db_program": 156},
                        "underwear": {"db_program": "underwear"},
                        "water_ssp": {"db_program": "water_ssp"}
                   }
                },
                "db_temperature": {
                    "options": {
                        "cold_water": {"db_temperature": 1},
                        "30c": {"db_temperature": 3},
                        "40c": {"db_temperature": 4},
                        "60c": {"db_temperature": 5},
                        "95c": {"db_temperature": 6}
                    },
                    "translation_key": "temperature"
                },
                "db_detergent": {
                    "options": {
                        "off": {"db_detergent": 0},
                        "l1": {"db_detergent": 1},
                        "l2": {"db_detergent": 2},
                        "l3": {"db_detergent": 3}
                    },
                    "translation_key": "detergent"
                },
                "db_dehydration_speed": {
                    "options": {
                        "no_spin": {"db_dehydration_speed": 0},
                        "800rpm": {"db_dehydration_speed": 3},
                        "1000rpm": {"db_dehydration_speed": 4}
                    },
                    "translation_key": "dehydration_speed"
                },
                "db_rinse_count": {
                    "options": {
                        "1_time": {"db_rinse_count": 1},
                        "2_times": {"db_rinse_count": 2},
                        "3_times": {"db_rinse_count": 3},
                        "4_times": {"db_rinse_count": 4},
                        "5_times": {"db_rinse_count": 5}
                    },
                    "translation_key": "soak_count"
                },
                "db_dry": {
                    "options": {
                        "off": {"db_dry": 0},
                        "smart": {"db_dry": 1},
                        "timer_240": {"db_dry": 12},
                        "timer_180": {"db_dry": 11},
                        "timer_120": {"db_dry": 7},
                        "timer_60": {"db_dry": 5},
                        "timer_30": {"db_dry": 4}
                    }
                }
            },
            Platform.SENSOR: {
                "db_error_code_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_remain_time_l": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "db_progress_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_running_status_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_error_code_r": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_remain_time_r": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "db_progress_r": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_running_status_r": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_remain_time_long": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_compound_washer": {
        "rationale": ["off", "on"],
        "initial_query": [
            {"db"}
        ],
        "entities": {
            Platform.BINARY_SENSOR: {
                "db_detergent_needed_l": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "db_detergent_needed_r": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                }
            },
            Platform.LOCK: {
                "db_baby_lock": {
                    "rationale": [0, 1],
                    "translation_key": "child_lock"
                }
            },
            Platform.SWITCH: {
                "db_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "power"
                },
                "db_control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                    "translation_key": "control_status"
                },
                "db_voice_not_disturb_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "nightly"
                },
                "db_cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "cycle_memory"
                }
            },
            Platform.SELECT: {
                "db_location": {
                    "options": {
                        "left": {"db_location": 1},
                        "right": {"db_location": 2}
                    }
                },
                "db_program": {
                    "options": {
                        "baby_clothes": {"db_program": "baby_clothes"},
                        "baby_clothes_dry": {"db_program": 151},
                        "clean_stains": {"db_program": "clean_stains"},
                        "cold_wash": {"db_program": "cold_wash"},
                        "cook_wash": {"db_program": "cook_wash"},
                        "fast_wash": {"db_program": 137},
                        "hot_wind_dry": {"db_program": 153},
                        "rinsing_dehydration": {"db_program": "rinsing_dehydration"},
                        "self_wash_5": {"db_program": "self_wash_5"},
                        "single_dehytration": {"db_program": "single_dehytration"},
                        "single_drying": {"db_program": "single_drying"},
                        "small_wash_dry": {"db_program": 138},
                        "socks": {"db_program": 148},
                        "standard": {"db_program": "standard"},
                        "underpants": {"db_program": 156},
                        "underwear": {"db_program": "underwear"},
                        "water_ssp": {"db_program": "water_ssp"}
                   }
                },
                "db_temperature": {
                    "options": {
                        "cold_water": {"db_temperature": 1},
                        "30c": {"db_temperature": 3},
                        "40c": {"db_temperature": 4},
                        "60c": {"db_temperature": 5},
                        "95c": {"db_temperature": 6}
                    },
                    "translation_key": "temperature"
                },
                "db_detergent": {
                    "options": {
                        "off": {"db_detergent": 0},
                        "l1": {"db_detergent": 1},
                        "l2": {"db_detergent": 2},
                        "l3": {"db_detergent": 3}
                    },
                    "translation_key": "detergent"
                },
                "db_dehydration_speed": {
                    "options": {
                        "no_spin": {"db_dehydration_speed": 0},
                        "800rpm": {"db_dehydration_speed": 3},
                        "1000rpm": {"db_dehydration_speed": 4}
                    },
                    "translation_key": "dehydration_speed"
                },
                "db_rinse_count": {
                    "options": {
                        "1_time": {"db_rinse_count": 1},
                        "2_times": {"db_rinse_count": 2},
                        "3_times": {"db_rinse_count": 3},
                        "4_times": {"db_rinse_count": 4},
                        "5_times": {"db_rinse_count": 5}
                    },
                    "translation_key": "soak_count"
                },
                "db_dry": {
                    "options": {
                        "off": {"db_dry": 0},
                        "smart": {"db_dry": 1},
                        "timer_240": {"db_dry": 12},
                        "timer_180": {"db_dry": 11},
                        "timer_120": {"db_dry": 7},
                        "timer_60": {"db_dry": 5},
                        "timer_30": {"db_dry": 4}
                    }
                }
            },
            Platform.SENSOR: {
                "db_error_code_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_remain_time_l": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "db_progress_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_running_status_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_error_code_r": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_remain_time_r": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "db_progress_r": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_running_status_r": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_remain_time_long": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    ("38208002", "38209227"): {
        "rationale": ["off", "on"],
        "initial_query": [
            {"db"},
            {"dc"}
        ],
        "entities": {
            Platform.BINARY_SENSOR: {
                "db_detergent_needed": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                    "translation_key": "db_detergent_needed_b"
                }
            },
            Platform.LOCK: {
                "db_baby_lock": {
                    "rationale": [0, 1],
                    "command": {"db_location": 2},
                    "translation_key": "db_baby_lock_b"
                },
                "dc_baby_lock": {
                    "rationale": [0, 1],
                    "command": {"dc_location": 1},
                    "translation_key": "dc_baby_lock_t"
                }
            },
            Platform.SWITCH: {
                "db_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["off", "on"],
                    "command": {"db_location": 2},
                    "translation_key": "db_power_b"
                },
                "db_control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                    "command": {"db_location": 2},
                    "translation_key": "db_control_status_b"
                },
                "db_voice_not_disturb_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "command": {"db_location": 2},
                    "translation_key": "db_voice_not_disturb_switch_b"
                },
                "db_cycle_memory": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "command": {"db_location": 2},
                    "translation_key": "db_cycle_memory_b"
                },
                "dc_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["off", "on"],
                    "command": {"dc_location": 1},
                    "translation_key": "dc_power_t"
                },
                "dc_control_status": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["pause", "start"],
                    "command": {"dc_location": 1},
                    "translation_key": "dc_control_status_t"
                },
                "dc_sterilize": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "command": {"dc_location": 1},
                    "translation_key": "dc_sterilize_t"
                },
                "dc_prevent_wrinkle": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "command": {"dc_location": 1},
                    "translation_key": "dc_prevent_wrinkle_t"
                }
            },
            Platform.SELECT: {
                "db_program": {
                    "options": {
                        "mixed_wash": {"db_program": "mixed_wash"},
                        "fast_wash": {"db_program": "fast_wash"},
                        "single_dehytration": {"db_program": "single_dehytration"},
                        "rinsing_dehydration": {"db_program": "rinsing_dehydration"},
                        "fast_wash_30": {"db_program": "fast_wash_30"},
                        "eco": {"db_program": "eco"},
                        "down_jacket": {"db_program": "down_jacket"},
                        "ssp": {"db_program": "ssp"},
                        "cotton": {"db_program": "cotton"},
                        "steep": {"db_program": "steep"},
                        "big": {"db_program": "big"},
                        "enzyme": {"db_program": "enzyme"},
                        "baby_clothes": {"db_program": "baby_clothes"},
                        "remove_mite_wash": {"db_program": "remove_mite_wash"},
                        "shirt": {"db_program": "shirt"},
                        "wool": {"db_program": "green_wool"},
                        "steam_sterilize_wash": {"db_program": "steam_sterilize_wash"},
                        "outdoor": {"db_program": "outdoor"},
                        "towel": {"db_program": "bath_towel"},
                        "jean": {"db_program": "jean"},
                    },
                    "command": {"db_location": 2},
                    "translation_key": "db_program_b"
                },
                "db_temperature": {
                    "options": {
                        "cold_water": {"db_temperature": 1},
                        "30c": {"db_temperature": 3},
                        "40c": {"db_temperature": 4},
                        "60c": {"db_temperature": 5},
                        "95c": {"db_temperature": 6},
                    },
                    "command": {"db_location": 2},
                    "translation_key": "db_temperature_b"
                },
                "db_detergent": {
                    "options": {
                        "off": {"db_detergent": 0},
                        "l1": {"db_detergent": 1},
                        "l2": {"db_detergent": 2},
                        "l3": {"db_detergent": 3},
                        "l4": {"db_detergent": 4},
                    },
                    "command": {"db_location": 2},
                    "translation_key": "db_detergent_b"
                },
                "db_dehydration_speed": {
                    "options": {
                        "no_spin": {"db_dehydration_speed": 0},
                        "800rpm": {"db_dehydration_speed": 3},
                        "1000rpm": {"db_dehydration_speed": 4},
                    },
                    "command": {"db_location": 2},
                    "translation_key": "db_dehydration_speed_b"
                },
                "db_rinse_count": {
                    "options": {
                        "1_time": {"db_rinse_count": 1},
                        "2_times": {"db_rinse_count": 2},
                        "3_times": {"db_rinse_count": 3},
                        "4_times": {"db_rinse_count": 4},
                        "5_times": {"db_rinse_count": 5},
                    },
                    "command": {"db_location": 2},
                    "translation_key": "db_rinse_count_b"
                },
                "dc_program": {
                    "options": {
                        "mixed_dry": {"dc_program": "mixed_wash"},
                        "quick_dry": {"dc_program": "quick_dry"},
                        "big_dry": {"dc_program": "big"},
                        "sterilize_dry": {"dc_program": "degerm"},
                        "air_wash": {"dc_program": "air_wash"},
                        "fixed_time_dry": {"dc_program": "fixed_time_dry"},
                        "shirt": {"dc_program": "shirt"},
                        "wool_care": {"dc_program": "wool_care"},
                        "jean": {"dc_program": "jean"},
                        "baby_clothes": {"dc_program": "baby_clothes"},
                        "cotton": {"dc_program": "cotton"},
                        "outdoor": {"dc_program": "outdoor"},
                        "hot_wind_dry": {"dc_program": "hot_air_dry"},
                        "fresh_air": {"dc_program": "cold_air_fresh_air"},
                        "towel": {"dc_program": "towel"},
                        "down_jacket": {"dc_program": "down_jacket"},
                    },
                    "command": {"dc_location": 1},
                    "translation_key": "dc_program_t"
                },
                "dc_intensity": {
                    "options": {
                        "iron_now": {"dc_intensity": 1},
                        "wear_now": {"dc_intensity": 2},
                        "store": {"dc_intensity": 3},
                    },
                    "command": {"dc_location": 1},
                    "translation_key": "dc_intensity_t"
                }
            },
            Platform.SENSOR: {
                "db_error_code": {
                    "device_class": SensorDeviceClass.ENUM,
                    "translation_key": "db_error_code_b"
                },
                "db_remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "db_remain_time_b"
                },
                "db_progress": {
                    "device_class": SensorDeviceClass.ENUM,
                    "translation_key": "db_progress_b"
                },
                "db_running_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "translation_key": "db_running_status_b"
                },
                "dc_error_code": {
                    "device_class": SensorDeviceClass.ENUM,
                    "translation_key": "dc_error_code_t"
                },
                "dc_remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "dc_remain_time_t"
                },
                "dc_dry_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "translation_key": "dc_dry_status_t"
                },
                "dc_running_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "translation_key": "dc_running_status_t"
                },
                "dc_dry_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "dc_dry_time_t"
                }
            }
        }
    }
}
