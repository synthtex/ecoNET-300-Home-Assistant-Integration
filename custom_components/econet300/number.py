"""Base Number for Econet300."""
from dataclasses import dataclass
import logging

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Limits, Econet300Api
from .common import Econet300Api, EconetDataCoordinator
from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR, ENTITY_MIN_VALUE, ENTITY_MAX_VALUE, EDITABLE_PARAMS_MAPPING_TABLE
from .entity import EconetEntity
from enum import StrEnum

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetNumberEntityDescription(NumberEntityDescription):
    """Describes Econet number entity."""

class UnitOfVolumeFlowRates(StrEnum):
    """Volume flow rate units."""

    KILOWATTHOUR_PER_KG = " kWh/kg"
    KG_PER_HOUR = " kg/h"


NUMBER_TYPES: tuple[EconetNumberEntityDescription, ...] = (
    EconetNumberEntityDescription(
        key="CO_TEMP_SET",
        name="CH boiler preset temperature",
        translation_key="co_temp_set",
        icon="mdi:thermometer",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_registry_visible_default=True,
        min_value=60,
        max_value=85,
        native_step=1,
    ),
    EconetNumberEntityDescription(
        key="CALORIFIC_KWH_KG",
        name="Fuel caloricity",
        mode=NumberMode.BOX,
        translation_key="calorific_set",
        icon="mdi:gauge-low",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfVolumeFlowRates.KILOWATTHOUR_PER_KG,
        entity_registry_visible_default=True,
        min_value=0.1,
        max_value=25,
        native_step=0.1,
    ),
    EconetNumberEntityDescription(
        key="FUEL_KG_H",
        name="Fuel feeder speed",
        mode=NumberMode.BOX,
        translation_key="fuelfeederspeed_set",
        icon="mdi:gauge-low",
        device_class=NumberDeviceClass.VOLUME_FLOW_RATE,
        native_unit_of_measurement=UnitOfVolumeFlowRates.KG_PER_HOUR,
        entity_registry_visible_default=True,
        min_value=0.1,
        max_value=25,
        native_step=0.1,
    ),
    EconetNumberEntityDescription(
        key="CWU_SET_TEMP",
        name="HUW set temperature",
        translation_key="temp_cwu_set",
        icon="mdi:thermometer",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_registry_visible_default=True,
        min_value=20,
        max_value=55,
        native_step=1,
    ),
)


class EconetNumber(EconetEntity, NumberEntity):
    """Describes Econet number sensor entity."""

    def __init__(
        self,
        description: EconetNumberEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize the EconetNumber entity."""
        super().__init__(description, coordinator, api)

    def _sync_state(self, value):
        """Sync state."""
        map_key = EDITABLE_PARAMS_MAPPING_TABLE.get(self.entity_description.key)
        
        self._attr_native_value = value
        self._attr_native_min_value = ENTITY_MIN_VALUE.get(map_key)
        self._attr_native_max_value = ENTITY_MAX_VALUE.get(map_key)

        self.async_write_ha_state()
        self.hass.async_create_task(self.async_set_limits_values())

    async def async_set_limits_values(self):
        """Async Sync number limits."""
        limits = await self._api.get_param_limits(self.entity_description.key)
        if limits is None:
            _LOGGER.warning(
                "Cannot add number entity: %s, numeric limits for this entity is None",
                self.entity_description.key,
            )
        else:
            self._attr_native_min_value = limits.minv
            self._attr_native_max_value = limits.maxv
            self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        
        if value == self._attr_native_value:
            return

        if value > self._attr_native_max_value:
            _LOGGER.warning(
                "Requested value: '%s' exceeds maximum allowed value: '%s'",
                value,
                self._attr_max_value,
            )

        if value < self._attr_native_min_value:
            _LOGGER.warning(
                "Requested value: '%s' is below allowed value: '%s'",
                value,
                self._attr_min_value,
            )
            return

        if not await self._api.set_param(self.entity_description.key, value):
            _LOGGER.warning("Setting value failed")
            return

        self._attr_native_value = value
        self.async_write_ha_state()


def can_add(desc: EconetNumberEntityDescription, coordinator: EconetDataCoordinator):
    """Check if a given entity can be added based on the availability of data in the coordinator."""
    return coordinator.has_data(desc.key) and coordinator.data[desc.key]


def apply_limits(desc: EconetNumberEntityDescription, limits: Limits):
    """Set the native minimum and maximum values for the given entity description."""
    desc.native_min_value = limits.minv
    desc.native_max_value = limits.maxv


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetNumber] = []

    for description in NUMBER_TYPES:
        number_limits = await api.get_param_limits(description.key)

        if number_limits is None:
            _LOGGER.warning(
                "Cannot add entity: {}, numeric limits for this entity is None"
            )
            continue

        if can_add(description, coordinator):
            apply_limits(description, number_limits)
            entities.append(EconetNumber(description, coordinator, api))
        else:
            _LOGGER.debug(
                "Cannot add entity - availability key: %s does not exist",
                description.key,
            )

    return async_add_entities(entities)
