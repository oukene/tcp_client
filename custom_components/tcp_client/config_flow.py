"""Config flow for Hello World integration."""
import logging
import voluptuous as vol
from typing import Any, Dict, Optional
import homeassistant.helpers.config_validation as cv

from .const import *

from homeassistant import config_entries


_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        errors = {}
        if user_input is not None:
            self.data = user_input
            return self.async_create_entry(title=user_input[CONF_DEVICE_NAME], data=self.data)

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_NAME): cv.string,
                }), errors=errors
        )
