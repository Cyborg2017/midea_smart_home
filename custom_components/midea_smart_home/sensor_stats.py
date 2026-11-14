"""Cloud statistics sensor definitions.

These sensors are independent of the LAN device state and are fetched by
MideaCloudStatsCoordinator.
"""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfEnergy, UnitOfVolume

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
            "key": "today_energy_consumption",
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
    ]
}
