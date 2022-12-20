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

* Small race condition in scheduling for the `is_running()`, now supports the `pedantic` flag

## [1.4.0] - 2022-12-20

### Added

* Support for the `verify()` family of methods for assertions

### Changed

* Improved stability of the scheduling infrastructure, should prevent dead pools - [#4](https://github.com/hivesolutions/colony/issues/4)
