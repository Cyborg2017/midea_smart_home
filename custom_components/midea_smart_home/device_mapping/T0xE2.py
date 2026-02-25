from homeassistant.const import Platform, UnitOfTemperature, UnitOfTime, PRECISION_WHOLE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "queries": [{}],
        "centralized": [],
        "calculate": {
            "get": [
                {
                    "lvalue": "[end_time]",
                    "rvalue": "[end_time_hour] * 60 + [end_time_minute]"
                }
            ],
            "set": {
            }
        },
        "entities": {
            Platform.WATER_HEATER: {
                "water_heater": {
                    "power": "power",
                    "operation_list": {
                        "off": {"power": "off"},
                        "heat": {"power": "on"},
                    },
                    "target_temperature": "temperature",
                    "current_temperature": "cur_temperature",
                    "min_temp": 30,
                    "max_temp": 75,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "protect": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "smart_sterilize": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "eplus": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "frequency_hot": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "temp_set"
                },
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "end_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "51001938": {
        "rationale": ["off", "on"],
        "queries": [{}],
        "centralized": [],
        "calculate": {
            "get": [
                {
                    "lvalue": "[end_time]",
                    "rvalue": "[end_time_hour] * 60 + [end_time_minute]"
                }
            ],
            "set": {
            }
        },
        "entities": {
            Platform.WATER_HEATER: {
                "water_heater": {
                    "power": "power",
                    "operation_list": {
                        "off": {"power": "off"},
                        "heat": {"power": "on"},
                    },
                    "target_temperature": "temperature",
                    "current_temperature": "cur_temperature",
                    "min_temp": 30,
                    "max_temp": 75,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "efficient": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "auto_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "frequency_hot": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "temp_set"
                },
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "end_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
