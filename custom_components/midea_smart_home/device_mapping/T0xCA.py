from homeassistant.const import Platform, UnitOfTemperature, PRECISION_WHOLE, PERCENTAGE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default_fridge": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "storage_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "freezing_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "preservation_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "storage_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "freezing_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "deep_cold_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "open_door_tips_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.BINARY_SENSOR: {
                "storage_door_state": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                },
                "freezer_door_state": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                }
            },
            Platform.CLIMATE: {
                "storage_zone": {
                    "power": "storage_power",
                    "hvac_modes": {
                        "off": {"storage_power": "off"},
                        "cool": {"storage_power": "on"}
                    },
                    "target_temperature": "storage_temperature",
                    "current_temperature": "refrigeration_real_temperature",
                    "pre_mode": "mode",
                    "min_temp": 2,
                    "max_temp": 8,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                },
                "freezing_zone": {
                    "power": "freezing_power",
                    "hvac_modes": {
                        "off": {"freezing_power": "off"},
                        "cool": {"freezing_power": "on"}
                    },
                    "target_temperature": "freezing_temperature",
                    "current_temperature": "freezing_real_temperature",
                    "min_temp": -24,
                    "max_temp": -16,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SELECT: {
                "flexzone_function": {
                    "options": {
                        "zero_degree": {"left_flexzone_temperature": "0", "right_flexzone_temperature": "0"},
                        "treasure": {"left_flexzone_temperature": "3", "right_flexzone_temperature": "3"},
                        "mother_baby": {"left_flexzone_temperature": "4", "right_flexzone_temperature": "4"}
                    }
                },
                "dsp_sterilization_mode": {
                    "options": {
                        "daily_mode": {"electronic_clean_strong": "off"},
                        "strong_mode": {"electronic_clean_strong": "on"}
                    }
                },
                "ice_making_function": {
                    "options": {
                        "off": {"freezing_ice_machine_power": "off", "rapid_ice_making": "off"},
                        "rapid_ice_making": {"freezing_ice_machine_power": "on", "rapid_ice_making": "on"},
                        "normal_ice_making": {"freezing_ice_machine_power": "on", "rapid_ice_making": "off"}
                    }
                },
                "open_door_warning_time": {
                    "options": {
                        "30": {"open_door_warning_time": "3"},
                        "40": {"open_door_warning_time": "4"},
                        "50": {"open_door_warning_time": "5"},
                        "60": {"open_door_warning_time": "6"},
                        "70": {"open_door_warning_time": "7"},
                        "80": {"open_door_warning_time": "8"},
                        "90": {"open_door_warning_time": "9"},
                        "100": {"open_door_warning_time": "10"},
                        "110": {"open_door_warning_time": "11"},
                        "120": {"open_door_warning_time": "12"},
                        "130": {"open_door_warning_time": "13"},
                        "140": {"open_door_warning_time": "14"},
                        "150": {"open_door_warning_time": "15"},
                        "160": {"open_door_warning_time": "16"},
                        "170": {"open_door_warning_time": "17"},
                        "180": {"open_door_warning_time": "18"},
                        "190": {"open_door_warning_time": "19"},
                        "200": {"open_door_warning_time": "20"},
                        "210": {"open_door_warning_time": "21"},
                        "220": {"open_door_warning_time": "22"},   
                        "230": {"open_door_warning_time": "23"},
                        "240": {"open_door_warning_time": "24"},
                        "250": {"open_door_warning_time": "25"},
                        "260": {"open_door_warning_time": "26"},
                        "270": {"open_door_warning_time": "27"},
                        "280": {"open_door_warning_time": "28"},
                        "290": {"open_door_warning_time": "29"},
                        "300": {"open_door_warning_time": "30"}
                    }
                }
            },
            Platform.SENSOR: {
                "storage_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "freezing_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "refrigeration_real_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "freezing_real_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "310A0808": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "storage_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "freezing_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "storage_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "freezing_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "intelligent_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.BINARY_SENSOR: {
                "storage_door_state": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                },
                "freezer_door_state": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                }
            },
            Platform.CLIMATE: {
                "storage_zone": {
                    "power": "storage_power",
                    "hvac_modes": {
                        "off": {"storage_power": "off"},
                        "cool": {"storage_power": "on"}
                    },
                    "target_temperature": "storage_temperature",
                    "current_temperature": "refrigeration_real_temperature",
                    "pre_mode": "mode",
                    "min_temp": 2,
                    "max_temp": 8,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                },
                "freezing_zone": {
                    "power": "freezing_power",
                    "hvac_modes": {
                        "off": {"freezing_power":    "off"},
                        "cool": {"freezing_power": "on"}
                    },
                    "target_temperature": "freezing_temperature",
                    "current_temperature": "freezing_real_temperature",
                    "min_temp": -24,
                    "max_temp": -16,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SENSOR: {
                "storage_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "freezing_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "refrigeration_real_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "freezing_real_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "310A1700": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "storage_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "freezing_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "storage_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "freezing_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "deep_cold_mode": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "freezing_light_open_chose": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "open_door_tips_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.BINARY_SENSOR: {
                "storage_door_state": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                },
                "freezer_door_state": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                }
            },
            Platform.CLIMATE: {
                "storage_zone": {
                    "power": "storage_power",
                    "hvac_modes": {
                        "off": {"storage_power": "off"},
                        "cool": {"storage_power": "on"}
                    },
                    "target_temperature": "storage_temperature",
                    "current_temperature": "refrigeration_real_temperature",
                    "pre_mode": "mode",
                    "min_temp": 2,
                    "max_temp": 8,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                },
                "freezing_zone": {
                    "power": "freezing_power",
                    "hvac_modes": {
                        "off": {"freezing_power": "off"},
                        "cool": {"freezing_power": "on"}
                    },
                    "target_temperature": "freezing_temperature",
                    "current_temperature": "freezing_real_temperature",
                    "min_temp": -24,
                    "max_temp": -16,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SELECT: {
                "flexzone_function": {
                    "options": {
                        "zero_degree": {"left_flexzone_temperature": "0"},
                        "treasure": {"left_flexzone_temperature": "2"},
                        "mother_baby": {"left_flexzone_temperature": "6"}
                    }
                },
                "ice_making_function": {
                    "options": {
                        "off": {"freezing_ice_machine_power": "off", "rapid_ice_making": "off"},
                        "rapid_ice_making": {"freezing_ice_machine_power": "on", "rapid_ice_making": "on"},
                        "normal_ice_making": {"freezing_ice_machine_power": "on", "rapid_ice_making": "off"}
                    }
                }
            },
            Platform.SENSOR: {
                "storage_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "freezing_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "refrigeration_real_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "freezing_real_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "left_flexzone_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "flexzone_temperature"
                },
                "left_variable_real_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "flexzone_real_temperature"
                }
            }
        }
    }
}
