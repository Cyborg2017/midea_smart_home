"""Aggregated Home Assistant imports shared by all device_mapping submodules.

Every T0x*.py file in this package pulls its HA symbols from here via
`from ._common import *`, so the set of imports lives in one place. Add a new
HA symbol here once and every device mapping gets it; remove one here when no
file references it anymore.
"""
from homeassistant.const import (
    PERCENTAGE,
    Platform,
    PRECISION_HALVES,
    PRECISION_WHOLE,
    UnitOfArea,
    UnitOfDensity,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfPressure,
    UnitOfRatio,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.humidifier import HumidifierDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.switch import SwitchDeviceClass

__all__ = [
    # homeassistant.const
    "Platform",
    "PERCENTAGE",
    "PRECISION_HALVES",
    "PRECISION_WHOLE",
    "UnitOfArea",
    "UnitOfDensity",
    "UnitOfElectricPotential",
    "UnitOfEnergy",
    "UnitOfPower",
    "UnitOfPressure",
    "UnitOfRatio",
    "UnitOfTemperature",
    "UnitOfTime",
    "UnitOfVolume",
    "UnitOfVolumeFlowRate",
    # homeassistant.components.*
    "BinarySensorDeviceClass",
    "HumidifierDeviceClass",
    "SensorDeviceClass",
    "SensorStateClass",
    "SwitchDeviceClass",
]
