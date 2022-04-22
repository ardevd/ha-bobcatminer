"""Config flow for Bobcat Miner integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from bobcatpy import Bobcat
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from .const import CONFIG_HOST, CONFIG_TIMEOUT, DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO adjust the data schema to the data that you need
STEP_MINER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONFIG_HOST): cv.string,
        vol.Optional(CONFIG_TIMEOUT, default=20): cv.positive_int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # Test the connection to the miner
    def _validate(host, timeout):
        miner = Bobcat(
            miner_ip=host,
            get_timeout=timeout,
            auto_connect=False)

        try:
            # Socket can still raise exception if the hostname doesn't resolve
            socket_errno = miner.ping()
        except:
            raise CannotConnect

        # Did it fail for any reason, like timeout?
        if socket_errno != 0:
            raise CannotConnect

    await hass.async_add_executor_job(
        _validate, data[CONFIG_HOST], data[CONFIG_TIMEOUT]
    )

    return {"title": "Bobcat Miner"}


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
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
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


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
