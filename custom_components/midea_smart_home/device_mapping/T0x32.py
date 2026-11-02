from custom_components.midea_smart_home.device_mapping._common import *

# T0x32 Electric Steamer (e.g. MZ-ZGS352001, sn8 6190008E)
#
# Status attributes are produced by the cloud Lua protocol file
# (T0x32_6190008E.lua) plus the custom wrapper in lua/T0x32_6190008E.lua,
# which flattens the nested "time" object into top-level keys:
#   workStatus: standby/schedule/working/pause/keepWarm/error
#   runMode, subType, workState, errorCode, foodType
#   targetTemperature, currentTemperature
#   waterShortageState: waterShortage/notWaterShortage
#   diyTotalStep, currWorkStep
#   remainAppointTimeSecond, remainWorkTimeSecond, remainKeepWarmTimeSecond,
#   appointTimeSecond, targetAppointTimeSecond, workTimeSecond,
#   keepWarmTimeSecond, alreadyKeepWarmTimeSecond, remainPauseTimeMinute
#
# Control attributes (sent via jsonToData):
#   workSwitch: standby/schedule/work/pause/keepWork/modifyParam
#   runMode: uint32 cooking mode
#   subCmd: 1 (set) / 3 (diy) / 5 (modify)
#   modifyTimeEnable, modifyTempEnable, targetTemperature, foodType
#   workTimeMinutes / appointTimeMinutes / keepWarmTimeMinutes
#   (translated by the Lua wrapper into the nested "time" object)

_STEAMER_MAPPING = {
    "rationale": ["off", "on"],
    "polling_query": [
        {}
    ],
    "calculate": {
        "get": [
            {
                "lvalue": "[remainWorkTimeMin]",
                "rvalue": "int([remainWorkTimeSecond] / 60)"
            },
            {
                "lvalue": "[remainAppointTimeMin]",
                "rvalue": "int([remainAppointTimeSecond] / 60)"
            },
            {
                "lvalue": "[remainKeepWarmTimeMin]",
                "rvalue": "int([remainKeepWarmTimeSecond] / 60)"
            },
            {
                "lvalue": "[workTimeMin]",
                "rvalue": "int([workTimeSecond] / 60)"
            },
            {
                "lvalue": "[appointTimeMin]",
                "rvalue": "int([appointTimeSecond] / 60)"
            },
            {
                "lvalue": "[keepWarmTimeMin]",
                "rvalue": "int([keepWarmTimeSecond] / 60)"
            }
        ],
        "set": []
    },
    "entities": {
        Platform.NUMBER: {
            "workTimeMinutes": {
                "translation_key": "work_time_minutes",
                "min": 1,
                "max": 240,
                "step": 1,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "status_key": "workTimeMin",
                "command": {
                    "workSwitch": "modifyParam",
                    "subCmd": 5,
                    "modifyTimeEnable": True,
                    "workTimeMinutes": "{value}"
                }
            },
            "appointTimeMinutes": {
                "translation_key": "appoint_time_minutes",
                "min": 0,
                "max": 720,
                "step": 1,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "status_key": "appointTimeMin",
                "command": {
                    "workSwitch": "modifyParam",
                    "subCmd": 5,
                    "modifyTimeEnable": True,
                    "appointTimeMinutes": "{value}"
                }
            },
            "keepWarmTimeMinutes": {
                "translation_key": "keep_warm_time_minutes",
                "min": 0,
                "max": 360,
                "step": 1,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "status_key": "keepWarmTimeMin",
                "command": {
                    "workSwitch": "modifyParam",
                    "subCmd": 5,
                    "modifyTimeEnable": True,
                    "keepWarmTimeMinutes": "{value}"
                }
            }
        },
        Platform.SELECT: {
            "steamer_control": {
                "translation_key": "steamer_control",
                "status_key": "workStatus",
                "options": {
                    "standby": {"workSwitch": "standby"},
                    "pause": {"workSwitch": "pause"},
                    "resume": {"workSwitch": "keepWork"}
                }
            },
            "steamer_start": {
                "translation_key": "steamer_start",
                "include_current": ["runMode", "workTimeMinutes", "appointTimeMinutes", "keepWarmTimeMinutes"],
                "options": {
                    "start_now": {"workSwitch": "work", "subCmd": 1},
                    "start_kuaizheng": {"workSwitch": "work", "subCmd": 1, "runMode": 7},
                    "start_kuaidun": {"workSwitch": "work", "subCmd": 1, "runMode": 8},
                    "schedule_now": {"workSwitch": "schedule", "subCmd": 1},
                    "schedule_kuaizheng": {"workSwitch": "schedule", "subCmd": 1, "runMode": 7},
                    "schedule_kuaidun": {"workSwitch": "schedule", "subCmd": 1, "runMode": 8}
                }
            }
        },
        Platform.SENSOR: {
            "workStatus": {
                "translation_key": "work_status",
                "device_class": SensorDeviceClass.ENUM,
                "options": ["standby", "schedule", "working", "pause", "keepWarm", "error"]
            },
            "runMode": {
                "translation_key": "run_mode"
            },
            "currentTemperature": {
                "translation_key": "current_temperature",
                "device_class": SensorDeviceClass.TEMPERATURE,
                "unit_of_measurement": UnitOfTemperature.CELSIUS,
                "state_class": SensorStateClass.MEASUREMENT,
                "suggested_display_precision": 0
            },
            "targetTemperature": {
                "translation_key": "target_temperature",
                "device_class": SensorDeviceClass.TEMPERATURE,
                "unit_of_measurement": UnitOfTemperature.CELSIUS,
                "state_class": SensorStateClass.MEASUREMENT,
                "suggested_display_precision": 0
            },
            "errorCode": {
                "translation_key": "error_code"
            },
            "waterShortageState": {
                "translation_key": "water_shortage_state",
                "device_class": SensorDeviceClass.ENUM,
                "options": ["waterShortage", "notWaterShortage"]
            },
            "foodType": {
                "translation_key": "food_type",
                "device_class": SensorDeviceClass.ENUM,
                "options": ["invalid", "cupCubilose", "cornerCubilose", "stripCubilose", "shredCubilose"]
            },
            "currWorkStep": {
                "translation_key": "curr_work_step"
            },
            "remainWorkTimeMin": {
                "translation_key": "remain_work_time_min",
                "device_class": SensorDeviceClass.DURATION,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "state_class": SensorStateClass.MEASUREMENT
            },
            "remainAppointTimeMin": {
                "translation_key": "remain_appoint_time_min",
                "device_class": SensorDeviceClass.DURATION,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "state_class": SensorStateClass.MEASUREMENT
            },
            "remainKeepWarmTimeMin": {
                "translation_key": "remain_keep_warm_time_min",
                "device_class": SensorDeviceClass.DURATION,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "state_class": SensorStateClass.MEASUREMENT
            },
            "workTimeMin": {
                "translation_key": "work_time_min",
                "device_class": SensorDeviceClass.DURATION,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "state_class": SensorStateClass.MEASUREMENT
            },
            "appointTimeMin": {
                "translation_key": "appoint_time_min",
                "device_class": SensorDeviceClass.DURATION,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "state_class": SensorStateClass.MEASUREMENT
            },
            "keepWarmTimeMin": {
                "translation_key": "keep_warm_time_min",
                "device_class": SensorDeviceClass.DURATION,
                "unit_of_measurement": UnitOfTime.MINUTES,
                "state_class": SensorStateClass.MEASUREMENT
            }
        }
    }
}

DEVICE_MAPPING = {
    "default": _STEAMER_MAPPING,
    "default_electric_steamer": _STEAMER_MAPPING,
    "mz_zgs352001": _STEAMER_MAPPING,
}
