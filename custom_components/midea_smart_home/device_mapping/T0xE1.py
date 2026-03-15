from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import Platform, UnitOfTemperature, UnitOfTime, PERCENTAGE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default_dishwasher": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
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
                },
                "wash_stage": {
                    "device_class": BinarySensorDeviceClass.RUNNING
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
                        "power_on": {"work_status": "power_on"},
                        "cancel": {"work_status": "cancel"},
                        "pause": {"operator": "pause"},
                        "resume": {"operator": "start"}
                    }
                },
                "wash_mode": {
                    "options": {
                        "neutral_gear": {"work_status": "cancel", "mode": "neutral_gear"},
                        "strong_wash": {"work_status": "work", "mode": "strong_wash"},
                        "standard_wash": {"work_status": "work", "mode": "standard_wash"},
                        "single_disinfect": {"work_status": "work", "mode": "single_disinfect"},
                        "eco_wash": {"work_status": "work", "mode": "eco_wash"},
                        "glass_wash": {"work_status": "work", "mode": "glass_wash"},
                        "fast_wash": {"work_status": "work", "mode": "fast_wash"},
                        "soak_wash": {"work_status": "work", "mode": "soak_wash"},
                        "self_clean": {"work_status": "work", "mode": "self_clean"},
                        "fruit_wash": {"work_status": "work", "mode": "fruit_wash"},
                        "germ": {"work_status": "work", "mode": "germ"},
                        "seafood_wash": {"work_status": "work", "mode": "seafood_wash"},
                        "hotpot_wash": {"work_status": "work", "mode": "hotpot_wash"}
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
                    "device_class": SensorDeviceClass.ENUM
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
                }
            }
        }
    },
    "76006450": {
        "rationale": ["off", "on"],
        "initial_query": [{}],
        "centralized": [],
        "entities": {
            Platform.BINARY_SENSOR: {
                "water_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                    "on_value": [1],
                    "off_value": [0],
                },
                "bright_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                    "on_value": [1],
                    "off_value": [0],
                },
                "softwater_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                    "on_value": [1],
                    "off_value": [0],
                },
            },
            Platform.SWITCH: {
                "work_status": {
                    "translation_key": "control_status",
                    "rationale": ["cancel", "work"],
                },
                "lock": {},
                "dryswitch": {
                    "translation_key": "dry",
                    "rationale": [0, 1],
                },
                "more_dry": {
                    "translation_key": "strong_flash_dry",
                    "rationale": [0, 1],
                },
                "uvswitch": {
                    "rationale": [0, 1],
                },
                "door_auto_open": {
                    "rationale": [0, 1],
                },
            },
            Platform.SELECT: {
                "work_status": {
                    "translation_key": "dishwasher_work_status_control",
                    "options": {
                        "power_off": {"work_status": "power_off"},
                        "power_on": {"work_status": "power_on"},
                        "cancel": {"work_status": "cancel"},
                        "pause": {"operator": "pause"},
                        "resume": {"operator": "start"},
                    },
                },
                "mode": {
                    "translation_key": "dishwasher_mode",
                    "options": {
                        "auto_wash": {"mode": "auto_wash"},
                        "strong_wash": {"mode": "strong_wash"},
                        "standard_wash": {"mode": "standard_wash"},
                        "eco_wash": {
                            "mode": "eco_wash",
                            "additional": 0,
                            "wash_region": 3,
                        },
                        "gentle_wash": {"mode": "glass_wash"},
                        "fast_wash": {"mode": "fast_wash"},
                        "pre_rinse": {"mode": "soak_wash"},
                        "self_clean": {"mode": "self_clean"},
                        "fruit_wash": {"mode": "fruit_wash"},
                        "germ": {"mode": "germ"},
                        "storage": {"mode": "single_dry"},
                        "seafood_wash": {"mode": "seafood_wash"},
                        "hotpot_wash": {"mode": "hotpot_wash"},
                        "quietnight_wash": {"mode": "quietnight_wash"},
                        "less_wash": {"mode": "less_wash"},
                        "oilnet_wash": {"mode": "oilnet_wash"},
                        "single_disinfect": {"mode": "single_disinfect"},
                    },
                },
                "wash_region": {
                    "translation_key": "dishwasher_wash_region",
                    "options": {
                        "upper": {"wash_region": 1, "additional": 0},
                        "lower": {"wash_region": 2, "additional": 0},
                        "upper_lower": {"wash_region": 3, "additional": 0},
                        "lower_zone_strong": {"wash_region": 2, "additional": 1},
                        "zone_strong": {"wash_region": 0, "additional": 1},
                    },
                },
            },
            Platform.NUMBER: {
                "air_set_hour": {
                    "translation_key": "dishwasher_storage_duration",
                    "min": 0,
                    "max": 168,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.HOURS,
                    "mode": "box",
                },
            },
            Platform.SENSOR: {
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "translation_key": "dishwasher_work_status",
                },
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                    "translation_key": "dishwasher_mode",
                },
                "left_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "air_left_hour": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.HOURS,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "dry_set_min": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM,
                },
            },
        },
    }
}
