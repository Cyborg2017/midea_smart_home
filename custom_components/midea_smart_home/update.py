"""Update entity for the Midea Smart Home integration.

Checks GitHub for new releases, allows downloading and installing updates,
and prompts the user to restart Home Assistant after a successful install.
"""
import asyncio
import json
import logging
import shutil
import zipfile
from datetime import timedelta
from pathlib import Path
from typing import Any

import aiohttp
from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    CONF_UPDATE_CHECK_INTERVAL,
    DOMAIN,
    UPDATE_CHECK_DEFAULT,
    UPDATE_CHECK_OFF,
)

_LOGGER = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/repos/Cyborg2017/midea_smart_home/releases"
GITHUB_RELEASE_URL = "https://github.com/Cyborg2017/midea_smart_home/releases/tag"
DOWNLOAD_TIMEOUT = 300  # 5 minutes per attempt
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds between retries
STARTUP_CHECK_DELAY = 30  # seconds after HA startup
API_TIMEOUT = 30  # seconds for GitHub API call

def _read_installed_version() -> str | None:
    """Read the installed version from manifest.json (must run in executor)."""
    try:
        manifest_path = Path(__file__).parent / "manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        return manifest.get("version")
    except (OSError, json.JSONDecodeError) as e:
        _LOGGER.error("Failed to read manifest.json: %s", e)
        return None

async def _schedule_periodic_check(
    hass: HomeAssistant,
    entry: ConfigEntry,
    entity: "MideaUpdateEntity",
) -> None:
    """Schedule (or reschedule) the periodic update check based on config."""
    # Cancel any existing periodic timer
    if entity._cancel_periodic is not None:
        entity._cancel_periodic()
        entity._cancel_periodic = None

    interval = entry.data.get(CONF_UPDATE_CHECK_INTERVAL, UPDATE_CHECK_DEFAULT)
    if interval and interval != UPDATE_CHECK_OFF:
        try:
            hours = int(interval)
            entity._cancel_periodic = async_track_time_interval(
                hass,
                entity.async_periodic_check,
                timedelta(hours=hours),
            )
            _LOGGER.info("Scheduled update check every %d hours", hours)
        except (ValueError, TypeError):
            _LOGGER.warning("Invalid update check interval: %s", interval)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the update entity."""
    # Read installed version in executor to avoid blocking the event loop
    installed_version = await hass.async_add_executor_job(_read_installed_version)
    entity = MideaUpdateEntity(hass, entry, installed_version)
    async_add_entities([entity])

    hass.data.setdefault(DOMAIN, {}).setdefault(entry.entry_id, {})
    hass.data[DOMAIN][entry.entry_id]["update_entity"] = entity

    # Always check for updates on HA startup (after a short delay)
    async def _async_startup_check() -> None:
        await asyncio.sleep(STARTUP_CHECK_DELAY)
        await entity.async_check_for_update()

    hass.async_create_task(_async_startup_check())

    # Schedule periodic check based on user configuration
    await _schedule_periodic_check(hass, entry, entity)


class MideaUpdateEntity(UpdateEntity):
    """Update entity for the Midea Smart Home integration."""

    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_supported_features = (
        UpdateEntityFeature.INSTALL
        | UpdateEntityFeature.PROGRESS
        | UpdateEntityFeature.RELEASE_NOTES
    )
    _attr_entity_picture = "/api/brand/midea_smart_home.png"
    _attr_has_entity_name = True
    _attr_translation_key = "check_for_updates"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, installed_version: str | None = None) -> None:
        self._hass = hass
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_update"
        self._attr_installed_version = installed_version
        self._attr_latest_version = None
        self._attr_release_summary = None
        self._attr_release_url = None
        self._attr_in_progress = False
        self._download_url: str | None = None
        self._latest_tag: str | None = None
        self._release_notes: str | None = None
        self._cancel_periodic = None
        # Title shown as "{title} {version}" in the update dialog
        language = hass.config.language or "en"
        self._attr_title = "新版本：" if language.startswith("zh") else "New Version:"

    async def async_reschedule_check(self) -> None:
        """Reschedule periodic update check after config change."""
        await _schedule_periodic_check(self._hass, self._entry, self)

    def release_notes(self) -> str | None:
        """Return the release notes for the latest version.

        Returns the full release body from GitHub for display in the
        Home Assistant update dialog.

        Note: This must be a method (not a property) because HA's
        async_release_notes passes the bound method to
        async_add_executor_job.
        """
        return self._release_notes

    async def async_periodic_check(self, now=None) -> None:
        """Periodic check callback from time tracker."""
        await self.async_check_for_update()

    async def async_check_for_update(self) -> None:
        """Check GitHub for the latest release."""
        session = async_get_clientsession(self._hass)
        try:
            timeout = aiohttp.ClientTimeout(total=API_TIMEOUT)
            async with session.get(
                GITHUB_API_URL,
                params={"per_page": 1},
                timeout=timeout,
                headers={"Accept": "application/vnd.github+json"},
            ) as response:
                if response.status != 200:
                    _LOGGER.warning("GitHub API returned status %d", response.status)
                    return

                releases = await response.json()
                if not releases:
                    _LOGGER.debug("No releases found on GitHub")
                    return

                latest_release = releases[0]
                tag_name = latest_release.get("tag_name", "")
                latest_version = tag_name.removeprefix("v") if tag_name else None

                if not latest_version:
                    _LOGGER.warning("No tag_name in latest release")
                    return

                installed_version = await self._hass.async_add_executor_job(_read_installed_version)
                self._attr_installed_version = installed_version

                if self._is_newer_version(latest_version, installed_version):
                    self._attr_latest_version = latest_version
                    body = latest_release.get("body", "")
                    self._release_notes = body if body else None
                    self._attr_release_summary = body[:255] if body else None
                    self._attr_release_url = f"{GITHUB_RELEASE_URL}/{tag_name}"
                    self._download_url = self._get_download_url(latest_release)
                    self._latest_tag = tag_name
                    _LOGGER.info(
                        "Update available: %s (installed: %s)",
                        latest_version,
                        installed_version,
                    )
                else:
                    self._attr_latest_version = installed_version
                    self._attr_release_summary = None
                    self._attr_release_url = None
                    self._release_notes = None
                    _LOGGER.debug("Already up to date: %s", installed_version)

                self.async_write_ha_state()

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            _LOGGER.warning("Failed to check for updates: %s", e)

    def _is_newer_version(self, latest: str, installed: str | None) -> bool:
        """Check if the latest version is newer than the installed version."""
        if not installed:
            return True
        if latest == installed:
            return False
        try:
            from awesomeversion import AwesomeVersion

            return AwesomeVersion(latest) > AwesomeVersion(installed)
        except Exception:
            return latest != installed

    def _get_download_url(self, release: dict) -> str | None:
        """Get the download URL for the midea_smart_home.zip asset."""
        assets = release.get("assets", [])
        for asset in assets:
            if asset.get("name") == "midea_smart_home.zip":
                return asset.get("browser_download_url")
        _LOGGER.warning("midea_smart_home.zip asset not found in release")
        return None

    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None:
        """Install the update by downloading and extracting the zip."""
        if not self._download_url:
            _LOGGER.error("No download URL available, cannot install")
            return

        session = async_get_clientsession(self._hass)
        self._attr_in_progress = 0
        self.async_write_ha_state()

        for attempt in range(MAX_RETRIES):
            try:
                _LOGGER.info(
                    "Downloading update (attempt %d/%d): %s",
                    attempt + 1,
                    MAX_RETRIES,
                    self._download_url,
                )
                self._attr_in_progress = 10
                self.async_write_ha_state()

                zip_data = await self._download_zip(session)

                # Download done; now installing (extraction + file replacement)
                self._attr_in_progress = 90
                self.async_write_ha_state()

                await self._hass.async_add_executor_job(self._install_zip, zip_data)

                self._attr_in_progress = False
                self._attr_installed_version = version
                self._attr_latest_version = version
                self.async_write_ha_state()

                _LOGGER.info("Update installed successfully: %s, restarting Home Assistant", version)

                # Schedule restart with a short delay so the websocket response
                # can be sent back to the frontend before HA shuts down.
                async def _async_restart() -> None:
                    await asyncio.sleep(1)
                    await self._hass.services.async_call("homeassistant", "restart")

                self._hass.async_create_task(_async_restart())
                return

            except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as e:
                _LOGGER.warning("Install attempt %d failed: %s", attempt + 1, e)
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    self._attr_in_progress = False
                    self.async_write_ha_state()
                    _LOGGER.error("All %d install attempts failed", MAX_RETRIES)
                    raise

    async def _download_zip(self, session: aiohttp.ClientSession) -> bytes:
        """Download the zip file from GitHub release with progress updates."""
        timeout = aiohttp.ClientTimeout(total=DOWNLOAD_TIMEOUT)
        async with session.get(self._download_url, timeout=timeout) as response:
            response.raise_for_status()

            # Determine total size from Content-Length header (if available)
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            chunks: list[bytes] = []

            # Download in 64KB chunks and update progress bar (10% -> 90%)
            async for chunk in response.content.iter_chunked(64 * 1024):
                chunks.append(chunk)
                downloaded += len(chunk)
                if total:
                    # Map download progress to 10%-90% range
                    pct = 10 + int((downloaded / total) * 80)
                    if pct > self._attr_in_progress:
                        self._attr_in_progress = pct
                        self.async_write_ha_state()

            return b"".join(chunks)

    def _install_zip(self, zip_data: bytes) -> None:
        """Extract the zip and replace the integration folder."""
        import tempfile

        component_dir = Path(__file__).parent
        custom_components_dir = component_dir.parent

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            zip_path = temp_path / "midea_smart_home.zip"
            zip_path.write_bytes(zip_data)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_path)

            extracted_dir = temp_path / "midea_smart_home"
            if not extracted_dir.exists():
                raise OSError("Extracted folder 'midea_smart_home' not found in zip")

            backup_dir = custom_components_dir / "midea_smart_home_backup"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)

            if component_dir.exists():
                shutil.move(str(component_dir), str(backup_dir))

            try:
                shutil.move(str(extracted_dir), str(component_dir))
                shutil.rmtree(backup_dir, ignore_errors=True)
            except OSError:
                # Restore from backup if move fails
                if backup_dir.exists() and not component_dir.exists():
                    shutil.move(str(backup_dir), str(component_dir))
                raise

            _LOGGER.info("Integration files updated successfully")
