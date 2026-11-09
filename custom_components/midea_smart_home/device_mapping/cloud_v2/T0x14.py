"""T0x14 电动窗帘设备映射定义（Thing Model V2 / v2_thing）"""
from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [
            {}
        ],
        "entities": {
            Platform.COVER: {
                "curtain_status": {
                    "open_value": "open",
                    "close_value": "close",
                    "stop_value": "stop",
                    "position_key": "curtain_position",
                    "device_class": CoverDeviceClass.CURTAIN,
                    "translation_key": "curtain",
                    "module_code": "electricCurtain",
                    "actions": {
                        "open": "open",
                        "close": "close",
                        "stop": "pause"
                    },
                    "target_position_key": "electricCurtain.targetOpeningPercentage"
                }
            },
            Platform.SELECT: {
                "electricCurtain.motorSpeed": {
                    "attribute": "electricCurtain.motorSpeed",
                    "translation_key": "motor_speed",
                    "thing_key": "electricCurtain.motorSpeed",
                    "options": [1, 2, 3],
                    "options_translation_keys": [
                        "motor_speed_silent",
                        "motor_speed_medium",
                        "motor_speed_fast"
                    ],
                    "icon": "mdi:speedometer"
                }
            },
            Platform.SWITCH: {
                "electricCurtain.motorReverse": {
                    "attribute": "electricCurtain.motorReverse",
                    "translation_key": "motor_reverse",
                    "thing_key": "electricCurtain.motorReverse",
                    "icon": "mdi:swap-horizontal"
                },
                "electricCurtain.manualPullMode": {
                    "attribute": "electricCurtain.manualPullMode",
                    "translation_key": "manual_pull_mode",
                    "thing_key": "electricCurtain.manualPullMode",
                    "icon": "mdi:hand-back-right"
                }
            },
            Platform.SENSOR: {
                "curtain_position": {
                    "attribute": "curtain_position",
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "thing_key": "electricCurtain.currentOpeningPercentage"
                }
            }
        }
    }
}
