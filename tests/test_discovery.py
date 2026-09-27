"""Regression tests for Midea LAN discovery."""

from enum import IntEnum
import importlib.util
from ipaddress import IPv4Network
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DISCOVERY_PATH = (
    REPOSITORY_ROOT
    / "custom_components"
    / "midea_smart_home"
    / "midea_lib"
    / "discovery.py"
)


def _load_discovery_module():
    """Load discovery.py without requiring a Home Assistant installation."""
    package_names = (
        "custom_components",
        "custom_components.midea_smart_home",
        "custom_components.midea_smart_home.midea_lib",
    )
    for package_name in package_names:
        package = types.ModuleType(package_name)
        package.__path__ = []
        sys.modules[package_name] = package

    ifaddr = types.ModuleType("ifaddr")
    ifaddr.get_adapters = lambda: []
    sys.modules["ifaddr"] = ifaddr

    defusedxml = types.ModuleType("defusedxml")
    defusedxml.ElementTree = types.SimpleNamespace()
    sys.modules["defusedxml"] = defusedxml

    class ProtocolVersion(IntEnum):
        V1 = 1
        V2 = 2
        V3 = 3

    const = types.ModuleType("custom_components.midea_smart_home.const")
    for name, value in {
        "CONF_DEVICE_ID": "device_id",
        "CONF_DEVICE_TYPE": "device_type",
        "CONF_IP": "ip",
        "CONF_PROTOCOL": "protocol",
        "CONF_SN": "sn",
        "CONF_SN8": "sn8",
        "CONF_UDPID": "udpid",
        "ProtocolVersion": ProtocolVersion,
    }.items():
        setattr(const, name, value)
    sys.modules[const.__name__] = const

    security = types.ModuleType(
        "custom_components.midea_smart_home.midea_lib.security"
    )
    security.LocalSecurity = object
    sys.modules[security.__name__] = security

    module_name = "custom_components.midea_smart_home.midea_lib.discovery"
    spec = importlib.util.spec_from_file_location(module_name, DISCOVERY_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


discovery = _load_discovery_module()


class FakeSocket:
    """Capture discovery destinations without opening a network socket."""

    def __init__(self):
        self.destinations = []

    def setsockopt(self, *args):
        pass

    def bind(self, *args):
        pass

    def setblocking(self, *args):
        pass

    def sendto(self, payload, destination):
        self.destinations.append(destination)

    def close(self):
        pass


class DiscoveryTests(unittest.TestCase):
    def test_unicast_explicit_ip_does_not_scan_local_interfaces(self):
        sock = FakeSocket()

        def fail_local_network_lookup():
            raise AssertionError(
                "an explicit unicast target must not inspect local interfaces"
            )

        with (
            patch.object(discovery.socket, "socket", return_value=sock),
            patch.object(
                discovery, "_get_local_networks", fail_local_network_lookup
            ),
            patch.object(discovery, "UNICAST_SCAN_TIMEOUT", 0),
        ):
            devices = discovery.discover_devices(
                timeout=0,
                scan_address="10.20.30.40",
                scan_mode="unicast",
            )

        self.assertEqual({}, devices)
        self.assertEqual(
            [("10.20.30.40", port) for port in discovery.DISCOVERY_PORTS],
            sock.destinations,
        )

    def test_unicast_router_address_scans_only_explicit_subnet(self):
        sock = FakeSocket()

        def fail_local_network_lookup():
            raise AssertionError(
                "an explicit subnet must not inspect local interfaces"
            )

        with (
            patch.object(discovery.socket, "socket", return_value=sock),
            patch.object(
                discovery, "_get_local_networks", fail_local_network_lookup
            ),
            patch.object(discovery, "UNICAST_SCAN_TIMEOUT", 0),
        ):
            devices = discovery.discover_devices(
                timeout=0,
                scan_address="10.20.30.1",
                scan_mode="unicast",
            )

        self.assertEqual({}, devices)
        self.assertEqual(254 * len(discovery.DISCOVERY_PORTS), len(sock.destinations))
        self.assertEqual(("10.20.30.1", 6445), sock.destinations[0])
        self.assertEqual(("10.20.30.254", 20086), sock.destinations[-1])
        self.assertNotIn(("10.20.30.255", 6445), sock.destinations)

    def test_unicast_auto_still_scans_local_interfaces(self):
        sock = FakeSocket()

        with (
            patch.object(discovery.socket, "socket", return_value=sock),
            patch.object(
                discovery,
                "_get_broadcast_addresses",
                return_value=["10.20.30.255"],
            ),
            patch.object(
                discovery,
                "_get_local_networks",
                return_value=[IPv4Network("10.20.30.0/30")],
            ),
            patch.object(discovery, "UNICAST_SCAN_TIMEOUT", 0),
        ):
            devices = discovery.discover_devices(
                timeout=0,
                scan_address="auto",
                scan_mode="unicast",
            )

        self.assertEqual({}, devices)
        self.assertEqual(
            [
                (host, port)
                for host in ("10.20.30.1", "10.20.30.2")
                for port in discovery.DISCOVERY_PORTS
            ],
            sock.destinations,
        )

    def test_broadcast_auto_falls_back_to_local_unicast(self):
        sock = FakeSocket()

        with (
            patch.object(discovery.socket, "socket", return_value=sock),
            patch.object(
                discovery,
                "_get_broadcast_addresses",
                return_value=["10.20.30.255"],
            ),
            patch.object(
                discovery,
                "_get_local_networks",
                return_value=[IPv4Network("10.20.30.0/30")],
            ),
            patch.object(discovery, "UNICAST_SCAN_TIMEOUT", 0),
        ):
            devices = discovery.discover_devices(
                timeout=0,
                scan_address="auto",
                scan_mode="broadcast",
            )

        self.assertEqual({}, devices)
        self.assertEqual(
            [
                (host, port)
                for host in (
                    "10.20.30.255",
                    "10.20.30.1",
                    "10.20.30.2",
                )
                for port in discovery.DISCOVERY_PORTS
            ],
            sock.destinations,
        )


if __name__ == "__main__":
    unittest.main()
