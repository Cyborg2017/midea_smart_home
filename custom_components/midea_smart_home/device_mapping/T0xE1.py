from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import Platform, UnitOfTemperature, UnitOfTime, PERCENTAGE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default_dishwasher": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "dish_wash": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "work_status_key": "work_status",
                    "defer_update": True,
                    "pending_commands": ["wash_mode", "additional"],
                    "start_command": {"work_status": "work"},
                    "stop_command": {"work_status": "cancel"}
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "dryswitch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                },
            },
            Platform.BINARY_SENSOR: {
                "doorswitch": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "rationale": [1, 0],
                    "translation_key": "door_opened"
                },
                "water_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                    "translation_key": "lack_water"
                },
                "softwater_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                }
            },
            Platform.NUMBER: {
                "air_set_hour": {
                    "min": 0,
                    "max": 72,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.HOURS
                },
            },
            Platform.SELECT: {
                "work_status": {
                    "options": {
                        "power_off": {"work_status": "power_off"},
                        "cancel": {"work_status": "cancel"},
                        "pause": {"operator": "pause"},
                        "start": {"work_status": "work", "pending_commands": ["wash_mode", "additional"]}
                    }
                },
                "wash_mode": {
                    "defer_update": True,
                    "options": {
                        "neutral_gear": {"mode": "neutral_gear"},
                        "strong_wash": {"mode": "strong_wash"},
                        "standard_wash": {"mode": "standard_wash"},
                        "single_disinfect": {"mode": "single_disinfect"},
                        "eco_wash": {"mode": "eco_wash"},
                        "glass_wash": {"mode": "glass_wash"},
                        "fast_wash": {"mode": "fast_wash"},
                        "soak_wash": {"mode": "soak_wash"},
                        "self_clean": {"mode": "self_clean"},
                        "fruit_wash": {"mode": "fruit_wash"},
                        "germ": {"mode": "germ"},
                        "seafood_wash": {"mode": "seafood_wash"},
                        "hotpot_wash": {"mode": "hotpot_wash"}
                    }
                },
                "additional": {
                    "defer_update": True,
                    "status_key": "additional",
                    "options": {
                        "none": {"additional": 0},
                        "extra_rinse_1": {"additional": 9},
                        "extra_rinse_2": {"additional": 10},
                        "few_dishes_rinse_1": {"additional": 13},
                        "few_dishes_rinse_2": {"additional": 14}
                    }
                }
            },
            Platform.SENSOR: {
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "softwater": {
                    "options": {
                        "1": {"softwater": 1},
                        "2": {"softwater": 2},
                        "3": {"softwater": 3},
                        "4": {"softwater": 4},
                        "5": {"softwater": 5}
                    },
                    "condition": {"not_eq": ["work_status", "work"]}
                },
                "left_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "remain_time"
                },
                "air_left_hour": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.HOURS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "wash_stage": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
