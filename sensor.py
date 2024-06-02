"""Platform for sensor integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from .sds011 import SDS011
from homeassistant.const import CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, CONF_NAME, CONF_UNIQUE_ID, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_UNIQUE_ID): cv.string,
        vol.Required(CONF_PORT): cv.string,
    }
)


def setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the available PM sensors."""
    try:
        collector = SDS011(config.get(CONF_PORT))
    except OSError as err:
        _LOGGER.error(
            "Could not open serial connection to %s (%s)",
            config.get(CONF_PORT),
            err,
        )
        return

    add_entities([
        ParticulateMatterSensor(collector, config.get(CONF_UNIQUE_ID), config.get(CONF_NAME), SensorDeviceClass.PM25),
        ParticulateMatterSensor(collector, config.get(CONF_UNIQUE_ID), config.get(CONF_NAME), SensorDeviceClass.PM10),
    ])


class ParticulateMatterSensor(SensorEntity):
    """Implementation of a SDS011 sensor."""

    _attr_native_value = None
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    def __init__(self, collector: SDS011, unique_id: str, name: str, device_class: SensorDeviceClass) -> None:
        """Initialize the sensor."""
        self._attr_name = name + " " + device_class
        self._collector = collector
        self._attr_device_class = device_class
        self._attr_unique_id = "sensor." + unique_id + "_" + device_class
        self.entity_id = self._attr_unique_id

    def update(self) -> None:
        """Read from sensor and update the state."""
        _LOGGER.info("Reading data from PM sensor")
        pm25, pm10 = self._collector.update_value()
        self._attr_native_value = pm25 if self._attr_device_class == SensorDeviceClass.PM25 else pm10
        _LOGGER.info(f'{self._attr_device_class}: {self._attr_native_value}')
