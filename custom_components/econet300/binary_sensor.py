"""Econet binary sensor"""
from dataclasses import dataclass

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import EconetEntity

from .common import EconetDataCoordinator, Econet300Api

from .const import (
    DOMAIN,
    SERVICE_COORDINATOR,
    SERVICE_API,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Econet binary sensor entity."""

    icon_off: str | None = None


BINARY_SENSOR_TYPES: tuple[EconetBinarySensorEntityDescription, ...] = (
    EconetBinarySensorEntityDescription(
        key="1544",
        translation_key="mixer_pump1",
        icon="mdi:pump",
        icon_off="mdi:pump-off",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    EconetBinarySensorEntityDescription(
        key="1541",
        translation_key="boiler_pump",
        icon="mdi:pump",
        icon_off="mdi:pump-off",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
)


class EconetBinarySensor(EconetEntity, BinarySensorEntity):
    """Describe Econet Binary Sensor"""

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
        super().__init__(coordinator)

    def _sync_state(self, value):
        """Sync state"""
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


def can_add(
    desc: EconetBinarySensorEntityDescription, coordinator: EconetDataCoordinator
):
    """Check can add key"""
    return coordinator.has_data(desc.key)


def create_binary_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """create binary sensors"""
    entities: list[EconetBinarySensor] = []

    for description in BINARY_SENSOR_TYPES:
        if can_add(description, coordinator):
            entities.append(EconetBinarySensor(description, coordinator, api))
        else:
            _LOGGER.debug(
                "Availability key: %s does not exist, entity will not be added",
                description.key,
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
