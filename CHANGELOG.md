# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Support for optional `name` parameter in `Scheduler.add_callable()` to provide human-readable names for scheduled callables

### Changed

*

### Fixed

*

## [1.4.35] - 2025-01-07

### Fixed

* Extended local path detection in `convert_reference_path_list()` to support parent directory patterns (`../`, `.../`) and Windows-style paths (`.\`, `..\`, `...\`)

## [1.4.34] - 2025-01-06

### Added

* Export of `conf_override` in `colony.base` module `__init__.py`

## [1.4.33] - 2025-01-06

### Added

* Comprehensive module documentation for `colony_wsgi.py` explaining purpose, use cases, configuration options, and examples
* New `conf_override()` context manager for temporarily overriding configuration values

## [1.4.32] - 2025-12-11

### Added

* Support for `BASE_PORT` and `NUMBER_THREADS` configuration options in WSGI
* Automatic port calculation based on base port and thread count
* Automatic host duplication for multi-port server configurations
* New `base_port`, `end_port`, and `number_threads` execution parameters

## [1.4.31] - 2025-12-11

### Added

* New `get_container()` method to the `PluginManager` class
* Added `container` field to the system information map
* New `get_exec_params()` method to retrieve execution parameters
* New `set_exec_param()` method to set execution parameters
* Added `exec_params` field to the system information map

### Changed

* Removed unused import from `colony_wsgi.py`

## [1.4.30] - 2025-12-03

### Fixed

* Directory creation fix, for Python 2

## [1.4.29] - 2025-12-03

### Fixed

* Removed Python 2 issue with the new code

## [1.4.28] - 2025-12-03

### Added

* New loading strategy for the manager `PluginManager.build()`

## [1.4.27] - 2025-04-06

### Changed

* New reconnect backoff times for kafka

## [1.4.26] - 2025-02-17

### Fixed

* Issue with Logstash logging strategy

## [1.4.25] - 2025-01-26

### Added

* Support for datetime and timestamp function in legacy
* Support for the Logstash notification system

### Changed

* Added more logging information to the logstash handler

## [1.4.24] - 2024-01-08

### Changed

* Added support for optional `kill_timer` avoiding `@atexit` issues

## [1.4.23] - 2024-01-04

### Added

* Add globals' vars managing utility to base

## [1.4.22] - 2024-01-03

### Changed

* Code format according to Black

### Fixed

* Issue with invalid Kafka configuration

## [1.4.21] - 2024-01-02

### Fixed

* Issue with the LogStashHandler

## [1.4.20] - 2023-12-28

### Changed

* Add `.pyi` and `.typed` to `package_data` in `setup.py`

## [1.4.19] - 2023-12-28

### Added

* Add new `LogstashHandler` to the logging system
* Initial support for types

## [1.4.18] - 2023-12-11

### Added

* Support for new `config/python/singleton.py` python configuration mode
* New `getLevelInt()` method to the `logging` module

### Fixed

* Multiple signals at exit, which could cause duplicate unloads

## [1.4.17] - 2023-11-28

### Added

* Made some alias to the more general `colony` config variables (`COLONY_PREFIX`, `COLONY_RUN_MODE`, and `COLONY_LAYOUT_MODE`)

## [1.4.16] - 2023-11-14

### Fixed

* Early return in Kafka method

## [1.4.15] - 2023-11-13

### Added

* Default topic support in Kafka config

## [1.4.14] - 2023-11-13

### Added

* Support for the `kafka_config()` method

## [1.4.13] - 2023-11-13

### Added

* Support for SASL in Kaka client

## [1.4.12] - 2023-10-28

### Added

* Support for broadcast notification using `notify_b()`

## [1.4.11] - 2023-10-15

### Fixed

* More legacy support

## [1.4.10] - 2023-10-15

### Fixed

* Python 3.12 compatibility

## [1.4.9] - 2023-10-13

### Fixed

* Unloading of plugins for run modes using `auto_unload`

## [1.4.8] - 2023-10-06

### Fixed

* Dry run execution issue

## [1.4.7] - 2023-10-05

### Added

* Dry run mode

## [1.4.6] - 2023-02-01

### Fixed

* Unit tests

## [1.4.5] - 2023-02-01

### Fixed

* Issue with the `object_attribute_names()` method that prevented proper serialization

## [1.4.4] - 2022-12-31

### Changed

* Behaviour of the `is_production()` method to be aligned with developers' expectations

## [1.4.3] - 2022-12-30

### Added

* Conversion of XML to Dictionary using `xml_to_dict()`
* Conversion of Dictionary to XML using `dict_to_xml()`

## [1.4.2] - 2022-12-21

### Changed

* Greatly improved scheduling solution - [#6](https://github.com/hivesolutions/colony/issues/6)
* Improved timeout overflow checking in scheduling

## [1.4.1] - 2022-12-20

### Fixed

* Small race condition in scheduling for the `is_running()`, now supports the `pedantic` flag

## [1.4.0] - 2022-12-20

### Added

* Support for the `verify()` family of methods for assertions

### Changed

* Improved stability of the scheduling infrastructure, should prevent dead pools - [#4](https://github.com/hivesolutions/colony/issues/4)
