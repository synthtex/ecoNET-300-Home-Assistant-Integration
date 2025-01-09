"""Base Select for Econet300."""

from dataclasses import dataclass
from typing import Any, Final

import logging

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR, AVAILABLE_NUMBER_OF_ECOSTERS, AVAILABLE_NUMBER_OF_MIXERS
from .entity import EconetEntity, EcosterEntity, MixerEntity

OFF: Final = "Off"
ON: Final = "On"

THERMOSTAT_CONTACT: Final = "Thermostat contact"
ECOSTER1: Final = "ecoSTER T1"
ECOSTER2: Final = "ecoSTER T2"
ECOSTER3: Final = "ecoSTER T3"

MODE_SCHEDULE: Final = "Schedule"
MODE_ECO: Final = "Economy mode"
MODE_COMFORT: Final = "Comfort mode"
MODE_OUTSIDE: Final = "Left the house mode"
MODE_AIRING: Final = "Air out mode"
MODE_PARTY: Final = "Party mode"
MODE_HOLIDAY: Final = "Holiday mode"
MODE_ANTIFREEZ: Final = "Frost protection mode"

WINTER: Final = "Winter"
SUMMER: Final = "Summer"
AUTO: Final = "Auto"

_LOGGER = logging.getLogger(__name__)

@dataclass
class EconetSelectEntityDescription(SelectEntityDescription):
    """Describes Econet select entity."""


class EconetSelect(EconetEntity, SelectEntity):
    """Represents an Econet300 select."""

    entity_description: EconetSelectEntityDescription

    def _sync_state(self, value):
        """Sync state."""
        selectstate = self._coordinator.data[self.entity_description.key]
        
        self._attr_current_option = self.entity_description.options[int(selectstate)]

        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if options := self.entity_description.options:
            if not await self._api.set_param(self.entity_description.key, options.index(option)):
                _LOGGER.warning("Setting option %s for %s failed", self.entity_description.options.option, self.entity_description.name)
                return
            
            self._attr_current_option = option
            self.async_write_ha_state()

    async def async_update(self, value: Any) -> None:
        """Update entity state."""
        if self.entity_description.options:
            self._attr_current_option = self.entity_description.options[int(value)]
            self.async_write_ha_state()

class EcosterSelect(EcosterEntity, EconetSelect):
    """Ecoster select class."""

    def __init__(
            self,
            description: EconetSelectEntityDescription,
            coordinator: EconetDataCoordinator,
            api: Econet300Api,
            idx: int,
        ):
            """Initialize a new instance of the EconetSensor class."""
            super().__init__(description, coordinator, api, idx)

class MixerSelect(MixerEntity, EconetSelect):
    """Ecoster select class."""

    def __init__(
            self,
            description: EconetSelectEntityDescription,
            coordinator: EconetDataCoordinator,
            api: Econet300Api,
            idx: int,
        ):
            """Initialize a new instance of the EconetSensor class."""
            super().__init__(description, coordinator, api, idx)


def can_add(desc: EconetSelectEntityDescription, coordinator: EconetDataCoordinator):
    """Check if it can add the key."""
    if desc.key not in coordinator.data:
        _LOGGER.debug("Key %s does not exist in coordinator.data", desc.key)
        return False
    return coordinator.has_data(desc.key) and coordinator.data[desc.key] is not None

def create_ecoster_selects(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create individual selects descriptions for ecoster."""
    entities = []

    for i in range(1, AVAILABLE_NUMBER_OF_ECOSTERS + 1):

        description = EconetSelectEntityDescription(
            key=f"STER_MODE_{i}",
            name=f"EcoSTER {i} Operating mode edit",
            options = [MODE_SCHEDULE, MODE_ECO, MODE_COMFORT, MODE_OUTSIDE, MODE_AIRING, MODE_PARTY, MODE_HOLIDAY, MODE_ANTIFREEZ],
            translation_key=f"ecoster_{i}_mode_select",
            icon="mdi:sync",
            entity_registry_visible_default=True,
        )

        if can_add(description, coordinator) and can_add(description, coordinator):
            entities.append(EcosterSelect(description, coordinator, api, i))
        else:
            _LOGGER.debug(
                "Availability key: %s does not exist, entity will not be added",
                description.key,
            )
    return entities

def create_mixer_selects(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create individual selects descriptions for ecoster."""
    entities = []

    for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1):

        description = EconetSelectEntityDescription(
            key=f"CTRL_WEATHER_MIX_{i}",
            name=f"Mixer {i} Weather temperature control circuit",
            options = [OFF, ON],
            translation_key=f"mixer_{i}_ctrl_weather",
            icon="mdi:weather-partly-cloudy",
            entity_registry_visible_default=True,
        )

        if can_add(description, coordinator) and can_add(description, coordinator):
            entities.append(MixerSelect(description, coordinator, api, i))
        else:
            _LOGGER.debug(
                "Availability key: %s does not exist, entity will not be added",
                description.key,
            )
        description = EconetSelectEntityDescription(
            key=f"MIX_THERM_MODE_{i}",
            name=f"Mixer {i} Circulation thermostat mode",
            options = [OFF, THERMOSTAT_CONTACT, ECOSTER1, ECOSTER2], # For future Check number of ecosters!!!
            translation_key=f"mixer_{i}_therm_mode",
            icon="mdi:thermostat-cog",
            entity_registry_visible_default=True,
        )

        if can_add(description, coordinator) and can_add(description, coordinator):
            entities.append(MixerSelect(description, coordinator, api, i))
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
    """Set up the select platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetSelect] = []
    entities = entities + create_ecoster_selects(coordinator, api)
    entities = entities + create_mixer_selects(coordinator, api)

    return async_add_entities(entities)
