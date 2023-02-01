# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

*

### Changed

*

### Fixed

*

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
