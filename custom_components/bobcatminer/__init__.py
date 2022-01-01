"""The Bobcat Miner integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from bobcatpy import Bobcat
from voluptuous.error import Error

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONFIG_HOST, DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=6)

# Supported platforms
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bobcat Miner from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    hass_data = dict(entry.data)
    bobcat = Bobcat(hass_data[CONFIG_HOST])

    async def _update_method():
        """Get the latest data from Bobcat Miner."""
        try:
            return await hass.async_add_executor_job(bobcat.status_summary)
        except Error as err:
            raise UpdateFailed(f"Unable to fetch data: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=_update_method,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    # Forward the setup to the sensor platform.
    # hass.async_create_task(
    #    hass.config_entries.async_forward_entry_setup(entry, PLATFORMS)
    # )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Remove config entry from domain.
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
