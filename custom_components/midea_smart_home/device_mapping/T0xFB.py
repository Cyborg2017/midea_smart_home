from homeassistant.const import Platform, UnitOfTemperature, PRECISION_WHOLE, UnitOfPower
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.SWITCH: {
                "auto_power_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "humidification": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ['off', 'no_change'],
                },
                "screen_close": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ['on', 'off'],
                    "translation_key": "display_on_off"
                },
                "voice": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ['close_buzzer', 'open_buzzer'],
                    "translation_key": "buzzer"
                }
            },
            Platform.CLIMATE: {
                "electric_heater": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on"}
                    },
                    "preset_modes": {
                        "full_off": {"gear": 0},
                        "left_warm": {"gear": 1},
                        "right_warm": {"gear": 2},
                        "full_on": {"gear": 3}
                    },
                    "target_temperature": "temperature",
                    "current_temperature": "cur_temperature",
                    "min_temp": 5,
                    "max_temp": 35,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE,
                }
            },
            Platform.SENSOR: {
                "power_statistics": {
                    "device_class": SensorDeviceClass.POWER,
                    "unit_of_measurement": UnitOfPower.WATT,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_heater": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.SWITCH: {
                "auto_power_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "humidification": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ['off', 'no_change'],
                },
                "screen_close": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ['on', 'off'],
                    "translation_key": "display_on_off"
                },
                "voice": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ['close_buzzer', 'open_buzzer'],
                    "translation_key": "buzzer"
                }
            },
            Platform.CLIMATE: {
                "electric_heater": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on"}
                    },
                    "preset_modes": {
                        "full_off": {"gear": 0},
                        "left_warm": {"gear": 1},
                        "right_warm": {"gear": 2},
                        "full_on": {"gear": 3}
                    },
                    "target_temperature": "temperature",
                    "current_temperature": "cur_temperature",
                    "min_temp": 5,
                    "max_temp": 35,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE,
                }
            },
            Platform.SENSOR: {
                "power_statistics": {
                    "device_class": SensorDeviceClass.POWER,
                    "unit_of_measurement": UnitOfPower.WATT,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
