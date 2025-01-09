"""Base Number for Econet300."""
from dataclasses import dataclass
import logging

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.exceptions import ServiceValidationError
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Limits, Econet300Api
from .common import EconetDataCoordinator
from .const import (
    DOMAIN,
    SERVICE_API,
    SERVICE_COORDINATOR,
    ENTITY_MIN_VALUE,
    ENTITY_MAX_VALUE,
    EDITABLE_PARAMS_MAPPING_TABLE,
    AVAILABLE_NUMBER_OF_MIXERS,
    AVAILABLE_NUMBER_OF_ECOSTERS

)
from .entity import EconetEntity, MixerEntity, EcosterEntity
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
        EconetNumberEntityDescription(
        key="EXTERN_BOILER_TEMP",
        name="Outer boiler turn-off temperature",
        translation_key="extern_boiler_temp",
        icon="mdi:thermometer",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_registry_visible_default=True,
        min_value=25,
        max_value=60,
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
        #self.hass.async_create_task(self.async_set_limits_values()) 

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
        if "MIX_SET_TEMP" in self.entity_description.key:
            if self.entity_description.key == f"MIX_SET_TEMP_{str(self._idx)}" and self._coordinator.data[f"CTRL_WEATHER_MIX_{str(self._idx)}"] == 1:
                _LOGGER.warning(f"Weather control for MIXER {str(self._idx)} is used to set the temperature.")
                raise ServiceValidationError(f"Weather control for MIXER {str(self._idx)} is used to set the temperature.")
                return
        else:
            if not await self._api.set_param(self.entity_description.key, value):
                _LOGGER.warning("Setting value failed")
                return

        if not await self._api.set_param(self.entity_description.key, value):
            _LOGGER.warning("Setting value failed")
            return

        self._attr_native_value = value
        self.async_write_ha_state()

class MixerNumber(MixerEntity, EconetNumber):
    """Mixer sensor class."""

    def __init__(
            self,
            description: EconetNumberEntityDescription,
            coordinator: EconetDataCoordinator,
            api: Econet300Api,
            idx: int,
        ):
            """Initialize a new instance of the EconetSensor class."""
            super().__init__(description, coordinator, api, idx)

class EcosterNumber(EcosterEntity, EconetNumber):
    """Mixer sensor class."""

    def __init__(
            self,
            description: EconetNumberEntityDescription,
            coordinator: EconetDataCoordinator,
            api: Econet300Api,
            idx: int,
        ):
            """Initialize a new instance of the EconetSensor class."""
            super().__init__(description, coordinator, api, idx)

def create_mixer_numbers(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create individual sensor descriptions for mixer sensors."""
    entities = []

    for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1):
        description = EconetNumberEntityDescription(
            key=f"MIX_HEAT_CURVE_{i}",  # MIX_HEAT_CURVE_4
            name=f"Mixer {i} Heating curve",
            translation_key=f"mix_heat_curve_{i}",
            icon="mdi:chart-bell-curve-cumulative",
            mode=NumberMode.BOX,
            device_class=NumberDeviceClass.POWER_FACTOR,
            entity_registry_visible_default=True,
            min_value=0.1,
            max_value=4.0,
            native_step=0.1,
        )
        if can_add(description, coordinator):
            entities.append(MixerNumber(description, coordinator, api, i))
            
        else:
            _LOGGER.debug(
                "Availability key: %s does not exist, entity will not be added",
                description.key,
            )
        avail_mixer_key = f"mixerTemp{i}"
        if can_add_number(avail_mixer_key, coordinator):
            weather_temp_factor = EconetNumberEntityDescription(
                key=f"WEATHER_TEMP_FACTOR_{i}",
                name=f"Mixer {i} Temperature coefficient weather",
                translation_key=f"weather_temp_factor_{i}",
                icon="mdi:chart-bell-curve",
                mode=NumberMode.BOX,
                device_class=NumberDeviceClass.POWER_FACTOR,
                entity_registry_visible_default=True,
                min_value=0,
                max_value=50,
                native_step=1,
            )
            entities.append(MixerNumber(weather_temp_factor, coordinator, api, i))
        else:
            _LOGGER.debug(
                f"Availability key: WEATHER_TEMP_FACTOR_{i} does not exist, entity will not be added"
            )
        if can_add_number(avail_mixer_key, coordinator):
            parallel_offset_heat_curv = EconetNumberEntityDescription(
                key=f"PARALLEL_OFFSET_HEAT_CURV_{i}",
                name=f"Mixer {i} Parallel displacement of heating curve",
                translation_key=f"parallel_offset_heat_curv_{i}",
                icon="mdi:chart-areaspline",
                mode=NumberMode.BOX,
                device_class=NumberDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                entity_registry_visible_default=True,
                min_value=-20,
                max_value=20,
                native_step=1,
            )
            entities.append(MixerNumber(parallel_offset_heat_curv, coordinator, api, i))
        else:
            _LOGGER.debug(
                f"Availability key: PARALLEL_OFFSET_HEAT_CURV_{i} does not exist, entity will not be added"
            )
        if can_add_number(avail_mixer_key, coordinator):
            low_mix_set_temp = EconetNumberEntityDescription(
                key=f"LOW_MIX_SET_TEMP_{i}",
                name=f"Mixer {i} Lowering temp. by thermostat",
                translation_key=f"parallel_offset_heat_curv_{i}",
                icon="mdi:thermometer-chevron-down",
                mode=NumberMode.BOX,
                device_class=NumberDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                entity_registry_visible_default=True,
                min_value=0,
                max_value=30,
                native_step=1,
            )
            entities.append(MixerNumber(low_mix_set_temp, coordinator, api, i))
        else:
            _LOGGER.debug(
                f"Availability key: LOW_MIX_SET_TEMP_{i} does not exist, entity will not be added"
            )
        if can_add_number(avail_mixer_key, coordinator):
            low_mix_set_temp = EconetNumberEntityDescription(
                key=f"MIX_SET_TEMP_{i}",
                name=f"Mixer {i} Set temperature heating circuit",
                translation_key=f"mix_set_temp_{i}",
                icon="mdi:thermometer",
                mode=NumberMode.BOX,
                device_class=NumberDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                entity_registry_visible_default=True,
                min_value=20,
                max_value=50,
                native_step=1,
            )
            entities.append(MixerNumber(low_mix_set_temp, coordinator, api, i))
        else:
            _LOGGER.debug(
                f"Availability key: MIX_SET_TEMP_{i} does not exist, entity will not be added"
            )
    return entities

def create_ecoster_numbers(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create individual sensor descriptions for mixer sensors."""
    entities = []
    for i in range(1, AVAILABLE_NUMBER_OF_ECOSTERS + 1):
        avail_ecoster_key = f"ecoSterTemp{i}"
        if can_add_number(avail_ecoster_key, coordinator):
            ster_temp_day = EconetNumberEntityDescription(
                key=f"STER_TEMP_DAY_{i}",
                name=f"ecoSTER {i} Temperature set point day",
                translation_key=f"ster_temp_day_{i}",
                icon="mdi:sun-thermometer-outline",
                mode=NumberMode.BOX,
                device_class=NumberDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                entity_registry_visible_default=True,
                min_value=10,
                max_value=35,
                native_step=0.1,
            )
            entities.append(EcosterNumber(ster_temp_day, coordinator, api, i))
        else:
            _LOGGER.debug(
                f"Availability key: STER_TEMP_DAY_{i} does not exist, entity will not be added"
            )
        if can_add_number(avail_ecoster_key, coordinator):
            ster_temp_night = EconetNumberEntityDescription(
                key=f"STER_TEMP_NIGHT_{i}",
                name=f"ecoSTER {i} Temperature set point night",
                translation_key=f"ster_temp_night_{i}",
                icon="mdi:sun-thermometer",
                mode=NumberMode.BOX,
                device_class=NumberDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                entity_registry_visible_default=True,
                min_value=10,
                max_value=35,
                native_step=0.1,
            )
            entities.append(EcosterNumber(ster_temp_night, coordinator, api, i))
        else:
            _LOGGER.debug(
                f"Availability key: STER_TEMP_NIGHT_{i} does not exist, entity will not be added"
            )
    return entities

def can_add_number(
    desc: str, coordinator: EconetDataCoordinator
):
    return (
        coordinator.has_data(desc)
        and coordinator.data[desc] is not None
    )

def can_add(desc: EconetNumberEntityDescription, coordinator: EconetDataCoordinator):
    """Check if a given entity can be added based on the availability of data in the coordinator."""
    _LOGGER 
    return coordinator.has_data(desc.key) and coordinator.data[desc.key]

def create_controller_numbers(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Add key."""
    entities = []

    for description in NUMBER_TYPES:
        # number_limits = await api.get_param_limits(description.key)

        # if number_limits is None:
        #     _LOGGER.warning(
        #         "Cannot add entity: {}, numeric limits for this entity is None"
        #     )
        #     continue

        if can_add(description, coordinator):
            # apply_limits(description, number_limits)
            entities.append(EconetNumber(description, coordinator, api))
        else:
            _LOGGER.debug(
                "Cannot add entity - availability key: %s does not exist",
                description.key,
            )
    return entities

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
    entities = entities + create_controller_numbers(coordinator, api)
    entities = entities + create_mixer_numbers(coordinator, api)
    entities = entities + create_ecoster_numbers(coordinator, api)
    
    return async_add_entities(entities)
