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
                    "translation_key": "curtain"
                }
            },
            Platform.SELECT: {
                "curtain_direction": {
                    "options": {
                        "positive": {"curtain_direction": "positive"},
                        "reverse": {"curtain_direction": "reverse"}
                    }
                }
            },
            Platform.SENSOR: {
                "curtain_position": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "curtain_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": ["open", "close", "stop"]
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "default_electric_curtain": {
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
                    "translation_key": "curtain"
                }
            },
            Platform.SELECT: {
                "curtain_direction": {
                    "options": {
                        "positive": {"curtain_direction": "positive"},
                        "reverse": {"curtain_direction": "reverse"}
                    }
                }
            },
            Platform.SENSOR: {
                "curtain_position": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "curtain_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": ["open", "close", "stop"]
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "79700Z76": {
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
                    "translation_key": "curtain"
                }
            },
            Platform.SELECT: {
                "curtain_direction": {
                    "options": {
                        "positive": {"curtain_direction": "positive"},
                        "reverse": {"curtain_direction": "reverse"}
                    }
                }
            },
            Platform.SENSOR: {
                "curtain_position": {
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "curtain_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": ["open", "close", "stop"]
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
