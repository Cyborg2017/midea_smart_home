from homeassistant.components.humidifier import HumidifierDeviceClass
from homeassistant.const import Platform, PERCENTAGE, UnitOfTemperature
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "polling_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "entities": {
            Platform.LOCK: {
                "child_lock": {}
            },
            Platform.SWITCH: {
                "anion": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "wind_swing_ud": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "purifier": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "display_on_off"
                },
                "self_clean": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sound": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "buzzer"
                },
                "water_pump": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                }
            },
            Platform.HUMIDIFIER: {
                "dehumidifier": {
                    "device_class": HumidifierDeviceClass.DEHUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 35,
                    "max_humidity": 85,
                    "target_humidity_step": 5,
                    "mode": "mode",
                    "modes": {
                        "continuity": {"mode": "continuity"},
                        "dry_clothes": {"mode": "dry_clothes"},
                        "auto": {"mode": "auto"},
                        "eco": {"mode": "eco"},
                        "set": {"mode": "set"}
                    }
                }
            },
            Platform.TEXT: {
                "external_humidity_sensor": {}
            },
            Platform.SELECT: {
                "wind_speed": {
                    "options": {
                        "silent": {"wind_speed": 20},
                        "low": {"wind_speed": 40},
                        "comfort": {"wind_speed": 60},
                        "high": {"wind_speed": 80},
                        "strong": {"wind_speed": 100}
                    },
                },
                "power_on_time": {
                     "options": {
                        "off": {"power_on_timer": "off"},
                        "30": {"power_on_timer": "on", "power_on_time_value": 30},
                        "60": {"power_on_timer": "on", "power_on_time_value": 60},
                        "90": {"power_on_timer": "on", "power_on_time_value": 90},
                        "120": {"power_on_timer": "on", "power_on_time_value": 120},
                        "150": {"power_on_timer": "on", "power_on_time_value": 150},
                        "180": {"power_on_timer": "on", "power_on_time_value": 180},
                        "210": {"power_on_timer": "on", "power_on_time_value": 210},
                        "240": {"power_on_timer": "on", "power_on_time_value": 240},
                        "270": {"power_on_timer": "on", "power_on_time_value": 270},
                        "300": {"power_on_timer": "on", "power_on_time_value": 300},
                        "330": {"power_on_timer": "on", "power_on_time_value": 330},
                        "360": {"power_on_timer": "on", "power_on_time_value": 360},
                        "390": {"power_on_timer": "on", "power_on_time_value": 390},
                        "420": {"power_on_timer": "on", "power_on_time_value": 420},
                        "450": {"power_on_timer": "on", "power_on_time_value": 450},
                        "480": {"power_on_timer": "on", "power_on_time_value": 480},
                        "510": {"power_on_timer": "on", "power_on_time_value": 510},
                        "540": {"power_on_timer": "on", "power_on_time_value": 540},
                        "570": {"power_on_timer": "on", "power_on_time_value": 570},
                        "600": {"power_on_timer": "on", "power_on_time_value": 600},
                        "660": {"power_on_timer": "on", "power_on_time_value": 660},
                        "720": {"power_on_timer": "on", "power_on_time_value": 720},
                        "780": {"power_on_timer": "on", "power_on_time_value": 780},
                        "840": {"power_on_timer": "on", "power_on_time_value": 840},
                        "900": {"power_on_timer": "on", "power_on_time_value": 900},
                        "960": {"power_on_timer": "on", "power_on_time_value": 960},
                        "1020": {"power_on_timer": "on", "power_on_time_value": 1020},
                        "1080": {"power_on_timer": "on", "power_on_time_value": 1080},
                        "1140": {"power_on_timer": "on", "power_on_time_value": 1140},
                        "1200": {"power_on_timer": "on", "power_on_time_value": 1200},
                        "1260": {"power_on_timer": "on", "power_on_time_value": 1260},
                        "1320": {"power_on_timer": "on", "power_on_time_value": 1320},
                        "1380": {"power_on_timer": "on", "power_on_time_value": 1380},
                        "1440": {"power_on_timer": "on", "power_on_time_value": 1440}
                    }
                },
                "power_off_time": {
                    "options": {
                        "off": {"power_off_timer": "off"},
                        "30": {"power_off_timer": "on", "power_off_time_value": 30},
                        "60": {"power_off_timer": "on", "power_off_time_value": 60},
                        "90": {"power_off_timer": "on", "power_off_time_value": 90},
                        "120": {"power_off_timer": "on", "power_off_time_value": 120},
                        "150": {"power_off_timer": "on", "power_off_time_value": 150},
                        "180": {"power_off_timer": "on", "power_off_time_value": 180},
                        "210": {"power_off_timer": "on", "power_off_time_value": 210},
                        "240": {"power_off_timer": "on", "power_off_time_value": 240},
                        "270": {"power_off_timer": "on", "power_off_time_value": 270},
                        "300": {"power_off_timer": "on", "power_off_time_value": 300},
                        "330": {"power_off_timer": "on", "power_off_time_value": 330},
                        "360": {"power_off_timer": "on", "power_off_time_value": 360},
                        "390": {"power_off_timer": "on", "power_off_time_value": 390},
                        "420": {"power_off_timer": "on", "power_off_time_value": 420},
                        "450": {"power_off_timer": "on", "power_off_time_value": 450},
                        "480": {"power_off_timer": "on", "power_off_time_value": 480},
                        "510": {"power_off_timer": "on", "power_off_time_value": 510},
                        "540": {"power_off_timer": "on", "power_off_time_value": 540},
                        "570": {"power_off_timer": "on", "power_off_time_value": 570},
                        "600": {"power_off_timer": "on", "power_off_time_value": 600},
                        "660": {"power_off_timer": "on", "power_off_time_value": 660},
                        "720": {"power_off_timer": "on", "power_off_time_value": 720},
                        "780": {"power_off_timer": "on", "power_off_time_value": 780},
                        "840": {"power_off_timer": "on", "power_off_time_value": 840},
                        "900": {"power_off_timer": "on", "power_off_time_value": 900},
                        "960": {"power_off_timer": "on", "power_off_time_value": 960},
                        "1020": {"power_off_timer": "on", "power_off_time_value": 1020},
                        "1080": {"power_off_timer": "on", "power_off_time_value": 1080},
                        "1140": {"power_off_timer": "on", "power_off_time_value": 1140},
                        "1200": {"power_off_timer": "on", "power_off_time_value": 1200},
                        "1260": {"power_off_timer": "on", "power_off_time_value": 1260},
                        "1320": {"power_off_timer": "on", "power_off_time_value": 1320},
                        "1380": {"power_off_timer": "on", "power_off_time_value": 1380},
                        "1440": {"power_off_timer": "on", "power_off_time_value": 1440}
                    }
                }
            },
            Platform.SENSOR: {
                "water_full_level": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "default_dehumidifier": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "polling_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "entities": {
            Platform.LOCK: {
                "child_lock": {}
            },
            Platform.SWITCH: {
                "anion": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "wind_swing_ud": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "purifier": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "display_on_off"
                },
                "self_clean": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sound": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "buzzer"
                },
                "water_pump": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                }
            },
            Platform.HUMIDIFIER: {
                "dehumidifier": {
                    "device_class": HumidifierDeviceClass.DEHUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 35,
                    "max_humidity": 85,
                    "target_humidity_step": 5,
                    "mode": "mode",
                    "modes": {
                        "continuity": {"mode": "continuity"},
                        "dry_clothes": {"mode": "dry_clothes"},
                        "auto": {"mode": "auto"},
                        "eco": {"mode": "eco"},
                        "set": {"mode": "set"}
                    }
                }
            },
            Platform.TEXT: {
                "external_humidity_sensor": {}
            },
            Platform.SELECT: {
                "wind_speed": {
                    "options": {
                        "silent": {"wind_speed": 20},
                        "low": {"wind_speed": 40},
                        "comfort": {"wind_speed": 60},
                        "high": {"wind_speed": 80},
                        "strong": {"wind_speed": 100}
                    },
                },
                "power_on_time": {
                     "options": {
                        "off": {"power_on_timer": "off"},
                        "30": {"power_on_timer": "on", "power_on_time_value": 30},
                        "60": {"power_on_timer": "on", "power_on_time_value": 60},
                        "90": {"power_on_timer": "on", "power_on_time_value": 90},
                        "120": {"power_on_timer": "on", "power_on_time_value": 120},
                        "150": {"power_on_timer": "on", "power_on_time_value": 150},
                        "180": {"power_on_timer": "on", "power_on_time_value": 180},
                        "210": {"power_on_timer": "on", "power_on_time_value": 210},
                        "240": {"power_on_timer": "on", "power_on_time_value": 240},
                        "270": {"power_on_timer": "on", "power_on_time_value": 270},
                        "300": {"power_on_timer": "on", "power_on_time_value": 300},
                        "330": {"power_on_timer": "on", "power_on_time_value": 330},
                        "360": {"power_on_timer": "on", "power_on_time_value": 360},
                        "390": {"power_on_timer": "on", "power_on_time_value": 390},
                        "420": {"power_on_timer": "on", "power_on_time_value": 420},
                        "450": {"power_on_timer": "on", "power_on_time_value": 450},
                        "480": {"power_on_timer": "on", "power_on_time_value": 480},
                        "510": {"power_on_timer": "on", "power_on_time_value": 510},
                        "540": {"power_on_timer": "on", "power_on_time_value": 540},
                        "570": {"power_on_timer": "on", "power_on_time_value": 570},
                        "600": {"power_on_timer": "on", "power_on_time_value": 600},
                        "660": {"power_on_timer": "on", "power_on_time_value": 660},
                        "720": {"power_on_timer": "on", "power_on_time_value": 720},
                        "780": {"power_on_timer": "on", "power_on_time_value": 780},
                        "840": {"power_on_timer": "on", "power_on_time_value": 840},
                        "900": {"power_on_timer": "on", "power_on_time_value": 900},
                        "960": {"power_on_timer": "on", "power_on_time_value": 960},
                        "1020": {"power_on_timer": "on", "power_on_time_value": 1020},
                        "1080": {"power_on_timer": "on", "power_on_time_value": 1080},
                        "1140": {"power_on_timer": "on", "power_on_time_value": 1140},
                        "1200": {"power_on_timer": "on", "power_on_time_value": 1200},
                        "1260": {"power_on_timer": "on", "power_on_time_value": 1260},
                        "1320": {"power_on_timer": "on", "power_on_time_value": 1320},
                        "1380": {"power_on_timer": "on", "power_on_time_value": 1380},
                        "1440": {"power_on_timer": "on", "power_on_time_value": 1440}
                    }
                },
                "power_off_time": {
                    "options": {
                        "off": {"power_off_timer": "off"},
                        "30": {"power_off_timer": "on", "power_off_time_value": 30},
                        "60": {"power_off_timer": "on", "power_off_time_value": 60},
                        "90": {"power_off_timer": "on", "power_off_time_value": 90},
                        "120": {"power_off_timer": "on", "power_off_time_value": 120},
                        "150": {"power_off_timer": "on", "power_off_time_value": 150},
                        "180": {"power_off_timer": "on", "power_off_time_value": 180},
                        "210": {"power_off_timer": "on", "power_off_time_value": 210},
                        "240": {"power_off_timer": "on", "power_off_time_value": 240},
                        "270": {"power_off_timer": "on", "power_off_time_value": 270},
                        "300": {"power_off_timer": "on", "power_off_time_value": 300},
                        "330": {"power_off_timer": "on", "power_off_time_value": 330},
                        "360": {"power_off_timer": "on", "power_off_time_value": 360},
                        "390": {"power_off_timer": "on", "power_off_time_value": 390},
                        "420": {"power_off_timer": "on", "power_off_time_value": 420},
                        "450": {"power_off_timer": "on", "power_off_time_value": 450},
                        "480": {"power_off_timer": "on", "power_off_time_value": 480},
                        "510": {"power_off_timer": "on", "power_off_time_value": 510},
                        "540": {"power_off_timer": "on", "power_off_time_value": 540},
                        "570": {"power_off_timer": "on", "power_off_time_value": 570},
                        "600": {"power_off_timer": "on", "power_off_time_value": 600},
                        "660": {"power_off_timer": "on", "power_off_time_value": 660},
                        "720": {"power_off_timer": "on", "power_off_time_value": 720},
                        "780": {"power_off_timer": "on", "power_off_time_value": 780},
                        "840": {"power_off_timer": "on", "power_off_time_value": 840},
                        "900": {"power_off_timer": "on", "power_off_time_value": 900},
                        "960": {"power_off_timer": "on", "power_off_time_value": 960},
                        "1020": {"power_off_timer": "on", "power_off_time_value": 1020},
                        "1080": {"power_off_timer": "on", "power_off_time_value": 1080},
                        "1140": {"power_off_timer": "on", "power_off_time_value": 1140},
                        "1200": {"power_off_timer": "on", "power_off_time_value": 1200},
                        "1260": {"power_off_timer": "on", "power_off_time_value": 1260},
                        "1320": {"power_off_timer": "on", "power_off_time_value": 1320},
                        "1380": {"power_off_timer": "on", "power_off_time_value": 1380},
                        "1440": {"power_off_timer": "on", "power_off_time_value": 1440}
                    }
                }
            },
            Platform.SENSOR: {
                "water_full_level": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "20104032": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"light, self_clean, sound"}
        ],
        "polling_query": [
            {}
        ],
        "entities": {
            Platform.LOCK: {
                "child_lock": {}
            },
            Platform.SWITCH: {
                "anion": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "wind_swing_ud": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "purifier": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "display_on_off"
                },
                "self_clean": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "sound": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "buzzer"
                }
            },
            Platform.HUMIDIFIER: {
                "dehumidifier": {
                    "device_class": HumidifierDeviceClass.DEHUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 35,
                    "max_humidity": 85,
                    "target_humidity_step": 5,
                    "mode": "mode",
                    "modes": {
                        "continuity": {"mode": "continuity"},
                        "dry_clothes": {"mode": "dry_clothes"},
                        "eco": {"mode": "eco"},
                        "set": {"mode": "set"}
                    }
                }
            },
            Platform.TEXT: {
                "external_humidity_sensor": {}
            },
            Platform.SELECT: {
                "wind_speed": {
                    "options": {
                        "silent": {"wind_speed": 20},
                        "comfort": {"wind_speed": 60},
                        "high": {"wind_speed": 80},
                        "strong": {"wind_speed": 100}
                    },
                },
                "power_on_time": {
                     "options": {
                        "off": {"power_on_timer": "off"},
                        "30": {"power_on_timer": "on", "power_on_time_value": 30},
                        "60": {"power_on_timer": "on", "power_on_time_value": 60},
                        "90": {"power_on_timer": "on", "power_on_time_value": 90},
                        "120": {"power_on_timer": "on", "power_on_time_value": 120},
                        "150": {"power_on_timer": "on", "power_on_time_value": 150},
                        "180": {"power_on_timer": "on", "power_on_time_value": 180},
                        "210": {"power_on_timer": "on", "power_on_time_value": 210},
                        "240": {"power_on_timer": "on", "power_on_time_value": 240},
                        "270": {"power_on_timer": "on", "power_on_time_value": 270},
                        "300": {"power_on_timer": "on", "power_on_time_value": 300},
                        "330": {"power_on_timer": "on", "power_on_time_value": 330},
                        "360": {"power_on_timer": "on", "power_on_time_value": 360},
                        "390": {"power_on_timer": "on", "power_on_time_value": 390},
                        "420": {"power_on_timer": "on", "power_on_time_value": 420},
                        "450": {"power_on_timer": "on", "power_on_time_value": 450},
                        "480": {"power_on_timer": "on", "power_on_time_value": 480},
                        "510": {"power_on_timer": "on", "power_on_time_value": 510},
                        "540": {"power_on_timer": "on", "power_on_time_value": 540},
                        "570": {"power_on_timer": "on", "power_on_time_value": 570},
                        "600": {"power_on_timer": "on", "power_on_time_value": 600},
                        "660": {"power_on_timer": "on", "power_on_time_value": 660},
                        "720": {"power_on_timer": "on", "power_on_time_value": 720},
                        "780": {"power_on_timer": "on", "power_on_time_value": 780},
                        "840": {"power_on_timer": "on", "power_on_time_value": 840},
                        "900": {"power_on_timer": "on", "power_on_time_value": 900},
                        "960": {"power_on_timer": "on", "power_on_time_value": 960},
                        "1020": {"power_on_timer": "on", "power_on_time_value": 1020},
                        "1080": {"power_on_timer": "on", "power_on_time_value": 1080},
                        "1140": {"power_on_timer": "on", "power_on_time_value": 1140},
                        "1200": {"power_on_timer": "on", "power_on_time_value": 1200},
                        "1260": {"power_on_timer": "on", "power_on_time_value": 1260},
                        "1320": {"power_on_timer": "on", "power_on_time_value": 1320},
                        "1380": {"power_on_timer": "on", "power_on_time_value": 1380},
                        "1440": {"power_on_timer": "on", "power_on_time_value": 1440}
                    }
                },
                "power_off_time": {
                    "options": {
                        "off": {"power_off_timer": "off"},
                        "30": {"power_off_timer": "on", "power_off_time_value": 30},
                        "60": {"power_off_timer": "on", "power_off_time_value": 60},
                        "90": {"power_off_timer": "on", "power_off_time_value": 90},
                        "120": {"power_off_timer": "on", "power_off_time_value": 120},
                        "150": {"power_off_timer": "on", "power_off_time_value": 150},
                        "180": {"power_off_timer": "on", "power_off_time_value": 180},
                        "210": {"power_off_timer": "on", "power_off_time_value": 210},
                        "240": {"power_off_timer": "on", "power_off_time_value": 240},
                        "270": {"power_off_timer": "on", "power_off_time_value": 270},
                        "300": {"power_off_timer": "on", "power_off_time_value": 300},
                        "330": {"power_off_timer": "on", "power_off_time_value": 330},
                        "360": {"power_off_timer": "on", "power_off_time_value": 360},
                        "390": {"power_off_timer": "on", "power_off_time_value": 390},
                        "420": {"power_off_timer": "on", "power_off_time_value": 420},
                        "450": {"power_off_timer": "on", "power_off_time_value": 450},
                        "480": {"power_off_timer": "on", "power_off_time_value": 480},
                        "510": {"power_off_timer": "on", "power_off_time_value": 510},
                        "540": {"power_off_timer": "on", "power_off_time_value": 540},
                        "570": {"power_off_timer": "on", "power_off_time_value": 570},
                        "600": {"power_off_timer": "on", "power_off_time_value": 600},
                        "660": {"power_off_timer": "on", "power_off_time_value": 660},
                        "720": {"power_off_timer": "on", "power_off_time_value": 720},
                        "780": {"power_off_timer": "on", "power_off_time_value": 780},
                        "840": {"power_off_timer": "on", "power_off_time_value": 840},
                        "900": {"power_off_timer": "on", "power_off_time_value": 900},
                        "960": {"power_off_timer": "on", "power_off_time_value": 960},
                        "1020": {"power_off_timer": "on", "power_off_time_value": 1020},
                        "1080": {"power_off_timer": "on", "power_off_time_value": 1080},
                        "1140": {"power_off_timer": "on", "power_off_time_value": 1140},
                        "1200": {"power_off_timer": "on", "power_off_time_value": 1200},
                        "1260": {"power_off_timer": "on", "power_off_time_value": 1260},
                        "1320": {"power_off_timer": "on", "power_off_time_value": 1320},
                        "1380": {"power_off_timer": "on", "power_off_time_value": 1380},
                        "1440": {"power_off_timer": "on", "power_off_time_value": 1440}
                    }
                }
            },
            Platform.SENSOR: {
                "water_full_level": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "cur_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "20104036": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"light, sound"}
        ],
        "polling_query": [
            {},
            {"light, sound"}
        ],
        "entities": {
            Platform.SWITCH: {
                "anion": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "display_on_off"
                },
                "sound": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1],
                    "translation_key": "buzzer"
                },
                "water_pump": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": [0, 1]
                }
            },
            Platform.HUMIDIFIER: {
                "dehumidifier": {
                    "device_class": HumidifierDeviceClass.DEHUMIDIFIER,
                    "power": "power",
                    "target_humidity": "humidity",
                    "current_humidity": "cur_humidity",
                    "min_humidity": 35,
                    "max_humidity": 85,
                    "target_humidity_step": 5,
                    "mode": "mode",
                    "modes": {
                        "continuity": {"mode": "continuity"},
                        "dry_clothes": {"mode": "dry_clothes"},
                        "auto": {"mode": "auto"},
                        "set": {"mode": "set"}
                    }
                }
            },
            Platform.TEXT: {
                "external_humidity_sensor": {}
            },
            Platform.SELECT: {
                "wind_speed": {
                    "options": {
                        "low": {"wind_speed": 40},
                        "high": {"wind_speed": 80}
                    },
                },
                "power_on_time": {
                     "options": {
                        "off": {"power_on_timer": "off"},
                        "30": {"power_on_timer": "on", "power_on_time_value": 30},
                        "60": {"power_on_timer": "on", "power_on_time_value": 60},
                        "90": {"power_on_timer": "on", "power_on_time_value": 90},
                        "120": {"power_on_timer": "on", "power_on_time_value": 120},
                        "150": {"power_on_timer": "on", "power_on_time_value": 150},
                        "180": {"power_on_timer": "on", "power_on_time_value": 180},
                        "210": {"power_on_timer": "on", "power_on_time_value": 210},
                        "240": {"power_on_timer": "on", "power_on_time_value": 240},
                        "270": {"power_on_timer": "on", "power_on_time_value": 270},
                        "300": {"power_on_timer": "on", "power_on_time_value": 300},
                        "330": {"power_on_timer": "on", "power_on_time_value": 330},
                        "360": {"power_on_timer": "on", "power_on_time_value": 360},
                        "390": {"power_on_timer": "on", "power_on_time_value": 390},
                        "420": {"power_on_timer": "on", "power_on_time_value": 420},
                        "450": {"power_on_timer": "on", "power_on_time_value": 450},
                        "480": {"power_on_timer": "on", "power_on_time_value": 480},
                        "510": {"power_on_timer": "on", "power_on_time_value": 510},
                        "540": {"power_on_timer": "on", "power_on_time_value": 540},
                        "570": {"power_on_timer": "on", "power_on_time_value": 570},
                        "600": {"power_on_timer": "on", "power_on_time_value": 600},
                        "660": {"power_on_timer": "on", "power_on_time_value": 660},
                        "720": {"power_on_timer": "on", "power_on_time_value": 720},
                        "780": {"power_on_timer": "on", "power_on_time_value": 780},
                        "840": {"power_on_timer": "on", "power_on_time_value": 840},
                        "900": {"power_on_timer": "on", "power_on_time_value": 900},
                        "960": {"power_on_timer": "on", "power_on_time_value": 960},
                        "1020": {"power_on_timer": "on", "power_on_time_value": 1020},
                        "1080": {"power_on_timer": "on", "power_on_time_value": 1080},
                        "1140": {"power_on_timer": "on", "power_on_time_value": 1140},
                        "1200": {"power_on_timer": "on", "power_on_time_value": 1200},
                        "1260": {"power_on_timer": "on", "power_on_time_value": 1260},
                        "1320": {"power_on_timer": "on", "power_on_time_value": 1320},
                        "1380": {"power_on_timer": "on", "power_on_time_value": 1380},
                        "1440": {"power_on_timer": "on", "power_on_time_value": 1440}
                    }
                },
                "power_off_time": {
                    "options": {
                        "off": {"power_off_timer": "off"},
                        "30": {"power_off_timer": "on", "power_off_time_value": 30},
                        "60": {"power_off_timer": "on", "power_off_time_value": 60},
                        "90": {"power_off_timer": "on", "power_off_time_value": 90},
                        "120": {"power_off_timer": "on", "power_off_time_value": 120},
                        "150": {"power_off_timer": "on", "power_off_time_value": 150},
                        "180": {"power_off_timer": "on", "power_off_time_value": 180},
                        "210": {"power_off_timer": "on", "power_off_time_value": 210},
                        "240": {"power_off_timer": "on", "power_off_time_value": 240},
                        "270": {"power_off_timer": "on", "power_off_time_value": 270},
                        "300": {"power_off_timer": "on", "power_off_time_value": 300},
                        "330": {"power_off_timer": "on", "power_off_time_value": 330},
                        "360": {"power_off_timer": "on", "power_off_time_value": 360},
                        "390": {"power_off_timer": "on", "power_off_time_value": 390},
                        "420": {"power_off_timer": "on", "power_off_time_value": 420},
                        "450": {"power_off_timer": "on", "power_off_time_value": 450},
                        "480": {"power_off_timer": "on", "power_off_time_value": 480},
                        "510": {"power_off_timer": "on", "power_off_time_value": 510},
                        "540": {"power_off_timer": "on", "power_off_time_value": 540},
                        "570": {"power_off_timer": "on", "power_off_time_value": 570},
                        "600": {"power_off_timer": "on", "power_off_time_value": 600},
                        "660": {"power_off_timer": "on", "power_off_time_value": 660},
                        "720": {"power_off_timer": "on", "power_off_time_value": 720},
                        "780": {"power_off_timer": "on", "power_off_time_value": 780},
                        "840": {"power_off_timer": "on", "power_off_time_value": 840},
                        "900": {"power_off_timer": "on", "power_off_time_value": 900},
                        "960": {"power_off_timer": "on", "power_off_time_value": 960},
                        "1020": {"power_off_timer": "on", "power_off_time_value": 1020},
                        "1080": {"power_off_timer": "on", "power_off_time_value": 1080},
                        "1140": {"power_off_timer": "on", "power_off_time_value": 1140},
                        "1200": {"power_off_timer": "on", "power_off_time_value": 1200},
                        "1260": {"power_off_timer": "on", "power_off_time_value": 1260},
                        "1320": {"power_off_timer": "on", "power_off_time_value": 1320},
                        "1380": {"power_off_timer": "on", "power_off_time_value": 1380},
                        "1440": {"power_off_timer": "on", "power_off_time_value": 1440}
                    }
                }
            },
            Platform.SENSOR: {
                "water_full_level": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "cur_humidity": {
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "tank_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
