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
    }
}
