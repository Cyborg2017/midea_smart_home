from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "calculate": {
            "get": [
                {
                    "lvalue": "[water_gage_bar]",
                    "rvalue": "float([water_gage] / 10.0)"
                }
            ],
        },
        "entities": {
            Platform.WATER_HEATER: {
                "bath_water_heater": {
                    "translation_key": "bath_water_heater",
                    "power": "power",
                    "operation_list": {
                        "off": {"power": "off"},
                        "normal": {"bath_mode": 0},
                        "smart_temp": {"bath_mode": 10}
                    },
                    "target_temperature": "current_bath_set_temperature",
                    "current_temperature": "bath_out_water_temperature",
                    "min_temp": 35,
                    "max_temp": 60,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.CLIMATE: {
                "heating": {
                    "translation_key": "heating",
                    "power": "heating_work",
                    "hvac_modes": {
                        "off": {"winter_mode": "off", "summer_mode":"on"},
                        "heat": {"winter_mode": "on", "summer_mode": "off"}
                    },
                    "preset_modes": {
                        "normal": {"heat_mode": 0},
                        "smart_away": {"heat_mode": 1},
                        "smart_home": {"heat_mode": 2}
                    },
                    "target_temperature": ["current_heat_set_temperature"],
                    "current_temperature": "heat_out_water_temperature",
                    "min_temp": 30,
                    "max_temp": 80,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SENSOR: {
                "fan_type": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "ignitor_output": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "fan_output": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "current_heat_set_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "current_bath_set_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "heat_out_water_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "bath_out_water_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "water_gage_bar": {
                    "device_class": SensorDeviceClass.PRESSURE,
                    "unit_of_measurement": UnitOfPressure.BAR,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            },
            Platform.BINARY_SENSOR: {
                "heating_work": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "bathing_work": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                }
            }
        }
    },
    "default_gas_all_hanging_tove": {
        "rationale": ["off", "on"],
        "calculate": {
            "get": [
                {
                    "lvalue": "[water_gage_bar]",
                    "rvalue": "float([water_gage] / 10.0)"
                }
            ],
        },
        "entities": {
            Platform.WATER_HEATER: {
                "bath_water_heater": {
                    "translation_key": "bath_water_heater",
                    "power": "power",
                    "operation_list": {
                        "off": {"power": "off"},
                        "normal": {"bath_mode": 0},
                        "smart_temp": {"bath_mode": 10}
                    },
                    "target_temperature": "current_bath_set_temperature",
                    "current_temperature": "bath_out_water_temperature",
                    "min_temp": 35,
                    "max_temp": 60,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.CLIMATE: {
                "heating": {
                    "translation_key": "heating",
                    "power": "heating_work",
                    "hvac_modes": {
                        "off": {"winter_mode": "off", "summer_mode":"on"},
                        "heat": {"winter_mode": "on", "summer_mode": "off"}
                    },
                    "preset_modes": {
                        "normal": {"heat_mode": 0},
                        "smart_away": {"heat_mode": 1},
                        "smart_home": {"heat_mode": 2}
                    },
                    "target_temperature": ["current_heat_set_temperature"],
                    "current_temperature": "heat_out_water_temperature",
                    "min_temp": 30,
                    "max_temp": 80,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SENSOR: {
                "fan_type": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "ignitor_output": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "fan_output": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "current_heat_set_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "current_bath_set_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "heat_out_water_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "bath_out_water_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "water_gage_bar": {
                    "device_class": SensorDeviceClass.PRESSURE,
                    "unit_of_measurement": UnitOfPressure.BAR,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            },
            Platform.BINARY_SENSOR: {
                "heating_work": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "bathing_work": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                }
            }
        }
    }
}
