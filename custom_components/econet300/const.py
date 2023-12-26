"""Constants from the Home Assistant"""
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
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
    0: "off",
    1: "fire_up",
    2: "fire_up",
    3: "work",
    4: "supervision",
    5: "halted",
    6: "stop",
    7: "burning_off",
    8: "manual",
    9: "alarm",
    10: "unsealing",
    11: "chimney",
    12: "stabilization",
    13: "no_transmission",
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
SENSOR_MAP = {
    "26": "tempFeeder",
    "28": "tempExternalSensor",
    "97": "fuelLevel",
    "139": "valveMixer1",
    "143": "servoMixer1",
    "151": "lambdaStatus",
    "153": "lambdaSet",
    "154": "lambdaLevel",
    "168": "main_server",
    "170": "signal",
    "171": "status_wifi",
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

BINARY_SENSOR_MAP = {
    "111": "weatherControl",
    "113": "unseal",
    "117": "thermostat",
    "118": "pumpCOWorks",
    "1536": "fanWorks",
    "1540": "aditionalFeeder",
    "1541": "pumpFireplaceWorks",
    "1542": "pumpCWUWorks",
}

ENTITY_UNIT_MAP = {
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
    "burnerOutput": PERCENTAGE,
}

STATE_CLASS_MAP = {
    "tempFeeder": SensorStateClass.MEASUREMENT,
    "tempExternalSensor": SensorStateClass.MEASUREMENT,
    "lambdaSet": SensorStateClass.MEASUREMENT,
    "lambdaLevel": SensorStateClass.MEASUREMENT,
    "tempCO": SensorStateClass.MEASUREMENT,
    "tempCOSet": SensorStateClass.MEASUREMENT,
    "boiler_power": SensorStateClass.MEASUREMENT,
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
    "burnerOutput": SensorStateClass.MEASUREMENT,
}

ENTITY_DEVICE_CLASS_MAP = {
    #############################
    ######### SENSORS ##########
    #############################
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
    "servoMixer1": "servo_mixer_1",
    "Status_wifi": "wifi_status",
    "main_server": "main_server",
    #############################
    ###### BINARY SENSORS #######
    #############################
    "weatherControl": BinarySensorDeviceClass.RUNNING,
    "unseal": BinarySensorDeviceClass.RUNNING,
    "thermostat": BinarySensorDeviceClass.RUNNING,
    "pumpCOWorks": BinarySensorDeviceClass.RUNNING,
    "fanWorks": BinarySensorDeviceClass.RUNNING,
    "aditionalFeeder": BinarySensorDeviceClass.RUNNING,
    "pumpFireplaceWorks": BinarySensorDeviceClass.RUNNING,
    "pumpCWUWorks": BinarySensorDeviceClass.RUNNING,
}

"""Add only keys where precision more than 0 needed"""
ENTITY_PRECISION = {
    "tempFeeder": 1,
    "tempExternalSensor": 1,
    "fuelLevel": 0,
    "lambdaLevel": 1,
    "lambdaSet": 1,
    "tempCO": 1,
    "tempCOSet": 0,
    "fanPower": 0,
    "mixerSetTemp1": 0,
    "mixerTemp1": 1,
    "tempBack": 2,
    "tempUpperBuffer": 1,
    "tempLowerBuffer": 1,
    "tempCWU": 1,
    "tempFlueGas": 1,
}

ENTITY_ICON = {
    "mode": "mdi:sync",
    "fanPower": "mdi:fan",
    "temCO": "mdi:thermometer-lines",
    "tempCOSet": "mdi:thermometer-chevron-up",
    "thermostat": "mdi:thermostat",
    "boilerPower": "mdi:gauge",
    "fuelLevel": "mdi:gas-station",
    "lambdaLevel": "mdi:lambda",
    "lambdaSet": "mdi:lambda",
    "lambdaStatus": "mdi:lambda",
    "quality": "mdi:signal",
    "pumpCOWorks": "mdi:pump",
    "fanWorks": "mdi:fan",
    "aditionalFeeder": "mdi:screw-lag",
    "pumpFireplaceWorks": "mdi:pump",
    "pumpCWUWorks": "mdi:pump",
    "main_server": "mdi:server",
}

ENTITY_ICON_OFF = {
    "pumpCOWorks": "mdi:pump-off",
    "fanWorks": "mdi:fan-off",
    "aditionalFeeder": "mdi:screw-lag",
    "pumpFireplaceWorks": "mdi:pump-off",
    "pumpCWUWorks": "mdi:pump-off",
}

ENTITY_VALUE_PROCESSOR = {
    "mode": lambda x: OPERATION_MODE_NAMES.get(x, "unknown"),
    "thermostat": (
        lambda x: "ON"
        if str(x).strip() == "true"
        else ("OFF" if str(x).strip() == "false" else None)
    ),
    "lambdaStatus": (
        lambda x: "stop"
        if x == 0
        else ("start" if x == 1 else ("working" if x == 2 else "unknown"))
    ),
    "status_wifi": lambda x: "Connected" if x == 1 else "Disconnected",
    "main_server": lambda x: "Server available" if x == 1 else "Server not available",
}

ENTITY_CATEGORY = {
    "signal": EntityCategory.DIAGNOSTIC,
    "quality": EntityCategory.DIAGNOSTIC,
    "softVer": EntityCategory.DIAGNOSTIC,
    "moduleASoftVer": EntityCategory.DIAGNOSTIC,
    "moduleBSoftVer": EntityCategory.DIAGNOSTIC,
    "modulePanelSoftVer": EntityCategory.DIAGNOSTIC,
    "moduleLambdaSoftVer": EntityCategory.DIAGNOSTIC,
    "protocolType": EntityCategory.DIAGNOSTIC,
    "controllerID": EntityCategory.DIAGNOSTIC,
    "Status_wifi": EntityCategory.DIAGNOSTIC,
    "main_server": EntityCategory.DIAGNOSTIC,
}

# Default values for visible 'entity_registry_visible_default=False,' in sensor.py
REG_PARAM_VISIBLE_DEFAULT = {
    "tempUpperBuffer": False,
    "tempLowerBuffer": False,
}
