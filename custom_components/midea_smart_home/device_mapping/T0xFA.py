from homeassistant.const import Platform
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "queries": [{}],
        "centralized": [],
        "entities": {
            Platform.SWITCH: {
                "display_on_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                    "translation_key": "screen_close",
                },
                "humidify": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["off", "1"],
                },
                "waterions": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "anion",
                }
            },
            Platform.FAN: {
                "fan": {
                    "power": "power",
                    "speeds": list({"gear": value + 1} for value in range(0, 3)),
                    "oscillate": "swing",
                    "preset_modes": {
                        "normal": {
                            "mode": "normal",
                            "speeds": list({"gear": value + 1} for value in range(0, 3))
                        },
                        "sleep": {
                            "mode": "sleep",
                            "speeds": list({"gear": value + 1} for value in range(0, 2))
                        },
                        "baby": {
                            "mode": "baby",
                            "speeds": list({"gear": value + 1} for value in range(0, 1))
                        }
                    }
                }
            },
            Platform.SENSOR: {
                "water_feedback": {
                    "device_class": SensorDeviceClass.ENUM,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
