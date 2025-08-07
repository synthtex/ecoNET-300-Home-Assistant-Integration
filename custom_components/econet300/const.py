"""Constants for the econet Integration integration."""

DOMAIN = "econet300"

SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"

DEVICE_INFO_MANUFACTURER = "PLUM"
DEVICE_INFO_MODEL = "ecoNET300"
DEVICE_INFO_CONTROLLER_NAME = "PLUM ecoNET300"
DEVICE_INFO_MIXER_NAME = "Mixer"
DEVICE_INFO_ECOSTER_NAME = "EcoSTER Touch"
DEVICE_INFO_THERMOSTAT_NAME = "EcoSTER Thermostat"

CONF_ENTRY_TITLE = "ecoNET300"
CONF_ENTRY_DESCRIPTION = "PLUM Econet300"

## Sys params
API_SYS_PARAMS_URI = "sysParams"
API_SYS_PARAMS_PARAM_UID = "uid"
API_SYS_PARAMS_PARAM_MODEL_ID = "controllerID"
API_SYS_PARAMS_PARAM_SW_REV = "softVer"
API_SYS_PARAMS_PARAM_HW_VER = "routerType"

## Reg params
API_REG_PARAMS_URI = "regParams"
API_REG_PARAMS_PARAM_DATA = "curr"
API_REG_PARAMSDATA_URI = "regParamsData"
API_REG_PARAMSDATA_PARAM_DATA = "data"


## Edit params
API_EDIT_PARAMS_URI = "editParams"
API_EDIT_PARAMS_DATA = "data"

## Editable params limits
# API_EDIT_PARAM_URI = "rmCurrNewParam"
# other data params edits 
# API_EDITABLE_PARAMS_LIMITS_URI = "rmCurrentDataParamsEdits"
# API_EDITABLE_PARAMS_LIMITS_URI = "editParams"
# API_EDITABLE_PARAMS_LIMITS_DATA = "data"

## Params mapping
EDITABLE_PARAMS_MAPPING_TABLE = {
    "CO_TEMP_SET": "CO_TEMP_SET",
    "CWU_SET_TEMP": "CWU_SET_TEMP",
    "MIX_SET_TEMP_1": "MIX_SET_TEMP_1",
    "MIX_SET_TEMP_2": "MIX_SET_TEMP_2",
    "MIX_SET_TEMP_3": "MIX_SET_TEMP_3",
    "MIX_SET_TEMP_4": "MIX_SET_TEMP_4",
    "MIX_SET_TEMP_5": "MIX_SET_TEMP_5",
    "CALORIFIC_KWH_KG": "CALORIFIC_KWH_KG",
    "FUEL_KG_H": "FUEL_KG_H",
    "EXTERN_BOILER_TEMP": "EXTERN_BOILER_TEMP",
    "mode": "BOILER_CONTROL",
    "STER_MODE_1": "STER_MODE_1",
    "STER_MODE_2": "STER_MODE_2",
    "STER_MODE_3": "STER_MODE_3",
    "MIX_HEAT_CURVE_1": "MIX_HEAT_CURVE_1",
    "MIX_HEAT_CURVE_2": "MIX_HEAT_CURVE_2",
    "MIX_HEAT_CURVE_3": "MIX_HEAT_CURVE_3",
    "MIX_HEAT_CURVE_4": "MIX_HEAT_CURVE_4",
    "MIX_HEAT_CURVE_5": "MIX_HEAT_CURVE_5",
    "WEATHER_TEMP_FACTOR_1": "WEATHER_TEMP_FACTOR_1",
    "WEATHER_TEMP_FACTOR_2": "WEATHER_TEMP_FACTOR_2",
    "WEATHER_TEMP_FACTOR_3": "WEATHER_TEMP_FACTOR_3",
    "WEATHER_TEMP_FACTOR_4": "WEATHER_TEMP_FACTOR_4",
    "WEATHER_TEMP_FACTOR_5": "WEATHER_TEMP_FACTOR_5",
    "PARALLEL_OFFSET_HEAT_CURV_1": "PARALLEL_OFFSET_HEAT_CURV_1",
    "PARALLEL_OFFSET_HEAT_CURV_2": "PARALLEL_OFFSET_HEAT_CURV_2",
    "PARALLEL_OFFSET_HEAT_CURV_3": "PARALLEL_OFFSET_HEAT_CURV_3",
    "PARALLEL_OFFSET_HEAT_CURV_4": "PARALLEL_OFFSET_HEAT_CURV_4",
    "PARALLEL_OFFSET_HEAT_CURV_5": "PARALLEL_OFFSET_HEAT_CURV_5",
    "LOW_MIX_SET_TEMP_1": "LOW_MIX_SET_TEMP_1",
    "LOW_MIX_SET_TEMP_2": "LOW_MIX_SET_TEMP_2",
    "LOW_MIX_SET_TEMP_3": "LOW_MIX_SET_TEMP_3",
    "LOW_MIX_SET_TEMP_4": "LOW_MIX_SET_TEMP_4",
    "LOW_MIX_SET_TEMP_5": "LOW_MIX_SET_TEMP_5",
    "STER_TEMP_DAY_1": "STER_TEMP_DAY_1",
    "STER_TEMP_DAY_2": "STER_TEMP_DAY_2",
    "STER_TEMP_DAY_3": "STER_TEMP_DAY_3",
    "STER_TEMP_NIGHT_1": "STER_TEMP_NIGHT_1",
    "STER_TEMP_NIGHT_2": "STER_TEMP_NIGHT_2",
    "STER_TEMP_NIGHT_3": "STER_TEMP_NIGHT_3",
    "STER_TEMP_ANTIFREEZ_1": "STER_TEMP_ANTIFREEZ_1",
    "STER_TEMP_ANTIFREEZ_2": "STER_TEMP_ANTIFREEZ_2",
    "STER_TEMP_ANTIFREEZ_3": "STER_TEMP_ANTIFREEZ_3",
    "STER_TEMP_SET_PARTY_1": "STER_TEMP_SET_PARTY_1",
    "STER_TEMP_SET_PARTY_2": "STER_TEMP_SET_PARTY_2",
    "STER_TEMP_SET_PARTY_3": "STER_TEMP_SET_PARTY_3",
    "STER_TEMP_SET_SUMMER_1": "STER_TEMP_SET_SUMMER_1",
    "STER_TEMP_SET_SUMMER_2": "STER_TEMP_SET_SUMMER_2",
    "STER_TEMP_SET_SUMMER_3": "STER_TEMP_SET_SUMMER_3",
    "MIX_THERM_MODE_1": "MIX_THERM_MODE_1",
    "MIX_THERM_MODE_2": "MIX_THERM_MODE_2",
    "MIX_THERM_MODE_3": "MIX_THERM_MODE_3",
    "MIX_THERM_MODE_4": "MIX_THERM_MODE_4",
    "MIX_THERM_MODE_5": "MIX_THERM_MODE_5",
    "CTRL_WEATHER_MIX_1": "CTRL_WEATHER_MIX_1",
    "CTRL_WEATHER_MIX_2": "CTRL_WEATHER_MIX_2",
    "CTRL_WEATHER_MIX_3": "CTRL_WEATHER_MIX_3",
    "CTRL_WEATHER_MIX_4": "CTRL_WEATHER_MIX_4",
    "CTRL_WEATHER_MIX_5": "CTRL_WEATHER_MIX_5"
}

AVAILABLE_NUMBER_OF_MIXERS = 5
AVAILABLE_NUMBER_OF_ECOSTERS = 3

ENTITY_MIN_VALUE = {
    "CO_TEMP_SET": 60,
    "CALORIFIC_KWH_KG": 0.1,
    "CWU_SET_TEMP": 20,
    "FUEL_KG_H": 0.1,
    "EXTERN_BOILER_TEMP": 25,
    "MIX_HEAT_CURVE_4": 0.1,
    "MIX_HEAT_CURVE_5": 0.1,
    "WEATHER_TEMP_FACTOR_4": 0,
    "WEATHER_TEMP_FACTOR_5": 0,
    "PARALLEL_OFFSET_HEAT_CURV_4": -20,
    "PARALLEL_OFFSET_HEAT_CURV_5": -20,
    "LOW_MIX_SET_TEMP_4": 0,
    "LOW_MIX_SET_TEMP_5": 0,
    "STER_TEMP_DAY_1": 10,
    "STER_TEMP_DAY_2": 10,
    "STER_TEMP_DAY_3": 10,
    "STER_TEMP_NIGHT_1": 10,
    "STER_TEMP_NIGHT_2": 10,
    "STER_TEMP_NIGHT_3": 10,
    "MIX_SET_TEMP_4": 20,
    "MIX_SET_TEMP_5": 20,
}

ENTITY_MAX_VALUE = {
    "CO_TEMP_SET": 85,
    "CALORIFIC_KWH_KG": 25,
    "CWU_SET_TEMP": 70,
    "FUEL_KG_H":25,
    "EXTERN_BOILER_TEMP": 60,
    "MIX_HEAT_CURVE_4": 4.0,
    "MIX_HEAT_CURVE_5": 4.0,
    "WEATHER_TEMP_FACTOR_4": 50,
    "WEATHER_TEMP_FACTOR_5": 50,
    "PARALLEL_OFFSET_HEAT_CURV_4": 20,
    "PARALLEL_OFFSET_HEAT_CURV_5": 20,
    "LOW_MIX_SET_TEMP_4": 30,
    "LOW_MIX_SET_TEMP_5": 30,
    "STER_TEMP_DAY_1": 35,
    "STER_TEMP_DAY_2": 35,
    "STER_TEMP_DAY_3": 35,
    "STER_TEMP_NIGHT_1": 35,
    "STER_TEMP_NIGHT_2": 35,
    "STER_TEMP_NIGHT_3": 35,
    "MIX_SET_TEMP_4": 50,
    "MIX_SET_TEMP_5": 70,

}

# Switch states

# STATE_ON: Final = "on"
# STATE_OFF: Final = "off"

## Boiler staus keys map
# boiler mode names from  endpoint http://LocalIP/econet/rmParamsEnums?
OPERATION_MODE_NAMES = {
    0: "TURNED OFF",
    1: "STOPPED",
    2: "FIRE UP",
    3: "WORK",
    4: "SUPERVISION",
    5: "Halted",
    6: "Cleaning",
    7: "BURNING OFF",
    8: "ALARM",
    9: "Manual",
    10: "UNSEALING",
    11: "Other",
    12: "STABILIZATION",
    13: "Purge",
    19: "Calibration",
    20: "Maintain",
    21: "Afterburning",
    22: "Chimney-sweep",
    23: "Kindling",
    24: "OpenDoor",
    25: "Cooling",
    26: "Safe",
}

ECOSTER_MODE_NAMES = {
    0: "Schedule",
    1: "Economy",
    2: "Comfort",
    3: "Outside",
    4: "Ventilation",
    133: "Party",
    6: "Holiday",
    7: "Frost protection",
    8: "Heat now mode",
    9: "HUW charging mode",
    10: "Off Mode",
    11: "Turn off heating",
}


# add constants to future
PRODUCT_TYPE = {
    0: "ECOMAX_850P_TYPE",  # regType 0
    1: "ECOMAX_850i_TYPE",  # regType 1
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
    "tempFeeder": 0,
    "tempCO": 0,
    "tempFlueGas": 0,
    "tempCWU": 1,
    "tempCWUSet": 0,
    "tempUpperBuffer": 0,
     "tempLowerBuffer": 0,
    "tempOpticalSensor": 0,
}

ALARMS_NAMES = {
    0: "No power",
    1: "Boiler sensor error",
    2: "Exceeding the maximum temperature of the boiler",
    3: "Sensor fault feeder",
    4: "Exceeding the maximum temperature of the tray",
    5: "Sensor fault system",
    6: "Exceeding the maximum flue gas temperature",
    7: "Firing up the boiler failed",
    8: "No fuel",
    9: "Loss of Containment",
    10: "Pressure sensor failed",
    11: "Faulty fan ",
    12: "ID Fan Pressure can not be reached ",
    13: "Burning off error ",
    14: "Photocell sensor failed",
    15: "Linear actuator blocked",
    16: "Incorrect work parameters",
    17: "Precaution of condensation ",
    18: "STB is disabled . Manual reset is needed when TB <65 °C Boiler STB ",
    19: "Opening the contact STB tray ",
    20: "Minimum water pressure exceeded",
    21: "Maximum water pressure exceeded",
    22: "Fuel feeder locked",
    23: "Extinguished flame ",
    24: "Faulty exhaust fan",
    25: "Error loading external feeder ",
    26: "Error Sensor solar collector SH ",
    27: "Error Sensor solar circuit SL ",
    28: "Sensor fault circuit H1- S",
    29: "Sensor fault circuit H2 - S",
    30: "Sensor fault circuit H3 - S",
    31: "Error weather sensor WS ",
    32: "HUW sensor error ",
    33: "Sensor error H0- S",
    34: "It takes frost protection - heat source are not included ",
    35: "It takes frost protection - the source of the attached ",
    36: "Exceeded max. Temperature solar collector ",
    37: "Exceeded max. Flow temperature of the floor ",
    38: "Cooling preventive solid fuel boiler ",
    39: "No communication with ecoLAMBDA ",
    40: "Lock the primary air damper ",
    41: "Lock the secondary air damper ",
    42: "Feeder full",
    43: "Furnace full",
    44: "No communication with B module",
    45: "Cleaning servomotor error",
    46: "Minimum pressure exceeded",
    47: "Maximum pressure exceeded",
    48: "Pressure sensor damage",
    49: "Maximum main heat source temperature exceeded",
    50: "Maximum additional heat source temperature exceeded",
    51: "Solar is OFF - temperature  is too high - wait for temperature drop",
    52: "Alarm for auger control system malfunction",
    53: "Clogged auger Alarm",
    54: "Temperature above maximum for the thermocouple.",
    55: "Thermocouple wired improperly.",
    255: "Alarm unknown"
}
