from homeassistant.const import Platform, UnitOfTemperature, CONCENTRATION_PARTS_PER_MILLION, \
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "queries": [{}],
        "centralized": [],
        "calculate": {
            "get": [
                {
                    "lvalue": "[indoor_temperature]",
                    "rvalue": "float([temperature]) / 10"
                },
            ],
        },
        "entities": {
            Platform.SENSOR: {
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "co2_value": {
                    "device_class": SensorDeviceClass.CO2,
                    "unit_of_measurement": CONCENTRATION_PARTS_PER_MILLION,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "pm10_value": {
                    "device_class": SensorDeviceClass.PM10,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "pm25_value": {
                    "device_class": SensorDeviceClass.PM25,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "voltage": {
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "battery_level"
                },
            }
        }
    }
}
