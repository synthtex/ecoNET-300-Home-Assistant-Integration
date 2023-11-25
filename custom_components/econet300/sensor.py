"""Sensor for Econet300"""
from dataclasses import dataclass
from typing import Callable, Any

import logging

from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common_functions import camel_to_snake
from .common import EconetDataCoordinator, Econet300Api
from .const import (
    DOMAIN,
    ENTITY_DEVICE_CLASS_MAP,
    STATE_CLASS_MAP,
    SERVICE_COORDINATOR,
    SERVICE_API,
<<<<<<< HEAD
    SENSOR_MAP,
    ENTITY_PRECISION,
    ENTITY_UNIT_MAP,
    ENTITY_VALUE_PROCESSOR,
    ENTITY_CATEGORY,
    ENTITY_ICON,
=======
    OPERATION_MODE_NAMES,
    REG_PARAM_PRECICION,
>>>>>>> 3939829 (add sensor precision)
)

from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes Econet sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x


<<<<<<< HEAD
class EconetSensor(EconetEntity, SensorEntity):
=======
SENSOR_TYPES: tuple[EconetSensorEntityDescription, ...] = (
    EconetSensorEntityDescription(
        key="fanPower",
        name="Fan power",
        icon="mdi:fan",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER_FACTOR,
        process_val=lambda x: round(x, 2),
    ),
    EconetSensorEntityDescription(
        key="tempCO",
        name="Boiler actual temp.",
        icon="mdi:thermometer-lines",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=REG_PARAM_PRECICION["tempCO"],
        process_val=lambda x: x,
    ),
    EconetSensorEntityDescription(
        key="tempCOSet",
        name="Boiler set temp.",
        icon="mdi:thermometer-chevron-up",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2),
    ),
    EconetSensorEntityDescription(
        key="tempFeeder",
        name="Feeder temp.",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=REG_PARAM_PRECICION["tempFeeder"],
        process_val=lambda x: x,
    ),
    EconetSensorEntityDescription(
        key="tempFlueGas",
        name="Exhaust temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=REG_PARAM_PRECICION["tempFlueGas"],
        process_val=lambda x: x,
    ),
    EconetSensorEntityDescription(
        key="mixerSetTemp1",
        name="Mixer 1 set temp.",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2),
    ),
    EconetSensorEntityDescription(
        key="tempBack",
        name="Water back temperature ",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2),
    ),
    EconetSensorEntityDescription(
        key="tempCWU",
        name="Water temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2),
    ),
    EconetSensorEntityDescription(
        key="tempExternalSensor",
        name="Outside temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=REG_PARAM_PRECICION["tempExternalSensor"],
        process_val=lambda x: x,
    ),
    EconetSensorEntityDescription(
        key="boilerPower",
        name="Boiler output",
        icon="mdi:gauge",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER_FACTOR,
        suggested_display_precision=REG_PARAM_PRECICION["boilerPower"],
        process_val=lambda x: x,
    ),
    EconetSensorEntityDescription(
        key="fuelLevel",
        name="Fuel level",
        icon="mdi:gas-station",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        process_val=lambda x: round(x, 1),
    ),
    EconetSensorEntityDescription(
        key="mode",
        name="Operation mode",
        icon="mdi:sync",
        device_class="DEVICE_CLASS_OPERATION_MODE",  # custom class for boiler status
        process_val=lambda x: OPERATION_MODE_NAMES.get(x, "Unknown"),
    ),
    EconetSensorEntityDescription(
        key="lambdaSet",
        name="Oxygen set level",
        icon="mdi:lambda",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        process_val=lambda x: x / 10,
    ),
    EconetSensorEntityDescription(
        key="lambdaLevel",
        name="Oxygen level",
        icon="mdi:lambda",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        process_val=lambda x: x / 10,
    ),
    EconetSensorEntityDescription(
        key="thermostat",
        name="Thermostat",
        icon="mdi:thermostat",
        process_val=lambda x: "ON"
        if str(x).strip() == "1"
        else ("OFF" if str(x).strip() == "0" else None),
    ),
    EconetSensorEntityDescription(
        key="lambdaStatus",
        name="Lambda status",
        icon="mdi:lambda",
        process_val=lambda x: "Stop"
        if x == 0
        else ("Start" if x == 1 else ("Working" if x == 2 else "Unknown")),
    ),
    EconetSensorEntityDescription(
        key="signal",
        name="Wi-Fi signal strength",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    EconetSensorEntityDescription(
        key="quality",
        name="Wi-Fi signal quality",
        icon="mdi:signal",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    EconetSensorEntityDescription(
        key="softVer",
        name="Module ecoNET software version",
        device_class="econet_software_version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    EconetSensorEntityDescription(
        key="moduleASoftVer",
        name="Module A version",
        device_class="module_a_software_version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    EconetSensorEntityDescription(
        key="moduleBSoftVer",
        name="Module B version",
        device_class="Module_b_software_version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    EconetSensorEntityDescription(
        key="modulePanelSoftVer",
        name="Module Panel version",
        icon="mdi:raspberry-pi",
        device_class="module_panel_software_version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    EconetSensorEntityDescription(
        key="moduleLambdaSoftVer",
        name="Module Lambda version",
        device_class="module_lamda_software_version",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    EconetSensorEntityDescription(
        key="protocolType",  #  "em" or "gm3_pomp"
        name="Protocol",
        device_class="protocol_type",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    EconetSensorEntityDescription(
        key="controllerID",
        name="Controler name",
        device_class="controller_ID",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


class EconetSensor(SensorEntity):
>>>>>>> 3939829 (add sensor precision)
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


def create_entity_description(key: str) -> EconetSensorEntityDescription:
    """Creates Econect300 sensor entity based on supplied key"""
    map_key = SENSOR_MAP.get(key, key)
    _LOGGER.debug("SENSOR_MAP: %s", SENSOR_MAP)
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
    for data_key in SENSOR_MAP:
        if data_key in coordinator_data:
            entities.append(
                EconetSensor(create_entity_description(data_key), coordinator, api)
            )
            _LOGGER.debug(
                "Key: %s mapped, sensor entity will be added",
                data_key,
            )
            continue
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
