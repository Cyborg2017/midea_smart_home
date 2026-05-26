from homeassistant.const import Platform, UnitOfTemperature, PRECISION_HALVES
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "initial_query": [
            {},
            {"run_status"}
        ],
        "entities": {
            Platform.CLIMATE: {
                "air_conditioner": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "heat"},
                        "cool": {"power": "on", "mode": "cool"},
                        "dry": {"power": "on", "mode": "dry"},
                        "fan_only": {"power": "on", "mode": "fan"}
                    },
                    "fan_modes": {
                        "high": {"wind_speed": "power"},
                        "middle": {"wind_speed": "middle"},
                        "low": {"wind_speed": "sleep"},
                        "auto": {"wind_speed": "auto"}
                    },
                    "preset_modes": {
                        "none": {
                            "eco": "off",
                            "sleep_switch": "off"
                        },
                        "eco": {"eco": "on"},
                        "sleep": {"sleep_switch": "on"}
                    },
                    "swing_modes": {
                        "swing_ud_no_site": {"wind_swing_ud": "on", "wind_swing_ud_site": "swing_ud_no_site"},
                        "swing_ud_site_1": {"wind_swing_ud": "off", "wind_swing_ud_site": "swing_ud_site_1"},
                        "swing_ud_site_2": {"wind_swing_ud": "off", "wind_swing_ud_site": "swing_ud_site_2"},
                        "swing_ud_site_3": {"wind_swing_ud": "off", "wind_swing_ud_site": "swing_ud_site_3"},
                        "swing_ud_site_4": {"wind_swing_ud": "off", "wind_swing_ud_site": "swing_ud_site_4"},
                        "swing_ud_site_5": {"wind_swing_ud": "off", "wind_swing_ud_site": "swing_ud_site_5"}
                    },
                    "target_temperature": ["temperature", "small_temperature"],
                    "current_temperature": "indoor_temperature",
                    "pre_mode": "mode",
                    "aux_heat": "ptc",
                    "min_temp": 17,
                    "max_temp": 30,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SWITCH: {
                "digit_display_switch": {
                    "device_class": SwitchDeviceClass.SWITCH
                },
                "ptc_setting": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "rationale": ["ptc_setting_off", "ptc_setting_on"],
                    "translation_key": "ptc"
                }
            },
            Platform.SENSOR: {
                "mode": {
                    "device_class": SensorDeviceClass.ENUM,
                },
                "indoor_temperature": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                }
            }
        }
    }
}
