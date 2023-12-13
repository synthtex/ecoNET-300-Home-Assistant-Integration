"""Sensor for Econet300"""
from dataclasses import dataclass
from typing import Callable, Any

import logging
import re

from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import EconetDataCoordinator, Econet300Api
from .const import (
    DOMAIN,
    REG_PARAM_DEVICE_CLASS,
    REG_PARAM_STATE_CLASS,
    REG_PARAM_TRANSLATION_KEY,
    SERVICE_COORDINATOR,
    SERVICE_API,
    REG_PARAM_MAP,
    REG_PARAM_PRECISION,
    REG_PARAM_UNIT,
    REG_PARAM_VALUE_PROCESSOR,
    REG_PARAM_ENTITY_CATEGORY,
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


def camel_to_snake(key):
    """Converting camel case return from api ti snake case to mach translations keys structure"""
    key = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", key).lower()


def create_entity_description(key: str):
    """Creates Econect300 sensor entity based on supplied key"""
    map_key = REG_PARAM_MAP.get(key, key)
    return EconetSensorEntityDescription(
        key=key,
        name=map_key,
        translation_key=REG_PARAM_TRANSLATION_KEY.get(map_key, None),
        native_unit_of_measurement=REG_PARAM_UNIT.get(map_key, None),
        state_class=REG_PARAM_STATE_CLASS.get(map_key, None),
        device_class=REG_PARAM_DEVICE_CLASS.get(map_key, None),
        suggested_display_precision=REG_PARAM_PRECISION.get(map_key, None),
        process_val=REG_PARAM_VALUE_PROCESSOR.get(map_key, lambda x: x),
        entity_category=REG_PARAM_ENTITY_CATEGORY.get(map_key, None),
    )


def create_controller_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Creating controller sensor entities"""
    entities = []
    coordinator_data = coordinator.data
    for data_key in coordinator_data:
        if data_key in REG_PARAM_MAP:
            entities.append(
                ControllerSensor(create_entity_description(data_key), coordinator, api)
            )
            _LOGGER.debug(
                "Key: %s mapped, entity will be added",
                data_key,
            )
        else:
            _LOGGER.debug(
                "Key: %s is not mapped, entity will not be added",
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
