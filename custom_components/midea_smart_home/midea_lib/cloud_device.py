"""Cloud runtime device classes.

Provides device objects that mirror the LAN MideaDevice public surface
(data, available, register_update, refresh_status, set_attribute(s),
open/close, device_id and a minimal controller stub) but talk to the
Midea cloud instead of a local TCP connection.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Callable

from ..const import DEFAULT_CLOUD_SCAN_INTERVAL
from .expression import ExpressionEvaluator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .cloud import MeijuCloud

_LOGGER = logging.getLogger(__name__)

# Mark the device unavailable after this many consecutive failed refreshes
FAILURE_THRESHOLD = 2


class _CloudControllerStub:
    """Minimal controller stand-in so coordinator code can read .ip."""

    def __init__(self) -> None:
        self.ip = ""

    @property
    def connected(self) -> bool:
        return True


class BaseCloudDevice:
    """Base class for cloud-backed devices.

    Mirrors the public surface of the LAN MideaDevice so the coordinator
    and entity layers can consume it unchanged.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        cloud: MeijuCloud,
        appliance_code: int,
        device_id: int,
        device_type: int,
        device_name: str,
        device_mapping: dict[str, Any] | None = None,
        scan_interval: int = DEFAULT_CLOUD_SCAN_INTERVAL,
    ) -> None:
        self._hass = hass
        self._cloud = cloud
        self._appliance_code = appliance_code
        self._device_id = device_id
        self._device_type = device_type
        self._device_name = device_name
        self._mapping = device_mapping or {}
        self._scan_interval = max(1, int(scan_interval))
        self._data: dict[str, Any] = {}
        self._available = False
        self._callbacks: list[Callable[[], None]] = []
        self._controller = _CloudControllerStub()
        self._poll_task: asyncio.Task | None = None
        self._refresh_tasks: set[asyncio.Task] = set()
        self._consecutive_failures = 0
        self._first_refresh_done = False

    @property
    def device_id(self) -> int:
        return self._device_id

    @property
    def device_type(self) -> int:
        return self._device_type

    @property
    def device_name(self) -> str:
        return self._device_name

    @property
    def appliance_code(self) -> int:
        return self._appliance_code

    @property
    def available(self) -> bool:
        return self._available

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    @property
    def controller(self) -> _CloudControllerStub:
        """Minimal controller stub (cloud devices have no LAN address)."""
        return self._controller

    def register_update(self, callback: Callable[[], None]) -> None:
        """Register a callback invoked on every data update."""
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def open(self) -> None:
        """Start the polling loop on the Home Assistant event loop."""
        self._hass.loop.call_soon_threadsafe(self._async_open)

    def close(self) -> None:
        """Stop the polling loop and any pending refresh tasks."""
        self._hass.loop.call_soon_threadsafe(self._async_close)

    def _async_open(self) -> None:
        if self._poll_task is None and not self._hass.is_stopping:
            self._poll_task = self._hass.loop.create_task(self._polling_loop())

    def _async_close(self) -> None:
        if self._poll_task is not None:
            self._poll_task.cancel()
            self._poll_task = None
        for task in self._refresh_tasks:
            task.cancel()
        self._refresh_tasks.clear()

    async def _polling_loop(self) -> None:
        """Periodically refresh device state from the cloud."""
        while True:
            try:
                await self.async_refresh()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                _LOGGER.error(
                    "[cloud_device] polling refresh failed: device_id=%s error=%s",
                    self._device_id,
                    e,
                )
            await asyncio.sleep(self._scan_interval)

    def refresh_status(self, query: dict | None = None) -> None:
        """Schedule an async refresh; safe to call from any thread."""
        self._schedule_async(self.async_refresh(query))

    def _schedule_async(self, coro) -> None:
        """Schedule a coroutine on the Home Assistant event loop."""

        def _start() -> None:
            task = self._hass.loop.create_task(coro)
            self._refresh_tasks.add(task)
            task.add_done_callback(self._refresh_tasks.discard)

        try:
            running_loop = asyncio.get_running_loop()
        except RuntimeError:
            running_loop = None
        if running_loop is self._hass.loop:
            _start()
        else:
            self._hass.loop.call_soon_threadsafe(_start)

    async def async_refresh(self, query: dict | None = None) -> None:
        """Refresh device state from the cloud (implemented by subclasses)."""
        raise NotImplementedError

    def set_attribute(self, attr: str, value: Any) -> None:
        """Set a single attribute (implemented by subclasses)."""
        raise NotImplementedError

    def set_attributes(self, controls: dict[str, Any]) -> None:
        """Set multiple attributes (implemented by subclasses)."""
        raise NotImplementedError

    def _register_refresh_success(self, status: dict[str, Any] | None = None) -> None:
        """Merge refreshed status, track availability and notify callbacks."""
        self._consecutive_failures = 0
        if status:
            self._data.update(status)
        if not self._available:
            self._available = True
            _LOGGER.info(
                "[cloud_device] device online: device_id=%s", self._device_id
            )
        self._notify_update()

    def _register_refresh_failure(self) -> None:
        """Track a failed refresh and mark the device offline when repeated."""
        self._consecutive_failures += 1
        if self._available and self._consecutive_failures >= FAILURE_THRESHOLD:
            self._available = False
            _LOGGER.warning(
                "[cloud_device] device offline: device_id=%s consecutive_failures=%s",
                self._device_id,
                self._consecutive_failures,
            )
            self._notify_update()

    def _apply_local_update(self, updates: dict[str, Any]) -> None:
        """Optimistically merge control values into local state and notify."""
        if not updates:
            return
        self._data.update(updates)
        self._notify_update()

    def _notify_update(self) -> None:
        for callback in self._callbacks:
            try:
                callback()
            except Exception as e:
                _LOGGER.error(
                    "[cloud_device] update callback failed: device_id=%s error=%s",
                    self._device_id,
                    e,
                )


class CloudV2Device(BaseCloudDevice):
    """Device backed by the Meiju cloud Thing Model V2 API.

    Status data is the dict of thing property name -> value returned by
    query_thing_properties; entity configs read thing_key paths.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        cloud: MeijuCloud,
        appliance_code: int,
        device_id: int,
        device_type: int,
        device_name: str,
        device_mapping: dict[str, Any] | None = None,
        scan_interval: int = DEFAULT_CLOUD_SCAN_INTERVAL,
    ) -> None:
        super().__init__(
            hass=hass,
            cloud=cloud,
            appliance_code=appliance_code,
            device_id=device_id,
            device_type=device_type,
            device_name=device_name,
            device_mapping=device_mapping,
            scan_interval=scan_interval,
        )
        # Reverse maps built from the entity configs: attribute -> thing_key
        # and attribute -> (module_code, action_code)
        self._attr_to_thing: dict[str, str] = {}
        self._attr_to_action: dict[str, tuple[str, str]] = {}
        # attribute -> (module_code, actions, target_position_key)
        self._attr_to_cover: dict[
            str, tuple[str, dict[str, str], str | None]
        ] = {}
        self._collect_thing_maps(self._mapping.get("entities") or {})

    def _collect_thing_maps(self, entities: Any) -> None:
        """Walk entity configs collecting attribute to thing_key/action maps."""

        def _walk(node: Any, key: str | None = None) -> None:
            if isinstance(node, dict):
                attr = node.get("attribute")
                if attr:
                    thing_key = node.get("thing_key")
                    if thing_key:
                        self._attr_to_thing[attr] = thing_key
                    thing_action = node.get("thing_action")
                    if thing_action:
                        action = self._parse_thing_action(thing_action)
                        if action:
                            self._attr_to_action[attr] = action
                # Cover-style configs dispatch control values as Thing
                # actions (module_code + actions) plus an optional target
                # position property.
                module_code = node.get("module_code")
                actions = node.get("actions")
                if module_code and isinstance(actions, dict) and actions:
                    target_key = node.get("target_position_key")
                    entry = (
                        str(module_code),
                        {str(k): str(v) for k, v in actions.items()},
                        target_key,
                    )
                    state_key = node.get("attribute") or key
                    if state_key:
                        self._attr_to_cover[str(state_key)] = entry
                    position_key = node.get("position_key")
                    if position_key:
                        self._attr_to_cover[str(position_key)] = entry
                for child_key, value in node.items():
                    _walk(value, child_key)
            elif isinstance(node, (list, tuple)):
                for item in node:
                    _walk(item)

        _walk(entities)

    @staticmethod
    def _parse_thing_action(thing_action: Any) -> tuple[str, str] | None:
        """Parse a thing_action config into (module_code, action_code)."""
        if isinstance(thing_action, dict):
            module_code = thing_action.get("module") or thing_action.get("module_code")
            action_code = thing_action.get("action") or thing_action.get("action_code")
            if module_code and action_code:
                return (str(module_code), str(action_code))
        elif isinstance(thing_action, (list, tuple)) and len(thing_action) == 2:
            return (str(thing_action[0]), str(thing_action[1]))
        return None

    async def async_refresh(self, query: dict | None = None) -> None:
        """Refresh state by querying Thing properties."""
        properties = None
        if query:
            # Explicit query maps attribute names to thing properties
            properties = [
                self._attr_to_thing[attr]
                for attr in query
                if attr in self._attr_to_thing
            ] or None
        status = await self._cloud.query_thing_properties(
            self._appliance_code, properties
        )
        if status:
            self._register_refresh_success(status)
        else:
            self._register_refresh_failure()

    def set_attribute(self, attr: str, value: Any) -> None:
        """Set a single attribute via the Thing Model API."""
        self.set_attributes({attr: value})

    def set_attributes(self, controls: dict[str, Any]) -> None:
        """Set multiple attributes; properties are merged into one request."""
        properties: dict[str, Any] = {}
        action_calls: list[tuple[str, str, dict[str, Any]]] = []
        optimistic: dict[str, Any] = {}
        for attr, value in (controls or {}).items():
            cover = self._attr_to_cover.get(attr)
            if cover:
                module_code, actions, target_key = cover
                if isinstance(value, str) and value in actions:
                    action_calls.append((module_code, actions[value], {}))
                    optimistic[attr] = value
                elif (
                    target_key
                    and isinstance(value, (int, float))
                    and not isinstance(value, bool)
                    and 0 <= value <= 100
                ):
                    position = int(value)
                    properties[target_key] = position
                    optimistic[attr] = position
                else:
                    _LOGGER.debug(
                        "[cloud_device] unmapped cover value: device_id=%s attribute=%s value=%r",
                        self._device_id,
                        attr,
                        value,
                    )
                continue
            thing_key = self._attr_to_thing.get(attr)
            if thing_key:
                # TODO: some thing properties need structured payloads
                # (e.g. {"mode": value} or list form); extend here when
                # entity configs require them.
                properties[thing_key] = value
                optimistic[thing_key] = value
                continue
            action = self._attr_to_action.get(attr)
            if action:
                module_code, action_code = action
                # TODO: the odm reference builds richer action bodies per
                # entity config; only the simple form is supported here.
                action_calls.append((module_code, action_code, {attr: value}))
                optimistic[attr] = value
        if not properties and not action_calls:
            return
        # Optimistic local update so entities react immediately
        self._apply_local_update(optimistic)
        self._schedule_async(self._async_send_controls(properties, action_calls))

    async def _async_send_controls(
        self,
        properties: dict[str, Any],
        action_calls: list[tuple[str, str, dict[str, Any]]],
    ) -> None:
        if properties:
            if not await self._cloud.set_thing_properties(
                self._appliance_code, properties
            ):
                _LOGGER.warning(
                    "[cloud_device] set thing properties failed: device_id=%s properties=%s",
                    self._device_id,
                    list(properties),
                )
        for module_code, action_code, body in action_calls:
            response = await self._cloud.perform_thing_action(
                self._appliance_code, module_code, action_code, body
            )
            if response is None:
                _LOGGER.warning(
                    "[cloud_device] perform thing action failed: device_id=%s module=%s action=%s",
                    self._device_id,
                    module_code,
                    action_code,
                )


class CloudV1Device(BaseCloudDevice):
    """Device backed by the Meiju cloud Lua status endpoint.

    Status keys are identical to the LAN device because the cloud runs the
    same Lua protocol. The Meiju cloud exposes no Lua control endpoint, so
    control entities are read-only.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        cloud: MeijuCloud,
        appliance_code: int,
        device_id: int,
        device_type: int,
        device_name: str,
        device_mapping: dict[str, Any] | None = None,
        scan_interval: int = DEFAULT_CLOUD_SCAN_INTERVAL,
        sn: str = "",
        sn8: str = "",
        subtype: int = 0,
        model_number: str | int = 0,
        manufacturer_code: str = "0000",
        category: str = "",
        lua_file: str = "",
        lua_common_dir: str = "",
    ) -> None:
        super().__init__(
            hass=hass,
            cloud=cloud,
            appliance_code=appliance_code,
            device_id=device_id,
            device_type=device_type,
            device_name=device_name,
            device_mapping=device_mapping,
            scan_interval=scan_interval,
        )
        self._initial_query = list(self._mapping.get("initial_query") or [{}])
        self._polling_query = list(
            self._mapping.get("polling_query") or self._initial_query
        )
        self._default_values = dict(self._mapping.get("default_values") or {})
        self._expression_evaluator = ExpressionEvaluator(
            self._mapping.get("calculate")
        )

    @staticmethod
    def _build_query_params(query_config: Any) -> dict[str, Any]:
        """Convert a mapping query entry into a cloud Lua query dict.

        Mirrors the query conversion of the LAN polling loop.
        """
        if isinstance(query_config, dict):
            if len(query_config) == 1:
                key = list(query_config.keys())[0]
                key = (
                    ",".join([k.strip() for k in key.split(",")])
                    if "," in key
                    else key
                )
                return {"query_type": key}
            return {}
        if isinstance(query_config, (set, frozenset, list, tuple)):
            if len(query_config) == 1:
                key = list(query_config)[0]
                key = (
                    ",".join([k.strip() for k in key.split(",")])
                    if "," in key
                    else key
                )
                return {"query_type": key}
        return {}

    def _apply_status_logic(self, status: dict[str, Any]) -> dict[str, Any]:
        """Apply default values and calculations over the merged state."""
        new_data = self._data.copy()
        new_data.update(status)
        for key, value in self._default_values.items():
            if key not in new_data:
                new_data[key] = value
        # TODO: port DeviceLogicHandler special handling (D9/E3) if the
        # cloud status responses require it.
        return self._expression_evaluator.apply_calculations(new_data)

    async def async_refresh(self, query: dict | None = None) -> None:
        """Refresh status via the cloud Lua query endpoint."""
        if query is not None:
            queries = [query]
        else:
            queries = (
                self._initial_query
                if not self._first_refresh_done
                else self._polling_query
            )
        any_success = False
        for query_config in queries:
            query_params = self._build_query_params(query_config)
            status = None
            try:
                status = await self._cloud.get_device_status(
                    self._appliance_code, query_params
                )
            except Exception as e:
                _LOGGER.warning(
                    "[cloud_device] status query error: device_id=%s query=%s error=%s",
                    self._device_id,
                    query_params,
                    e,
                )
            if status and "message" not in status:
                self._register_refresh_success(self._apply_status_logic(status))
                any_success = True
        self._first_refresh_done = True
        if not any_success:
            self._register_refresh_failure()

    def set_attribute(self, attr: str, value: Any) -> None:
        """Cloud_v1 is read-only: the Meiju cloud has no control endpoint."""
        self.set_attributes({attr: value})

    def set_attributes(self, controls: dict[str, Any]) -> None:
        """Cloud_v1 is read-only; log the dropped control at debug level."""
        _LOGGER.debug(
            "[cloud_device] control ignored (cloud_v1 read-only): device_id=%s controls=%s",
            self._device_id,
            controls,
        )
