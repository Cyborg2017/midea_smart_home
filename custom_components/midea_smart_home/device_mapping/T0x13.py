from homeassistant.const import Platform, UnitOfTime

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "queries": [{}],
        "centralized": [],
        "entities": {
            Platform.LIGHT: {
                "light": {
                    "power": "power",
                    "brightness": {"brightness": [0, 255]},
                    "color_temp": {
                        "color_temperature": {
                            "kelvin_range": [2700, 6500],
                            "device_range": [0, 255]
                        }
                    },
                    "preset_modes": {
                        "night": {"scene_light": "night"},
                        "read": {"scene_light": "read"},
                        "mild": {"scene_light": "mild"},
                        "life": {"scene_light": "life"},
                        "film": {"scene_light": "film"},
                        "manual": {"scene_light": "manual"},
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
