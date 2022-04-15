"""Constants for the Senec integration."""
from collections import namedtuple
from datetime import timedelta
from typing import Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import ENERGY_KILO_WATT_HOUR, PERCENTAGE, POWER_WATT

DOMAIN = "senec"


"""Default config for Senec."""
DEFAULT_HOST = "Senec"
DEFAULT_NAME = "senec"

"""Fixed constants."""
SCAN_INTERVAL = timedelta(seconds=60)

"""Supported sensor types."""

SENSOR_TYPES = [
    SensorEntityDescription(
        key="system_state",
        name="System State",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_generated_power",
        name="Solar Generated Power",
        native_unit_of_measurement=POWER_WATT,
        icon="mdi:solar-power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="house_power",
        name="House Power",
        native_unit_of_measurement=POWER_WATT,
        icon="mdi:home-import-outline",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_state_power",
        name="Battery State Power",
        native_unit_of_measurement=POWER_WATT,
        icon="mdi:home-battery",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_charge_power",
        name="Battery Charge Power",
        native_unit_of_measurement=POWER_WATT,
        icon="mdi:home-battery",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_discharge_power",
        name="Battery Discharge Power",
        native_unit_of_measurement=POWER_WATT,
        icon="mdi:home-battery-outline",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_charge_percent",
        name="Battery Charge Percent",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:home-battery",
        # device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_state_power",
        name="Grid State Power",
        native_unit_of_measurement=POWER_WATT,
        icon="mdi:transmission-tower",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_imported_power",
        name="Grid Imported Power",
        native_unit_of_measurement=POWER_WATT,
        icon="mdi:transmission-tower-import",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="grid_exported_power",
        name="Grid Exported Power",
        native_unit_of_measurement=POWER_WATT,
        icon="mdi:transmission-tower-export",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(                          
        key="wallbox_power",
        name="Wallbox Power",
        native_unit_of_measurement=POWER_WATT,           
        icon="mdi:car-arrow-left",            
        device_class=SensorDeviceClass.POWER,            
        state_class=SensorStateClass.MEASUREMENT,     
    ), 
    SensorEntityDescription(                             
        key="wallbox_ev_connected",                             
        name="Wallbox EV Connected",                                       
        icon="mdi:car-electric",        
    ),
    SensorEntityDescription(
        key="house_total_consumption",
        name="House consumed",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:home-import-outline",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="solar_total_generated",
        name="Solar generated",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="battery_total_charged",
        name="Battery charged",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:home-battery",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="battery_total_discharged",
        name="Battery discharged",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:home-battery-outline",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="grid_total_import",
        name="Grid Imported",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:transmission-tower-import",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="grid_total_export",
        name="Grid Exported",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:transmission-tower-export",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription( 
        key="wallbox_energy",      
        name="Wallbox charged",          
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:ev-station",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
]
