"""Constants for the Senec integration."""
from datetime import timedelta

from homeassistant.const import ENERGY_KILO_WATT_HOUR, PERCENTAGE, POWER_WATT, ELECTRIC_POTENTIAL_VOLT

DOMAIN = "senec"


"""Default config for Senec."""
DEFAULT_HOST = "senec"
DEFAULT_NAME = "senec"

"""Fixed constants."""
SCAN_INTERVAL = timedelta(seconds=60)

"""Supported sensor types."""

SENSOR_TYPES = {
    "system_state": ["", "mdi:solar-power"],
    "solar_generated_power": [POWER_WATT, "mdi:solar-power"],
    "house_power": [POWER_WATT, "mdi:home-import-outline"],
    "battery_state_power": [POWER_WATT, "mdi:ev-station"],
    "battery_charge_percent": [PERCENTAGE, "mdi:ev-station"],
    "grid_state_power": [POWER_WATT, "mdi:transmission-tower"],
    "grid_imported_power": [POWER_WATT, "mdi:transmission-tower"],
    "grid_exported_power": [POWER_WATT, "mdi:transmission-tower"],
}
