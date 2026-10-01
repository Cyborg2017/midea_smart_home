from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [{}],
        "calculate": {
            "get": [
                {
                    "lvalue": "[temperature]",
                    "rvalue": "float(([set_temperature] - 106) / 74 * 37 + 38)"
                },
                {
                    "lvalue": "[cur_temperature]",
                    "rvalue": "float(([water_box_temperature] - 106) / 74 * 37 + 38)"
                }
            ],
            "set": [
                {
                    "lvalue": "[set_temperature]",
                    "rvalue": "float(([temperature] - 38) / 37 * 74 + 106)"
                }
            ]
        },
        "entities": {
            Platform.WATER_HEATER: {
                "water_heater": {
                    "power": "power",
                    "operation_list": {
                        "off": {"power": "off"},
                        "heat": {"power": "on"}
                    },
                    "target_temperature": "temperature",
                    "current_temperature": "cur_temperature",
                    "min_temp": 38,
                    "max_temp": 75,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_WHOLE
                }
            },
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "mute": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "standard": {"mode": "standard"},
                        "energy": {"mode": "energy"},
                        "compatibilizing": {"mode": "compatibilizing"}
                    }
                }
            },
            Platform.SENSOR: {
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
