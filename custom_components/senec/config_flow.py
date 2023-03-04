"""Config flow for senec integration."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant, callback
from homeassistant.util import slugify
from pysenec import Senec
from requests.exceptions import HTTPError, Timeout

from .const import DOMAIN  # pylint:disable=unused-import
from .const import DEFAULT_HOST, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


@callback
def senec_entries(hass: HomeAssistant):
    """Return the hosts already configured."""
    return {
        entry.data[CONF_HOST] for entry in hass.config_entries.async_entries(DOMAIN)
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for senec."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def _host_in_configuration_exists(self, host) -> bool:
        """Return True if host exists in configuration."""
        if host in senec_entries(self.hass):
            return True
        return False

    async def _test_connection(self, host):
        """Check if we can connect to the Senec device."""
        websession = self.hass.helpers.aiohttp_client.async_get_clientsession()
        try:
            senec_client = Senec(host, websession)
            await senec_client.update()
            return True
        except (OSError, HTTPError, Timeout):
            self._errors[CONF_HOST] = "cannot_connect"
            _LOGGER.error(
                "Could not connect to Senec device at %s, check host ip address",
                host,
            )
        return False

    async def async_step_user(self, user_input=None):
        """Step when user initializes a integration."""
        self._errors = {}
        if user_input is not None:
            # set some defaults in case we need to return to the form
            name = slugify(user_input.get(CONF_NAME, DEFAULT_NAME))
            host_entry = user_input.get(CONF_HOST, DEFAULT_HOST)
            scan_interval = user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

            if scan_interval < 5:
                self._errors[CONF_SCAN_INTERVAL] = "scan interval too low"
            if self._host_in_configuration_exists(host_entry):
                self._errors[CONF_HOST] = "already_configured"
            else:
                if await self._test_connection(host_entry):
                    return self.async_create_entry(
                        title=name,
                        data={CONF_HOST: host_entry},
                        options={CONF_SCAN_INTERVAL: scan_interval},
                    )
        else:
            user_input = {}
            user_input[CONF_NAME] = DEFAULT_NAME
            user_input[CONF_HOST] = DEFAULT_HOST
            user_input[CONF_SCAN_INTERVAL] = DEFAULT_SCAN_INTERVAL

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=user_input.get(CONF_NAME, DEFAULT_NAME)
                    ): str,
                    vol.Required(
                        CONF_HOST, default=user_input.get(CONF_HOST, DEFAULT_HOST)
                    ): str,
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=user_input.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): cv.positive_int,
                }
            ),
            errors=self._errors,
        )

    async def async_step_import(self, user_input=None):
        """Import a config entry."""
        host_entry = user_input.get(CONF_HOST, DEFAULT_HOST)

        if self._host_in_configuration_exists(host_entry):
            return self.async_abort(reason="already_configured")
        return await self.async_step_user(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return SenecOptionsFlowHandler(config_entry)


class SenecOptionsFlowHandler(config_entries.OptionsFlow):
    """Senec config flow options handler."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize Senec options flow."""

        self.config_entry = config_entry
        self.options = dict(config_entry.options)
        self._errors = {}

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.options[CONF_SCAN_INTERVAL],
                    ): cv.positive_int,
                }
            ),
        )
