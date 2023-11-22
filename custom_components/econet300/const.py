"""Constants for the econet Integration integration."""

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
API_REG_PARAMS_DATA_PARAM_DATA ='data'

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

# Sensors precision value from econet dev
REG_PARAM_PRECICION = {
    "boilerPowerKW": 1,
    "boilerPower": 0,
    "fuelStream": 1,
    "ecoSterTemp": 1,
    "ecoSterSetTemp": 1,
    "tempExternalSensor": 1,
    "lambdaSet": 1,
    "lambdaLevel": 1,
    "thermoTemp": 1,
    "thermoSetTemp": 0,
}

# Sensors units from econet dev
RG_PARAM_UNIT = {
    'T1': '°C',
    'T2': '°C',
    'T3': '°C',
    'T4': '°C',
    'T5': '°C',
    'T6': '°C',
    'P1': '%',
    'P2': '%',
    'H': '',
    'TzCWU': '°C',
    'tempCO': '°C',
    'tempCOSet': '°C',
    'tempCWU': '°C',
    'tempCWUSet': '°C',
    'tempOpticalSensor': '%',
    'fanPower': '%',
    'fuelLevel': '%',
    'tempUpperBuffer': '°C',
    'tempLowerBuffer': '°C',
    'tempUpperSolar': '°C',
    'tempLowerSolar': '°C',
    'tempFireplace': '°C',
    'tempExternalSensor': '°C',
    'tempBack': '°C',
    'fuelStream': 'kg/h',
    'tempFeeder': '°C',
    'tempFlueGas': '°C',
    'boilerPowerKW': 'kW',
    'boilerPower': '%',
    'ecoSterTemp1': '°C',
    'ecoSterTemp2': '°C',
    'ecoSterTemp3': '°C',
    'ecoSterTemp4': '°C',
    'ecoSterTemp5': '°C',
    'ecoSterTemp6': '°C',
    'ecoSterTemp7': '°C',
    'ecoSterTemp8': '°C',
    'ecoSterSetTemp1': '°C',
    'ecoSterSetTemp2': '°C',
    'ecoSterSetTemp3': '°C',
    'ecoSterSetTemp4': '°C',
    'ecoSterSetTemp5': '°C',
    'ecoSterSetTemp6': '°C',
    'ecoSterSetTemp7': '°C',
    'ecoSterSetTemp8': '°C',
    'mixerTemp1': '°C',
    'mixerTemp2': '°C',
    'mixerTemp3': '°C',
    'mixerTemp4': '°C',
    'mixerTemp5': '°C',
    'mixerTemp6': '°C',
    'mixerTemp7': '°C',
    'mixerTemp8': '°C',
    'mixerSetTemp1': '°C',
    'mixerSetTemp2': '°C',
    'mixerSetTemp3': '°C',
    'mixerSetTemp4': '°C',
    'mixerSetTemp5': '°C',
    'mixerSetTemp6': '°C',
    'mixerSetTemp7': '°C',
    'mixerSetTemp8': '°C',
    'lambdaLevel': '%',
    'lambdaSet': '%',
    'LPTc': '°C',
    'LPTsc': '°C',
    'BHThc': '°C',
    'LPTbackc': '°C',
    'LPTbc': '°C',
    'totalGain': 'kWh',
    'blowFan1BlowPower': '%',
    'blowFan2BlowPower': '%',
    'tempExchanger': '°C',
    'tempAirIn': '°C',
    'tempAirOut': '°C',
    'thermoTemp': '°C',
    'thermoSetTemp': '°C',
    'fanPowerExhaust': '%'
}