"""Constants for the Midea Smart Home integration.

This module contains all constant definitions used across the integration,
including configuration keys, device types, paths, and embedded Lua scripts.
"""

DOMAIN = "midea_smart_home"

JSON_FILES_PATH = f".storage/{DOMAIN}/json_files"
LUA_DEVICE_PATH = f".storage/{DOMAIN}/lua_devices"
LUA_COMMON_PATH = f".storage/{DOMAIN}/lua_common"

CONF_ACCOUNT = "account"
CONF_PASSWORD = "password"
CONF_DEVICE_ID = "device_id"
CONF_TOKEN = "token"
CONF_KEY = "key"
CONF_LUA_FILE = "lua_file"
CONF_DEVICE_TYPE = "device_type"
CONF_IP = "ip"
CONF_PORT = "port"
CONF_SN = "sn"
CONF_SN8 = "sn8"
CONF_PRODUCT_MODEL = "product_model"
CONF_MODEL_NUMBER = "model_number"
CONF_MANUFACTURER_CODE = "manufacturer_code"
CONF_DEVICE_NAME = "device_name"
CONF_PROTOCOL = "protocol"
CONF_CATEGORY = "category"

DEFAULT_PORT = 6444


class ProtocolVersion:
    V1 = 1
    V2 = 2
    V3 = 3

DEVICE_TYPES = {
    0x17: "Laundry Machine",
    0x26: "Bath Heater",
    0xAC: "Floor Air Conditioner / Wall Air Conditioner / Central Air Conditioner / Central Fresh Air / Central Miniaturized Fresh Air",
    0xB0: "Microwave Oven",
    0xB6: "Range Hood",
    0x9C: "Integrated Stove",
    0xB8: "Smart Robot Vacuum",
    0xBF: "Microwave Steam Oven",
    0xCA: "Multi-Door Fridge",
    0xD9: "Twin Tub Washing Machine",
    0xDA: "Top Load Washing Machine",
    0xDB: "Cylinder Washing Machine",
    0xDC: "Clothes Dryer",
    0xE1: "Dishwasher",
    0xE2: "Electric Water Heater",
    0xE3: "Gas Water Heater",
    0xE6: "Gas Wall Hanging Stove",
    0xEA: "Rice Cooker",
    0xED: "Net Drinking Machine / Water Purifier / Pipeline Machine",
    0xFA: "Electric Fan",
    0xFB: "Electric Heater",
    0xFC: "Air Purifier",
    0xFD: "Humidifier"
}

PLATFORMS = ["climate", "sensor", "switch", "select", "button", "number", "vacuum", "binary_sensor", "fan", "humidifier", "light", "cover", "water_heater"]
