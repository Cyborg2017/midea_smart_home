from homeassistant.const import Platform, UnitOfTemperature, UnitOfTime, PERCENTAGE
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.components.humidifier import HumidifierDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "queries": [{}],
        "centralized": [],
        "entities": {
            Platform.SWITCH: {
                "buzzer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "voice",
                },
                "airDry_on_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "airdry_on_off",
                },
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "power_on_timer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "power_off_timer": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.BINARY_SENSOR: {
                "add_water_flag": {
                    "device_class": BinarySensorDeviceClass.PROBLEM,
                }
            },
            Platform.HUMIDIFIER: {
                "humidifier": {
                    "device_class": HumidifierDeviceClass.HUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 30,
                    "max_humidity": 80,
                    "mode": "humidity_mode",
                    "modes": {
                        "manual": {"humidity_mode": "manual"},
                        "auto": {"humidity_mode": "auto"},
                        "sleep": {"humidity_mode": "sleep"}
                    }
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
                "running_percent": {
                    "device_class": SensorDeviceClass.POWER_FACTOR,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
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
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "time_on": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "time_off": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
