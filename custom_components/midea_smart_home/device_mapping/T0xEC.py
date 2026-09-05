from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "centralized": [
            "cmd_code",
            "taste",
            "time_work_hr",
            "time_work_min"
        ],
        "calculate": {
            "get": [
                {"lvalue": "[remain_time]", "rvalue": "[time_work_hr] * 60 + [time_work_min]"}
            ]
        },
        "entities": {
            Platform.SELECT: {
                "cmd_code": {
                    "options": {
                        "soup": {"cmd_code": "20003", "work_status": 1},
                        "meat_chicken": {"cmd_code": "20004", "work_status": 1},
                        "beef_mutton": {"cmd_code": "20005", "work_status": 1},
                        "beans_tendon": {"cmd_code": "20006", "work_status": 1},
                        "fragrant_rice": {"cmd_code": "20007", "work_status": 1},
                        "plain_soup": {"cmd_code": "20008", "work_status": 1},
                        "stewed_meat": {"cmd_code": "20009", "work_status": 1},
                        "multigrain_porridge": {"cmd_code": "20012", "work_status": 1},
                        "keep_warm": {"cmd_code": "20017", "work_status": 1},
                        "waterless_bake": {"cmd_code": "20018", "work_status": 1},
                        "fragrant_porridge": {"cmd_code": "20025", "work_status": 1},
                        "quick_porridge": {"cmd_code": "20026", "work_status": 1},
                        "quick_rice": {"cmd_code": "20027", "work_status": 1},
                        "multigrain_rice": {"cmd_code": "20028", "work_status": 1},
                        "open_lid_cook": {"cmd_code": "20029", "work_status": 1},
                        "stop": {"work_status": 0}
                    }
                },
                "taste": {
                    "options": {
                        "1": {"taste": "1"},
                        "2": {"taste": "2"},
                        "3": {"taste": "3"}
                    }
                }
            },
            Platform.NUMBER: {
                "time_work_hr": {
                    "min": 0,
                    "max": 23,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.HOURS
                },
                "time_work_min": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "temperature_bottom": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "temperature_bottom"
                },
                "remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_electric_pressure_cooker": {
        "rationale": ["off", "on"],
        "centralized": [
            "cmd_code",
            "taste",
            "time_work_hr",
            "time_work_min"
        ],
        "calculate": {
            "get": [
                {"lvalue": "[remain_time]", "rvalue": "[time_work_hr] * 60 + [time_work_min]"}
            ]
        },
        "entities": {
            Platform.SELECT: {
                "cmd_code": {
                    "options": {
                        "soup": {"cmd_code": "20003", "work_status": 1},
                        "meat_chicken": {"cmd_code": "20004", "work_status": 1},
                        "beef_mutton": {"cmd_code": "20005", "work_status": 1},
                        "beans_tendon": {"cmd_code": "20006", "work_status": 1},
                        "fragrant_rice": {"cmd_code": "20007", "work_status": 1},
                        "plain_soup": {"cmd_code": "20008", "work_status": 1},
                        "stewed_meat": {"cmd_code": "20009", "work_status": 1},
                        "multigrain_porridge": {"cmd_code": "20012", "work_status": 1},
                        "keep_warm": {"cmd_code": "20017", "work_status": 1},
                        "waterless_bake": {"cmd_code": "20018", "work_status": 1},
                        "fragrant_porridge": {"cmd_code": "20025", "work_status": 1},
                        "quick_porridge": {"cmd_code": "20026", "work_status": 1},
                        "quick_rice": {"cmd_code": "20027", "work_status": 1},
                        "multigrain_rice": {"cmd_code": "20028", "work_status": 1},
                        "open_lid_cook": {"cmd_code": "20029", "work_status": 1},
                        "stop": {"work_status": 0}
                    }
                },
                "taste": {
                    "options": {
                        "1": {"taste": "1"},
                        "2": {"taste": "2"},
                        "3": {"taste": "3"}
                    }
                }
            },
            Platform.NUMBER: {
                "time_work_hr": {
                    "min": 0,
                    "max": 23,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.HOURS
                },
                "time_work_min": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "temperature_bottom": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "temperature_bottom"
                },
                "remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "61100524": {
        "rationale": ["off", "on"],
        "centralized": [
            "cmd_code",
            "taste",
            "time_work_hr",
            "time_work_min"
        ],
        "calculate": {
            "get": [
                {"lvalue": "[remain_time]", "rvalue": "[time_work_hr] * 60 + [time_work_min]"}
            ]
        },
        "entities": {
            Platform.SELECT: {
                "cmd_code": {
                    "options": {
                        "soup": {"cmd_code": "20003", "work_status": 1},
                        "meat_chicken": {"cmd_code": "20004", "work_status": 1},
                        "beef_mutton": {"cmd_code": "20005", "work_status": 1},
                        "beans_tendon": {"cmd_code": "20006", "work_status": 1},
                        "fragrant_rice": {"cmd_code": "20007", "work_status": 1},
                        "plain_soup": {"cmd_code": "20008", "work_status": 1},
                        "stewed_meat": {"cmd_code": "20009", "work_status": 1},
                        "multigrain_porridge": {"cmd_code": "20012", "work_status": 1},
                        "keep_warm": {"cmd_code": "20017", "work_status": 1},
                        "waterless_bake": {"cmd_code": "20018", "work_status": 1},
                        "fragrant_porridge": {"cmd_code": "20025", "work_status": 1},
                        "quick_porridge": {"cmd_code": "20026", "work_status": 1},
                        "quick_rice": {"cmd_code": "20027", "work_status": 1},
                        "multigrain_rice": {"cmd_code": "20028", "work_status": 1},
                        "open_lid_cook": {"cmd_code": "20029", "work_status": 1},
                        "stop": {"work_status": 0}
                    }
                },
                "taste": {
                    "options": {
                        "1": {"taste": "1"},
                        "2": {"taste": "2"},
                        "3": {"taste": "3"}
                    }
                }
            },
            Platform.NUMBER: {
                "time_work_hr": {
                    "min": 0,
                    "max": 23,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.HOURS
                },
                "time_work_min": {
                    "min": 0,
                    "max": 59,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "temperature_bottom": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "temperature_bottom"
                },
                "remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
