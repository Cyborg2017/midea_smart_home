"""Aggregated Home Assistant imports shared by all device_mapping submodules.

Every T0x*.py file in this package pulls its HA symbols from here via
`from ._common import *`, so the set of imports lives in one place. Add a new
HA symbol here once and every device mapping gets it; remove one here when no
file references it anymore.

HA version-compatibility shim for `UnitOfDensity` / `UnitOfRatio` (added in
HA 2026.7, replacing the legacy `CONCENTRATION_*` string constants scheduled
for removal in HA Core 2027.7+) is also exposed here as the legacy
`CONCENTRATION_*` names -- bound to the new enums on HA >= 2026.7, or to the
legacy constants otherwise. Both resolve to identical string values, so
device_mapping code can reference the stable `CONCENTRATION_*` names regardless
of HA version.
"""
from homeassistant.const import (
    MAJOR_VERSION,
    MINOR_VERSION,
    PERCENTAGE,
    Platform,
    PRECISION_HALVES,
    PRECISION_WHOLE,
    UnitOfArea,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.humidifier import HumidifierDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.switch import SwitchDeviceClass

if (MAJOR_VERSION, MINOR_VERSION) >= (2026, 7):
    from homeassistant.const import (  # pylint: disable=E0611
        UnitOfDensity,
        UnitOfRatio,
    )

    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER = UnitOfDensity.MICROGRAMS_PER_CUBIC_METER
    CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER = UnitOfDensity.MILLIGRAMS_PER_CUBIC_METER
    CONCENTRATION_PARTS_PER_MILLION = UnitOfRatio.PARTS_PER_MILLION
else:
    from homeassistant.const import (  # type: ignore[no-redef]
        CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER,
        CONCENTRATION_PARTS_PER_MILLION,
    )

__all__ = [
    # homeassistant.const
    "Platform",
    "PERCENTAGE",
    "PRECISION_HALVES",
    "PRECISION_WHOLE",
    "UnitOfArea",
    "UnitOfElectricPotential",
    "UnitOfEnergy",
    "UnitOfPower",
    "UnitOfPressure",
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
    # version-compat concentration units
    "CONCENTRATION_MICROGRAMS_PER_CUBIC_METER",
    "CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER",
    "CONCENTRATION_PARTS_PER_MILLION",
]
