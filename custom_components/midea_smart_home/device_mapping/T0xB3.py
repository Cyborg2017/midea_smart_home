from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [{}],
        "polling_query": [{}],
        "calculate": {
            "get": [
                {
                    "lvalue": "[downstair_remain_time]",
                    "rvalue": "[downstair_sec] + 60 * [downstair_min] + 3600 * [downstair_hour]"
                },
                {
                    "lvalue": "[order_time]",
                    "rvalue": "[order_sec] + 60 * [order_min] + 3600 * [order_hour]"
                },
                {
                    "lvalue": "[upstair_remain_time]",
                    "rvalue": "[upstair_sec] + 60 * [upstair_min] + 3600 * [upstair_hour]"
                }
            ]
        },
        "entities": {
            Platform.SELECT: {
                "downstair_mode": {
                    "options": {
                        "off": {"downstair_work_status": "power_off"},
                        "standby": {"downstair_work_status": "power_on"},
                        "dry": {"downstair_mode": "2"},
                        "sterilize": {"downstair_mode": "3"},
                        "storage": {"downstair_mode": "26"}
                    }
                },
                "upstair_mode": {
                    "options": {
                        "off": {"upstair_work_status": "power_off"},
                        "standby": {"upstair_work_status": "power_on"},
                        "clean": {"upstair_mode": "23"},
                        "storage": {"upstair_mode": "26"}
                    }
                }
            },
            Platform.BINARY_SENSOR: {
                "door_downstair": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                    "rationale": ["close", "open"]
                },
                "door_upstair": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                    "rationale": ["close", "open"]
                },
                "downstair_iscooling": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": ["uncooling", "cooling"]
                },
                "downstair_ispreheat": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": ["unpreheat", "preheat"]
                },
                "is_error": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "upstair_iscooling": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": ["uncooling", "cooling"]
                },
                "upstair_ispreheat": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": ["unpreheat", "preheat"]
                }
            },
            Platform.SENSOR: {
                "downstair_remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "downstair_temp": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "downstair_work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "order_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "upstair_remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "upstair_temp": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "upstair_work_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    },
    "0090Q15S": {
        "rationale": ["off", "on"],
        "initial_query": [{}],
        "polling_query": [{}],
        "calculate": {
            "get": [
                {
                    "lvalue": "[downstair_remain_time]",
                    "rvalue": "[downstair_sec] + 60 * [downstair_min] + 3600 * [downstair_hour]"
                },
                {
                    "lvalue": "[order_time]",
                    "rvalue": "[order_sec] + 60 * [order_min] + 3600 * [order_hour]"
                },
                {
                    "lvalue": "[upstair_remain_time]",
                    "rvalue": "[upstair_sec] + 60 * [upstair_min] + 3600 * [upstair_hour]"
                }
            ]
        },
        "entities": {
            Platform.SELECT: {
                "downstair_mode": {
                    "options": {
                        "off": {"downstair_work_status": "power_off"},
                        "standby": {"downstair_work_status": "power_on"},
                        "dry": {"downstair_mode": "2"},
                        "sterilize": {"downstair_mode": "3"},
                        "storage": {"downstair_mode": "26"}
                    }
                },
                "upstair_mode": {
                    "options": {
                        "off": {"upstair_work_status": "power_off"},
                        "standby": {"upstair_work_status": "power_on"},
                        "clean": {"upstair_mode": "23"},
                        "storage": {"upstair_mode": "26"}
                    }
                }
            },
            Platform.BINARY_SENSOR: {
                "door_downstair": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                    "rationale": ["close", "open"]
                },
                "door_upstair": {
                    "device_class": BinarySensorDeviceClass.DOOR,
                    "rationale": ["close", "open"]
                },
                "downstair_iscooling": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": ["uncooling", "cooling"]
                },
                "downstair_ispreheat": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": ["unpreheat", "preheat"]
                },
                "is_error": {
                    "device_class": BinarySensorDeviceClass.PROBLEM
                },
                "upstair_iscooling": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": ["uncooling", "cooling"]
                },
                "upstair_ispreheat": {
                    "device_class": BinarySensorDeviceClass.RUNNING,
                    "rationale": ["unpreheat", "preheat"]
                }
            },
            Platform.SENSOR: {
                "downstair_remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "downstair_temp": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "downstair_work_status": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                },
                "order_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "upstair_remain_time": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.SECONDS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "upstair_temp": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "upstair_work_status": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
