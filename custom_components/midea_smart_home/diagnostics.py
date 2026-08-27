"""Diagnostic bundle: recent integration logs + per-device attribute dump.

Mirrors the backup archive pattern: a zip is written under config/www so it
is served as a static file via the /local/ path, with a short TTL and stale
file sweeping. The zip contains:

  - midea_debug.log          : recent log records captured in memory
  - device_attributes.json   : metadata + full attribute dict for every device

The ring buffer is attached (once) to the integration logger tree so records
emitted by any sub-logger (e.g. midea_lib.device, coordinator, ...) are
captured. The handler level is DEBUG, but records only reach it at the
logger's effective level — so INFO/WARN/ERROR are always captured, and DEBUG
records are captured once the user enables debug logging for this
integration (Settings -> System -> Logs -> Custom log levels).
"""
import json
import logging
import time
import traceback
import zipfile
from collections import deque
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DIAG_TTL = 600  # seconds
DIAG_DIR = "midea_smart_home"  # under config/www
RING_BUFFER_SIZE = 3000  # recent log records kept in memory
INTEGRATION_LOGGER = f"custom_components.{DOMAIN}"


class RingBufferHandler(logging.Handler):
    """Thread-safe in-memory ring buffer of recent log records."""

    def __init__(self, capacity: int = RING_BUFFER_SIZE) -> None:
        super().__init__(level=logging.DEBUG)
        self._records: deque[logging.LogRecord] = deque(maxlen=capacity)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self._records.append(record)
        except Exception:  # pragma: no cover - logging must never throw
            self.handleError(record)

    def snapshot(self) -> list[logging.LogRecord]:
        """Return a flat list copy of the buffered records."""
        return list(self._records)

    def clear(self) -> None:
        self._records.clear()

_handler: RingBufferHandler | None = None

def install_ring_buffer() -> RingBufferHandler:
    """Attach (once) a ring-buffer handler to the integration logger tree.

    Children loggers (midea_lib.*, coordinator, ...) propagate to this
    parent logger by default, so a single handler captures the whole tree.
    """
    global _handler
    if _handler is not None:
        return _handler

    _handler = RingBufferHandler()
    logger = logging.getLogger(INTEGRATION_LOGGER)
    if not any(isinstance(h, RingBufferHandler) for h in logger.handlers):
        logger.addHandler(_handler)
    return _handler

def _format_records(records: list[logging.LogRecord]) -> str:
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    lines: list[str] = []
    for rec in records:
        try:
            lines.append(formatter.format(rec))
            if rec.exc_info:
                lines.extend(
                    "  " + line
                    for line in traceback.format_exception(*rec.exc_info)
                )
        except Exception:  # pragma: no cover
            continue
    return "\n".join(lines)

def _sweep_expired(diag_dir: Path) -> None:
    """Delete leftover diagnostic archives older than DIAG_TTL."""
    cutoff = time.time() - DIAG_TTL
    for stale in diag_dir.glob("midea_smart_home_diagnostics_*.zip"):
        try:
            if stale.stat().st_mtime < cutoff:
                stale.unlink()
        except OSError as err:
            _LOGGER.warning("Failed to remove stale diagnostics %s: %s", stale, err)

def _collect_device_attributes(hass: HomeAssistant, entry: ConfigEntry) -> dict:
    """Gather metadata + current attribute dict for every configured device."""
    entry_data = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})
    devices: list[dict] = []

    for device_id_str, data in entry_data.items():
        if device_id_str == "device_list" or not isinstance(data, dict):
            continue
        coordinator = data.get("coordinator")
        if not coordinator:
            continue

        midea_device = getattr(coordinator, "device", None)
        try:
            attr_data = dict(midea_device.data or {}) if midea_device else {}
        except Exception as err:
            attr_data = {"_error": f"failed to read attributes: {err}"}

        # IP lives on the low-level controller (the per-device dict under
        # hass.data intentionally omits ip/port to avoid duplication).
        ip_address = ""
        controller = getattr(midea_device, "controller", None) if midea_device else None
        if controller is not None:
            ip_address = getattr(controller, "ip", "") or ""

        devices.append({
            "device_id": data.get("device_id"),
            "sn": data.get("sn", ""),
            "sn8": data.get("sn8", ""),
            "model": data.get("product_model", ""),
            "device_type": data.get("device_type", ""),
            "ip": ip_address,
            "protocol": data.get("protocol", ""),
            "category": data.get("category", ""),
            "available": getattr(midea_device, "available", None) if midea_device else None,
            "last_update_success": getattr(coordinator, "last_update_success", None),
            "attributes": attr_data,
        })

    return {
        "integration": DOMAIN,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "entry_id": entry.entry_id,
        "device_count": len(devices),
        "devices": devices,
    }

def build_diagnostics_archive(
    hass: HomeAssistant, entry: ConfigEntry
) -> tuple[str | None, dict]:
    """Create the diagnostics zip under www/ and report capture stats.

    Blocking helper, run via hass.async_add_executor_job. Returns
    (web_path or None on failure, stats dict).
    """
    diag_dir = Path(hass.config.config_dir) / "www" / DIAG_DIR
    diag_dir.mkdir(parents=True, exist_ok=True)
    _sweep_expired(diag_dir)

    # 1) Recent logs captured by the ring buffer
    record_count = 0
    log_text = ""
    if _handler is not None:
        records = _handler.snapshot()
        record_count = len(records)
        log_text = _format_records(records)

    # 2) Device attributes snapshot
    attrs = _collect_device_attributes(hass, entry)
    device_count = attrs["device_count"]

    stem = time.strftime("midea_smart_home_diagnostics_%Y%m%d")
    zip_path = diag_dir / f"{stem}.zip"
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(
                "midea_debug.log",
                log_text or "(no log records captured yet)",
            )
            archive.writestr(
                "device_attributes.json",
                json.dumps(
                    attrs, indent=2, ensure_ascii=False, default=str
                ),
            )
    except OSError as err:
        _LOGGER.error("Failed to build diagnostics archive: %s", err)
        return None, {"record_count": record_count, "device_count": device_count}

    _LOGGER.info("Diagnostics archive written to %s", zip_path)
    return (
        f"/local/{DIAG_DIR}/{zip_path.name}",
        {"record_count": record_count, "device_count": device_count},
    )

def schedule_diagnostics_cleanup(hass: HomeAssistant, web_path: str) -> None:
    """Delete the archive file after DIAG_TTL seconds."""
    from homeassistant.helpers.event import async_call_later

    zip_path = Path(hass.config.config_dir) / "www" / web_path.removeprefix("/local/")

    async def _delete(_now):
        try:
            await hass.async_add_executor_job(zip_path.unlink)
        except OSError:
            pass  # already swept or removed

    async_call_later(hass, DIAG_TTL, _delete)
