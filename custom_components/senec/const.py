"""Constants for the Senec integration."""
from datetime import timedelta

from homeassistant.const import ENERGY_KILO_WATT_HOUR, POWER_WATT, PERCENTAGE, VOLT

DOMAIN = "senec"


"""Default config for Senec."""
DEFAULT_HOST = "senec"
DEFAULT_NAME = "senec"

"""Fixed constants."""
SCAN_INTERVAL = timedelta(seconds=60)

"""Supported sensor types."""

SENSOR_TYPES = {
    "solar_generated_power": [POWER_WATT, "mdi:solar-power"],
    "house_power": [POWER_WATT, "mdi:power-socket-europe"],
    "battery_state_power": [POWER_WATT, "mdi:car-battery"],
    "battery_charge_percent": [PERCENTAGE, "mdi:car-battery"],
    "grid_state_power": [POWER_WATT, "mdi:transmission-tower"],
}
