"""Econet binary sensor."""
from dataclasses import dataclass
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
    BinarySensorEntity,
    BinarySensorEntityDescription,
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
    availability_key: str = ""


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


def create_binary_entity_description(key: str) -> EconetBinarySensorEntityDescription:
    """Create Econet300 binary entity description"""
    map_key = BINARY_SENSOR_MAP.get(key, key)
    _LOGGER.debug("create_binary_entity_description: %s", map_key)
    entity_description = EconetBinarySensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(map_key),
        device_class=ENTITY_DEVICE_CLASS_MAP.get(map_key, None),
        icon=ENTITY_ICON.get(map_key, None),
        icon_off=ENTITY_ICON_OFF.get(map_key, None),
    )
    _LOGGER.debug("create_binary_entity_description: %s", entity_description)
    return entity_description


def can_add_mixer(desc: str, coordinator: EconetDataCoordinator):
    return coordinator.has_data(desc) and coordinator.data[desc] is not None


def create_binary_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """create binary sensors"""
    _LOGGER.debug("Entering create_binary_sensors function")
    _LOGGER.debug("api: %s", api)
    entities: list[EconetBinarySensor] = []
    _LOGGER.debug("Initialized entities list: %s", entities)
    coordinator_data = coordinator.data
    _LOGGER.debug("Updated coordinator with its data: %s", coordinator_data)
    for data_key in BINARY_SENSOR_MAP:
        _LOGGER.debug("Processing data_key: %s", data_key)
        if data_key in coordinator_data:
            entity = EconetBinarySensor(
                create_binary_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug("Created and appended entity: %s", entity)
            _LOGGER.debug("Key: %s mapped, binary entity will be added", data_key)
        else:
            _LOGGER.debug(
                "key: %s is not mapped, binary sensor entity will not be added",
                data_key,
            )
    _LOGGER.debug("Exiting create_binary_sensors function with entities: %s", entities)
    return entities


def create_mixer_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    entities = []

    for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1):
        availaimility_mixer_key = f"mixerTemp{i}"
        if can_add_mixer(availaimility_mixer_key, coordinator):
            description = EconetBinarySensorEntityDescription(
                availability_key=availaimility_mixer_key,
                key=f"mixerPumpWorks{i}",
                name=f"Mixer {i}",
                icon="mdi:pump",
                device_class=BinarySensorDeviceClass.RUNNING,
            )

            entities.append(MixerBinarySensor(description, coordinator, api, i))
        else:
            _LOGGER.debug(
                "Availability key: "
                + description.key
                + " does not exist, entity will not be "
                "added"
            )

    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    entities=entities + create_mixer_sensors(coordinator, api),
) -> bool:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetBinarySensor] = []
    entities.extend(create_binary_sensors(coordinator, api))

    return async_add_entities(entities)
