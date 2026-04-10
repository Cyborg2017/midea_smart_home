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
                },
                "wash_stage": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
