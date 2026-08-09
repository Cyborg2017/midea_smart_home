from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import Platform, UnitOfTime

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.COVER: {
                "updown": {
                    "open_value": "up",
                    "close_value": "down",
                    "stop_value": "pause",
                }
            },
            Platform.NUMBER: {
                "custom_height": {
                    "min": 0,
                    "max": 100,
                    "step": 10,
                    "mode": "box"
                },
                "custom_timing": {
                    "min": 0,
                    "max": 180,
                    "step": 5,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            },
            Platform.LIGHT: {
                "common_light": {
                    "power": "light",
                    "brightness": {"light_brightness": [20, 100]}
                }
            },
            Platform.SWITCH: {
                "laundry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "offline_voice_function": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "location_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "default_laundry_rack": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.COVER: {
                "updown": {
                    "open_value": "up",
                    "close_value": "down",
                    "stop_value": "pause",
                }
            },
            Platform.NUMBER: {
                "custom_height": {
                    "min": 0,
                    "max": 100,
                    "step": 10,
                    "mode": "box"
                },
                "custom_timing": {
                    "min": 0,
                    "max": 180,
                    "step": 5,
                    "mode": "box",
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            },
            Platform.LIGHT: {
                "common_light": {
                    "power": "light",
                    "brightness": {"light_brightness": [20, 100]}
                }
            },
            Platform.SWITCH: {
                "laundry": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "offline_voice_function": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.SENSOR: {
                "location_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
