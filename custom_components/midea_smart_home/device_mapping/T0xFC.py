from homeassistant.const import Platform, UnitOfTemperature, PERCENTAGE, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.NUMBER: {
                "hosting_upper": {
                    "min": 10,
                    "max": 75,
                    "step": 1
                },
                "hosting_lower": {
                    "min": 10,
                    "max": 75,
                    "step": 1
                }
            },
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "waterions":{
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "manual": {"mode": "manual"},
                        "sleep": {"mode": "sleep"},
                        "auto": {"mode": "auto"},
                        "air_dry": {"mode": "air_dry"}
                    }
                },
                "bias_gear":{
                    "options": {
                        "none": {"bias_gear": 4},
                        "conversation_scene": {"bias_gear": -10},
                        "yoga_scene": {"bias_gear": -20}
                    },
                    "command": {
                        "mode": "auto",
                        "sub_mode": "denoise"
                    }
                },
                "bright": {
                    "options": {
                        "full": {"bright": 0},
                        "half": {"bright": 6},
                        "off": {"bright": 7}
                    }
                },
                "gear": {
                    "options": {
                        "low": {"wind_speed": 1},
                        "medium": {"wind_speed": 2},
                        "high": {"wind_speed": 3}
                    }
                }
            },
            Platform.SENSOR: {
                "deep_filter_percent": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temperature_feedback": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "humidify_feedback": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_humidity"
                },
                "hcho":{
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,

                },
                "pm1":{
                    "device_class": SensorDeviceClass.PM1,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,

                },
                "pm25":{
                    "device_class": SensorDeviceClass.PM25,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "pm10":{
                    "device_class": SensorDeviceClass.PM10,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,

                }
            }
        }
    },
    "default_air_purifier": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.NUMBER: {
                "hosting_upper": {
                    "min": 10,
                    "max": 75,
                    "step": 1
                },
                "hosting_lower": {
                    "min": 10,
                    "max": 75,
                    "step": 1
                }
            },
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "waterions":{
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "manual": {"mode": "manual"},
                        "sleep": {"mode": "sleep"},
                        "auto": {"mode": "auto"},
                        "air_dry": {"mode": "air_dry"}
                    }
                },
                "bias_gear":{
                    "options": {
                        "none": {"bias_gear": 4},
                        "conversation_scene": {"bias_gear": -10},
                        "yoga_scene": {"bias_gear": -20}
                    },
                    "command": {
                        "mode": "auto",
                        "sub_mode": "denoise"
                    }
                },
                "bright": {
                    "options": {
                        "full": {"bright": 0},
                        "half": {"bright": 6},
                        "off": {"bright": 7}
                    }
                },
                "gear": {
                    "options": {
                        "low": {"wind_speed": 1},
                        "medium": {"wind_speed": 2},
                        "high": {"wind_speed": 3}
                    }
                }
            },
            Platform.SENSOR: {
                "deep_filter_percent": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "temperature_feedback": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "humidify_feedback": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_humidity"
                },
                "hcho":{
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,

                },
                "pm1":{
                    "device_class": SensorDeviceClass.PM1,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,

                },
                "pm25":{
                    "device_class": SensorDeviceClass.PM25,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "pm10":{
                    "device_class": SensorDeviceClass.PM10,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,

                }
            }
        }
    }
}
