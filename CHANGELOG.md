# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2025-01-23

### Changed

- Optimized database queries with `select_related()` and `prefetch_related()` for better performance

## [0.1.1] - 2025-01-22

### Fixed

- Fixed template packaging for PyPI distribution

## [0.1.0] - 2026-01-22

### Added
- Initial release
- Endpoint lookup by MAC address via ERS API
- Network Access Device (NAD) lookup by IP/hostname
- Active session data from Monitoring API
- Configurable device_mappings for tab visibility
- Settings page with connection test
- API response caching
- Support for NetBox 4.0+
