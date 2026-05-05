# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.11] - 2026-05-05

### Fixed

- Fix `ProgrammingError: relation "netbox_cisco_ise_ciscoise" does not exist` on NetBox 4.5+ when navigating to `/core/system/`. The unmanaged permission-anchor model is now flagged with `_netbox_private = True`, and a data migration sets `ObjectType.public = False` so NetBox's object-count loop excludes it.

## [0.1.4] - 2026-01-26

### Added

- **Virtual Chassis Support**
  - For Virtual Chassis members, NAD lookups now use the chassis name (original hostname) instead of member-specific name
  - Example: Member "switch.2" queries ISE using "switch" to find the NAD

## [0.1.3] - 2025-01-23

### Fixed

- Code formatting fixes for CI compliance

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
