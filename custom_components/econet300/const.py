"""Constants from the Home Assistant"""
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfTemperature,
    EntityCategory,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)

# Constant for the econet Integration integration
DOMAIN = "econet300"

SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"

DEVICE_INFO_MANUFACTURER = "PLUM"
DEVICE_INFO_MODEL = "ecoNET300"
DEVICE_INFO_CONTROLLER_NAME = "PLUM ecoNET300"
DEVICE_INFO_MIXER_NAME = "Mixer"

CONF_ENTRY_TITLE = "ecoNET300"
CONF_ENTRY_DESCRIPTION = "PLUM Econet300"

## Sys params
API_SYS_PARAMS_URI = "sysParams"
API_SYS_PARAMS_PARAM_UID = "uid"
API_SYS_PARAMS_PARAM_SW_REV = "softVer"
API_SYS_PARAMS_PARAM_HW_VER = "routerType"

## Reg params
API_REG_PARAMS_URI = "regParams"
API_REG_PARAMS_PARAM_DATA = "curr"

## Reg params data all in one
API_REG_PARAMS_DATA_URI = "regParamsData"
API_REG_PARAMS_DATA_PARAM_DATA = "data"

## Map names for params data in API_REG_PARAMS_DATA_URI
API_RM_CURRENT_DATA_PARAMS_URI = "rmCurrentDataParams"

## Mapunits for params data map API_RM_CURRENT_DATA_PARAMS_URI
API_RM_PARAMSUNITSNAMES_URI = "rmParamsUnitsNames"

## Boiler staus keys map
# boiler mode names from  endpoint http://LocalIP/econet/rmParamsEnums?
OPERATION_MODE_NAMES = {
    0: "TURNED OFF",
    1: "FIRE UP",
    2: "FIRE UP",
    3: "WORK",
    4: "SUPERVISION",
    5: "Halted",
    6: "STOP",
    7: "BURNING OFF",
    8: "MANUAL",
    9: "ALARM",
    10: "UNSEALING",
    11: "CHIMNEY",
    12: "STABILIZATION",
    13: "NO TRANSMISSION",
}

# add constants to future
PRODUCT_TYPE = {
    0: "ECOMAX_850P_TYPE",
    1: "ECOMAX_850i_TYPE",
}

## Editable params limits
API_EDIT_PARAM_URI = "rmCurrNewParam"
API_EDITABLE_PARAMS_LIMITS_URI = "rmCurrentDataParamsEdits"
API_EDITABLE_PARAMS_LIMITS_DATA = "data"

EDITABLE_PARAMS_MAPPING_TABLE = {
    "tempCOSet": "1280",
    "tempCWUSet": "1281",
    "mixerSetTemp1": "1287",
    "mixerSetTemp2": "1288",
    "mixerSetTemp3": "1289",
    "mixerSetTemp4": "1290",
    "mixerSetTemp5": "1291",
    "mixerSetTemp6": "1292",
}

#######################
######## REG PARAM MAPS
#######################
REG_PARAM_MAP = {
    "26": "tempFeeder",
    "28": "tempExternalSensor",
    "97": "fuelLevel",
    "117": "thermostat",
    "139": "valveMixer1",
    "151": "lambdaStatus",
    "153": "lambdaSet",
    "154": "lambdaLevel",
    "170": "signal",
    "1024": "tempCO",
    "1025": "tempCWU",
    "1028": "tempUpperBuffer",
    "1029": "tempLowerBuffer",
    "1030": "tempFlueGas",
    "1031": "mixerTemp1",
    "1287": "mixerSetTemp1",
    "1792": "mode",
    "1794": "boilerPower",
    "1795": "fanPower",
    "1280": "tempCOSet",
}

# Unknown ID's
# tempBack: "tempBack", pas mane nera tokio parametro
#    "1025": "tempCOSet", pas mane nera i6jungtas :(
#               quality


# Sensors units from econet dev
REG_PARAM_UNIT = {
    "tempCO": UnitOfTemperature.CELSIUS,
    "tempCOSet": UnitOfTemperature.CELSIUS,
    "tempExternalSensor": UnitOfTemperature.CELSIUS,
    "tempFeeder": UnitOfTemperature.CELSIUS,
    "lambdaLevel": PERCENTAGE,
    "lambdaSet": PERCENTAGE,
    "thermoTemp": UnitOfTemperature.CELSIUS,
    "fanPower": PERCENTAGE,
    "tempFlueGas": UnitOfTemperature.CELSIUS,
    "mixerSetTemp1": UnitOfTemperature.CELSIUS,
    "mixerTemp1": UnitOfTemperature.CELSIUS,
    "tempBack": UnitOfTemperature.CELSIUS,
    "tempCWU": UnitOfTemperature.CELSIUS,
    "boilerPower": PERCENTAGE,
    "fuelLevel": PERCENTAGE,
    "tempUpperBuffer": UnitOfTemperature.CELSIUS,
    "tempLowerBuffer": UnitOfTemperature.CELSIUS,
    "signal": SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    "quality": PERCENTAGE,
    "valveMixer1": PERCENTAGE,
}

REG_PARAM_STATE_CLASS = {
    "tempFeeder": SensorStateClass.MEASUREMENT,
    "tempExternalSensor": SensorStateClass.MEASUREMENT,
    "lambdaSet": SensorStateClass.MEASUREMENT,
    "lambdaLevel": SensorStateClass.MEASUREMENT,
    "tempCO": SensorStateClass.MEASUREMENT,
    "tempCOSet": SensorStateClass.MEASUREMENT,
    "boilerPower": SensorStateClass.MEASUREMENT,
    "fanPower": SensorStateClass.MEASUREMENT,
    "tempFlueGas": SensorStateClass.MEASUREMENT,
    "mixerSetTemp1": SensorStateClass.MEASUREMENT,
    "tempBack": SensorStateClass.MEASUREMENT,
    "tempCWU": SensorStateClass.MEASUREMENT,
    "fuelLevel": SensorStateClass.MEASUREMENT,
    "tempUpperBuffer": SensorStateClass.MEASUREMENT,
    "tempLowerBuffer": SensorStateClass.MEASUREMENT,
    "signal": SensorStateClass.MEASUREMENT,
    "quality": SensorStateClass.MEASUREMENT,
    "valveMixer1": SensorStateClass.MEASUREMENT,
}

REG_PARAM_DEVICE_CLASS = {
    "tempFeeder": SensorDeviceClass.TEMPERATURE,
    "tempExternalSensor": SensorDeviceClass.TEMPERATURE,
    "tempCO": SensorDeviceClass.TEMPERATURE,
    "tempCOSet": SensorDeviceClass.TEMPERATURE,
    "boilerPower": SensorDeviceClass.POWER_FACTOR,
    "fanPower": SensorDeviceClass.POWER_FACTOR,
    "tempFlueGas": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp1": SensorDeviceClass.TEMPERATURE,
    "tempBack": SensorDeviceClass.TEMPERATURE,
    "tempCWU": SensorDeviceClass.TEMPERATURE,
    "mode": "DEVICE_CLASS_OPERATION_MODE",
    "tempUpperBuffer": SensorDeviceClass.TEMPERATURE,
    "tempLowerBuffer": SensorDeviceClass.TEMPERATURE,
    "signal": SensorDeviceClass.SIGNAL_STRENGTH,
    "softVer": "econet_software_version",
    "moduleASoftVer": "module_a_software_version",
    "moduleBSoftVer": "Module_b_software_version",
    "modulePanelSoftVer": "module_panel_software_version",
    "moduleLambdaSoftVer": "module_lamda_software_version",
    "protocolType": "protocol_type",
    "controllerID": "controller_ID",
    "valveMixer1": "valve_mixer_1",
}

"""Add only keys where precision more than 0 needed"""
REG_PARAM_PRECISION = {
    "tempFeeder": 1,
    "tempExternalSensor": 1,
    "lambdaLevel": 1,
    "lambdaSet": 1,
    "tempCO": 1,
    "mixerTemp1": 1,
    "tempBack": 2,
    "tempUpperBuffer": 1,
    "tempLowerBuffer": 1,
    "tempCWU": 1,
    "tempFlueGas": 1,
}

REG_PARAM_VALUE_PROCESSOR = {
    "mode": lambda x: OPERATION_MODE_NAMES.get(x, "Unknown"),
    "thermostat": lambda x: "ON"
    if str(x).strip() == "true"
    else ("OFF" if str(x).strip() == "false" else None),
    "lambdaStatus": lambda x: "STOP"
    if x == 0
    else ("START" if x == 1 else ("Working" if x == 2 else "Unknown")),
}

REG_PARAM_ENTITY_CATEGORY = {
    "signal": EntityCategory.DIAGNOSTIC,
    "quality": EntityCategory.DIAGNOSTIC,
    "softVer": EntityCategory.DIAGNOSTIC,
    "moduleASoftVer": EntityCategory.DIAGNOSTIC,
    "moduleBSoftVer": EntityCategory.DIAGNOSTIC,
    "modulePanelSoftVer": EntityCategory.DIAGNOSTIC,
    "moduleLambdaSoftVer": EntityCategory.DIAGNOSTIC,
    "protocolType": EntityCategory.DIAGNOSTIC,
    "controllerID": EntityCategory.DIAGNOSTIC,
}

# Default values for visible 'entity_registry_visible_default=False,' in sensor.py
REG_PARAM_VISIBLE_DEFAULT = {
    "tempUpperBuffer": False,
    "tempLowerBuffer": False,
}
