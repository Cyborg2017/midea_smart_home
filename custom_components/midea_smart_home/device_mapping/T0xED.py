from homeassistant.const import Platform, PERCENTAGE, UnitOfTemperature, UnitOfTime, UnitOfVolume, CONCENTRATION_PARTS_PER_MILLION
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

DEVICE_MAPPING = {
    "default": {
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
            Platform.BINARY_SENSOR: {
                "standby_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": [1, 0],
                    "translation_key": "water_output_switch"
                },
                "sleep": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "rationale": ["on", "off"],
                    "translation_key": "screen_status"
                },
                "lack_water": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                    "translation_key": "pure_water_status"
                },
                "out_water": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "out_ice": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "ice_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "ice_gall_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "filter": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                }
            },
            Platform.SWITCH: {
                "wash": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "antifreeze": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "heat": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
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
                },
                "ice": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "autoclean_remind": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "include_current": ["autoclean_remind_cycle"]
                },
                "drainage": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "autoclean_ctrl": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sleep": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                    "translation_key": "display_on_off"
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
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "out_tds": {
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
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
                "hot_pot_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "water_consumption_l": {
                    "device_class": SensorDeviceClass.WATER,
                    "unit_of_measurement": UnitOfVolume.LITERS,
                    "state_class": SensorStateClass.TOTAL
                },
                "current_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                }
            }
        }
    },
    "default_water_purifier": {
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
            Platform.BINARY_SENSOR: {
                "standby_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": [1, 0],
                    "translation_key": "water_output_switch"
                }
            },
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
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "out_tds": {
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
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
                "hot_pot_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                },
                "water_consumption_l": {
                    "device_class": SensorDeviceClass.WATER,
                    "unit_of_measurement": UnitOfVolume.LITERS,
                    "state_class": SensorStateClass.TOTAL
                }
            }
        }
    },
    "632009F5": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.BINARY_SENSOR: {
                "standby_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": [1, 0],
                    "translation_key": "water_output_switch"
                }
            },
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
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "out_tds": {
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
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
            Platform.BINARY_SENSOR: {
                "standby_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": [1, 0],
                    "translation_key": "water_output_switch"
                }
            },
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
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "out_tds": {
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
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
                },
                "sleep": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                    "translation_key": "display_on_off"
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
                },
                "set_germicidal_countdown_days": {
                    "options": {
                        "7": {"set_germicidal_countdown_days": 7},
                        "10": {"set_germicidal_countdown_days": 10},
                        "15": {"set_germicidal_countdown_days": 15},
                        "20": {"set_germicidal_countdown_days": 20},
                        "25": {"set_germicidal_countdown_days": 25},
                        "30": {"set_germicidal_countdown_days": 30}
                    },
                    "command": {"set_germicidal_countdown": "on"}
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
            Platform.BINARY_SENSOR: {
                "sleep": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "rationale": ["on", "off"],
                    "translation_key": "screen_status"
                },
                "out_water": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "heat_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING
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
    },
    "632009HD": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH
                }
            },
            Platform.SELECT: {
                "quantify_1": {
                    "options": {
                        "15": {"quantify_1": 15},
                        "20": {"quantify_1": 20},
                        "25": {"quantify_1": 25},
                        "30": {"quantify_1": 30},
                        "35": {"quantify_1": 35},
                        "40": {"quantify_1": 40},
                        "45": {"quantify_1": 45},
                        "50": {"quantify_1": 50},
                    },
                    "translation_key": "quantified_water_volume"
                },
                "plateau_boiling_point": {
                    "options": {
                        "81": {"plateau_boiling_point": 10},
                        "82": {"plateau_boiling_point": 20},
                        "83": {"plateau_boiling_point": 30},
                        "84": {"plateau_boiling_point": 40},
                        "85": {"plateau_boiling_point": 50},
                        "86": {"plateau_boiling_point": 60},
                        "87": {"plateau_boiling_point": 70},
                        "88": {"plateau_boiling_point": 80},
                        "89": {"plateau_boiling_point": 90},
                        "90": {"plateau_boiling_point": 100},
                        "91": {"plateau_boiling_point": 110},
                        "92": {"plateau_boiling_point": 120},
                        "93": {"plateau_boiling_point": 130},
                        "94": {"plateau_boiling_point": 140},
                        "95": {"plateau_boiling_point": 150},
                        "96": {"plateau_boiling_point": 160},
                        "97": {"plateau_boiling_point": 170},
                        "98": {"plateau_boiling_point": 180},
                        "99": {"plateau_boiling_point": 190},
                        "100": {"plateau_boiling_point": 0}
                    },
                    "command": {"plateau_power": "on"}
                }
            },
            Platform.NUMBER: {
                "milk_temperature": {
                    "min": 45,
                    "max": 50,
                    "step": 1,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS
                },
                "honey_temperature": {
                    "min": 50,
                    "max": 70,
                    "step": 1,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS
                },
                "tea_temperature": {
                    "min": 71,
                    "max": 85,
                    "step": 1,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS
                },
                "custom_temperature_1": {
                    "min": 86,
                    "max": 100,
                    "step": 1,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "translation_key": "boiling_water_temperature"
                }
            },
            Platform.BINARY_SENSOR: {
                "sleep": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "rationale": ["on", "off"],
                    "translation_key": "screen_status"
                }
            },
            Platform.SENSOR: {
                "current_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "cur_temperature"
                }
            }
        }
    },
    "6320084C": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "germicidal": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "lock": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "set_germicidal_countdown": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sleep": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                    "translation_key": "display_on_off"
                }
            },
            Platform.SELECT: {
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
                "custom_temperature_1": {
                    "options": {
                        "75": {"custom_temperature_1": 75},
                        "80": {"custom_temperature_1": 80},
                        "83": {"custom_temperature_1": 83},
                        "90": {"custom_temperature_1": 90},
                        "95": {"custom_temperature_1": 95}
                    },
                    "translation_key": "boiling_water_temperature"
                },
                "tea_temperature": {
                    "options": {
                        "75": {"tea_temperature": 75},
                        "80": {"tea_temperature": 80},
                        "83": {"tea_temperature": 83},
                        "90": {"tea_temperature": 90},
                        "95": {"tea_temperature": 95}
                    }
                },
                "custom_temperature_2": {
                    "options": {
                        "30": {"custom_temperature_2": 30},
                        "35": {"custom_temperature_2": 35},
                        "40": {"custom_temperature_2": 40},
                        "45": {"custom_temperature_2": 45},
                        "50": {"custom_temperature_2": 50},
                        "55": {"custom_temperature_2": 55},
                        "60": {"custom_temperature_2": 60}
                    },
                    "translation_key": "warm_water_temperature"
                },
                "milk_temperature": {
                    "options": {
                        "30": {"milk_temperature": 30},
                        "35": {"milk_temperature": 35},
                        "40": {"milk_temperature": 40},
                        "45": {"milk_temperature": 45},
                        "50": {"milk_temperature": 50},
                        "55": {"milk_temperature": 55},
                        "60": {"milk_temperature": 60}
                    }
                },
                "set_germicidal_countdown_days": {
                    "options": {
                        "7": {"set_germicidal_countdown_days": 7},
                        "10": {"set_germicidal_countdown_days": 10},
                        "15": {"set_germicidal_countdown_days": 15},
                        "20": {"set_germicidal_countdown_days": 20},
                        "25": {"set_germicidal_countdown_days": 25},
                        "30": {"set_germicidal_countdown_days": 30}
                    },
                    "command": {"set_germicidal_countdown": "on"}
                }
            },
            Platform.BINARY_SENSOR: {
                "sleep": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "rationale": ["on", "off"],
                    "translation_key": "screen_status"
                },
                "out_water": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "heat_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                }
            },
            Platform.SENSOR: {
                "germicidal_left_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "germicidal_countdown": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.DAYS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    },
    "default_net_drinking_machine": {
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
                "cool": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "ice": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "autoclean_remind": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "include_current": ["autoclean_remind_cycle"]
                },
                "drainage": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "autoclean_ctrl": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sleep": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                    "translation_key": "display_on_off"
                }
            },
            Platform.SELECT: {
                "cur_quantify": {
                    "options": {
                        "off_quantify": {"cur_quantify": 0},
                        "small_cup": {"cur_quantify": 3},
                        "medium_cup": {"cur_quantify": 4},
                        "large_cup": {"cur_quantify": 5}
                    }
                },
                "quantify_3": {
                    "options": {
                        "100": {"quantify_3": 10},
                        "150": {"quantify_3": 15},
                        "200": {"quantify_3": 20},
                        "250": {"quantify_3": 25}
                    },
                    "translation_key": "quantify_small_cup"
                },
                "quantify_4": {
                    "options": {
                        "300": {"quantify_4": 30},
                        "350": {"quantify_4": 35},
                        "400": {"quantify_4": 40},
                        "450": {"quantify_4": 45}
                    },
                    "translation_key": "quantify_medium_cup"
                },
                "quantify_5": {
                    "options": {
                        "500": {"quantify_5": 50},
                        "550": {"quantify_5": 55},
                        "600": {"quantify_5": 60}
                    },
                    "translation_key": "quantify_large_cup"
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
                },
                "autoclean_remind_cycle": {
                    "options": {
                        "7": {"autoclean_remind_cycle": 7},
                        "15": {"autoclean_remind_cycle": 15},
                        "30": {"autoclean_remind_cycle": 30},
                        "60": {"autoclean_remind_cycle": 60},
                        "90": {"autoclean_remind_cycle": 90}
                    },
                    "command": {"autoclean_remind": "on"}
                },
                "autoclean_time": {
                    "options": {
                        "5": {"autoclean_time": 5},
                        "10": {"autoclean_time": 10},
                        "15": {"autoclean_time": 15}
                    }
                }
            },
            Platform.NUMBER: {
                "custom_temperature_1": {
                    "min": 86,
                    "max": 98,
                    "step": 1,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "translation_key": "boiling_water_temperature"
                },
                "milk_temperature": {
                    "min": 40,
                    "max": 85,
                    "step": 1,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "translation_key": "warm_water_temperature"
                }
            },
            Platform.BINARY_SENSOR: {
                "sleep": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "rationale": ["on", "off"],
                    "translation_key": "screen_status"
                },
                "lack_water": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                    "translation_key": "pure_water_status"
                },
                "out_water": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "out_ice": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "ice_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "ice_gall_status": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                },
                "filter": {
                    "device_class": BinarySensorDeviceClass.RUNNING
                }
            },
            Platform.SENSOR: {
                "out_tds": {
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
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
                },
                "water_consumption_l": {
                    "device_class": SensorDeviceClass.WATER,
                    "unit_of_measurement": UnitOfVolume.LITERS,
                    "state_class": SensorStateClass.TOTAL
                },
                "autoclean_remind_cycle_remainder": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.DAYS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "autoclean_time_remainder": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
