from homeassistant.const import Platform, UnitOfTime
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default_compound_washer": {
        "rationale": ["off", "on"],
        "initial_query": [
            {"db"}
        ],
        "entities": {
            Platform.BINARY_SENSOR: {
                "db_door_opened_l": {
                    "device_class": BinarySensorDeviceClass.OPENING
                },
                "db_door_opened_r": {
                    "device_class": BinarySensorDeviceClass.OPENING
                },
                "db_bucket_water_overheating_l": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "db_bucket_water_overheating_r": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "db_drying_tunnel_overheating_l": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "db_drying_tunnel_overheating_r": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "db_detergent_needed_l": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "db_detergent_needed_r": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
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
                "db_baby_lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "lock"
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
                        "cold_water": {"db_temperature": 0},
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
                "db_remain_time_l": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "db_remain_time_r": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "db_progress_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_progress_r": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_running_status_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_running_status_r": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_error_code_l": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "db_error_code_r": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
