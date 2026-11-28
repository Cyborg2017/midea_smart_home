from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "entities": {
            Platform.SWITCH: {
                "airPurifier.power": {
                    "attribute": "airPurifier.power",
                    "translation_key": "power",
                    "thing_key": "airPurifier.power",
                    "device_class": SwitchDeviceClass.SWITCH,
                    "icon": "mdi:power"
                },
                "airPurifier.netIonsSwitch": {
                    "attribute": "airPurifier.netIonsSwitch",
                    "translation_key": "waterions",
                    "thing_key": "airPurifier.netIonsSwitch",
                    "device_class": SwitchDeviceClass.SWITCH,
                    "icon": "mdi:weather-windy"
                },
                "promptTone.promptToneSwitch": {
                    "attribute": "promptTone.promptToneSwitch",
                    "translation_key": "buzzer",
                    "thing_key": "promptTone.promptToneSwitch",
                    "device_class": SwitchDeviceClass.SWITCH,
                    "icon": "mdi:volume-high"
                }
            },
            Platform.LOCK: {
                "childLock.childLockSwitch": {
                    "attribute": "childLock.childLockSwitch",
                    "translation_key": "child_lock",
                    "thing_key": "childLock.childLockSwitch",
                    "icon": "mdi:lock"
                }
            },
            Platform.NUMBER: {
                "airPurifier.intelligentHostingPowerOnPm2_5": {
                    "attribute": "airPurifier.intelligentHostingPowerOnPm2_5",
                    "translation_key": "hosting_upper",
                    "thing_key": "airPurifier.intelligentHostingPowerOnPm2_5",
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box",
                    "icon": "mdi:transfer-up"
                },
                "airPurifier.intelligentHostingPowerOffPm2_5": {
                    "attribute": "airPurifier.intelligentHostingPowerOffPm2_5",
                    "translation_key": "hosting_lower",
                    "thing_key": "airPurifier.intelligentHostingPowerOffPm2_5",
                    "min": 10,
                    "max": 75,
                    "step": 1,
                    "mode": "box",
                    "icon": "mdi:transfer-down"
                }
            },
            Platform.SELECT: {
                "airPurifier.windSpeed": {
                    "attribute": "airPurifier.windSpeed",
                    "translation_key": "purifier_wind_speed",
                    "thing_key": "airPurifier.windSpeed",
                    "options": [1, 2, 3],
                    "options_translation_keys": ["low", "middle", "high"],
                    "icon": "mdi:fan"
                },
                "airPurifier.workMode": {
                    "attribute": "airPurifier.workMode",
                    "translation_key": "purifier_work_mode",
                    "thing_key": "airPurifier.workMode",
                    "options": [0, 2, 5, 6],
                    "options_translation_keys": [
                        "manual",
                        "sleep",
                        "hosting",
                        "air_dry"
                    ],
                    "icon": "mdi:cog"
                },
                "screenDisplay.brightnessGear": {
                    "attribute": "screenDisplay.brightnessGear",
                    "translation_key": "bright",
                    "thing_key": "screenDisplay.brightnessGear",
                    "options": [0, 1, 2],
                    "options_translation_keys": ["off", "half", "full"],
                    "icon": "mdi:brightness-6"
                },
                "noise_mode": {
                    "translation_key": "bias_gear",
                    "options_translation_keys": [
                        "none",
                        "conversation_scene",
                        "yoga_scene"
                    ],
                    "options": {
                        "none": {
                            "airPurifier.autoModeSelection": 0
                        },
                        "conversation_scene": {
                            "airPurifier.autoModeSelection": 3,
                            "airPurifier.autoModeWindSpeedOffsetValue": -10
                        },
                        "yoga_scene": {
                            "airPurifier.autoModeSelection": 3,
                            "airPurifier.autoModeWindSpeedOffsetValue": -20
                        }
                    },
                    "icon": "mdi:weather-windy"
                }
            },
            Platform.SENSOR: {
                "airPurifier.pm2_5": {
                    "attribute": "airPurifier.pm2_5",
                    "translation_key": "pm25",
                    "thing_key": "airPurifier.pm2_5",
                    "device_class": SensorDeviceClass.PM25,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "icon": "mdi:blur"
                },
                "airPurifier.pm10": {
                    "attribute": "airPurifier.pm10",
                    "translation_key": "pm10",
                    "thing_key": "airPurifier.pm10",
                    "device_class": SensorDeviceClass.PM10,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "unit_of_measurement": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    "icon": "mdi:blur"
                },
                "airPurifier.formaldehyde": {
                    "attribute": "airPurifier.formaldehyde",
                    "translation_key": "hcho",
                    "thing_key": "airPurifier.formaldehyde",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "unit_of_measurement": "mg/m³",
                    "icon": "mdi:chemical-weapon"
                },
                "airPurifier.currentTemperature": {
                    "attribute": "airPurifier.currentTemperature",
                    "translation_key": "cur_temperature",
                    "thing_key": "airPurifier.currentTemperature",
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "icon": "mdi:thermometer"
                },
                "airPurifier.currentHumidity": {
                    "attribute": "airPurifier.currentHumidity",
                    "translation_key": "cur_humidity",
                    "thing_key": "airPurifier.currentHumidity",
                    "device_class": SensorDeviceClass.HUMIDITY,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "unit_of_measurement": PERCENTAGE,
                    "icon": "mdi:water-percent"
                },
                "compositeAirFilter.filterLeftLife": {
                    "attribute": "compositeAirFilter.filterLeftLife",
                    "translation_key": "deep_filter_percent",
                    "thing_key": "compositeAirFilter.filterLeftLife",
                    "state_class": SensorStateClass.MEASUREMENT,
                    "unit_of_measurement": PERCENTAGE,
                    "icon": "mdi:air-filter"
                }
            }
        }
    }
}
