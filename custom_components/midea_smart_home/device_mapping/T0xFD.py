from homeassistant.const import Platform, UnitOfTemperature, UnitOfTime, PERCENTAGE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "airDry_on_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "airdry_on_off"
                },
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "humidity_mode": {
                    "options": {
                        "manual": {"humidity_mode": "manual"},
                        "auto": {"humidity_mode": "auto"},
                        "sleep": {"humidity_mode": "sleep"}
                    }
                },
                "wind_speed": {
                    "options": {
                        "low": {"wind_speed": "low"},
                        "middle": {"wind_speed": "middle"},
                        "high": {"wind_speed": "high"}
                    }
                }
            },
            Platform.SENSOR: {
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "air_dry_left_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_air_humidifier": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "airDry_on_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "airdry_on_off"
                },
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "humidity_mode": {
                    "options": {
                        "manual": {"humidity_mode": "manual"},
                        "auto": {"humidity_mode": "auto"},
                        "sleep": {"humidity_mode": "sleep"}
                    }
                },
                "wind_speed": {
                    "options": {
                        "low": {"wind_speed": "low"},
                        "middle": {"wind_speed": "middle"},
                        "high": {"wind_speed": "high"}
                    }
                }
            },
            Platform.SENSOR: {
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "air_dry_left_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "202Z3119": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "airDry_on_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "airdry_on_off"
                },
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "light_color": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["off", "warm"]
                }
            },
            Platform.SELECT: {
                "humidity_mode": {
                    "options": {
                        "manual": {"humidity_mode": "manual"},
                        "moist_skin": {"humidity_mode": "moist_skin"},
                        "sleep": {"humidity_mode": "sleep"}
                    }
                },
                "wind_speed": {
                    "options": {
                        "low": {"wind_speed": "low"},
                        "middle": {"wind_speed": "middle"},
                        "high": {"wind_speed": "high"}
                    }
                },
                "bright_led": {
                    "options": {
                        "exit": {"bright_led": "exit"},
                        "dark": {"bright_led": "dark"},
                        "light": {"bright_led": "light"}
                    }
                }
            },
            Platform.SENSOR: {
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "air_dry_left_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
