"""The Bobcat Miner integration."""
from __future__ import annotations

from datetime import timedelta
import logging

import async_timeout
from bobcatpy import Bobcat
from voluptuous.error import Error

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONFIG_HOST, DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)

# Supported platforms
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bobcat Miner from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    # Get config values from hass
    hass_data = dict(entry.data)

    # Instantiate the Bobcat Miner API
    bobcat = Bobcat(miner_ip=hass_data[CONFIG_HOST])

    # Update method that retrieves new data from the miner
    async def _update_method():
        """Get the latest data from Bobcat Miner."""
        try:
            async with async_timeout.timeout(30):
                return await bobcat.status_summary()

        except Error as err:
            raise UpdateFailed(f"Unable to fetch data: {err}") from err

    # Construct the DataUpdateCoordinator object
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=_update_method,
        update_interval=SCAN_INTERVAL,
    )

    # Store a reference to the coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Load platforms from the config
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Remove config entry from domain.
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
