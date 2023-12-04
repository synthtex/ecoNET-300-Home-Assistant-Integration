"""Constants from the Home Assistant"""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
)
from homeassistant.const import (
    UnitOfTemperature,
    PERCENTAGE
)

#Constant for the econet Integration integration
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
API_REG_PARAMS_DATA_PARAM_DATA ="data"

## Map names for params data in API_REG_PARAMS_DATA_URI
API_RM_CURRENT_DATA_PARAMS_URI ="rmCurrentDataParams"

## Mapunits for params data map API_RM_CURRENT_DATA_PARAMS_URI
API_RM_PARAMSUNITSNAMES_URI ="rmParamsUnitsNames"

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

#######################
######## REG PARAM MAPS
#######################
REG_PARAM_MAP = {
    "26": "tempFeeder",
    "28": "tempExternalSensor",
    "97": "fuelLevel",
    "117": "thermostat",
    "151": "lambdaStatus",
    "153": "lambdaSet",
    "154": "lambdaLevel",
    "1024": "tempCO",
    "1025": "tempCWU",
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
}

"""Add only keys where precision more than 0 needed"""
REG_PARAM_PRECISION = {
    "tempFeeder": 1,
    "tempExternalSensor": 1,
    "lambdaLevel": 1,
    "tempCO": 1,
    "tempCOSet": 1,
    "fanPower": 2,
    "mixerSetTemp1": 2,
    "tempBack": 2,
    "fuelLevel": 1,
}

REG_PARAM_VALUE_PROCESSOR = {
    "boilerPower": (lambda x: OPERATION_MODE_NAMES.get(x, "Unknown")),
#    "thermostat": (lambda x: "ON" if str(x).strip() == "1" else ("OFF" if str(x).strip() == "0" else None),),
#    "lambdaStatus": (lambda x: "STOP" if x == 0 else ("START" if x == 1 else ("Working" if x == 2 else "Unknown")),)
}
