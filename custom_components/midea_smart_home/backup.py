"""Short-lived backup archives under config/www for clickable downloads.

Same-origin links to /api/... are swallowed by the HA frontend router, so a
clickable download must go through the static /local/ path instead. The zip
is written to www/midea_smart_home/ with a date-stamped name and auto-deleted
after BACKUP_TTL seconds (stale files are also swept on the next run).
"""
import logging
import time
import zipfile
from pathlib import Path

from homeassistant.core import HomeAssistant

from .const import JSON_FILES_PATH

_LOGGER = logging.getLogger(__name__)

BACKUP_TTL = 600  # seconds
BACKUP_DIR = "midea_smart_home"  # under config/www

def _sweep_expired(backup_dir: Path) -> None:
    """Delete leftover backup archives older than BACKUP_TTL."""
    cutoff = time.time() - BACKUP_TTL
    for stale in backup_dir.glob("midea_smart_home_backup_*.zip"):
        try:
            if stale.stat().st_mtime < cutoff:
                stale.unlink()
        except OSError as err:
            _LOGGER.warning("Failed to remove stale backup %s: %s", stale, err)

def _write_backup(zip_path: Path, json_dir: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        if json_dir.exists():
            for path in sorted(json_dir.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(json_dir))

def build_backup_archive(hass: HomeAssistant) -> tuple[str | None, int]:
    """Create the backup zip under www/ and report the packaged file count.

    Blocking helper, run via hass.async_add_executor_job. Returns
    (web_path or None on failure, file_count).
    """
    backup_dir = Path(hass.config.config_dir) / "www" / BACKUP_DIR
    backup_dir.mkdir(parents=True, exist_ok=True)
    _sweep_expired(backup_dir)

    json_dir = Path(hass.config.config_dir) / JSON_FILES_PATH
    file_count = sum(1 for p in json_dir.rglob("*") if p.is_file()) if json_dir.exists() else 0

    zip_stem = time.strftime("midea_smart_home_backup_%Y%m%d")
    zip_path = backup_dir / f"{zip_stem}.zip"
    try:
        _write_backup(zip_path, json_dir)
    except OSError as err:
        _LOGGER.error("Failed to build backup archive: %s", err)
        return None, file_count

    _LOGGER.info("Backup archive written to %s", zip_path)
    return f"/local/{BACKUP_DIR}/{zip_path.name}", file_count

def schedule_backup_cleanup(hass: HomeAssistant, web_path: str) -> None:
    """Delete the archive file after BACKUP_TTL seconds."""
    from homeassistant.helpers.event import async_call_later

    zip_path = Path(hass.config.config_dir) / "www" / web_path.removeprefix("/local/")

    async def _delete(_now):
        try:
            await hass.async_add_executor_job(zip_path.unlink)
        except OSError:
            pass  # already swept or removed

    async_call_later(hass, BACKUP_TTL, _delete)
