from homeassistant.const import Platform, UnitOfTime, UnitOfArea
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.VACUUM: {
                "vacuum": {
                    "control": "work_status",
                    "fan_speeds": {
                        "status_key": "fan_level",
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
                    "status_key": "work_mode",
                    "options": {
                        "sweep_and_mop": {"work_mode_setting": {"work_mode": "sweep_and_mop"}},
                        "sweep": {"work_mode_setting": {"work_mode": "sweep"}},
                        "mop": {"work_mode_setting": {"work_mode": "mop"}},
                        "sweep_then_mop": {"work_mode_setting": {"work_mode": "sweep_then_mop"}}
                    }
                }
            },
            Platform.SENSOR: {
                "battery_percent": {
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                },
                "area": {
                    "device_class": SensorDeviceClass.AREA,
                    "unit_of_measurement": UnitOfArea.SQUARE_METERS,
                },
                "work_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                },
                "sub_work_status": {
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
    },
    "default_robot_cleaner": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.VACUUM: {
                "vacuum": {
                    "control": "work_status",
                    "fan_speeds": {
                        "status_key": "fan_level",
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
                    "status_key": "work_mode",
                    "options": {
                        "sweep_and_mop": {"work_mode_setting": {"work_mode": "sweep_and_mop"}},
                        "sweep": {"work_mode_setting": {"work_mode": "sweep"}},
                        "mop": {"work_mode_setting": {"work_mode": "mop"}},
                        "sweep_then_mop": {"work_mode_setting": {"work_mode": "sweep_then_mop"}}
                    }
                }
            },
            Platform.SENSOR: {
                "battery_percent": {
                    "device_class": SensorDeviceClass.BATTERY,
                    "unit_of_measurement": "%",
                },
                "area": {
                    "device_class": SensorDeviceClass.AREA,
                    "unit_of_measurement": UnitOfArea.SQUARE_METERS,
                },
                "work_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                },
                "sub_work_status": {
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
