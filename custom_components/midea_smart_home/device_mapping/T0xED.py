from homeassistant.const import Platform, PERCENTAGE
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
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "life_2": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
