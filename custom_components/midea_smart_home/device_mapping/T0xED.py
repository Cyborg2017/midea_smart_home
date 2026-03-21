from homeassistant.const import Platform, PERCENTAGE, UnitOfTemperature, UnitOfTime, UnitOfVolume
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default_water_purifier": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "wash": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SELECT: {
                "no_obsolete_water": {
                    "options": {
                        "water_saving": {"no_obsolete_water": "off", "save_mode": "on"},
                        "water_quality": {"no_obsolete_water": "on", "save_mode": "off"}
                    }
                },
                "cur_quantify": {
                    "options": {
                        "off_quantify": {"cur_quantify": 0},
                        "small_amount": {"cur_quantify": 21},
                        "normal_amount": {"cur_quantify": 22},
                        "large_amount": {"cur_quantify": 23},
                    }
                },
                "first_custom_out_water_ml_0": {
                    "options": {
                        "none": {"first_custom_out_water_mode": 1},
                        "500": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 500},
                        "600": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 600},
                        "700": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 700},
                        "800": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 800},
                        "900": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 900},
                        "1000": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 1000},
                        "1250": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 1250},
                        "1500": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 1500},
                        "1750": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 1750},
                        "2000": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 2000},
                        "2250": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 2250},
                        "2500": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 2500},
                        "3000": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 3000},
                        "3500": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 3500},
                        "4000": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 4000},
                        "4500": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 4500},
                        "5000": {"first_custom_out_water_mode": 0, "first_custom_out_water_ml": 5000}
                    }
                },
                "first_custom_out_water_ml_1": {
                    "options": {
                        "none": {"first_custom_out_water_mode": 0},
                        "500": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 500},
                        "600": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 600},
                        "700": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 700},
                        "800": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 800},
                        "900": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 900},
                        "1000": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 1000},
                        "1250": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 1250},
                        "1500": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 1500},
                        "1750": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 1750},
                        "2000": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 2000},
                        "2250": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 2250},
                        "2500": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 2500},
                        "3000": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 3000},
                        "3500": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 3500},
                        "4000": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 4000},
                        "4500": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 4500},
                        "5000": {"first_custom_out_water_mode": 1, "first_custom_out_water_ml": 5000}
                    }
                }
            },
            Platform.NUMBER: {
                "quantify_21": {
                    "min": 500,
                    "max": 5000,
                    "step": 500,
                    "unit_of_measurement": "mL"
                },
                "quantify_22": {
                    "min": 500,
                    "max": 5000,
                    "step": 500,
                    "unit_of_measurement": "mL"
                },
                "quantify_23": {
                    "min": 500,
                    "max": 5000,
                    "step": 500,
                    "unit_of_measurement": "mL"
                }
            },
            Platform.SENSOR: {
                "in_tds": {
                    "unit_of_measurement": "mg/L",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "out_tds": {
                    "unit_of_measurement": "mg/L",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "life_1": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "life_pcb"
                },
                "life_2": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "life_ro"
                }
            }
        }
    },
    "632009F5": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "wash": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "antifreeze": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "heat": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "no_obsolete_water": {
                    "options": {
                        "water_saving": {"no_obsolete_water": "off", "save_mode": "on"},
                        "water_quality": {"no_obsolete_water": "on", "save_mode": "off"}
                    }
                },
                "hydration_setting": {
                    "options": {
                        "empty": {"hydration_setting": 1},
                        "half": {"hydration_setting": 2},
                        "full": {"hydration_setting": 3}
                    }
                }
            },
            Platform.NUMBER: {
                "quantify_21": {
                    "min": 300,
                    "max": 500,
                    "step": 100,
                    "unit_of_measurement": "mL"
                },
                "quantify_22": {
                    "min": 500,
                    "max": 1000,
                    "step": 100,
                    "unit_of_measurement": "mL"
                },
                "quantify_23": {
                    "min": 1000,
                    "max": 1500,
                    "step": 100,
                    "unit_of_measurement": "mL"
                }
            },
            Platform.SENSOR: {
                "in_tds": {
                    "unit_of_measurement": "mg/L",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "out_tds": {
                    "unit_of_measurement": "mg/L",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "life_1": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "life_ro"
                },
                "life_2": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "life_pcb"
                },
                "hot_pot_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                }
            }
        }
    },
    "632009G9": {
        "rationale": ["off", "on"],
        "calculate": {
            "get": [
                {
                    "lvalue": "[water_consumption_l]",
                    "rvalue": "float([water_consumption] / 1000.0)"
                }
            ],
        },
        "entities": {
            Platform.SWITCH: {
                "wash": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SELECT: {
                "no_obsolete_water": {
                    "options": {
                        "water_saving": {"no_obsolete_water": "off", "save_mode": "on"},
                        "water_quality": {"no_obsolete_water": "on", "save_mode": "off"}
                    }
                },
                "cur_quantify": {
                    "options": {
                        "off_quantify": {"cur_quantify": 0},
                        "small_amount": {"cur_quantify": 21},
                        "normal_amount": {"cur_quantify": 22},
                        "large_amount": {"cur_quantify": 23},
                    }
                }
            },
            Platform.NUMBER: {
                "quantify_21": {
                    "min": 300,
                    "max": 1000,
                    "step": 100,
                    "unit_of_measurement": "mL"
                },
                "quantify_22": {
                    "min": 1100,
                    "max": 1900,
                    "step": 100,
                    "unit_of_measurement": "mL"
                },
                "quantify_23": {
                    "min": 2000,
                    "max": 5000,
                    "step": 500,
                    "unit_of_measurement": "mL"
                }
            },
            Platform.SENSOR: {
                "in_tds": {
                    "unit_of_measurement": "mg/L",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "out_tds": {
                    "unit_of_measurement": "mg/L",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "life_1": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "life_ro"
                },
                "life_2": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "life_pcb"
                },
                "maxlife_1": {
                    "unit_of_measurement": "mths",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "max_life_ro"
                },
                "maxlife_2": {
                    "unit_of_measurement": "mths",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "max_life_pcb"
                },
                "water_consumption_l": {
                    "device_class": SensorDeviceClass.WATER,
                    "unit_of_measurement": UnitOfVolume.LITERS,
                    "state_class": SensorStateClass.TOTAL
                }
            }
        }
    },
    "default_pipeline_machine": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "germicidal": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "drainage": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "cool": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "human_sensing_switch": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "set_germicidal_countdown": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SELECT: {
                "cur_quantify": {
                    "options": {
                        "off_quantify": {"cur_quantify": 0},
                        "small_amount": {"cur_quantify": 1},
                        "normal_amount": {"cur_quantify": 2},
                        "large_amount": {"cur_quantify": 3},
                    }
                },
                "quantify_1": {
                    "options": {
                        "50": {"quantify_1": 5},
                        "100": {"quantify_1": 10},
                        "150": {"quantify_1": 15},
                        "200": {"quantify_1": 20},
                        "250": {"quantify_1": 25},
                        "300": {"quantify_1": 30}
                    }
                },
                "quantify_2": {
                    "options": {
                        "150": {"quantify_2": 15},
                        "200": {"quantify_2": 20},
                        "250": {"quantify_2": 25},
                        "300": {"quantify_2": 30},
                        "400": {"quantify_2": 40},
                        "500": {"quantify_2": 50}
                    }
                },
                "quantify_3": {
                    "options": {
                        "300": {"quantify_3": 30},
                        "400": {"quantify_3": 40},
                        "500": {"quantify_3": 50},
                        "600": {"quantify_3": 60},
                        "700": {"quantify_3": 70}
                    }
                },
                "screenout_time": {
                    "options": {
                        "10": {"screenout_time": 10},
                        "30": {"screenout_time": 30},
                        "60": {"screenout_time": 60},
                        "120": {"screenout_time": 120},
                        "180": {"screenout_time": 180},
                        "300": {"screenout_time": 300}
                    }
                }
            },
            Platform.NUMBER: {
                "custom_temperature_1": {
                    "min": 35,
                    "max": 95,
                    "step": 5,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS
                }
            },
            Platform.SENSOR: {
                "germicidal_left_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "current_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "germicidal_countdown": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.DAYS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
