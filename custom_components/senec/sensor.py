"""Platform for Senec sensors."""
import logging

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from . import SenecDataUpdateCoordinator, SenecEntity
from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, config_entry: ConfigEntry, async_add_entities):
    """Initialize sensor platform from config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    for description in SENSOR_TYPES:
        entity = SenecSensor(coordinator, description)
        entities.append(entity)

    async_add_entities(entities)


class SenecSensor(SenecEntity, SensorEntity):
    """Sensor for the single values (e.g. pv power, ac power)."""

    def __init__(
        self,
        coordinator: SenecDataUpdateCoordinator,
        description: SensorEntityDescription,
    ):
        """Initialize a singular value sensor."""
        super().__init__(coordinator=coordinator, description=description)
