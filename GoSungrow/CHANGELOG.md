## [3.0.7] - 2023-09-04
### Features

- Alpha support for Modbus, (direct connect to your Sungrow inverter).


### Fixes

- Fixup ResultData.result_data.org_id error.


## [3.0.6] - 2023-05-10
### Features

- Added extra sub-commands:
```
show ps save
show device save
show template save
show point save
show point ps-save
show point device-save
show point template-save
```

### Fixes

- HA binary_sensor not being set correctly.


## [3.0.5] - Not released


## [3.0.4] - 2023-01-05
### Features

### Fixes

- Fixes to the Energy Dashboard of HA.


## [3.0.3] - 2022-12-23
### Features

- Merry Christmas!
- Now supports the Energy Dashboard of HA!

### Fixes

- Fix double virtual.virtual entries.
- Fixup float value determination logic.
- CacheTimeout matches fetch schedule.
- Fixed unit type guessing - "Template error: float got invalid input"
- Fix battery class - correct point used for HA.
- Added more DeviceClass types for HA - will affect long term stats as units will change on some points.


## [3.0.2] - 2022-12-21
### Features

- Control of GoSungrow via MQTT; gosungrow_option_fetchschedule, gosungrow_option_loglevel, gosungrow_option_sleepdelay & gosungrow_option_servicestate
- Updated MQTT message types.

### Fixes

- Incorrect units on points p13119 & p13149.


## [3.0.1] - 2022-12-15
### Changed

- HA install fixups.


## [3.0.0] - 2022-12-14
### Changed

- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/10))
- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/9))
- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/8))
- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/7))
- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/6))
- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/5))
- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/4))
- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/3))


## [2.2.0] - 2022-03-21
### Changed

- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/2))


## [2.1.3] - 2022-03-14
### Changed

- GoSunGrow for HA ([fixes #1](https://github.com/MickMake/GoSunGrow/issues/1))

