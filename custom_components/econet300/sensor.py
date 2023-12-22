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
    ENTITY_DEVICE_CLASS_MAP,
    STATE_CLASS_MAP,
    SERVICE_COORDINATOR,
    SERVICE_API,
    SENSOR_REG_PARAM_MAP,
    ENTITY_PRECISION,
    ENTITY_UNIT_MAP,
    ENTITY_VALUE_PROCESSOR,
    ENTITY_CATEGORY,
    ENTITY_ICON,
)

from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes Econet sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x


class EconetSensor(EconetEntity, SensorEntity):
    """Econet Sensor"""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        entity_description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET sensor."""
        self.entity_description = entity_description
        self.api = api
        self._attr_native_value = None
        super().__init__(coordinator)
        _LOGGER.debug(
            "EconetSensor initialized with unique_id: %s, entity_description: %s",
            self.unique_id,
            self.entity_description,
        )

    def _sync_state(self, value):
        """Sync state"""
        _LOGGER.debug("Update EconetSensor entity: %s", self.entity_description.name)
        self._attr_native_value = self.entity_description.process_val(value)
        self.async_write_ha_state()


def camel_to_snake(key: str) -> str:
    """Converting camel case return from api ti snake case to mach translations keys structure"""
    key = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", key).lower()


def create_entity_description(key: str) -> EconetSensorEntityDescription:
    """Creates Econect300 sensor entity based on supplied key"""
    map_key = SENSOR_REG_PARAM_MAP.get(key, key)
    _LOGGER.debug("SENSOR_REG_PARAM_MAP: %s", SENSOR_REG_PARAM_MAP)
    _LOGGER.debug("Creating entity description for key: %s, map_key: %s", key, map_key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        device_class=ENTITY_DEVICE_CLASS_MAP.get(map_key, None),
        entity_category=ENTITY_CATEGORY.get(map_key, None),
        translation_key=camel_to_snake(map_key),
        icon=ENTITY_ICON.get(map_key, None),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(map_key, None),
        state_class=STATE_CLASS_MAP.get(map_key, None),
        suggested_display_precision=ENTITY_PRECISION.get(map_key, None),
        process_val=ENTITY_VALUE_PROCESSOR.get(map_key, lambda x: x),
    )
    _LOGGER.debug("Created entity description: %s", entity_description)
    return entity_description


def create_controller_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Creating controller sensor entities"""
    entities: list[EconetSensor] = []
    coordinator_data = coordinator.data
    for data_key in coordinator_data:
        if data_key in SENSOR_REG_PARAM_MAP:
            entities.append(
                EconetSensor(create_entity_description(data_key), coordinator, api)
            )
            _LOGGER.debug(
                "Key: %s mapped, sensor entity will be added",
                data_key,
            )
        else:
            _LOGGER.debug(
                "Key: %s is not mapped, sensor entity will not be added",
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
    entities.extend(create_controller_sensors(coordinator, api))

    return async_add_entities(entities)
