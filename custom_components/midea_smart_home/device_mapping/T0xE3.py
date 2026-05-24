from homeassistant.const import Platform, UnitOfTemperature, PRECISION_WHOLE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.WATER_HEATER: {
                "water_heater": {
                    "power": "power",
                    "operation_list": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "shower"}
                    },
                    "target_temperature": "temperature",
                    "current_temperature": "out_water_tem",
                    "min_temp": 32,
                    "max_temp": 65,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_master": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_dot": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_pressure": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "cold_water_conservation": {
                    "options": {
                        "off": {"cold_water_conservation": "off"},
                        "on": {"cold_water_conservation": "on"}
                    }
                }
            },
            Platform.SENSOR: {
                "out_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "return_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "in_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "temp_set"
                }
            },
            Platform.BINARY_SENSOR: {
                "feedback": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                }
            }
        }
    },
    "default_gas_water_heater": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.WATER_HEATER: {
                "water_heater": {
                    "power": "power",
                    "operation_list": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "shower"}
                    },
                    "target_temperature": "temperature",
                    "current_temperature": "out_water_tem",
                    "min_temp": 32,
                    "max_temp": 65,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_master": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_dot": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_pressure": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "cold_water_conservation": {
                    "options": {
                        "off": {"cold_water_conservation": "off"},
                        "on": {"cold_water_conservation": "on"}
                    }
                }
            },
            Platform.SENSOR: {
                "out_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "return_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "in_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "temp_set"
                }
            },
            Platform.BINARY_SENSOR: {
                "feedback": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                }
            }
        }
    },
    "5110186B": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.WATER_HEATER: {
                "water_heater": {
                    "power": "power",
                    "operation_list": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "shower"}
                    },
                    "target_temperature": "temperature",
                    "current_temperature": "out_water_tem",
                    "min_temp": 32,
                    "max_temp": 65,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_master": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_dot": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_pressure": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "change_litre_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "cold_water_conservation": {
                    "options": {
                        "off": {"cold_water_conservation": "off"},
                        "on": {"cold_water_conservation": "on"}
                    }
                },
                "mode": {
                    "translation_key": "e3_mode",
                    "options": {
                        "shower": {"mode": "shower"},
                        "kitchen": {"mode": "kitchen"},
                        "high_temperature": {"mode": "high_temperature"}
                    }
                }
            },
            Platform.SENSOR: {
                "out_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "return_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "in_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "temp_set"
                }
            },
            Platform.BINARY_SENSOR: {
                "feedback": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                }
            }
        }
    }
}
