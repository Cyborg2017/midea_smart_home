from homeassistant.const import Platform
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "display_on_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                },
                "humidify": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["off", "1"],
                },
                "waterions": {
                    "device_class": SwitchDeviceClass.SWITCH,
                }
            },
            Platform.FAN: {
                "fan": {
                    "power": "power",
                    "speeds": list({"gear": value + 1} for value in range(0, 12)),
                    "oscillate": "swing",
                    "preset_modes": {
                        "normal": {
                            "mode": "normal",
                            "speeds": list({"gear": value + 1} for value in range(0, 12))
                        },
                        "comfort": {
                            "mode": "comfort",
                            "speeds": list({"gear": value + 1} for value in range(0, 3))
                        },
                        "sleep": {
                            "mode": "sleep",
                            "speeds": list({"gear": value + 1} for value in range(0, 3))
                        },
                        "baby": {
                            "mode": "baby",
                            "speeds": list({"gear": value + 1} for value in range(0, 1))
                        },
                        "strong": {
                            "mode": "strong",
                            "speeds": [{"gear": 12}]
                        }
                    }
                }
            },
            Platform.SENSOR: {
                "water_feedback": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "default_fan": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "display_on_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"],
                },
                "humidify": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["off", "1"],
                },
                "waterions": {
                    "device_class": SwitchDeviceClass.SWITCH,
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
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "BGF10000": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.FAN: {
                "fan": {
                    "power": "power",
                    "speeds": list({"gear": value + 1} for value in range(0, 12)),
                    "oscillate": "swing",
                    "preset_modes": {
                        "normal": {
                            "mode": "normal",
                            "speeds": list({"gear": value + 1} for value in range(0, 12))
                        },
                        "comfort": {
                            "mode": "comfort",
                            "speeds": list({"gear": value + 1} for value in range(0, 3))
                        },
                        "sleep": {
                            "mode": "sleep",
                            "speeds": list({"gear": value + 1} for value in range(0, 3))
                        },
                        "strong": {
                            "mode": "strong",
                            "speeds": [{"gear": 12}]
                        }
                    }
                }
            }
        }
    },
    "56011C99": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "display_on_off": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["on", "off"]
                },
                "voice": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["close_buzzer", "open_buzzer"],
                    "translation_key": "buzzer"
                }
            },
            Platform.FAN: {
                "fan": {
                    "power": "power",
                    "speeds": list({"gear": value + 1} for value in range(0, 9)),
                    "oscillate": "lr_swing",
                    "preset_modes": {
                        "normal": {
                            "mode": "normal",
                            "speeds": list({"gear": value + 1} for value in range(0, 9))
                        },
                        "storm": {
                            "mode": "storm",
                            "speeds": [{"gear": 9}]
                        }
                    }
                }
            },
            Platform.SELECT: {
                "ud_swing": {
                    "options": {
                        "off": {"ud_swing": "off"},
                        "angle_30": {"ud_swing": "30"},
                        "angle_60": {"ud_swing": "60"},
                        "angle_135": {"ud_swing": "135"}
                    }
                }
            }
        }
    }
}
