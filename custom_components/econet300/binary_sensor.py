"""Econet binary sensor"""
from dataclasses import dataclass

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import EconetEntity
from .common_functions import camel_to_snake
from .common import EconetDataCoordinator, Econet300Api
from .const import (
    DOMAIN,
    SERVICE_COORDINATOR,
    SERVICE_API,
    BINARY_SENSOR_MAP,
    ENTITY_DEVICE_CLASS_MAP,
    ENTITY_ICON,
    ENTITY_ICON_OFF,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Econet binary sensor entity."""

    icon_off: str | None = None


class EconetBinarySensor(EconetEntity, BinarySensorEntity):
    """Econet Binary Sensor"""

    entity_description: EconetBinarySensorEntityDescription

    def __init__(
        self,
        entity_description: EconetBinarySensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET binary sensor."""
        self.entity_description = entity_description
        self.api = api
        self._attr_is_on = None
        super().__init__(coordinator)
        _LOGGER.debug(
            "EconetBinarySensor initialized with unique_id: %s, entity_description: %s",
            self.unique_id,
            self.entity_description,
        )

    def _sync_state(self, value):
        """Sync state"""
        _LOGGER.debug("EconetBinarySensor _sync_state: %s", value)
        self._attr_is_on = value
        self.async_write_ha_state()

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend."""
        return (
            self.entity_description.icon_off
            if self.entity_description.icon_off is not None and not self.is_on
            else self.entity_description.icon
        )


def create_binary_entity_descritpion(key: str) -> EconetBinarySensorEntityDescription:
    """Create Econet300 binary entity description"""
    map_key = BINARY_SENSOR_MAP.get(key, key)
    _LOGGER.debug("create_binary_entity_descritpion: %s", map_key)
    entity_description = EconetBinarySensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(map_key),
        device_class=ENTITY_DEVICE_CLASS_MAP.get(map_key, None),
        icon=ENTITY_ICON.get(map_key, None),
        icon_off=ENTITY_ICON_OFF.get(map_key, None),
    )
    _LOGGER.debug("create_binary_entity_descritpion: %s", entity_description)
    return entity_description


def create_binary_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """create binary sensors"""
    entities: list[EconetBinarySensor] = []

    coordinator = coordinator.data
    for data_key in BINARY_SENSOR_MAP:
        if data_key in BINARY_SENSOR_MAP:
            entities.append(
                EconetBinarySensor(
                    create_binary_entity_descritpion(data_key), coordinator, api
                )
            )
            _LOGGER.debug("Key: %s mapped, binary entity will be added", data_key)
        else:
            _LOGGER.debug(
                "key: %s is not mapped, binary sensor entity will not be added",
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

    entities: list[EconetBinarySensor] = []
    entities.extend(create_binary_sensors(coordinator, api))

    return async_add_entities(entities)
