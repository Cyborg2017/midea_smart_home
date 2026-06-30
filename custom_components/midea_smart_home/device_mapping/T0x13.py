from homeassistant.const import Platform, UnitOfTime

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.LIGHT: {
                "light": {
                    "power": "power",
                    "brightness": {"brightness": [1, 100]},
                    "color_temp": {
                        "color_temperature": {
                            "kelvin_range": [3000, 5700],
                            "device_range": [0, 100]
                        }
                    },
                    "preset_modes": {
                        "moon": {"scene_light": "moon"},
                        "read": {"scene_light": "read"},
                        "mild": {"scene_light": "mild"},
                        "life": {"scene_light": "life"},
                        "film": {"scene_light": "film"},
                        "manual": {"scene_light": "manual"}
                    }
                }
            },
            Platform.SELECT: {
                "link_age_model": {
                    "options": {
                        "breath": {"link_age_model": "breath"},
                        "blink": {"link_age_model": "blink"},
                        "discolor": {"link_age_model": "discolor"}
                    }
                }
            },
            Platform.NUMBER: {
                "delay_light_off": {
                    "min": 0,
                    "max": 60,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            }
        }
    },
    "default_lamp": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.LIGHT: {
                "light": {
                    "power": "power",
                    "brightness": {"brightness": [1, 100]},
                    "color_temp": {
                        "color_temperature": {
                            "kelvin_range": [3000, 5700],
                            "device_range": [0, 100]
                        }
                    },
                    "preset_modes": {
                        "moon": {"scene_light": "moon"},
                        "read": {"scene_light": "read"},
                        "mild": {"scene_light": "mild"},
                        "life": {"scene_light": "life"},
                        "film": {"scene_light": "film"},
                        "manual": {"scene_light": "manual"}
                    }
                }
            },
            Platform.SELECT: {
                "link_age_model": {
                    "options": {
                        "breath": {"link_age_model": "breath"},
                        "blink": {"link_age_model": "blink"},
                        "discolor": {"link_age_model": "discolor"}
                    }
                }
            },
            Platform.NUMBER: {
                "delay_light_off": {
                    "min": 0,
                    "max": 60,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            }
        }
    },
    "M0200002": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.LIGHT: {
                "light": {
                    "power": "power",
                    "brightness": {"brightness": [1, 100]},
                    "color_temp": {
                        "color_temperature": {
                            "kelvin_range": [3000, 5700],
                            "device_range": [0, 100]
                        }
                    },
                    "preset_modes": {
                        "moon": {"scene_light": "moon"},
                        "read": {"scene_light": "read"},
                        "mild": {"scene_light": "mild"},
                        "life": {"scene_light": "life"},
                        "film": {"scene_light": "film"},
                        "manual": {"scene_light": "manual"}
                    }
                }
            },
            Platform.SELECT: {
                "link_age_model": {
                    "options": {
                        "breath": {"link_age_model": "breath"},
                        "blink": {"link_age_model": "blink"},
                        "discolor": {"link_age_model": "discolor"}
                    }
                }
            },
            Platform.NUMBER: {
                "delay_light_off": {
                    "min": 0,
                    "max": 60,
                    "step": 1,
                    "unit_of_measurement": UnitOfTime.MINUTES
                }
            }
        }
    },
    "default_fan_light": {
        "rationale": ["off", "on"],
        "queries": [{}],
        "centralized": [],
        "entities": {
            Platform.LIGHT: {
                "light": {
                    "power": "led_power",
                    "brightness": {"brightness": [1, 100]},
                    "color_temp": {
                        "color_temperature": {
                            "kelvin_range": [2700, 6500],
                            "device_range": [0, 100]
                        }
                    },
                    "preset_modes": {
                        "work": {"led_scene_light": "work"},
                        "eating": {"led_scene_light": "eating"},
                        "film": {"led_scene_light": "film"},
                        "night": {"led_scene_light": "night"},
                        "ledmanual": {"led_scene_light": "ledmanual"}
                    }
                }
            },
            Platform.FAN: {
                "fan": {
                    "power": "fan_power",
                    "speeds": list({"fan_speed": str(value)} for value in [1, 21, 41, 61, 81, 100]),
                    "directions": {
                        "forward": {"arround_dir": "1"},
                        "reverse": {"arround_dir": "0"}
                    },
                    "preset_modes": {
                        "fanmanual": {"fan_scene": "fanmanual"},
                        "const_temperature": {"fan_scene": "const_temperature"},
                        "baby_wind": {"fan_scene": "baby_wind"},
                        "sleep_wind": {"fan_scene": "sleep_wind"},
                        "forest_wind": {"fan_scene": "forest_wind"}
                    }
                }
            }
        }
    },
    "M0200015": {
        "rationale": ["off", "on"],
        "queries": [{}],
        "centralized": [],
        "entities": {
            Platform.LIGHT: {
                "light": {
                    "power": "led_power",
                    "brightness": {"brightness": [1, 100]},
                    "color_temp": {
                        "color_temperature": {
                            "kelvin_range": [2700, 6500],
                            "device_range": [0, 100]
                        }
                    },
                    "preset_modes": {
                        "work": {"led_scene_light": "work"},
                        "eating": {"led_scene_light": "eating"},
                        "film": {"led_scene_light": "film"},
                        "night": {"led_scene_light": "night"},
                        "ledmanual": {"led_scene_light": "ledmanual"}
                    }
                }
            },
            Platform.FAN: {
                "fan": {
                    "power": "fan_power",
                    "speeds": list({"fan_speed": str(value)} for value in [1, 21, 41, 61, 81, 100]),
                    "directions": {
                        "forward": {"arround_dir": "1"},
                        "reverse": {"arround_dir": "0"}
                    },
                    "preset_modes": {
                        "fanmanual": {"fan_scene": "fanmanual"},
                        "const_temperature": {"fan_scene": "const_temperature"},
                        "baby_wind": {"fan_scene": "baby_wind"},
                        "sleep_wind": {"fan_scene": "sleep_wind"},
                        "forest_wind": {"fan_scene": "forest_wind"}
                    }
                }
            }
        }
    }
}
