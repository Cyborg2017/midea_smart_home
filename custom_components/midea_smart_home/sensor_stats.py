"""Cloud statistics sensor definitions.

These sensors are independent of the LAN device state and are fetched by
MideaCloudStatsCoordinator.
"""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfEnergy, UnitOfVolume

# Per-drum statistics keys end with a drum suffix; map it to the drum name
# used by the "drum_locations" declaration of the device mapping.
_DRUM_SUFFIXES = {"_b": "bottom", "_l": "left", "_r": "right"}

def drum_for_stats_key(key: str) -> str | None:
    """Return the drum a statistics key belongs to, or None if it is global."""
    for suffix, drum in _DRUM_SUFFIXES.items():
        if key.endswith(suffix):
            return drum
    return None

# Cloud statistics sensors keyed by device type.
CLOUD_STATS_SENSORS = {
    0xB6: [
        {
            "key": "fan_cleanliness",
            "unit": PERCENTAGE,
            "state_class": SensorStateClass.MEASUREMENT,
            "precision": 0,
            "icon": "mdi:fan",
        },
        {
            "key": "oil_box_cleanliness",
            "unit": PERCENTAGE,
            "state_class": SensorStateClass.MEASUREMENT,
            "precision": 0,
            "icon": "mdi:oil",
        },
        {
            "key": "filter_cleanliness",
            "unit": PERCENTAGE,
            "state_class": SensorStateClass.MEASUREMENT,
            "precision": 0,
            "icon": "mdi:air-filter",
        }
    ],
    0xAC: [
        {
            "key": "yesterday_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 2,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "monthly_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 2,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "yearly_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        }
    ],
    0xD9: [
        {
            "key": "today_energy_consumption_b",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "today_water_consumption_b",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "weekly_energy_consumption_b",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "weekly_water_consumption_b",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "monthly_energy_consumption_b",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "monthly_water_consumption_b",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "today_energy_consumption_l",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "today_water_consumption_l",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "weekly_energy_consumption_l",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "weekly_water_consumption_l",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "monthly_energy_consumption_l",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "monthly_water_consumption_l",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "today_energy_consumption_r",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "today_water_consumption_r",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "weekly_energy_consumption_r",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "weekly_water_consumption_r",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "monthly_energy_consumption_r",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "monthly_water_consumption_r",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        }
    ],
    0xDB: [
        {
            "key": "today_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "today_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "weekly_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "weekly_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "monthly_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "monthly_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        }
    ],
    0xE1: [
        {
            "key": "today_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "today_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "weekly_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "weekly_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "monthly_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "monthly_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        },
        {
            "key": "yearly_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "yearly_energy_consumption",
            "device_class": SensorDeviceClass.ENERGY,
            "unit": UnitOfEnergy.KILO_WATT_HOUR,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:lightning-bolt",
        }
    ],
    0xE3: [
        {
            "key": "today_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "today_gas_consumption",
            "device_class": SensorDeviceClass.GAS,
            "unit": UnitOfVolume.CUBIC_METERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:fire",
        },
        {
            "key": "monthly_water_consumption",
            "device_class": SensorDeviceClass.WATER,
            "unit": UnitOfVolume.LITERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 1,
            "icon": "mdi:water",
        },
        {
            "key": "monthly_gas_consumption",
            "device_class": SensorDeviceClass.GAS,
            "unit": UnitOfVolume.CUBIC_METERS,
            "state_class": SensorStateClass.TOTAL,
            "precision": 3,
            "icon": "mdi:fire",
        }
    ]
}
