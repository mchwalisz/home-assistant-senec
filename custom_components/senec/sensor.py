"""Platform for Senec sensors."""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.util import Throttle
from requests.exceptions import HTTPError, Timeout

from . import SenecEntity
from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Initialize sensor platform from config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    for sensor in SENSOR_TYPES:
        entities.append(SenecSensor(coordinator, sensor))
    async_add_entities(entities)


class SenecSensor(SenecEntity):
    """Sensor for the single values (e.g. pv power, ac power)."""

    def __init__(self, coordinator, sensor):
        """Initialize a singular value sensor."""
        self._sensor = sensor
        self.coordinator = coordinator
        self._name = DOMAIN.title()

        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name}_{self._sensor}"

    @property
    def state(self):
        """Return the current state."""
        return getattr(self.coordinator.senec, self._sensor)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSOR_TYPES[self._sensor][0]

    @property
    def icon(self):
        """Return the sensor icon."""
        return SENSOR_TYPES[self._sensor][1]

    @property
    def should_poll(self):
        """Device should not be polled, returns False."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self.coordinator.async_remove_listener(self.async_write_ha_state)

    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()
