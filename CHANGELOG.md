## v0.1.0

### Added (6)
* [Entity/Sensor] Added `feeder temperature`
* [Entity/Sensor] Added `fan power`
* [Entity/Sensor] Added `exhaust emperature`
* [Entity/Sensor] Added `fireplace temperature`
* [Entity/Sensor] Added `water back temperature`
* [Entity/Sensor] Added `water temperature`
* [Entity/Sensor] Added `outside temperature`
* [Entity/Sensor] Added `boiler power output`
* [Entity/BinarySensor] Added `water pump works`
* [Entity/BinarySensor] Added `fireplace pump works`
* [Entity/BinarySensor] Added `solar pump works`
* [Entity/BinarySensor] Added `lighter works`
* [Config] Added config via GUI

## v0.1.1
Add new sensors and binary sensor
Add hardware version

## v0.1.5
[Entity/Sensor] Added `lambdaLevel`
[Entity/Sensor] Added `Wi-Fi signal strength`
[Entity/Sensor] Added `Wi-Fi signal quality`
[Entity/Sensor] Added `Module ecoNET software version`
[Entity/Sensor] Added `Module A version`
[Entity/Sensor] Added `Module B version`
[Entity/Sensor] Added `Module Panel version`
[Entity/Sensor] Added `Module Lambda version`

## v0.1.6
fix error in Entity sensor.wi_fi_signal_quality

## v0.1.7
Added `Thermostat sensor` ON or OFF
Added `lambdaStatus`
Added `mode` boiler operation names to status

## v0.1.7-3
Rename boiler mode names
Added `protocol_Type` to DIAGNOSTIC sensor
Added `controllerID` to DIAGNOSTIC sensor   

## v0.1.8
Added REG_PARAM_PRECICION parameters from econet dev file
Added translations for the sensors
Added translations dictonary
By default sensors off: Fan2, Solar pump, Fireplace pump
Changed depricated unit TEMP_CELSIUS to UnitOfTemperature.CELSIUS

## [v0.3.0] 2023-11-30
Thank for @pblxptr add new code line from him
- Added: [New features boiler set temperature]
- Added: [Mixer sensor new device]
- Added: [Comments in code]
- Added: [Configuration in project code style by HA rules]

## [v0.3.1] 2023-12-04
- Rename: `tempCWU` sensor name from `water temperature` to `HUW temperature`
- Rename:  `pumpCO` binary_sensor name from `Pump` to `Boiler pump`
- Added: `HUW temperature` sensor key `tempCWUSet`
- Added: `Upper buffer temperature` sensor (by defoult off)

## [v0.3.3] 2023-12-14
- Change readme pictures links
- cleaned translation files and rename keys by requrements
- Added: alarm constants for future

## [v1.0.0-beta-11] 2024-10-03
- Added: `boiler_status` sensor
- Added: `boiler_status` binary_sensor
- Added: `boiler_status` sensor key `boiler_status`
- Added: `boiler_status` binary_sensor key `boiler_status`
- Added: `boiler_status` sensor key `boiler_status_text`
- Added: `boiler_status` binary_sensor key `boiler_status_text`

## [v1.0.1-beta] 2024-10-03
- Small code changes update repo

## [v1.0.2-beta] 2024-10-15
- Tests file structure according to documentation
- Code style chcnges by ruff recomendation
- Separated entity by types for better management
- Moved Mixer sensors to the Mixer sensor group and added icons

## [v1.0.3-beta] 2024-10-15
### Added
- Introduced new `ServoMixer1` state handling with predefined Home Assistant states (`STATE_OFF`, `STATE_CLOSING`, `STATE_OPENING`).
- Added logging for non-numeric values in sensor processing to improve debugging.

### Changed
- Updated `ENTITY_VALUE_PROCESSOR` to use predefined Home Assistant states for `ServoMixer1`.
- Improved error handling in `create_controller_sensors` to skip non-numeric values and log warnings.

### Fixed
- Fixed `ValueError` caused by non-numeric values in sensor state processing.
- Resolved Mypy type incompatibility issue in `STATE_CLASS_MAP` by removing the `servoMixer1` entry with `None` value.

## [v1.0.4-beta] 2024-11-04
#### New Features
- **New Sensors Added**: Introduced new sensors for enhanced monitoring.
  - Added sensors: workAt100, workAt50, workAt30, FeederWork, FiringUpCount. (Commit: e41f882)

#### Improvements
- **Valve State Constant**: Changed the valve STATE constant for better consistency. (Commit: 3835797)
- **Entity Value Processor**: Updated ENTITY_VALUE_PROCESSOR to use STATE_ON and STATE_OFF constants for improved state handling. (Commit: 17959c6)
- **Controller Name**: Added 'Controller name' to 'model_id' device info for better support and identification. (Commit: b5cf889)

#### Bug Fixes
- **Boiler Status Keys**: Fixed the mapping of boiler status keys to include operation status. (Commit: a486402)

