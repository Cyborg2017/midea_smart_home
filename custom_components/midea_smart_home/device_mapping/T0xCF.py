from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "control_type": "0x11",
        "initial_query": [{"0x11"}, {"0x12"}],
        "polling_query": [{"0x11"}, {"0x12"}],
        "entities": {
            Platform.CLIMATE: {
                "thermostat_1": {
                    "power": "thermostat_power_state1",
                    "hvac_modes": {
                        "off": {"thermostat_power_state1": "off"},
                        "auto": {"thermostat_power_state1": "on"},
                    },
                    "preset_modes": {
                        "none": {"thermostat_power_state1": "off"},
                        "heat": {
                            "thermostat_power_state1": "on",
                            "mode_set1": "2",
                        },
                        "cool": {
                            "thermostat_power_state1": "on",
                            "mode_set1": "1",
                        },
                        "fan_only": {
                            "thermostat_power_state1": "on",
                            "mode_set1": "0",
                        },
                        "ground": {
                            "thermostat_power_state1": "on",
                            "mode_set1": "3",
                        },
                        "heat_ground": {
                            "thermostat_power_state1": "on",
                            "mode_set1": "4",
                        },
                    },
                    "fan_modes": {
                        "auto": {"fan_level_set1": "0"},
                        "low": {"fan_level_set1": "1"},
                        "medium": {"fan_level_set1": "2"},
                        "high": {"fan_level_set1": "3"}
                    },
                    "target_temperature": "temp_set1",
                    "current_temperature": "room_temp1",
                    "pre_mode": "mode_set1",
                    "min_temp": 5,
                    "max_temp": 70,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                },
                "thermostat_2": {
                    "power": "thermostat_power_state2",
                    "hvac_modes": {
                        "off": {"thermostat_power_state2": "off"},
                        "auto": {"thermostat_power_state2": "on"},
                    },
                    "preset_modes": {
                        "none": {"thermostat_power_state2": "off"},
                        "heat": {
                            "thermostat_power_state2": "on",
                            "mode_set2": "2",
                        },
                        "cool": {
                            "thermostat_power_state2": "on",
                            "mode_set2": "1",
                        },
                        "fan_only": {
                            "thermostat_power_state2": "on",
                            "mode_set2": "0",
                        },
                        "ground": {
                            "thermostat_power_state2": "on",
                            "mode_set2": "3",
                        },
                        "heat_ground": {
                            "thermostat_power_state2": "on",
                            "mode_set2": "4",
                        },
                    },
                    "fan_modes": {
                        "auto": {"fan_level_set2": "0"},
                        "low": {"fan_level_set2": "1"},
                        "medium": {"fan_level_set2": "2"},
                        "high": {"fan_level_set2": "3"}
                    },
                    "target_temperature": "temp_set2",
                    "current_temperature": "room_temp2",
                    "pre_mode": "mode_set2",
                    "min_temp": 5,
                    "max_temp": 70,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                },
                "thermostat_3": {
                    "power": "thermostat_power_state3",
                    "hvac_modes": {
                        "off": {"thermostat_power_state3": "off"},
                        "auto": {"thermostat_power_state3": "on"},
                    },
                    "preset_modes": {
                        "none": {"thermostat_power_state3": "off"},
                        "heat": {
                            "thermostat_power_state3": "on",
                            "mode_set3": "2",
                        },
                        "cool": {
                            "thermostat_power_state3": "on",
                            "mode_set3": "1",
                        },
                        "fan_only": {
                            "thermostat_power_state3": "on",
                            "mode_set3": "0",
                        },
                        "ground": {
                            "thermostat_power_state3": "on",
                            "mode_set3": "3",
                        },
                        "heat_ground": {
                            "thermostat_power_state3": "on",
                            "mode_set3": "4",
                        },
                    },
                    "fan_modes": {
                        "auto": {"fan_level_set3": "0"},
                        "low": {"fan_level_set3": "1"},
                        "medium": {"fan_level_set3": "2"},
                        "high": {"fan_level_set3": "3"}
                    },
                    "target_temperature": "temp_set3",
                    "current_temperature": "room_temp3",
                    "pre_mode": "mode_set3",
                    "min_temp": 5,
                    "max_temp": 70,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                },
                "thermostat_4": {
                    "power": "thermostat_power_state4",
                    "hvac_modes": {
                        "off": {"thermostat_power_state4": "off"},
                        "auto": {"thermostat_power_state4": "on"},
                    },
                    "preset_modes": {
                        "none": {"thermostat_power_state4": "off"},
                        "heat": {
                            "thermostat_power_state4": "on",
                            "mode_set4": "2",
                        },
                        "cool": {
                            "thermostat_power_state4": "on",
                            "mode_set4": "1",
                        },
                        "fan_only": {
                            "thermostat_power_state4": "on",
                            "mode_set4": "0",
                        },
                        "ground": {
                            "thermostat_power_state4": "on",
                            "mode_set4": "3",
                        },
                        "heat_ground": {
                            "thermostat_power_state4": "on",
                            "mode_set4": "4",
                        },
                    },
                    "fan_modes": {
                        "auto": {"fan_level_set4": "0"},
                        "low": {"fan_level_set4": "1"},
                        "medium": {"fan_level_set4": "2"},
                        "high": {"fan_level_set4": "3"}
                    },
                    "target_temperature": "temp_set4",
                    "current_temperature": "room_temp4",
                    "pre_mode": "mode_set4",
                    "min_temp": 5,
                    "max_temp": 70,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                },
                "thermostat_5": {
                    "power": "thermostat_power_state5",
                    "hvac_modes": {
                        "off": {"thermostat_power_state5": "off"},
                        "auto": {"thermostat_power_state5": "on"},
                    },
                    "preset_modes": {
                        "none": {"thermostat_power_state5": "off"},
                        "heat": {
                            "thermostat_power_state5": "on",
                            "mode_set5": "2",
                        },
                        "cool": {
                            "thermostat_power_state5": "on",
                            "mode_set5": "1",
                        },
                        "fan_only": {
                            "thermostat_power_state5": "on",
                            "mode_set5": "0",
                        },
                        "ground": {
                            "thermostat_power_state5": "on",
                            "mode_set5": "3",
                        },
                        "heat_ground": {
                            "thermostat_power_state5": "on",
                            "mode_set5": "4",
                        },
                    },
                    "fan_modes": {
                        "auto": {"fan_level_set5": "0"},
                        "low": {"fan_level_set5": "1"},
                        "medium": {"fan_level_set5": "2"},
                        "high": {"fan_level_set5": "3"}
                    },
                    "target_temperature": "temp_set5",
                    "current_temperature": "room_temp5",
                    "pre_mode": "mode_set5",
                    "min_temp": 5,
                    "max_temp": 70,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                },
            },
            Platform.SWITCH: {
                "energysaving_state1": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "sleep_state1": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "energysaving_state2": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "sleep_state2": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "energysaving_state3": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "sleep_state3": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "energysaving_state4": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "sleep_state4": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "energysaving_state5": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "sleep_state5": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "mode_set1": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "room_temp1": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temp_set1": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "mode_set2": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "room_temp2": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temp_set2": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "mode_set3": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "room_temp3": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temp_set3": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "mode_set4": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "room_temp4": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temp_set4": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "mode_set5": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "room_temp5": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temp_set5": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "00000M33": {
        "rationale": ["off", "on"],
        "initial_query": [{}],
        "polling_query": [{}],
        "control_type": "1",
        "entities": {
            Platform.CLIMATE: {
                "floor_heating": {
                    "power": "power_state",
                    "hvac_modes": {
                        "off": {"power_state": "off"},
                        "heat": {"power_state": "on", "run_mode": "heat"},
                        "cool": {"power_state": "on", "run_mode": "cool"},
                        "auto": {"power_state": "on", "run_mode": "auto"},
                    },
                    "target_temperature": "temp_set",
                    "current_temperature": "cur_temp",
                    "min_temp": 5,
                    "max_temp": 55,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": 1
                }
            },
            Platform.SWITCH: {
                "silence_set_state": {
                    "control_key": "silence_function_state",
                    "command": {"control_type": "5"},
                }
            },
            Platform.SENSOR: {
                "cur_temp": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "temp_set": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
