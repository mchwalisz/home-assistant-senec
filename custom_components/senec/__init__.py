"""The senec integration."""
import asyncio
import logging
from datetime import timedelta

import async_timeout
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity, EntityDescription
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pysenec import Senec

from .const import (
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the senec component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up senec from a config entry."""
    session = async_get_clientsession(hass)

    coordinator = SenecDataUpdateCoordinator(hass, session, entry)

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    # Registers update listener to update config entry when options are updated.
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options from user interface."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


class SenecDataUpdateCoordinator(DataUpdateCoordinator):
    """Define an object to hold Senec data."""

    def __init__(self, hass, session, entry):
        """Initialize."""
        self._host = entry.data[CONF_HOST]
        self._scan_interval = entry.options[CONF_SCAN_INTERVAL]
        self.senec = Senec(self._host, websession=session)
        self.name = entry.title
        self._entry = entry

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=self._scan_interval),
        )

    async def _async_update_data(self):
        """Update data via library."""
        with async_timeout.timeout(20):
            await self.senec.update()
        return self.senec


async def async_unload_entry(hass, entry):
    """Unload Senec config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""
    version = config_entry.version

    _LOGGER.info("Migrating from version %s", version)

    if version == 1:
        # Add scan interval as configurable option
        data = {**config_entry.data}
        new_options = {}

        new_options[CONF_SCAN_INTERVAL] = DEFAULT_SCAN_INTERVAL

        config_entry.version = 2
        hass.config_entries.async_update_entry(
            config_entry, data=data, options=new_options
        )

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True


class SenecEntity(Entity):
    """Defines a base Senec entity."""

    _attr_should_poll = False

    def __init__(
        self, coordinator: SenecDataUpdateCoordinator, description: EntityDescription
    ) -> None:
        """Initialize the Atag entity."""
        self.coordinator = coordinator
        self._name = coordinator._entry.title
        self._state = None

        self.entity_description = description

    @property
    def device_info(self) -> dict:
        """Return info for device registry."""
        device = self._name
        return {
            "identifiers": {(DOMAIN, device)},
            "name": "Senec Home Battery",
            "model": "Senec",
            "sw_version": None,
            "manufacturer": "Senec",
        }

    @property
    def state(self):
        """Return the current state."""
        sensor = self.entity_description.key
        value = getattr(self.coordinator.senec, sensor)
        try:
            rounded_value = round(float(value), 2)
            return rounded_value
        except ValueError:
            return value

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        sensor = self.entity_description.key
        return f"{self._name}_{sensor}"

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update entity."""
        await self.coordinator.async_request_refresh()
