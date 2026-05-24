"""Midea Smart Home Device Discovery."""

import logging
import select
import socket
import time
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

DISCOVERY_TIMEOUT = 8.0
DISCOVERY_RETRIES = 5
DISCOVERY_INTERVAL = 2.0
DISCOVERY_PORTS = [6445, 20086]

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

def _get_broadcast_addresses() -> list:
    nets = []
    adapters = ifaddr.get_adapters()
    for adapter in adapters:
        for ip in adapter.ips:
            if ip.is_IPv4 and ip.network_prefix < 32:
                local_network = IPv4Network(f"{ip.ip}/{ip.network_prefix}", strict=False)
                if (
                    local_network.is_private
                    and not local_network.is_loopback
                    and not local_network.is_link_local
                ):
                    addr = str(local_network.broadcast_address)
                    if addr not in nets:
                        nets.append(addr)
    return nets

def _parse_v1_response(data: bytes, addr: tuple) -> dict | None:
    try:
        root = ElementTree.fromstring(data.decode(encoding="utf-8", errors="replace"))
        child = root.find("body/device")
        if not child:
            return None
        m = child.attrib
        device_id = int(m.get("apc_sn", "0")[-8:], 16)
        device_type = int(m.get("apc_type", "0"), 16)
        sn = m.get("apc_sn", "")
        sn8 = sn[9:17] if len(sn) > 17 else ""
        return {
            CONF_DEVICE_ID: device_id,
            CONF_IP: addr[0],
            CONF_DEVICE_TYPE: device_type,
            CONF_SN: sn,
            CONF_SN8: sn8,
            CONF_PROTOCOL: ProtocolVersion.V1,
        }
    except Exception:
        return None

def _parse_v2_v3_response(data: bytes, addr: tuple, security: LocalSecurity) -> dict | None:
    if data[:2].hex() == "8370" and data[8:10].hex() == "5a5a":
        protocol = ProtocolVersion.V3
        inner_data = data[8:-16] if len(data) > 24 else data[8:]
    elif data[:2].hex() == "5a5a":
        msg_type = data[2:4].hex()
        if msg_type == "0110":
            return _parse_0110_response(data, addr)
        protocol = ProtocolVersion.V2
        inner_data = data
    else:
        return None

    device_id = int.from_bytes(inner_data[20:26], "little")
    encrypt_data = inner_data[40:-16]
    if len(encrypt_data) < 16:
        return None

    reply = security.aes_decrypt(encrypt_data)
    if len(reply) < 41:
        return None

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

    return {
        CONF_DEVICE_ID: device_id,
        CONF_IP: addr[0],
        CONF_DEVICE_TYPE: device_type,
        CONF_SN: sn,
        CONF_SN8: sn8,
        CONF_PROTOCOL: protocol,
    }

def _parse_0110_response(data: bytes, addr: tuple) -> dict | None:
    if len(data) < 120:
        return None

    try:
        device_id = int.from_bytes(data[16:22], "little")

        ssid_raw = data[81:]
        ssid_end = ssid_raw.find(b'\x00')
        if ssid_end >= 0:
            ssid = ssid_raw[:ssid_end].decode("utf-8", errors="ignore")
        else:
            ssid = ssid_raw[:32].decode("utf-8", errors="ignore")

        device_type = int.from_bytes(data[108:110], "little")

        sn8 = ""
        if "_" in ssid:
            try:
                sn8 = ssid.split("_")[-1][:8]
            except (IndexError, ValueError):
                pass

        _LOGGER.warning(
            "Device %s (type=0x%02X) at %s uses V2 protocol variant 0x0110. "
            "This format is recognized but TCP communication is not yet supported.",
            ssid, device_type, addr[0]
        )

        return {
            CONF_DEVICE_ID: device_id,
            CONF_IP: addr[0],
            CONF_DEVICE_TYPE: device_type,
            CONF_SN: ssid,
            CONF_SN8: sn8,
            CONF_PROTOCOL: ProtocolVersion.V2,
        }
    except Exception:
        return None

def _parse_scan_address(scan_address: str) -> list:
    if not scan_address or scan_address.lower() == "auto":
        return None

    parts = scan_address.strip().split(".")
    if len(parts) != 4:
        _LOGGER.warning("Invalid scan address format: %s, using auto detection", scan_address)
        return None

    try:
        octets = [int(p) for p in parts]
        if not all(0 <= o <= 255 for o in octets):
            return None

        broadcast_addr = f"{octets[0]}.{octets[1]}.{octets[2]}.255"
        if octets[3] == 1 or octets[3] == 255:
            return [broadcast_addr]
        else:
            return [scan_address]
    except ValueError:
        return None

def discover_devices(timeout: float = DISCOVERY_TIMEOUT, scan_address: str = "auto") -> dict:
    target_addresses = _parse_scan_address(scan_address)
    if target_addresses is None:
        nets = _get_broadcast_addresses()
    else:
        nets = target_addresses

    if not nets:
        _LOGGER.warning("No valid network interfaces found for discovery")
        return {}

    _LOGGER.debug("Broadcast addresses: %s", nets)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setblocking(False)

    devices = {}
    security = LocalSecurity()
    start_time = time.time()

    def send_broadcast():
        for addr in nets:
            for port in DISCOVERY_PORTS:
                try:
                    sock.sendto(BROADCAST_MSG, (addr, port))
                except (socket.error, OSError) as e:
                    _LOGGER.debug("Send to %s:%d failed: %s", addr, port, e)

    def receive_responses():
        while True:
            try:
                ready = select.select([sock], [], [], 0.1)
                if not ready[0]:
                    break
                data, addr = sock.recvfrom(512)
                if len(data) < 40:
                    continue

                device_info = None
                if data[:6].hex() == "3c3f786d6c20":
                    device_info = _parse_v1_response(data, addr)
                else:
                    device_info = _parse_v2_v3_response(data, addr, security)

                if device_info is None:
                    continue

                device_id = device_info[CONF_DEVICE_ID]
                if device_id in devices:
                    continue

                if device_info[CONF_PROTOCOL] == ProtocolVersion.V1:
                    protocol_name = "V1"
                elif device_info[CONF_PROTOCOL] == ProtocolVersion.V2:
                    protocol_name = "V2"
                else:
                    protocol_name = "V3"
                _LOGGER.debug(
                    "Found device %d (%s) at %s, type=0x%x",
                    device_id, protocol_name, addr[0], device_info[CONF_DEVICE_TYPE]
                )
                devices[device_id] = device_info
            except (socket.error, OSError):
                break

    send_broadcast()
    last_broadcast_time = time.time()

    while time.time() - start_time < timeout:
        receive_responses()

        elapsed = time.time() - last_broadcast_time
        if elapsed >= DISCOVERY_INTERVAL:
            retry_count = int((time.time() - start_time) / DISCOVERY_INTERVAL)
            if retry_count < DISCOVERY_RETRIES:
                send_broadcast()
                last_broadcast_time = time.time()

    sock.close()
    _LOGGER.info("Discovery completed, found %d devices", len(devices))
    return devices
