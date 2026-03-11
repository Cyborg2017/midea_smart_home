"""Midea Smart Home Device Discovery."""

import logging
import socket
from ipaddress import IPv4Network
import ifaddr
from defusedxml import ElementTree

from ..const import (
    CONF_DEVICE_ID,
    CONF_DEVICE_TYPE,
    CONF_IP,
    CONF_PROTOCOL,
    CONF_SN,
    CONF_SN8,
    ProtocolVersion,
)
from .security import LocalSecurity

_LOGGER = logging.getLogger(__name__)

DISCOVERY_TIMEOUT = 3.0
DISCOVERY_RETRIES = 10
DISCOVERY_PORTS = [6445, 20086]

def discover_devices(timeout: float = DISCOVERY_TIMEOUT) -> dict:
    BROADCAST_MSG = bytes([
        0x5A, 0x5A, 0x01, 0x11, 0x48, 0x00, 0x92, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x7F, 0x75, 0xBD, 0x6B, 0x3E, 0x4F, 0x8B, 0x76,
        0x2E, 0x84, 0x9C, 0x6E, 0x57, 0x8D, 0x65, 0x90,
        0x03, 0x6E, 0x9D, 0x43, 0x42, 0xA5, 0x0F, 0x1F,
        0x56, 0x9E, 0xB8, 0xEC, 0x91, 0x8E, 0x92, 0xE5,
    ])

    nets = []
    adapters = ifaddr.get_adapters()
    for adapter in adapters:
        for ip in adapter.ips:
            if ip.is_IPv4 and ip.network_prefix < 32:
                local_network = IPv4Network(f"{ip.ip}/{ip.network_prefix}", strict=False)
                if local_network.is_private and not local_network.is_loopback:
                    addr = str(local_network.broadcast_address)
                    if addr not in nets:
                        nets.append(addr)

    if not nets:
        return {}

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    for _ in range(DISCOVERY_RETRIES):
        for addr in nets:
            for port in DISCOVERY_PORTS:
                try:
                    sock.sendto(BROADCAST_MSG, (addr, port))
                except (socket.error, OSError):
                    pass

    devices = {}
    security = LocalSecurity()

    while True:
        try:
            data, addr = sock.recvfrom(512)
            if len(data) < 40:
                continue

            protocol = None
            inner_data = None

            if data[:2].hex() == "8370" and data[8:10].hex() == "5a5a":
                protocol = ProtocolVersion.V3
                inner_data = data[8:-16] if len(data) > 24 else data[8:]
            elif data[:2].hex() == "5a5a":
                protocol = ProtocolVersion.V2
                inner_data = data
            elif data[:6].hex() == "3c3f786d6c20":
                protocol = ProtocolVersion.V1
                try:
                    root = ElementTree.fromstring(
                        data.decode(encoding="utf-8", errors="replace")
                    )
                    child = root.find("body/device")
                    if not child:
                        continue
                    m = child.attrib
                    device_id = int(m.get("apc_sn", "0")[-8:], 16)
                    if device_id in devices:
                        continue
                    device_type = int(m.get("apc_type", "0"), 16)
                    port = int(m.get("port", "6444"))
                    sn = m.get("apc_sn", "")
                    sn8 = sn[9:17] if len(sn) > 17 else ""
                    devices[device_id] = {
                        CONF_DEVICE_ID: device_id,
                        CONF_IP: addr[0],
                        CONF_DEVICE_TYPE: device_type,
                        CONF_SN: sn,
                        CONF_SN8: sn8,
                        CONF_PROTOCOL: protocol,
                    }
                    continue
                except Exception:
                    continue
            else:
                continue

            if inner_data is None:
                continue

            device_id = int.from_bytes(inner_data[20:26], "little")
            if device_id in devices:
                continue

            encrypt_data = inner_data[40:-16]
            if len(encrypt_data) < 16:
                continue

            reply = security.aes_decrypt(encrypt_data)
            if len(reply) < 41:
                continue

            sn = reply[8:40].decode("utf-8", errors="ignore").rstrip('\x00')
            ssid_len = reply[40]
            ssid = reply[41:41+ssid_len].decode("utf-8", errors="ignore")

            sn8 = sn[9:17] if len(sn) > 17 else ""

            device_type = 0
            if "_" in ssid:
                type_str = ssid.split("_")[1]
                try:
                    device_type = int(type_str, 16)
                except ValueError:
                    pass

            devices[device_id] = {
                CONF_DEVICE_ID: device_id,
                CONF_IP: addr[0],
                CONF_DEVICE_TYPE: device_type,
                CONF_SN: sn,
                CONF_SN8: sn8,
                CONF_PROTOCOL: protocol,
            }
        except socket.timeout:
            break
        except (socket.error, OSError):
            continue

    sock.close()
    return devices
