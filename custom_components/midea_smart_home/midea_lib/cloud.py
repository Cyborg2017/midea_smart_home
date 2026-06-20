"""Midea Smart Home Cloud API client."""

import json
import logging
import time
from datetime import UTC, datetime
from secrets import token_hex
from threading import Lock
from typing import Any, cast

from aiohttp import ClientConnectionError, ClientSession, ClientTimeout

from .exceptions import ElementMissing
from .security import CloudSecurity, MeijuCloudSecurity, MideaAirSecurity

SN8_MIN_SERIAL_LENGTH = 17

_LOGGER = logging.getLogger(__name__)

SUPPORTED_CLOUDS = {
    "Meiju Cloud": {
        "class_name": "MeijuCloud",
        "app_id": "900",
        "app_key": "46579c15",
        "login_key": "ad0ee21d48a64bf49f4fb583ab76e799",
        "iot_key": bytes.fromhex(
            format(9795516279659324117647275084689641883661667, "x"),
        ).decode(),
        "hmac_key": bytes.fromhex(
            format(117390035944627627450677220413733956185864939010425, "x"),
        ).decode(),
        "api_url": "https://mp-prod.smartmidea.net/mas/v5/app/proxy?alias=",
    },
    "NetHome Plus": {
        "default": True,
        "class_name": "MideaAirCloud",
        "app_id": "1017",
        "app_key": "3742e9e5842d4ad59c2db887e12449f9",
        "api_url": "https://mapp.appsmb.com",
    },
}

# Multiple preset accounts, each paired with a specific cloud API.
# All credentials are XOR-encoded (3-element format: key, key^username, key^password).
# All accounts share the same base key. Each account will be tried in order; if one fails, the next is used.
PRESET_ACCOUNTS: list[dict[str, Any]] = [
    # Account 1: midea_smart_home@yeah.net / mideasmarthome26 -> NetHome Plus
    {
        "data": [
            39182118275972017797890111985649342047468653967530949796945843010512,
            39182118961190965041038356452242204560213308172028239508034309545636,
            39182118275972017797890111985698725417270634364159392795375039678950,
        ],
        "cloud_name": "NetHome Plus"
    },
    # Account 2: nethome+us@mailinator.com / password1 -> NetHome Plus
    {
        "data": [
            39182118275972017797890111985649342047468653967530949796945843010512,
            39182118967175364252556792044274029144236606293186564273988733916349,
            39182118275972017797890111985649342047468653969590117477294774902753,
        ],
        "cloud_name": "NetHome Plus"
    },
    # Account 3: midea_cloud@outlook.com / a0d6e30c94b15 -> NetHome Plus
    {
        "data": [
            39182118275972017797890111985649342047468653967530949796945843010512,
            39182118275980892824833804202177448991093361348247890162501600564413,
            39182118275972017797890111985649342050088014265865102175083010656997,
        ],
        "cloud_name": "NetHome Plus"
    }
]

def get_default_cloud() -> str:
    for key, value in SUPPORTED_CLOUDS.items():
        if cast(dict, value).get("default"):
            return key
    raise ElementMissing

def get_preset_account_cloud() -> dict[str, str]:
    """Return the first preset account (backward compat for discover step)."""
    data = PRESET_ACCOUNTS[0]["data"]
    username = bytes.fromhex(
        format((data[0] ^ data[1]), "X"),
    ).decode("utf-8", errors="ignore")
    password = bytes.fromhex(
        format((data[0] ^ data[2]), "X"),
    ).decode("utf-8", errors="ignore")
    return {
        "username": username,
        "password": password,
        "cloud_name": PRESET_ACCOUNTS[0]["cloud_name"],
    }

def get_all_preset_accounts() -> list[dict[str, str]]:
    """Return all preset accounts as [{username, password, cloud_name}, ...].

    Each account uses 3-element XOR encoding: [key, key^username, key^password].
    """
    accounts = []
    for preset in PRESET_ACCOUNTS:
        data = preset["data"]
        username = bytes.fromhex(
            format((data[0] ^ data[1]), "X"),
        ).decode("utf-8", errors="ignore")
        password = bytes.fromhex(
            format((data[0] ^ data[2]), "X"),
        ).decode("utf-8", errors="ignore")
        accounts.append({
            "username": username,
            "password": password,
            "cloud_name": preset["cloud_name"],
        })
    return accounts


class MideaCloud:
    """Midea Cloud base class."""

    def __init__(
        self,
        session: ClientSession,
        security: CloudSecurity,
        app_id: str,
        app_key: str,
        account: str,
        password: str,
        api_url: str,
    ) -> None:
        self._device_id = CloudSecurity.get_deviceid(account)
        self._session = session
        self._security = security
        self._api_lock = Lock()
        self._app_id = app_id
        self._app_key = app_key
        self._account = account
        self._password = password
        self._api_url = api_url
        self._access_token: str | None = None
        self._uid: str | None = None
        self._login_id = ""

    def _make_general_data(self) -> dict[Any, Any]:
        return {}

    async def _api_request(
        self,
        endpoint: str,
        data: dict[str, Any],
        header: dict[str, Any] | None = None,
    ) -> dict | None:
        header = header or {}
        if not data.get("reqId"):
            data.update({"reqId": token_hex(16)})
        if not data.get("stamp"):
            data.update(
                {"stamp": datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")},
            )
        random = str(int(time.time()))
        url = self._api_url + endpoint
        dump_data = json.dumps(data)
        sign = self._security.sign("", dump_data, random)
        header.update(
            {
                "content-type": "application/json; charset=utf-8",
                "secretVersion": "1",
                "sign": sign,
                "random": random,
            },
        )
        if self._uid is not None:
            header.update({"uid": self._uid})
        if self._access_token is not None:
            header.update({"accessToken": self._access_token})
        response: dict = {"code": -1}
        for _ in range(3):
            try:
                with self._api_lock:
                    r = await self._session.request(
                        "POST",
                        url,
                        headers=header,
                        data=dump_data,
                        timeout=ClientTimeout(10),
                    )
                    raw = await r.read()
                    response = json.loads(raw)
                    break
            except (TimeoutError, ClientConnectionError, json.JSONDecodeError) as e:
                _LOGGER.warning("Midea cloud API error, url: %s, error: %s", url, repr(e))
        if int(response["code"]) == 0 and "data" in response:
            return cast(dict, response["data"])
        return None

    async def _get_login_id(self) -> str | None:
        data = self._make_general_data()
        data.update({"loginAccount": f"{self._account}"})
        if response := await self._api_request(
            endpoint="/v1/user/login/id/get",
            data=data,
        ):
            return response.get("loginId")
        return None

    async def login(self) -> bool:
        raise NotImplementedError

    async def get_cloud_keys(self, appliance_id: int) -> dict[int, dict[str, Any]]:
        result = {}
        for method in [1, 2]:
            udp_id = self._security.get_udp_id(appliance_id, method)
            data = self._make_general_data()
            data.update({"udpid": udp_id})
            response = await self._api_request(
                endpoint="/v1/iot/secure/getToken",
                data=data,
            )
            if response and "tokenlist" in response:
                for token in response["tokenlist"]:
                    if token["udpId"] == udp_id:
                        result[method] = {
                            "token": token["token"].lower(),
                            "key": token["key"].lower(),
                        }
        return result

    async def list_appliances(
        self,
        home_id: str | None,
    ) -> dict[int, dict[str, Any]] | None:
        raise NotImplementedError


class MeijuCloud(MideaCloud):
    """Meiju Cloud."""

    def __init__(
        self,
        cloud_name: str,
        session: ClientSession,
        account: str,
        password: str,
    ) -> None:
        cloud_data = cast(dict[str, Any], SUPPORTED_CLOUDS[cloud_name])
        super().__init__(
            session=session,
            security=MeijuCloudSecurity(
                login_key=cloud_data["login_key"],
                iot_key=cloud_data["iot_key"],
                hmac_key=cloud_data["hmac_key"],
            ),
            app_id=cloud_data["app_id"],
            app_key=cloud_data["app_key"],
            account=account,
            password=password,
            api_url=cloud_data["api_url"],
        )

    def _make_general_data(self) -> dict[str, Any]:
        return {
            "src": self._app_id,
            "format": "2",
            "stamp": datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S"),
            "platformId": "1",
            "deviceId": self._device_id,
            "reqId": token_hex(16),
            "uid": self._uid,
            "clientType": "1",
            "appId": self._app_id,
            "language": "en_US",
        }

    async def login(self) -> bool:
        if login_id := await self._get_login_id():
            self._login_id = login_id
            stamp = datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")
            data = {
                "iotData": {
                    "clientType": 1,
                    "deviceId": self._device_id,
                    "iampwd": self._security.encrypt_iam_password(
                        self._login_id,
                        self._password,
                    ),
                    "iotAppId": self._app_id,
                    "loginAccount": self._account,
                    "password": self._security.encrypt_password(
                        self._login_id,
                        self._password,
                    ),
                    "reqId": token_hex(16),
                    "stamp": stamp,
                },
                "data": {
                    "appKey": self._app_key,
                    "deviceId": self._device_id,
                    "platform": 2,
                },
                "timestamp": stamp,
                "stamp": stamp,
            }
            if response := await self._api_request(
                endpoint="/mj/user/login",
                data=data,
            ):
                self._access_token = response["mdata"]["accessToken"]
                self._security.set_aes_keys(
                    self._security.aes_decrypt_with_fixed_key(response["key"]),
                    b"0",
                )
                return True
        _LOGGER.warning("Meiju Cloud login failed for device %s", self._device_id)
        return False

    async def list_appliances(
        self,
        home_id: str | None,
    ) -> dict[int, dict[str, Any]] | None:
        data = {"homegroupId": home_id}
        if response := await self._api_request(
            endpoint="/v1/appliance/home/list/get",
            data=data,
        ):
            appliances = {}
            for home in response.get("homeList") or []:
                home_name = home.get("name", home.get("nickname", ""))
                for room in home.get("roomList") or []:
                    room_name = room.get("name", room.get("nickname", ""))
                    for appliance in room.get("applianceList"):
                        try:
                            model_number = int(appliance.get("modelNumber", 0))
                        except (ValueError, TypeError):
                            model_number = 0
                        device_info = {
                            "name": appliance.get("name"),
                            "type": int(appliance.get("type"), 16),
                            "sn": (
                                self._security.aes_decrypt(appliance.get("sn"))
                                if appliance.get("sn")
                                else ""
                            ),
                            "sn8": appliance.get("sn8", "00000000"),
                            "model_number": model_number,
                            "manufacturer_code": appliance.get(
                                "enterpriseCode",
                                "0000",
                            ),
                            "model": appliance.get("productModel"),
                            "online": appliance.get("onlineStatus") == "1",
                            "category": appliance.get("category", ""),
                            "home_name": home_name,
                            "room_name": room_name,
                        }
                        sn8 = device_info.get("sn8")
                        if not sn8 or len(sn8) == 0:
                            device_info["sn8"] = "00000000"
                        model = device_info.get("model")
                        if not model or len(model) == 0:
                            device_info["model"] = device_info["sn8"]
                        appliances[int(appliance["applianceCode"])] = device_info
            return appliances
        return None


class MideaAirCloud(MideaCloud):
    """Midea Air Cloud."""

    def __init__(
        self,
        cloud_name: str,
        session: ClientSession,
        account: str,
        password: str,
    ) -> None:
        cloud_data = cast(dict[str, Any], SUPPORTED_CLOUDS[cloud_name])
        super().__init__(
            session=session,
            security=MideaAirSecurity(login_key=cloud_data["app_key"]),
            app_id=cloud_data["app_id"],
            app_key=cloud_data["app_key"],
            account=account,
            password=password,
            api_url=cloud_data["api_url"],
        )
        self._session_id: str | None = None

    def _make_general_data(self) -> dict[str, Any]:
        data = {
            "src": self._app_id,
            "format": "2",
            "stamp": datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S"),
            "deviceId": self._device_id,
            "reqId": token_hex(16),
            "clientType": "1",
            "appId": self._app_id,
        }
        if self._session_id is not None:
            data.update({"sessionId": self._session_id})
        return data

    async def _api_request(
        self,
        endpoint: str,
        data: dict[str, Any],
        header: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        header = header or {}
        url = self._api_url + endpoint
        sign = self._security.sign(url, data, "")
        data.update({"sign": sign})
        if self._uid is not None:
            header.update({"uid": self._uid})
        if self._access_token is not None:
            header.update({"accessToken": self._access_token})
        response: dict = {"errorCode": -1}
        for _ in range(3):
            try:
                with self._api_lock:
                    r = await self._session.request(
                        "POST",
                        url,
                        headers=header,
                        data=data,
                        timeout=ClientTimeout(10),
                    )
                    raw = await r.read()
                    response = json.loads(raw)
                    break
            except (TimeoutError, ClientConnectionError, json.JSONDecodeError) as e:
                _LOGGER.warning("Midea cloud API error, url: %s, error: %s", url, repr(e))
        if int(response["errorCode"]) == 0 and "result" in response:
            return cast(dict[str, Any], response["result"])
        return None

    async def login(self) -> bool:
        if login_id := await self._get_login_id():
            self._login_id = login_id
            data = self._make_general_data()
            data.update(
                {
                    "loginAccount": self._account,
                    "password": self._security.encrypt_password(
                        self._login_id,
                        self._password,
                    ),
                },
            )
            if response := await self._api_request(
                endpoint="/v1/user/login",
                data=data,
            ):
                self._access_token = response["accessToken"]
                self._uid = response["userId"]
                self._session_id = response["sessionId"]
                return True
        _LOGGER.warning("Midea Air Cloud login failed for device %s", self._device_id)
        return False

    async def list_appliances(
        self,
        home_id: str | None,
    ) -> dict[int, dict[str, Any]] | None:
        data = self._make_general_data()
        if response := await self._api_request(
            endpoint="/v1/appliance/user/list/get",
            data=data,
        ):
            appliances = {}
            for appliance in response["list"]:
                try:
                    model_number = int(appliance.get("modelNumber", 0))
                except ValueError:
                    model_number = 0
                device_info = {
                    "name": appliance.get("name"),
                    "type": int(appliance.get("type"), 16),
                    "sn": appliance.get("sn"),
                    "sn8": "",
                    "model_number": model_number,
                    "manufacturer_code": appliance.get("enterpriseCode", "0000"),
                    "model": "",
                    "online": appliance.get("onlineStatus") == "1",
                }
                serial_num = device_info.get("sn")
                device_info["sn8"] = (
                    serial_num[9:17]
                    if (serial_num and len(serial_num) > SN8_MIN_SERIAL_LENGTH)
                    else ""
                )
                device_info["model"] = device_info.get("sn8")
                appliances[int(appliance["id"])] = device_info
            return appliances
        return None

def get_midea_cloud(
    cloud_name: str,
    session: ClientSession,
    account: str,
    password: str,
) -> MideaCloud:
    if cloud_name not in SUPPORTED_CLOUDS:
        raise ElementMissing(f"Unsupported Cloud specified: {cloud_name}")

    cloud_data = cast(dict[str, Any], SUPPORTED_CLOUDS[cloud_name])
    return cast(
        MideaCloud,
        globals()[cloud_data["class_name"]](
            cloud_name=cloud_name,
            session=session,
            account=account,
            password=password,
        ),
    )

async def download_lua_file(hass, access_token: str, sn: str, device_type: int, mf_code: str, model_number: str = "0") -> tuple[bool, str]:
    """Download and process Lua file from cloud.

    Returns:
        tuple[bool, str]: (success, lua_content)
    """
    import hashlib
    import hmac

    # Use the same hardcoded keys as in all_in_one_getter.py
    iot_key = bytes.fromhex(format(9795516279659324117647275084689641883661667, 'x')).decode()
    hmac_key = bytes.fromhex(format(117390035944627627450677220413733956185864939010425, 'x')).decode()

    lua_data = {
        "applianceSn": sn,
        "applianceType": f"0x{device_type:X}",
        "applianceMFCode": mf_code,
        "version": "0",
        "iotAppId": "900",
        "modelNumber": model_number or "0",
        "reqId": token_hex(16),
        "stamp": datetime.now().strftime("%Y%m%d%H%M%S"),
    }

    # Build request
    json_data = json.dumps(lua_data, separators=(',', ':'))
    random = str(int(time.time()))

    # Sign
    msg = iot_key + json_data + random
    sign = hmac.new(hmac_key.encode("ascii"), msg.encode("ascii"), hashlib.sha256).hexdigest()

    # Build headers
    headers = {
        "content-type": "application/json; charset=utf-8",
        "secretVersion": "1",
        "accesstoken": access_token,
    }
    headers["random"] = random
    headers["sign"] = sign

    _LOGGER.info("Lua download request data: %s", lua_data)

    # Send request
    api_url = "https://mp-prod.smartmidea.net/mas/v5/app/proxy?alias=/v1/appliance/protocol/lua/luaGet"

    try:
        async with ClientSession() as session:
            async with session.post(api_url, headers=headers, data=json_data, timeout=30) as response:
                result = await response.json()

                _LOGGER.info("Lua download response: %s", result)

                if str(result.get("code")) == "0" and "data" in result:
                    data_section = result["data"]
                    if "url" in data_section:
                        lua_url = data_section["url"]

                        # Download Lua file content
                        async with session.get(lua_url, timeout=30) as lua_response:
                            if lua_response.status == 200:
                                lua_content = await lua_response.text()

                                # Decrypt and process Lua code
                                from .lua import decrypt_lua_code
                                formatted_lua = decrypt_lua_code(lua_content)

                                # Remove local bit = require("bit")
                                modified = formatted_lua.replace('local bit = require("bit")', '')

                                # Add local bit = require "bit" at the beginning
                                modified = 'local bit = require "bit".bit\n' + modified

                                # Modify dataType check
                                modified = modified.replace(
                                    'if ((dataType ~= 0x02) and (dataType ~= 0x03) and (dataType ~= 0x04)) then         return nil     end',
                                    ''
                                )

                                # Fix tonumber error when db_error_code is nil
                                modified = modified.replace(
                                    'if (tonumber(tb["db_error_code"], 16) ~= 0)',
                                    'if (tb["db_error_code"] and tonumber(tb["db_error_code"], 16) ~= 0)'
                                )

                                # Fix Lua 5.1 # operator on 0-indexed tables.
                                # bodyBytes is built as {[0]=b0, [1]=b1, ...} but Lua 5.1's #
                                # only counts keys starting from 1, so # returns length-1,
                                # causing binToModel to return nil for short messages.
                                import re
                                modified = re.sub(
                                    r'if\s*\(\s*#binData\s*<\s*(\d+)\s*\)\s*then\b',
                                    r'if ((function(t) local c=0; for _ in pairs(t) do c=c+1 end return c end)(binData) < \1) then',
                                    modified,
                                )

                                modified = modified.replace("\r\n", "\n")
                                return True, modified
                            else:
                                _LOGGER.error("Failed to download Lua file from URL: %s", lua_response.status)
                    else:
                        _LOGGER.error("No URL in Lua download response")
                else:
                    _LOGGER.error("Lua download API failed: %s", result)
    except Exception as e:
        _LOGGER.error("Lua download exception: %s", e)

    return False, ""
