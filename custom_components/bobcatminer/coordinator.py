"""Bobcat Miner DataUpdateController"""

from .const import DOMAIN
from bobcatpy import Bobcat, BobcatRateLimitException
import logging
import async_timeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=30)


class BobcatMinerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage Bobcat miner data and operations."""

    def __init__(self, hass: HomeAssistant, bobcat: Bobcat) -> None:
        """Initialize the coordinator."""

        # Update method that retrieves new data from the miner
        async def _update_method():
            """Get the latest data from Bobcat Miner."""
            try:
                async with async_timeout.timeout(30):
                    return await bobcat.status_summary()

            except BobcatRateLimitException as err:
                raise UpdateFailed(f"Unable to fetch data: {err}") from err


        self.bobcat = bobcat

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
            update_method=_update_method,
        )
