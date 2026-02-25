from homeassistant.const import Platform, UnitOfTime, UnitOfArea
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "queries": [
            {"query_type": "work"}
        ],
        "centralized": ["work_status", "battery_percent", "sweep_mop_mode", "mop", "sub_work_status"],
        "entities": {
            Platform.VACUUM: {
                "vacuum": {
                    "battery_level": "battery_percent",
                    "control": "work_status",
                    "fan_speeds": {
                        "soft": {"fan_setting": {"level": "soft"}},
                        "normal": {"fan_setting": {"level": "normal"}},
                        "high": {"fan_setting": {"level": "high"}}
                    },
                    "control_actions": {
                        "start": "work",
                        "stop": "stop",
                        "pause": "pause",
                        "return": "charge"
                    }
                }
            },
            Platform.SELECT: {
                "sweep_mop_mode": {
                    "options": {
                        "sweep_and_mop": {"work_mode_setting": {"work_mode": "sweep_and_mop"}},
                        "sweep": {"work_mode_setting": {"work_mode": "sweep"}},
                        "mop": {"work_mode_setting": {"work_mode": "mop"}},
                        "sweep_then_mop": {"work_mode_setting": {"work_mode": "sweep_then_mop"}}
                    }
                }
            },
            Platform.BINARY_SENSOR: {
                "is_charging": {
                    "device_class": BinarySensorDeviceClass.BATTERY_CHARGING,
                    "on_value": ["charging"],
                    "off_value": ["work", "stop", "pause", "on_base"]
                }
            },
            Platform.SENSOR: {
                "battery_percent": {
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "voice_level": {
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "area": {
                    "device_class": SensorDeviceClass.AREA,
                    "unit_of_measurement": UnitOfArea.SQUARE_METERS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "work_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "dust_count": {
                    "device_class": SensorDeviceClass.ENUM,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "sweep_then_mop_mode_progress": {
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "sub_work_status": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "mop": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "sweep_mop_mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "work_status": {
                    "device_class": SensorDeviceClass.ENUM,
                }
            }
        }
    }
}
