from homeassistant.const import Platform, UnitOfDensity, UnitOfRatio, UnitOfTemperature, PERCENTAGE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SENSOR: {
                "cube_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_temperature"
                },
                "cube_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_humidity"
                },
                "cube_arofene": {
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": UnitOfDensity.MILLIGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "hcho"
                },
                "cube_co2_value": {
                    "device_class": SensorDeviceClass.CO2,
                    "unit_of_measurement": UnitOfRatio.PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_co2"
                },
                "cube_pm25_value": {
                    "device_class": SensorDeviceClass.PM25,
                    "unit_of_measurement": UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "pm25"
                },
                "cube_tvoc": {
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "tvoc_density"
                }
            }
        }
    },
    "default_air_cube": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SENSOR: {
                "cube_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_temperature"
                },
                "cube_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_humidity"
                },
                "cube_arofene": {
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": UnitOfDensity.MILLIGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "hcho"
                },
                "cube_co2_value": {
                    "device_class": SensorDeviceClass.CO2,
                    "unit_of_measurement": UnitOfRatio.PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_co2"
                },
                "cube_pm25_value": {
                    "device_class": SensorDeviceClass.PM25,
                    "unit_of_measurement": UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "pm25"
                },
                "cube_tvoc": {
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "tvoc_density"
                }
            }
        }
    },
    "127PD075": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SENSOR: {
                "cube_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_temperature"
                },
                "cube_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_humidity"
                },
                "cube_arofene": {
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": UnitOfDensity.MILLIGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "hcho"
                },
                "cube_co2_value": {
                    "device_class": SensorDeviceClass.CO2,
                    "unit_of_measurement": UnitOfRatio.PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "indoor_co2"
                },
                "cube_pm25_value": {
                    "device_class": SensorDeviceClass.PM25,
                    "unit_of_measurement": UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "pm25"
                },
                "cube_tvoc": {
                    "device_class": SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
                    "unit_of_measurement": UnitOfDensity.MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "tvoc_density"
                }
            }
        }
    }
}
