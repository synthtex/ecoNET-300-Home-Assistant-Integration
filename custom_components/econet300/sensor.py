"""Sensor for Econet300"""
from dataclasses import dataclass
from typing import Callable, Any

import logging

from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import EconetDataCoordinator, Econet300Api
from .const import (
    DOMAIN,
    REG_PARAM_DEVICE_CLASS,
    REG_PARAM_STATE_CLASS,
    SERVICE_COORDINATOR,
    SERVICE_API,
    REG_PARAM_MAP,
    REG_PARAM_PRECISION,
    REG_PARAM_UNIT,
)
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes Econet sensor entity."""
    process_val: Callable[[Any], Any] = lambda x: x


class EconetSensor(SensorEntity):
    """Econet Sensor"""

    def __init__(self, entity_description, name, unique_id):
        super().__init__(name=name, unique_id=unique_id)
        self.entity_description = entity_description
        self._attr_native_value = None

    def _sync_state(self, value):
        """Sync state"""
        _LOGGER.debug("Update EconetSensor entity: %s", self.entity_description.name)

        self._attr_native_value = self.entity_description.process_val(value)

        self.async_write_ha_state()


class ControllerSensor(EconetEntity, EconetSensor):
    """class controller"""

    def __init__(
        self,
        description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        super().__init__(description, coordinator, api)

def get_human_readable_key(key: str):
    """CHECK if supplied key is defined and return it's value otherwise return appropriate result"""
    if key in REG_PARAM_MAP:
        return REG_PARAM_MAP[key]
    else:
        return key

def get_native_unit_of_measurement(key: str):
    """CHECK if supplied key is defined and return it's value otherwise return appropriate result"""
    if key in REG_PARAM_UNIT:
        return REG_PARAM_UNIT[key]
    else:
        return None

def get_state_class(key: str):
    """CHECK if supplied key is defined and return it's value otherwise return appropriate result"""
    if key in REG_PARAM_STATE_CLASS:
        return REG_PARAM_STATE_CLASS[key]
    else:
        return None

def get_device_class(key: str):
    """CHECK if supplied key is defined and return it's value otherwise return appropriate result"""
    if key in REG_PARAM_DEVICE_CLASS:
        return REG_PARAM_DEVICE_CLASS[key]
    else:
        return None

def create_controller_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """add key"""
    entities = []

    coordinator_data = coordinator.data
    for data_key in coordinator_data:
        if data_key in REG_PARAM_MAP:
            human_readable_key = get_human_readable_key(data_key)
            entity_description = EconetSensorEntityDescription(
                key=human_readable_key,
                translation_key=human_readable_key,
                native_unit_of_measurement=get_native_unit_of_measurement(human_readable_key),
                state_class=get_state_class(human_readable_key),
                device_class=get_device_class(human_readable_key),
                suggested_display_precision=REG_PARAM_PRECISION["tempCO"],
                process_val=lambda x: x,
            )
            entities.append(ControllerSensor(entity_description, coordinator, api))
            _LOGGER.debug(
                "Availability key: %s exist, entity will be added",
                data_key,
            )
        else:
            _LOGGER.debug(
                "Availability key: %s does not exist, entity will not be added",
                data_key,
            )

    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetSensor] = []
    entities = entities + create_controller_sensors(coordinator, api)

    return async_add_entities(entities)
