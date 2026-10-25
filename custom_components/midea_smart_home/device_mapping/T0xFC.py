from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.FAN: {
                "fan": {
                    "translation_key": "air_purifier",
                    "power": "power",
                    "speeds": list({"wind_speed": value + 1} for value in range(0, 3)),
                    "preset_modes": {
                        "auto": {
                            "mode": "auto"
                        },
                        "air_dry": {
                            "mode": "air_dry"
                        },
                        "fast": {
                            "mode": "fast"
                        },
                        "manual": {
                            "mode": "manual",
                            "speeds": list({"wind_speed": value + 1} for value in range(0, 3))
                        },
                        "sleep": {
                            "mode": "sleep"
                        }
                    }
                }
            },
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.NUMBER: {
                "hosting_upper": {
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box",
                    "mode": "box"
                },
                "hosting_lower": {
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box",
                    "mode": "box"
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
                },
                "hosting": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SELECT: {
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
                },
                "purifying_rate":{
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tvoc":{
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "tvoc_density"
                }
            }
        }
    },
    "default_air_purifier": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.FAN: {
                "fan": {
                    "translation_key": "air_purifier",
                    "power": "power",
                    "speeds": list({"wind_speed": value + 1} for value in range(0, 3)),
                    "preset_modes": {
                        "auto": {
                            "mode": "auto",
                        },
                        "air_dry": {
                            "mode": "air_dry"
                        },
                        "fast": {
                            "mode": "fast"
                        },
                        "manual": {
                            "mode": "manual",
                            "speeds": list({"wind_speed": value + 1} for value in range(0, 3))
                        },
                        "sleep": {
                            "mode": "sleep"
                        }
                    }
                }
            },
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.NUMBER: {
                "hosting_upper": {
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box"
                },
                "hosting_lower": {
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box"
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
                },
                "hosting": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SELECT: {
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
                },
                "purifying_rate":{
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tvoc":{
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "tvoc_density"
                }
            }
        }
    },
    "571Z3081": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.FAN: {
                "fan": {
                    "translation_key": "air_purifier",
                    "power": "power",
                    "speeds": list({"wind_speed": value + 1} for value in range(0, 3)),
                    "preset_modes": {
                        "auto": {
                            "mode": "auto"
                        },
                        "air_dry": {
                            "mode": "air_dry"
                        },
                        "manual": {
                            "mode": "manual",
                            "speeds": list({"wind_speed": value + 1} for value in range(0, 3))
                        },
                        "sleep": {
                            "mode": "sleep"
                        }
                    }
                }
            },
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.NUMBER: {
                "hosting_upper": {
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box"
                },
                "hosting_lower": {
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box"
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
    "571Z306N": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.FAN: {
                "fan": {
                    "translation_key": "air_purifier",
                    "power": "power",
                    "speeds": list({"wind_speed": value + 1} for value in range(0, 99)),
                    "preset_modes": {
                        "sleep": {
                            "mode": "sleep"
                        },
                        "fast": {
                            "mode": "fast"
                        },
                        "auto": {
                            "mode": "auto",
                            "hosting": "on"
                        },
                        "manual": {
                            "mode": "manual",
                            "speeds": list({"wind_speed": value + 1} for value in range(0, 12))
                        }
                    }
                }
            },
            Platform.LOCK: {
                "lock": {
                    "translation_key": "child_lock"
                }
            },
            Platform.NUMBER: {
                "hosting_upper": {
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box"
                },
                "hosting_lower": {
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box"
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
                    "translation_key": "anion"
                }
            },
            Platform.SELECT: {
                "bright": {
                    "options": {
                        "full": {"bright": 0},
                        "half": {"bright": 6},
                        "off": {"bright": 7}
                    }
                }
            },
            Platform.SENSOR: {
                "deep_filter_percent": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "pm25":{
                    "device_class": SensorDeviceClass.PM25,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "purifying_rate":{
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tvoc":{
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "tvoc_density"
                }
            }
        }
    }
}
