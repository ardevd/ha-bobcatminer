"""Config flow for Bobcat Miner integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from bobcatpy import Bobcat
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from .const import CONFIG_HOST, DOMAIN

_LOGGER = logging.getLogger(__name__)

# adjust the data schema to the data that you need
STEP_MINER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONFIG_HOST): cv.string,
    }
)


async def validate_input(data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    # Test the connection to the miner and get miner name
    bobcat = Bobcat(miner_ip=data[CONFIG_HOST])

    try:
        await bobcat.status_summary()

        # Get miner animal name
        miner_status = await bobcat.status_summary()
        miner_animal = miner_status["animal"]
        return {"title": miner_animal}

    except Exception as exc:
        _LOGGER.error("Bobcat raised exception when retrieving miner status")
        raise CannotConnect from exc


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bobcat Miner."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_MINER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_MINER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
