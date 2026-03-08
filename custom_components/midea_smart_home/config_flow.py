import base64
import json
import logging
import socket
from ipaddress import IPv4Network
from pathlib import Path
from typing import Any

import ifaddr
import lupa.lua51
import voluptuous as vol
from aiohttp import ClientSession
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    BIT_LUA,
    CJSON_LUA,
    CONF_ACCOUNT,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_IP,
    CONF_KEY,
    CONF_LUA_FILE,
    CONF_MANUFACTURER_CODE,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_SN,
    CONF_SN8,
    CONF_PRODUCT_MODEL,
    CONF_MODEL_NUMBER,
    CONF_TOKEN,
    DEFAULT_PORT,
    DEVICE_TYPES,
    DOMAIN,
    JSON_FILES_PATH,
    LUA_COMMON_PATH,
    LUA_DEVICE_PATH,
    ProtocolVersion,
)
from .midea_lib.packet_builder import PacketBuilder

_LOGGER = logging.getLogger(__name__)

DISCOVERY_TIMEOUT = 3.0
DISCOVERY_RETRIES = 10
DISCOVERY_PORTS = [6445, 20086]

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_ACCOUNT): str,
    vol.Required(CONF_PASSWORD): str,
})

def _write_lua_file(file_path: Path, content: str) -> bool:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError as e:
        _LOGGER.error("Error writing Lua file %s: %s", file_path, e)
        return False

def get_lua_storage_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / LUA_DEVICE_PATH

def get_lua_common_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / LUA_COMMON_PATH

def get_lua_file_path(hass_config_dir: str, device_id: int, device_type: int, sn8: str = "") -> Path:
    if sn8:
        return get_lua_storage_path(hass_config_dir) / f"{device_id}_T0x{hex(device_type)[2:].upper()}_{sn8}.lua"
    return get_lua_storage_path(hass_config_dir) / f"{device_id}_T0x{hex(device_type)[2:]}.lua"

def get_json_files_path(hass_config_dir: str) -> Path:
    return Path(hass_config_dir) / JSON_FILES_PATH

def get_device_json_path(hass_config_dir: str, device_id: int, device_type: int, sn8: str = "") -> Path:
    if sn8:
        return get_json_files_path(hass_config_dir) / f"{device_id}_T0x{hex(device_type)[2:].upper()}_{sn8}.json"
    return get_json_files_path(hass_config_dir) / f"{device_id}_T0x{hex(device_type)[2:]}.json"

def discover_devices(timeout: float = DISCOVERY_TIMEOUT) -> dict:
    from .midea_lib.security import LocalSecurity
    from defusedxml import ElementTree
    
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

class MideaLocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    
    def __init__(self):
        self._discovered_devices: dict = {}
        self._selected_devices: list = []
        self._current_device_index: int = 0
        self._devices_data: list = []
        self._account: str = None
        self._password: str = None
        self._session: ClientSession = None
        self._preset_cloud = None
        self._user_cloud = None
        self._existing_entry: config_entries.ConfigEntry | None = None
        self._cloud_devices: dict = {}

    async def _cleanup_session(self):
        if self._session:
            await self._session.close()
            self._session = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors = {}
        
        if user_input is not None:
            self._account = user_input.get(CONF_ACCOUNT)
            self._password = user_input.get(CONF_PASSWORD)
            
            existing_entries = self.hass.config_entries.async_entries(DOMAIN)
            for entry in existing_entries:
                if entry.title == f"Midea | {self._account}":
                    self._existing_entry = entry
                    self._devices_data = list(entry.data.get("devices", []))
                    break
            
            return await self.async_step_discover()
        
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "note": "请输入美的美居账号密码，用于下载设备 Lua 文件"
            },
        )

    async def async_step_discover(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        self._discovered_devices = await self.hass.async_add_executor_job(
            discover_devices, DISCOVERY_TIMEOUT
        )
        
        if not self._discovered_devices:
            return self.async_show_form(
                step_id="discover",
                errors={"base": "no_devices_found"},
                description_placeholders={"note": "局域网中未发现设备"},
            )
        
        self._session = ClientSession()
        
        try:
            from .midea_lib.cloud import get_midea_cloud, get_preset_account_cloud
            
            preset = get_preset_account_cloud()
            self._preset_cloud = get_midea_cloud(
                cloud_name=preset["cloud_name"],
                session=self._session,
                account=preset["username"],
                password=preset["password"],
            )
            
            if not await self._preset_cloud.login():
                _LOGGER.warning("Preset cloud login failed")
            
            self._user_cloud = get_midea_cloud(
                cloud_name="美的美居",
                session=self._session,
                account=self._account,
                password=self._password,
            )
            
            if not await self._user_cloud.login():
                _LOGGER.warning("User account login failed")
                await self._cleanup_session()
                return self.async_abort(reason="auth_failed")
            
            _LOGGER.info("Cloud login success")
            
            self._cloud_devices = await self._user_cloud.list_appliances(home_id=None) or {}
            _LOGGER.info("Cloud devices list: %s", self._cloud_devices)
            
            lua_common_dir = get_lua_common_path(self.hass.config.config_dir)
            await self._download_common_lua_files(lua_common_dir)
            
        except (json.JSONDecodeError, OSError) as err:
            _LOGGER.error("Failed to login to cloud: %s", err)
            await self._cleanup_session()
            return self.async_abort(reason="auth_failed")
        
        device_options = {}
        
        for did, info in self._discovered_devices.items():
            cloud_device = self._cloud_devices.get(did, {})
            device_name = cloud_device.get("name", DEVICE_TYPES.get(info[CONF_DEVICE_TYPE], f"T0x{info[CONF_DEVICE_TYPE]:02X}"))
            device_options[str(did)] = f"{device_name} ( {info[CONF_IP]} )"
        
        return self.async_show_form(
            step_id="select_device",
            data_schema=vol.Schema({
                vol.Required("devices"): cv.multi_select(device_options),
            }),
        )

    async def async_step_select_device(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is None:
            return self.async_abort(reason="no_devices_selected")
        
        selected = user_input.get("devices", [])
        if not selected:
            return self.async_abort(reason="no_devices_selected")
        
        self._selected_devices = [
            self._discovered_devices[int(did)]
            for did in selected
        ]
        self._current_device_index = 0
        
        return await self.async_step_get_token()

    def _save_device_to_json(self, device_data: dict):
        """Save device data to JSON file."""
        try:
            json_dir = get_json_files_path(self.hass.config.config_dir)
            json_dir.mkdir(parents=True, exist_ok=True)
            
            device_id = device_data.get(CONF_DEVICE_ID)
            device_type_str = device_data.get(CONF_DEVICE_TYPE)
            sn8 = device_data.get(CONF_SN8, "")
            
            if not device_id or not device_type_str:
                return
            
            # Convert device_type from string to integer
            try:
                device_type = int(device_type_str, 16)
            except ValueError:
                _LOGGER.error("Invalid device type format: %s", device_type_str)
                return
            
            json_path = get_device_json_path(self.hass.config.config_dir, device_id, device_type, sn8)
            
            # Read existing data if file exists
            existing_data = {}
            if json_path.exists():
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                except (json.JSONDecodeError, OSError) as e:
                    _LOGGER.error("Failed to read existing JSON file: %s", e)
            
            # Update with new data
            existing_data.update(device_data)
            
            # Write back to file
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
            _LOGGER.info("Saved device data to JSON file: %s", json_path)
        except (json.JSONEncodeError, OSError) as e:
            _LOGGER.error("Failed to save device data to JSON file: %s", e)

    async def async_step_get_token(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if self._current_device_index >= len(self._selected_devices):
            await self._cleanup_session()
            
            if self._devices_data:
                if self._existing_entry:
                    existing_data = dict(self._existing_entry.data)
                    existing_data["devices"] = self._devices_data
                    if CONF_ACCOUNT not in existing_data:
                        existing_data[CONF_ACCOUNT] = self._account
                        existing_data[CONF_PASSWORD] = self._password
                    self.hass.config_entries.async_update_entry(
                        self._existing_entry,
                        data=existing_data,
                    )
                    await self.hass.config_entries.async_reload(self._existing_entry.entry_id)
                    return self.async_abort(reason="devices_updated")
                return self.async_create_entry(
                    title=f"Midea | {self._account}",
                    data={
                        "devices": self._devices_data,
                        CONF_ACCOUNT: self._account,
                        CONF_PASSWORD: self._password,
                    },
                )
            return self.async_abort(reason="no_devices")
        
        current_device = self._selected_devices[self._current_device_index]
        device_id = current_device[CONF_DEVICE_ID]
        protocol = current_device.get(CONF_PROTOCOL, ProtocolVersion.V3)
        # Ensure protocol has a valid value (V1, V2, or V3), default to V3 if None
        if protocol is None:
            protocol = ProtocolVersion.V3
        is_v3 = protocol == ProtocolVersion.V3
        
        if user_input is not None:
            lua_file = user_input.get(CONF_LUA_FILE, "")
            token = user_input.get(CONF_TOKEN, "")
            key = user_input.get(CONF_KEY, "")
            device_type = current_device.get(CONF_DEVICE_TYPE)
            sn = current_device.get(CONF_SN, "")
            sn8 = current_device.get(CONF_SN8, "")
            
            if not lua_file or (is_v3 and (not token or not key)):
                return self._show_token_form(
                    current_device, device_id, protocol, token, key, lua_file,
                    error="请填写所有必填项" if is_v3 else "请填写 Lua 文件路径"
                )
            
            from .device import MideaCodec, DeviceController
            lua_common_dir = Path(self.hass.config.config_dir) / LUA_COMMON_PATH
            ip_address = current_device[CONF_IP]
            
            def validate_device():
                try:
                    if not lua_file or not lua_file.strip():
                        return False, "请填写 Lua 文件路径"
                    
                    lua_path = Path(lua_file)
                    if not lua_path.exists():
                        return False, f"Lua 文件不存在：{lua_file}"
                    
                    _LOGGER.info("Validating device %s with lua: %s, protocol: %s", device_id, lua_file, protocol)
                    codec = MideaCodec(lua_file, str(lua_common_dir), sn=sn, subtype=0, device_type=device_type, sn8=sn8)
                    
                    query_hex = codec.build_query()
                    if not query_hex:
                        return False, "设备不支持本地控制：无法构建查询命令"
                    
                    import socket as socket_module
                    
                    try:
                        test_sock = socket_module.socket(socket_module.AF_INET, socket_module.SOCK_STREAM)
                        test_sock.settimeout(3)
                        test_sock.connect((ip_address, DEFAULT_PORT))
                        test_sock.close()
                    except socket_module.timeout:
                        return False, "连接超时：设备可能不在线或网络不通"
                    except ConnectionRefusedError:
                        return False, "连接被拒绝：设备端口未开放或不支持本地控制"
                    except OSError as e:
                        if "No route to host" in str(e) or "Network is unreachable" in str(e):
                            return False, "网络不可达：请检查设备IP和网段"
                        elif "Host is down" in str(e):
                            return False, "设备离线：设备已关机或网络断开"
                        else:
                            return False, f"网络错误：{str(e)}"
                    
                    if is_v3:
                        controller = DeviceController(
                            device_id=device_id,
                            ip_address=ip_address,
                            port=DEFAULT_PORT,
                            token=token,
                            key=key,
                            codec=codec,
                        )
                    else:
                        controller = DeviceController(
                            device_id=device_id,
                            ip_address=ip_address,
                            port=DEFAULT_PORT,
                            token="",
                            key="",
                            codec=codec,
                            protocol=protocol,
                        )
                    if not controller.connect():
                        _LOGGER.warning("Device %s validation failed: cannot connect", device_id)
                        return False, "认证失败：Token 或 Key 无效"
                    
                    try:
                        sock = controller._sock
                        security = controller._security
                        
                        data_bytes = bytes.fromhex(query_hex)
                        packet = PacketBuilder(device_id, data_bytes).finalize()
                        
                        if is_v3:
                            encrypted = security.encode_8370(bytes(packet), 0x6)
                            sock.send(encrypted)
                            response = sock.recv(512)
                            messages, _ = security.decode_8370(response)
                        else:
                            sock.send(packet)
                            response = sock.recv(512)
                            messages = []
                            if len(response) > 6:
                                msg_len = response[4] + (response[5] << 8)
                                if len(response) >= msg_len:
                                    messages = [response[:msg_len]]
                        
                        if messages and len(messages[0]) > 56:
                            encrypted_data = bytes(messages[0][40:-16])
                            decrypted = security.aes_decrypt(encrypted_data)
                            status = codec.decode_status(decrypted.hex())
                            if not status:
                                return False, "设备不支持本地控制：Lua脚本无法解析设备响应"
                            _LOGGER.info("Device %s status: %s", device_id, status)
                        else:
                            return False, "设备不支持本地控制：未收到有效响应"
                    except socket.timeout:
                        return False, "响应超时：设备未返回数据"
                    except Exception as e:
                        _LOGGER.warning("Device %s query test failed: %s", device_id, e)
                        return False, f"设备不支持本地控制：{str(e)}"
                    finally:
                        controller.close()
                    
                    _LOGGER.info("Device %s validation successful", device_id)
                    return True, None
                except lupa.lua51.LuaError as e:
                    _LOGGER.error("Device %s Lua error: %s", device_id, e)
                    return False, f"设备不支持本地控制：Lua脚本解析错误"
                except (socket.error, OSError, ValueError) as e:
                    _LOGGER.error("Device %s validation error: %s", device_id, e)
                    return False, str(e)
            
            valid, error_msg = await self.hass.async_add_executor_job(validate_device)
            if not valid:
                return self._show_token_form(
                    current_device, device_id, protocol, token, key, lua_file,
                    error=error_msg
                )
            
            device_data = {
                CONF_DEVICE_ID: device_id,
                CONF_IP: current_device[CONF_IP],
                CONF_PORT: DEFAULT_PORT,
                CONF_DEVICE_TYPE: hex(current_device.get(CONF_DEVICE_TYPE)),
                CONF_SN: sn,
                CONF_SN8: sn8,
                CONF_PRODUCT_MODEL: current_device.get(CONF_PRODUCT_MODEL, ""),
                CONF_MODEL_NUMBER: current_device.get(CONF_MODEL_NUMBER, ""),
                CONF_DEVICE_NAME: current_device.get(CONF_DEVICE_NAME, ""),
                CONF_MANUFACTURER_CODE: current_device.get(CONF_MANUFACTURER_CODE, "0000"),
                CONF_TOKEN: token if is_v3 else "",
                CONF_KEY: key if is_v3 else "",
                CONF_LUA_FILE: lua_file,
                CONF_PROTOCOL: protocol,
            }
            
            existing_index = next(
                (i for i, d in enumerate(self._devices_data) if d.get(CONF_DEVICE_ID) == device_id),
                None
            )
            if existing_index is not None:
                self._devices_data[existing_index] = device_data
            else:
                self._devices_data.append(device_data)
            
            await self.hass.async_add_executor_job(self._save_device_to_json, device_data)
            
            self._current_device_index += 1
            return await self.async_step_get_token()
        
        token = None
        key = None
        lua_file = None
        
        try:
            if is_v3 and self._preset_cloud:
                keys = await self._preset_cloud.get_cloud_keys(device_id)
                if keys:
                    method = list(keys.keys())[0]
                    token = keys[method]["token"]
                    key = keys[method]["key"]
                    _LOGGER.info("Got token/key for device %s", device_id)
            
            if self._user_cloud:
                cloud_device = self._cloud_devices.get(device_id, {})
                
                if cloud_device:
                    current_device[CONF_SN] = cloud_device.get("sn") or current_device.get(CONF_SN, "")
                    current_device[CONF_SN8] = cloud_device.get("sn8") or current_device.get(CONF_SN8, "")
                    current_device[CONF_PRODUCT_MODEL] = cloud_device.get("model") or current_device.get(CONF_PRODUCT_MODEL, "")
                    current_device[CONF_MODEL_NUMBER] = cloud_device.get("model_number") or current_device.get(CONF_MODEL_NUMBER, "")
                    current_device[CONF_DEVICE_NAME] = cloud_device.get("name") or current_device.get(CONF_DEVICE_NAME, "")
                    current_device[CONF_MANUFACTURER_CODE] = cloud_device.get("manufacturer_code") or current_device.get(CONF_MANUFACTURER_CODE, "0000")
                
                sn = current_device.get(CONF_SN, "")
                sn8 = current_device.get(CONF_SN8, "")
                model_number = current_device.get(CONF_MODEL_NUMBER)
                device_type = current_device.get(CONF_DEVICE_TYPE)
                manufacturer_code = current_device.get(CONF_MANUFACTURER_CODE, sn[:4] or "0000")
                
                lua_storage_dir = get_lua_storage_path(self.hass.config.config_dir)
                lua_storage_dir.mkdir(parents=True, exist_ok=True)
                
                lua_file = await self._download_lua_file(
                    self._user_cloud, device_id, device_type, sn, sn8, model_number, manufacturer_code, lua_storage_dir
                )
        except (socket.error, OSError, ValueError, json.JSONDecodeError) as err:
            _LOGGER.error("Failed to get token/key or lua: %s", err)
        
        device_type = current_device.get(CONF_DEVICE_TYPE)
        sn8 = current_device.get(CONF_SN8, "")
        lua_file_path = get_lua_file_path(self.hass.config.config_dir, device_id, device_type, sn8)
        
        if not lua_file and lua_file_path.exists():
            lua_file = str(lua_file_path)
        
        return self._show_token_form(
            current_device, device_id, protocol, token or "", key or "", lua_file or ""
        )
    
    def _show_token_form(
        self,
        current_device: dict,
        device_id: int,
        protocol: int,
        token: str,
        key: str,
        lua_file: str,
        error: str = ""
    ) -> FlowResult:
        is_v3 = protocol == ProtocolVersion.V3
        device_type = current_device.get(CONF_DEVICE_TYPE)
        sn8 = current_device.get(CONF_SN8, "")
        
        protocol_name = f"V{protocol}"
        device_name = current_device.get(CONF_DEVICE_NAME, DEVICE_TYPES.get(device_type, f"T0x{device_type:02X}"))
        model = current_device.get(CONF_PRODUCT_MODEL, "")
        
        # Build description with HTML line breaks for proper rendering
        description_parts = [
            f"设备名称：{device_name}",
            f"设备型号：{model if model else '未知'}",
            f"设备 ID: {device_id}",
            f"IP 地址：{current_device[CONF_IP]}",
            f"SN8: {sn8 if sn8 else '未知'}",
            f"协议版本：{protocol_name}",
        ]
        
        if error:
            description_parts.append(f"\n{error}")
        
        description = "\n".join(description_parts)
        
        if is_v3:
            data_schema = vol.Schema({
                vol.Required(CONF_TOKEN, default=token): str,
                vol.Required(CONF_KEY, default=key): str,
                vol.Required(CONF_LUA_FILE, default=lua_file): str,
            })
        else:
            data_schema = vol.Schema({
                vol.Optional(CONF_TOKEN, default=token): str,
                vol.Optional(CONF_KEY, default=key): str,
                vol.Required(CONF_LUA_FILE, default=lua_file): str,
            })
        
        return self.async_show_form(
            step_id="get_token",
            data_schema=data_schema,
            errors={"base": "lua_error"} if error else None,
            description_placeholders={
                "description": description,
                "progress": f"({self._current_device_index + 1}/{len(self._selected_devices)})",
                "token_required": "必填" if is_v3 else "选填 (V1/V2 设备不需要)",
                "key_required": "必填" if is_v3 else "选填 (V1/V2 设备不需要)",
            },
        )

    async def _download_lua_file(
        self, cloud, device_id: int, device_type: int, sn: str, sn8: str, model_number: str, manufacturer_code: str, storage_dir: Path
    ) -> str | None:
        def _format_lua_code(lua_code: str) -> str:
            """解密Lua代码 - 使用 all_in_one_getter.py 中的逻辑"""
            try:
                from Crypto.Cipher import AES
                from Crypto.Util.Padding import unpad
                
                fixed_key = format(10864842703515613082, 'x').encode("ascii")
                encrypted_bytes = bytes.fromhex(lua_code.strip())
                cipher = AES.new(fixed_key, AES.MODE_ECB)
                decrypted = unpad(cipher.decrypt(encrypted_bytes), len(fixed_key))
                return decrypted.decode("utf-8", errors="ignore")
            except (ValueError, OSError):
                return lua_code

        try:
            if sn8:
                lua_file_path = storage_dir / f"{device_id}_T0x{hex(device_type)[2:].upper()}_{sn8}.lua"
            else:
                lua_file_path = storage_dir / f"{device_id}_T0x{hex(device_type)[2:]}.lua"
            
            if lua_file_path.exists():
                _LOGGER.info("Lua file already exists: %s", lua_file_path)
                return str(lua_file_path)
            
            manufacturer_codes = [manufacturer_code]
            if manufacturer_code != "0000":
                manufacturer_codes.append("0000")
            if manufacturer_code != "2130":
                manufacturer_codes.append("2130")
            
            for mf_code in manufacturer_codes:
                _LOGGER.info(
                    "Downloading Lua for device_type=0x%s, sn=%s, manufacturer_code=%s",
                    hex(device_type)[2:], sn, mf_code
                )
                
                # 直接使用 all_in_one_getter.py 中的下载逻辑，不通过 midealocal
                from datetime import datetime
                from secrets import token_hex
                import hashlib
                import hmac
                import json as json_module
                
                # 使用 all_in_one_getter.py 中相同的硬编码密钥
                iot_key = bytes.fromhex(format(9795516279659324117647275084689641883661667, 'x')).decode()
                hmac_key = bytes.fromhex(format(117390035944627627450677220413733956185864939010425, 'x')).decode()
                
                lua_data = {
                    "applianceSn": sn,
                    "applianceType": f"0x{device_type:X}",  # 使用大写格式，与 all_in_one_getter.py 一致
                    "applianceMFCode": mf_code,
                    "version": "0",
                    "iotAppId": "900",
                    "modelNumber": model_number or "0",
                    "reqId": token_hex(16),
                    "stamp": datetime.now().strftime("%Y%m%d%H%M%S"),
                }
                
                # 构建请求
                json_data = json_module.dumps(lua_data, separators=(',', ':'))
                random = str(int(__import__('time').time()))
                
                # 签名 - 与 all_in_one_getter.py 一致
                msg = iot_key + json_data + random
                sign = hmac.new(hmac_key.encode("ascii"), msg.encode("ascii"), hashlib.sha256).hexdigest()
                
                # 构建 headers - 与 all_in_one_getter.py 一致
                headers = {
                    "content-type": "application/json; charset=utf-8",
                    "secretVersion": "1",
                    "accesstoken": cloud._access_token,
                }
                headers["random"] = random
                headers["sign"] = sign
                
                _LOGGER.info("Lua download request data: %s", lua_data)
                _LOGGER.info("Lua download headers: %s", headers)
                
                # 发送请求
                api_url = "https://mp-prod.smartmidea.net/mas/v5/app/proxy?alias=/v1/appliance/protocol/lua/luaGet"
                
                async with ClientSession() as session:
                    async with session.post(api_url, headers=headers, data=json_data, timeout=30) as response:
                        result = await response.json()
                        
                        _LOGGER.info("Lua download response: %s", result)
                        
                        if str(result.get("code")) == "0" and "data" in result:
                            data_section = result["data"]
                            if "url" in data_section:
                                lua_url = data_section["url"]
                                
                                # 下载 Lua 文件内容
                                async with session.get(lua_url, timeout=30) as lua_response:
                                    if lua_response.status == 200:
                                        lua_content = await lua_response.text()
                                        
                                        # 解密 Lua 代码
                                        formatted_lua = _format_lua_code(lua_content)
                                        
                                        # 移除local bit = require("bit")
                                        modified = formatted_lua.replace('local bit = require("bit")', '')
                                        
                                        # 在文件开头添加local bit = require "bit"
                                        modified = 'local bit = require "bit".bit\n' + modified
                                        
                                        # 修改 dataType 检查（已注释）
                                        modified = modified.replace(
                                            'if ((dataType ~= 0x02) and (dataType ~= 0x03) and (dataType ~= 0x04)) then         return nil     end',
                                            ''
                                        )
                                        
                                        modified = modified.replace("\r\n", "\n")
                                        
                                        # 使用修改后的 Lua 代码
                                        success = await self.hass.async_add_executor_job(_write_lua_file, lua_file_path, modified)
                                        
                                        if success:
                                            _LOGGER.info("Downloaded Lua file for device type 0x%s, sn8: %s, mf_code: %s", hex(device_type)[2:], sn8, mf_code)
                                            return str(lua_file_path)
                
                _LOGGER.warning("download_lua with mf_code=%s returned no path, trying next...", mf_code)
        except (socket.error, OSError, ValueError, json.JSONDecodeError) as err:
            _LOGGER.error("Failed to download Lua file: %s", err)
        return None

    async def _download_common_lua_files(
        self, storage_dir: Path
    ) -> bool:
        try:
            storage_dir.mkdir(parents=True, exist_ok=True)
            
            common_files = {
                "bit.lua": base64.b64decode(BIT_LUA.encode("utf-8")).decode("utf-8"),
                "cjson.lua": base64.b64decode(CJSON_LUA.encode("utf-8")).decode("utf-8"),
            }
            
            for file_name, content in common_files.items():
                file_path = storage_dir / file_name
                
                if file_path.exists():
                    _LOGGER.info("Common Lua file already exists: %s", file_path)
                    continue
                
                success = await self.hass.async_add_executor_job(
                    _write_lua_file, file_path, content
                )
                if success:
                    _LOGGER.info("Created common Lua file: %s", file_name)
            
            return True
        except OSError as err:
            _LOGGER.error("Failed to create common Lua files: %s", err)
            return False

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        return MideaLocalOptionsFlowHandler(config_entry)

class MideaLocalOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self._config_entry = config_entry
        self._account = config_entry.data.get(CONF_ACCOUNT, "")
        self._password = config_entry.data.get(CONF_PASSWORD, "")

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            new_data = dict(self._config_entry.data)
            
            account = user_input.get(CONF_ACCOUNT) or self._account
            password = user_input.get(CONF_PASSWORD) or self._password
            
            if user_input.get("refresh_cloud"):
                if account and password:
                    self._account = account
                    self._password = password
                    devices = new_data.get("devices", [])
                    devices = await self._refresh_cloud_device_info(devices)
                    new_data["devices"] = devices
                    new_data[CONF_ACCOUNT] = account
                    new_data[CONF_PASSWORD] = password
                    self.hass.config_entries.async_update_entry(
                        self._config_entry,
                        data=new_data,
                    )
                    return self.async_create_entry(title="", data={"update_interval": user_input.get("update_interval", 1)})
                return self.async_show_form(
                    step_id="init",
                    errors={"base": "no_account_password"},
                    description_placeholders={"note": "请先配置账号密码"},
                )
            
            if user_input.get(CONF_ACCOUNT):
                new_data[CONF_ACCOUNT] = user_input[CONF_ACCOUNT]
            if user_input.get(CONF_PASSWORD):
                new_data[CONF_PASSWORD] = user_input[CONF_PASSWORD]
            
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data=new_data,
            )
            return self.async_create_entry(title="", data={"update_interval": user_input.get("update_interval", 1)})
        
        options = self._config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "update_interval",
                    default=options.get("update_interval", 1),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=30)),
                vol.Optional(
                    CONF_ACCOUNT,
                    default=self._account,
                ): str,
                vol.Optional(
                    CONF_PASSWORD,
                    default=self._password,
                ): str,
                vol.Optional(
                    "refresh_cloud",
                    default=False,
                ): bool,
            }),
        )
    
    async def _refresh_cloud_device_info(self, devices: list) -> list:
        """Refresh device info from cloud."""
        from .midea_lib.cloud import get_midea_cloud
        
        cloud_device_info = {}
        session = ClientSession()
        try:
            cloud = get_midea_cloud(
                cloud_name="美的美居",
                session=session,
                account=self._account,
                password=self._password,
            )
            if await cloud.login():
                device_ids = [d.get(CONF_DEVICE_ID) for d in devices if d.get(CONF_DEVICE_ID)]
                cloud_devices = await cloud.list_appliances(home_id=None) or {}
                for device_id in device_ids:
                    if device_id in cloud_devices:
                        device = cloud_devices[device_id]
                        cloud_device_info[device_id] = {
                            CONF_SN: device.get("sn", ""),
                            CONF_SN8: device.get("sn8", ""),
                            CONF_PRODUCT_MODEL: device.get("model", ""),
                            CONF_MODEL_NUMBER: device.get("model_number", ""),
                            CONF_DEVICE_NAME: device.get("name", ""),
                        }
                _LOGGER.info("Refreshed device info from cloud for %d devices", len(cloud_device_info))
        except (socket.error, OSError, ValueError, json.JSONDecodeError) as err:
            _LOGGER.warning("Failed to refresh device info from cloud: %s", err)
        finally:
            await session.close()
        
        for device in devices:
            device_id = device.get(CONF_DEVICE_ID)
            if device_id in cloud_device_info:
                device.update(cloud_device_info[device_id])
        
        return devices
