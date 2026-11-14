"""Cloud-side statistics fetchers.

These statistics are only available from the Midea App plugin endpoints, so
they are fetched independently of the LAN device state.  The same fetchers
work for LAN, cloud v1 and cloud v2 connected devices.
"""
from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any
from uuid import uuid4

_LOGGER = logging.getLogger(__name__)

# Device types that expose cloud statistics.
CLOUD_STATS_DEVICE_TYPES = frozenset({0xB6, 0xAC, 0xDB})

# App plugin aliases (appended to the cloud proxy base url).
_RANGE_HOOD_API = "/cfhrs/b6/v1/api"
_AC_ELEC_API = "/jykt/bluetooth/control/queryElec"
_WASH_CONSUMPTION_API = (
    "/xyj/h5/washConsumption/energy/v1/consumption/get{period}Consumption"
)

# Defaults used by the washing machine consumption endpoint.
_WASH_DEFAULT_CATEGORY = "DB"
_WASH_DEFAULT_PROJECT_NO = "13153"

def _plugin_result(response: dict | None, code_key: str) -> Any:
    """Return the result payload when the plugin response reports success."""
    if not isinstance(response, dict):
        return None
    code = response.get(code_key)
    if code is None:
        for key in ("code", "retCode", "errCode", "errorCode"):
            if key in response:
                code = response[key]
                break
    if code is not None and str(code) != "0":
        return None
    result = response.get("result")
    return result if result is not None else response.get("data")

def _find_item(items: Any, key: str, value: str) -> dict | None:
    """Return the first dict in a list whose key matches value."""
    if not isinstance(items, list):
        return None
    for item in items:
        if isinstance(item, dict) and str(item.get(key)) == value:
            return item
    return None

def _to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

async def _fetch_range_hood(cloud, appliance_code, sn8: str) -> dict[str, Any]:
    """Fetch range hood cleanliness percentages."""
    response = await cloud.app_plugin_request(
        _RANGE_HOOD_API,
        {
            "msg": "getDirty",
            "params": {
                "task": [],
                "applianceId": str(appliance_code),
                "platform": sn8,
            }
        }
    )
    result = _plugin_result(response, "retCode")
    if not isinstance(result, dict):
        return {}
    return {
        "fan_cleanliness": _to_float(result.get("fanDirtyPercent")),
        "oil_box_cleanliness": _to_float(result.get("oilBoxDirtyPercent")),
        "filter_cleanliness": _to_float(result.get("netDirtyPercent")),
    }

async def _fetch_air_conditioner(
    cloud, appliance_code, today: date
) -> dict[str, Any]:
    """Fetch today/month/year energy consumption for an air conditioner."""
    stats: dict[str, Any] = {}
    for stat_type in (1, 2, 3):
        response = await cloud.app_plugin_request(
            _AC_ELEC_API,
            {
                "applianceId": str(appliance_code),
                "type": stat_type,
                "date": today.isoformat(),
            },
        )
        result = _plugin_result(response, "errCode")
        if not isinstance(result, dict):
            continue
        if stat_type == 1:
            # type 1 is the current week: pick today's entry.
            item = _find_item(result.get("elecDetails"), "key", today.isoformat())
            value = _to_float(item.get("value")) if item else None
            if value is not None:
                stats["today_energy_consumption"] = value
        else:
            value = _to_float(result.get("totalValue"))
            if value is not None:
                stats[
                    "monthly_energy_consumption"
                    if stat_type == 2
                    else "yearly_energy_consumption"
                ] = value
    return stats

def _wash_body(
    appliance_code,
    uid: str | None,
    category: str,
    project_no: str,
    query_time: str,
) -> dict[str, Any]:
    """Build the request body shared by the wash consumption endpoints.

    The consumption service identifies the user by the numeric IoT user id;
    the account uid (a GUID) is rejected as "no permission for this device".
    """
    return {
        "stamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "reqId": str(uuid4()),
        "requestId": str(uuid4()),
        "activityId": "xxxxxx",
        "userId": str(uid or ""),
        "applianceId": str(appliance_code),
        "category": category,
        "project_no": str(project_no),
        "queryTime": query_time,
    }

async def _fetch_wash_period(
    cloud,
    appliance_code,
    uid,
    category,
    project_no,
    period: str,
    query_time: str,
) -> list[dict]:
    response = await cloud.app_plugin_request(
        _WASH_CONSUMPTION_API.format(period=period),
        _wash_body(appliance_code, uid, category, project_no, query_time),
        sign_request=False,
    )
    result = _plugin_result(response, "errorCode")
    return result if isinstance(result, list) else []

async def _fetch_washing_machine(
    cloud,
    appliance_code,
    today: date,
    category: str,
    project_no: str,
) -> dict[str, Any]:
    """Fetch today/week/month energy and water usage for a washing machine."""
    uid = cloud.iot_user_id or cloud.uid
    today_str = today.isoformat()
    stats: dict[str, Any] = {}

    day_item = _find_item(
        await _fetch_wash_period(
            cloud, appliance_code, uid, category, project_no, "Day", today_str
        ),
        "day",
        today_str,
    )
    if day_item:
        for source, target in (
            ("dayPower", "today_energy_consumption"),
            ("dayWater", "today_water_consumption"),
        ):
            value = _to_float(day_item.get(source))
            if value is not None:
                stats[target] = value

    week_items = await _fetch_wash_period(
        cloud, appliance_code, uid, category, project_no, "Week", today_str
    )
    week_item = next(
        (
            item
            for item in week_items
            if isinstance(item, dict)
            and str(item.get("weekStart")) <= today_str <= str(item.get("weekEnd"))
        ),
        None,
    )
    if week_item:
        for source, target in (
            ("weekPower", "weekly_energy_consumption"),
            ("weekWater", "weekly_water_consumption"),
        ):
            value = _to_float(week_item.get(source))
            if value is not None:
                stats[target] = value

    month_item = _find_item(
        await _fetch_wash_period(
            cloud, appliance_code, uid, category, project_no, "Month", today_str
        ),
        "month",
        today.strftime("%Y-%m"),
    )
    if month_item:
        for source, target in (
            ("monthPower", "monthly_energy_consumption"),
            ("monthWater", "monthly_water_consumption"),
        ):
            value = _to_float(month_item.get(source))
            if value is not None:
                stats[target] = value

    return stats

async def async_fetch_cloud_stats(
    cloud,
    *,
    device_type: int,
    appliance_code,
    sn8: str = "",
    category: str = "",
    project_no: str = "",
) -> dict[str, Any]:
    """Fetch all cloud statistics supported for a device type."""
    if cloud is None:
        return {}

    today = date.today()
    if device_type == 0xB6:
        return await _fetch_range_hood(cloud, appliance_code, sn8)
    if device_type == 0xAC:
        return await _fetch_air_conditioner(cloud, appliance_code, today)
    if device_type == 0xDB:
        return await _fetch_washing_machine(
            cloud,
            appliance_code,
            today,
            category or _WASH_DEFAULT_CATEGORY,
            project_no or _WASH_DEFAULT_PROJECT_NO,
        )
    return {}
