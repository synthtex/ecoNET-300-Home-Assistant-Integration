"""Base Climate for Econet300."""
from dataclasses import dataclass
import logging
from typing import Any, Final

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityDescription,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_TENTHS,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Econet300Api
from .common import EconetDataCoordinator
from .const import (
    DOMAIN,
    SERVICE_API,
    SERVICE_COORDINATOR,
    AVAILABLE_NUMBER_OF_ECOSTERS
)
from .entity import EcosterThermEntity


_LOGGER = logging.getLogger(__name__)

TEMPERATURE_STEP: Final = 0.1

PRESET_SCHEDULE: Final = "Schedule"
PRESET_ECO: Final = "Economy mode"
PRESET_COMFORT: Final = "Comfort mode"
PRESET_OUTSIDE: Final = "Left the house mode"
PRESET_AIRING: Final = "Air out mode"
PRESET_PARTY: Final = "Party mode"
PRESET_HOLIDAY: Final = "Holiday mode"
PRESET_ANTIFREEZE: Final = "Frost protection mode"
PRESET_UNKNOWN: Final = "unknown"

EM_TO_HA_MODE: Final[dict[int, str]] = {
    0: PRESET_SCHEDULE,
    1: PRESET_ECO,
    2: PRESET_COMFORT,
    3: PRESET_OUTSIDE,
    4: PRESET_AIRING,
    133: PRESET_PARTY,
    6: PRESET_HOLIDAY,
    7: PRESET_ANTIFREEZE,
}

HA_TO_EM_MODE: Final = {v: k for k, v in EM_TO_HA_MODE.items()}

HA_PRESET_TO_EM_TEMP: Final[dict[str, str]] = {
    PRESET_ECO: "STER_TEMP_NIGHT_",
    PRESET_COMFORT: "STER_TEMP_DAY_",
    PRESET_OUTSIDE: "STER_TEMP_NIGHT_",
    PRESET_PARTY: "STER_TEMP_SET_PARTY_",
    PRESET_HOLIDAY: "STER_TEMP_SET_SUMMER_",
    PRESET_ANTIFREEZE: "STER_TEMP_ANTIFREEZ_",
}

@dataclass(frozen=True, kw_only=True)
class EconetClimateEntityDescription(ClimateEntityDescription):
    """Describes Climate entity."""


class EconetClimate(EcosterThermEntity, ClimateEntity):
    """Econet Climate class."""
    _attr_hvac_mode = HVACMode.HEAT
    _attr_hvac_modes = [HVACMode.HEAT]
    _attr_precision = PRECISION_TENTHS
    _attr_supported_features = (ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE)
    _attr_preset_mode: str | None
    _attr_preset_modes = list(HA_TO_EM_MODE)
    _attr_target_temperature_name: str | None = None
    _attr_target_temperature_step = TEMPERATURE_STEP
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _callbacks: dict[str]
    entity_description: EconetClimateEntityDescription


    def __init__(
            self,
            description: EconetClimateEntityDescription,
            coordinator: EconetDataCoordinator,
            api: Econet300Api,
            idx: int,
    ):
            """Initialize a new instance of the EconetClimate class."""
            self.idx = idx
            super().__init__(description, coordinator, api, idx)
    # may be
    def _sync_state(self, value):
        """Sync state."""
        therm_number = str(self.idx)
        data = self._coordinator.data
        
        value = data[f"ecoSterTemp{therm_number}"]
        mode = data[f"ecoSterMode{therm_number}"]
        
        preset_mode = EM_TO_HA_MODE[mode]
        thermstate = self._coordinator.data[f"ecoSterContacts{str(self.idx)}"]
        temperature = self._coordinator.data[f"ecoSterSetTemp{str(self.idx)}"]
        if thermstate is True:
            self._attr_hvac_action = HVACAction.HEATING
        else:
            self._attr_hvac_action = HVACAction.IDLE
        
        if mode == 7:
            self._attr_min_temp = 5
            self._attr_max_temp = 30
        else:
            self._attr_min_temp = 10
            self._attr_max_temp = 35

        self._attr_preset_mode = preset_mode
        self._attr_current_temperature = value
        self._attr_target_temperature = temperature
        self.hass.async_create_task(self._async_update_target_temperature_attributes())
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        # Tell mypy that once we here, temperature name is already set
        assert isinstance(self.target_temperature_name, str)

        temperature = round(kwargs[ATTR_TEMPERATURE], 1)
        await self._api.set_param(f"{self.target_temperature_name}{str(self.idx)}", temperature)
        self._attr_target_temperature = temperature
        self.async_write_ha_state()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        mode = HA_TO_EM_MODE[preset_mode]
        if mode == 133:
            mode = 5
        
        _LOGGER.warning("SET Therm mode: %s to %s",self.entity_description.key, mode)
        await self._api.set_param(self.entity_description.key, mode)
        self._attr_preset_mode = preset_mode
        await self._async_update_target_temperature_attributes()
        self.async_write_ha_state()

    async def async_update_target_temperature(self, value: float) -> None:
        """Update target temperature."""
        self._attr_target_temperature = value
        await self._async_update_target_temperature_attributes(value)
        self.async_write_ha_state()

    async def _async_update_target_temperature_attributes(
        self, target_temp: float | None = None
    ) -> None:
        """Update target temperature parameter name and boundaries."""
        preset_mode = self.preset_mode

        if preset_mode == PRESET_SCHEDULE:
            preset_mode = await self._async_get_current_schedule_preset(target_temp)

        if not preset_mode or preset_mode in (PRESET_AIRING, PRESET_UNKNOWN):
            # Couldn't identify preset in schedule mode or
            # preset is airing.
            return

        target_temperature_name = HA_PRESET_TO_EM_TEMP[preset_mode]
        if self.target_temperature_name == target_temperature_name:
            # Target temperature parameter name is unchanged.
            return

        self._attr_target_temperature_name = target_temperature_name


    async def _async_get_current_schedule_preset(
        self, target_temp: float | None = None
    ) -> str:
        """Get current preset for the schedule mode."""
        if target_temp is None:
            target_temp = self._coordinator.data[f"ecoSterSetTemp{str(self.idx)}"]
        target_temp = round(target_temp, 1)
        comfort_temp = self._coordinator.data[f"{HA_PRESET_TO_EM_TEMP[PRESET_COMFORT]}{str(self.idx)}"]
        eco_temp = self._coordinator.data[f"{HA_PRESET_TO_EM_TEMP[PRESET_ECO]}{str(self.idx)}"]

        schedule_preset = PRESET_UNKNOWN
        if target_temp == comfort_temp and target_temp != eco_temp:
            schedule_preset = PRESET_COMFORT

        if target_temp == eco_temp and target_temp != comfort_temp:
            schedule_preset = PRESET_ECO

        return schedule_preset

    @property
    def target_temperature_name(self) -> str | None:
        """Return the target temperature name."""
        return self._attr_target_temperature_name

def can_add(desc: EconetClimateEntityDescription, coordinator: EconetDataCoordinator):
    """Check if it can add the key."""
    if desc.key not in coordinator.data:
        _LOGGER.debug("Key %s does not exist in coordinator.data", desc.key)
        return False
    return coordinator.has_data(desc.key) and coordinator.data[desc.key] is not None

def create_ecoster_climate(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create individual selects descriptions for ecoster."""
    entities = []

    for i in range(1, AVAILABLE_NUMBER_OF_ECOSTERS + 1):

        description = EconetClimateEntityDescription(
            key=f"STER_MODE_{i}",
            name=f"EcoSTER Thermostat {i}",
            translation_key=f"ecoster_{i}_thermostat",
            entity_registry_visible_default=True,
        )

        if can_add(description, coordinator) and can_add(description, coordinator):
            entities.append(EconetClimate(description, coordinator, api, i))
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

    entities: list[EconetClimate] = []
    entities = entities + create_ecoster_climate(coordinator, api)

    return async_add_entities(entities)
