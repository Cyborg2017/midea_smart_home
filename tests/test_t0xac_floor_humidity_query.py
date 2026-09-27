"""Regression tests for floor AC humidity polling."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from types import ModuleType
import unittest


class _EnumMeta(type):
    def __getattr__(cls, name):
        return name.lower()


class _Values(metaclass=_EnumMeta):
    pass


def _load_mapping_module():
    common = ModuleType("custom_components.midea_smart_home.device_mapping._common")
    enum_names = {
        "Platform",
        "UnitOfArea",
        "UnitOfElectricCurrent",
        "UnitOfElectricPotential",
        "UnitOfEnergy",
        "UnitOfFrequency",
        "UnitOfPower",
        "UnitOfPressure",
        "UnitOfTemperature",
        "UnitOfTime",
        "UnitOfVolume",
        "UnitOfVolumeFlowRate",
        "BinarySensorDeviceClass",
        "HumidifierDeviceClass",
        "SensorDeviceClass",
        "SensorStateClass",
        "SwitchDeviceClass",
    }
    scalar_names = {
        "PERCENTAGE",
        "PRECISION_HALVES",
        "PRECISION_WHOLE",
        "CONCENTRATION_MICROGRAMS_PER_CUBIC_METER",
        "CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER",
        "CONCENTRATION_PARTS_PER_MILLION",
    }
    setattr(common, "__all__", sorted(enum_names | scalar_names))
    for name in enum_names:
        setattr(common, name, _Values)
    for name in scalar_names:
        setattr(common, name, name.lower())
    sys.modules[common.__name__] = common

    path = (
        Path(__file__).parents[1]
        / "custom_components/midea_smart_home/device_mapping/T0xAC.py"
    )
    spec = spec_from_file_location("test_midea_mapping.T0xAC", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load mapping module from {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestFloorAcHumidityQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        module = _load_mapping_module()
        cls.mapping = module.DEVICE_MAPPING["default_floor_air_conditioner"]

    def test_humidity_is_queried_initially(self):
        self.assertIn({"indoor_humidity"}, self.mapping["initial_query"])

    def test_humidity_is_queried_while_polling(self):
        self.assertIn({"indoor_humidity"}, self.mapping["polling_query"])


if __name__ == "__main__":
    unittest.main()
