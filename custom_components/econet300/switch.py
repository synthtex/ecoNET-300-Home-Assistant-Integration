"""Base Switch for Econet300."""
from dataclasses import dataclass
from typing import Any, Final, Literal, Union
from typing_extensions import TypeAlias

import logging

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)

STATE_ON: Final = range(1,26)
STATE_OFF: Final = "0"

ParameterValue: TypeAlias = Union[int, float, bool, Literal["off", "on"]]

def _normalize_parameter_value(value: ParameterValue) -> int:
    """Normalize a parameter value."""
    if value in (STATE_OFF, STATE_ON):
        return 1 if value == STATE_ON else 0

    return int(value)

@dataclass
class EconetSwitchEntityDescription(SwitchEntityDescription):
    """Describes Econet switch entity."""
    state_off: ParameterValue = STATE_OFF
    state_on: ParameterValue = STATE_ON
    icon_off: str | None = None


SWITCH_TYPES: tuple[EconetSwitchEntityDescription, ...] = (
    EconetSwitchEntityDescription(
        key="mode",
        name="CH Boiler Switch",
        translation_key="boiler_switch",
        icon="mdi:light-switch",
        icon_off="mdi:light-switch-off",
        state_off= 0,
        state_on= range(1,26),
        entity_registry_visible_default=True,
    ),
)

class EconetSwitch(EconetEntity, SwitchEntity):
    """Describes Econet switch entity."""

    _attr_is_on: bool | None = None
    entity_description: EconetSwitchEntityDescription

    def __init__(
        self,
        description: EconetSwitchEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize the ControllerSwitch."""
        super().__init__(description, coordinator, api)

    def _sync_state(self, value):
        """Sync state."""
        boilerstate = self._coordinator.data[self.entity_description.key]
        if boilerstate == 0:
            self._attr_is_on = False
        else:
            self._attr_is_on = True
        self.async_write_ha_state()
        
    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend."""
        return (
            self.entity_description.icon_off
            if self.entity_description.icon_off is not None and not self.is_on
            else self.entity_description.icon
        )


    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        if not await self._api.set_param(self.entity_description.key, 1):
            _LOGGER.warning("Switch on the Boiler failed")
            return

        self._attr_is_on = True
        self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        if not await self._api.set_param(self.entity_description.key, 0):
            _LOGGER.warning("Switch off the Boiler failed")
            return
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_update(self, value) -> None:
        """Update entity state."""
        boilerstate = self._coordinator.data[self.entity_description.key]
        if boilerstate == 0:
            self._attr_is_on = False
        else:
            self._attr_is_on = True
        self.async_write_ha_state()

def can_add(desc: EconetSwitchEntityDescription, coordinator: EconetDataCoordinator):
    """Check if it can add the key."""
    if desc.key not in coordinator.data:
        _LOGGER.debug("Key %s does not exist in coordinator.data", desc.key)
        return False
    return coordinator.has_data(desc.key) and coordinator.data[desc.key] is not None

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the switch platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetSwitch] = []

    for description in SWITCH_TYPES:

        if can_add(description, coordinator):
            entities.append(EconetSwitch(description, coordinator, api))
        else:
            _LOGGER.debug(
                "Cannot add entity - availability key: %s does not exist",
                description.key,
            )

    return async_add_entities(entities)
