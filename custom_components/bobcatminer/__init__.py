"""The Bobcat Miner integration."""
from __future__ import annotations



from bobcatpy import Bobcat
from voluptuous.error import Error

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONFIG_HOST, DOMAIN
from .coordinator import BobcatMinerDataUpdateCoordinator


# Supported platforms
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bobcat Miner from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    # Get config values from hass
    hass_data = dict(entry.data)

    # Instantiate the Bobcat Miner API
    bobcat = Bobcat(miner_ip=hass_data[CONFIG_HOST])

    # Construct the DataUpdateCoordinator object
    coordinator = BobcatMinerDataUpdateCoordinator(hass, bobcat)

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
