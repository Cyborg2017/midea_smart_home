from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [{}],
        "entities": {
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SELECT: {
                "mode_state": {
                    "options": {
                        "passby": {"mode_state": "passby"},
                        "auto": {"mode_state": "auto"},
                        "manual": {"mode_state": "manual"},
                        "sleep": {"mode_state": "sleep"},
                        "energy_save": {"mode_state": "energy_save"},
                        "ultimate": {"mode_state": "ultimate"}
                    }
                },
                "fan_set": {
                    "options": {
                        "off": {"fan_set": "0"},
                        "low": {"fan_set": "1"},
                        "medium": {"fan_set": "2"},
                        "high": {"fan_set": "3"},
                        "auto": {"fan_set": "4"}
                    }
                }
            },
            Platform.SENSOR: {
                "room_temp_value": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_temperature"
                },
                "tvoc_value": {
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": "mg/m³",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "tvoc_density"
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "room_aqi_value": {
                    "device_class": SensorDeviceClass.AQI,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "humidity_value": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_humidity"
                },
                "hcho_value": {
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": "mg/m³",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "hcho"
                },
                "pm25_value": {
                    "device_class": SensorDeviceClass.PM25,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "pm25"
                },
                "co2_value": {
                    "device_class": SensorDeviceClass.CO2,
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_co2"
                }
            }
        }
    }
}
