from custom_components.midea_smart_home.device_mapping._common import *

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "calculate": {
            "get": [
                {
                    "lvalue": "[b3_upstair_remaining_time_min]",
                    "rvalue": "int(([b3_upstair_remaining_time] + 59) / 60)"
                },
                {
                    "lvalue": "[b3_upstair_destination_time_min]",
                    "rvalue": "int([b3_upstair_destination_time] / 60)"
                },
                {
                    "lvalue": "[b6_inverter_voltage_v]",
                    "rvalue": "float([b6_inverter_voltage] / 10.0)"
                }
            ],
        },
        "entities": {
            Platform.LIGHT: {
                "common_light": {
                    "power": "b6_light",
                    "brightness": {"b6_lightness": [20, 100]},
                    "command": {
                        "type": "b6"
                    }
                }
            },
            Platform.SWITCH: {
                "total_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "total_power",
                    "command": {
                        "type": "total"
                    }
                },
                "b6_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "b6_power",
                    "command": {
                        "type": "b6"
                    }
                },
                "b6_smoke_stove_linkage": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {
                        "type": "b6",
                        "b6_setting": "smoke_stove_linkage"
                    }
                },
                "b6_power_on_light": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "command": {
                        "type": "b6",
                        "b6_setting": "power_on_light"
                    }
                }
            },
            Platform.SELECT: {
                "b3_function_control": {
                    "status_key": "b3_function_control",
                    "options": {
                        "off": {"b3_function_control": 1},
                        "sterilize": {"b3_function_control": 2, "b3_work_destination_time": 60},
                        "dry": {"b3_function_control": 4, "b3_work_destination_time": 120},
                    },
                    "command": {
                        "type": "b3",
                        "b3_work_cabinet_control": 1
                    }
                },
                "b6_gear": {
                    "options": {
                        "off": {"b6_gear": "0"},
                        "low": {"b6_gear": "1"},
                        "medium": {"b6_gear": "2"},
                        "high": {"b6_gear": "3"},
                        "extreme": {"b6_gear": "4"}
                    },
                    "translation_key": "gear",
                    "command": {
                        "type": "b6"
                    }
                },
                "b6_smoke_stove_linkage_gear": {
                    "options": {
                        "gear_1": {"b6_smoke_stove_linkage_gear": 1},
                        "gear_2": {"b6_smoke_stove_linkage_gear": 2},
                        "gear_3": {"b6_smoke_stove_linkage_gear": 3},
                    },
                    "command": {
                        "type": "b6",
                        "b6_setting": "smoke_stove_linkage"
                    }
                },
                "b6_delay_gear_linkage_gear": {
                    "options": {
                        "gear_1": {"b6_delay_gear_linkage_gear": 1},
                        "gear_2": {"b6_delay_gear_linkage_gear": 2},
                        "gear_3": {"b6_delay_gear_linkage_gear": 3},
                    },
                    "command": {
                        "type": "b6",
                        "b6_setting": "delay_gear_linkage"
                    }
                },
                "b6_delay_time_value": {
                    "options": {
                        "off": {"b6_delay_time": "off"},
                        "1_min": {"b6_delay_time": "on", "b6_delay_time_value": 1},
                        "2_min": {"b6_delay_time": "on", "b6_delay_time_value": 2},
                        "3_min": {"b6_delay_time": "on", "b6_delay_time_value": 3},
                        "4_min": {"b6_delay_time": "on", "b6_delay_time_value": 4},
                        "5_min": {"b6_delay_time": "on", "b6_delay_time_value": 5},
                        "6_min": {"b6_delay_time": "on", "b6_delay_time_value": 6},
                        "7_min": {"b6_delay_time": "on", "b6_delay_time_value": 7},
                        "8_min": {"b6_delay_time": "on", "b6_delay_time_value": 8},
                        "9_min": {"b6_delay_time": "on", "b6_delay_time_value": 9},
                        "10_min": {"b6_delay_time": "on", "b6_delay_time_value": 10},
                    },
                    "command": {
                        "type": "b6",
                        "b6_setting": "delay_time"
                    }
                }
            },
            Platform.BINARY_SENSOR: {
                "b3_upstair_door": {
                    "device_class": BinarySensorDeviceClass.OPENING,
                    "rationale": ["close", "open"]
                },
            },
            Platform.SENSOR: {
                "b3_upstair_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": ["power_off", "uperization", "drying", "standby"],
                },
                "b3_upstair_remaining_time_min": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "b3_upstair_destination_temp": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "b3_upstair_destination_time_min": {
                    "device_class": SensorDeviceClass.DURATION,
                    "unit_of_measurement": UnitOfTime.MINUTES,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "b6_work_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": [
                        "power_off", "initial", "working", "power_off_delay",
                        "hotclean", "error", "clean", "check",
                        "vvvf_gear", "mute_gear", "ai_dry_clean", "clean_finish",
                        "air_duct_detection", "standby",
                    ],
                },
                "b6_air_volume": {
                    "device_class": SensorDeviceClass.VOLUME_FLOW_RATE,
                    "unit_of_measurement": UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "b6_wind_pressure": {
                    "device_class": SensorDeviceClass.PRESSURE,
                    "unit_of_measurement": UnitOfPressure.PA,
                    "state_class": SensorStateClass.MEASUREMENT,
                    "translation_key": "wind_pressure"
                },
                "b6_inverter_voltage_v": {
                    "device_class": SensorDeviceClass.VOLTAGE,
                    "unit_of_measurement": UnitOfElectricPotential.VOLT,
                    "state_class": SensorStateClass.MEASUREMENT,
                },
                "b7_left_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": ["power_off", "working", "ai", "power_off_delay"],
                },
                "b7_left_gear": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": ["0", "1", "2", "3", "4"],
                },
                "b7_right_status": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": ["power_off", "working", "ai", "power_off_delay"],
                },
                "b7_right_gear": {
                    "device_class": SensorDeviceClass.ENUM,
                    "options": ["0", "1", "2", "3", "4"],
                }
            }
        }
    }
}
