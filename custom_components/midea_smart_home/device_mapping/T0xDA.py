from homeassistant.const import Platform, UnitOfTime
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.NUMBER: {
                "temperature": {
                    "min": 0,
                    "max": 100,
                    "step": 1
                },
                "detergent": {
                    "min": 0,
                    "max": 5,
                    "step": 1
                },
                "softener": {
                    "min": 0,
                    "max": 5,
                    "step": 1
                },
                "dehydration_speed": {
                    "min": 0,
                    "max": 1600,
                    "step": 100
                },
                "soak_time": {
                    "min": 0,
                    "max": 40,
                    "step": 10
                },
                "wash_time": {
                    "min": 0,
                    "max": 20,
                    "step": 1
                },
                "rinse_count": {
                    "min": 0,
                    "max": 3,
                    "step": 1
                },
                "dehydration_time": {
                    "min": 0,
                    "max": 9,
                    "step": 1
                },
                "wash_level": {
                    "min": 0,
                    "max": 8,
                    "step": 1
                },
                "rinse_level": {
                    "min": 0,
                    "max": 8,
                    "step": 1
                },
                "wash_strength": {
                    "min": 1,
                    "max": 4,
                    "step": 1
                }
            },
            Platform.BINARY_SENSOR: {
                "softener_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "detergent_lack": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "door_opened": {
                    "device_class": BinarySensorDeviceClass.OPENING
                },
                "bucket_water_overheating": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                }
            },
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "control_status": {
                    "rationale": ["pause", "start"]
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "normal": {"mode": "normal"},
                        "dry": {"mode": "dry"},
                        "continus": {"mode": "continus"},
                    }
                },
                "program": {
                    "options": {
                        "standard": {"program": "standard"},
                        "fast": {"program": "fast"},
                        "blanket": {"program": "blanket"},
                        "wool": {"program": "wool"},
                        "embathe": {"program": "embathe"},
                        "memory": {"program": "memory"},
                        "child": {"program": "child"},
                        "strong_wash": {"program": "strong_wash"},
                        "bucket_self_clean": {"program": "bucket_self_clean"},
                    }
                }
            },
            Platform.SENSOR: {
                "running_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "appointment_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
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
                }
            }
        }
    }
}
