# Claude Code Instructions for netbox-cisco-ise

## Project Overview

This is a NetBox plugin that integrates Cisco Identity Services Engine (ISE) with NetBox. It displays endpoint identity information, Network Access Device (NAD) details, and active session status on Device detail pages.

## NetBox Plugin Certification Requirements

This plugin is targeting the [NetBox Plugin Certification Program](https://github.com/netbox-community/netbox/wiki/Plugin-Certification-Program). All development must adhere to these standards:

### License Requirements
- **License**: Apache 2.0 (OSI-approved, compatible with NetBox)
- **License File**: Must exist at repository root as `LICENSE`, `LICENSE.md`, or `LICENSE.txt`
- **PyPI Designation**: License must be specified in `pyproject.toml`

### Documentation Requirements

#### README Must Include:
- [ ] Headline summarizing the plugin's value
- [ ] Concise introduction explaining functionality
- [ ] Version compatibility matrix (NetBox 4.0+ only)
- [ ] Dependency list with compatible version ranges
- [ ] Screenshots or demonstrations
- [ ] Installation instructions
- [ ] Support and engagement information
- [ ] Square icon (48x48px-500x500px) in SVG or PNG with CC license

#### Additional Documentation:
- [ ] GitHub Wiki with expanded documentation
- [ ] CHANGELOG.md with release notes following Keep a Changelog format
- [ ] Release notes must highlight breaking changes with bold headers

### Code Quality Requirements

#### Testing:
- [ ] Comprehensive test suite via GitHub Actions CI
- [ ] Tests must pass on Python 3.10, 3.11, 3.12
- [ ] Import verification at minimum
- [ ] Use `responses` library for mocking HTTP requests

#### Linting:
- [ ] Code formatted with `black`
- [ ] Imports sorted with `isort`
- [ ] Linted with `flake8` (max-line-length=120)

### Version Compatibility
- **NetBox**: 4.0+ only (not compatible with 3.x)
- **Python**: 3.10+
- **Cisco ISE**: 2.x and 3.x

## Development Commands

```bash
# Install for development
pip install -e ".[dev]"

# Format code
black netbox_cisco_ise/

# Sort imports
isort netbox_cisco_ise/

# Lint
flake8 netbox_cisco_ise/ --max-line-length=120 --ignore=E501,W503,E203

# Run tests
pytest tests/ -v

# Verify import
python -c "import netbox_cisco_ise; print(f'Plugin version: {netbox_cisco_ise.__version__}')"
```

## File Structure

```
netbox-cisco-ise/
├── .claude/                    # Claude Code instructions
│   └── settings.md
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI workflow (lint + test)
│       └── release.yml         # PyPI publish on release
├── docs/
│   └── icon.png                # Plugin icon (required for certification)
├── netbox_cisco_ise/           # Plugin source code
│   ├── __init__.py             # Plugin config and version
│   ├── ise_client.py           # ISE ERS/Monitoring API client
│   ├── views.py                # Django views with ViewTab registration
│   ├── forms.py                # Settings and configuration forms
│   ├── navigation.py           # Plugin menu items
│   ├── urls.py                 # URL routing
│   └── templates/              # HTML templates
│       └── netbox_cisco_ise/
│           ├── endpoint_tab.html
│           ├── nad_tab.html
│           └── settings.html
├── tests/
│   ├── conftest.py             # Pytest fixtures
│   ├── test_ise_client.py      # API client tests
│   └── test_views.py           # View tests
├── screenshots/                # Screenshots for README
├── CHANGELOG.md                # Release history
├── LICENSE                     # Apache 2.0 license
├── PLAN.md                     # Implementation plan
├── pyproject.toml              # Package configuration
└── README.md                   # Project documentation
```

## Key Files

- **`__init__.py`**: Contains `PluginConfig` class with version, author, device_mappings
- **`ise_client.py`**: API client for ISE ERS and Monitoring APIs with caching
- **`views.py`**: ViewTab classes for Device detail pages (endpoint and NAD views)

## ISE API Endpoints Used

### ERS API (port 9060 or 443)
- `/ers/config/endpoint` - Endpoint search and details
- `/ers/config/networkdevice` - NAD search and details
- `/ers/config/endpointgroup` - Endpoint identity groups
- `/ers/config/authorizationprofile` - Authorization profiles

### Monitoring API (port 443)
- `/admin/API/mnt/Session/MACAddress/{mac}` - Active session by MAC
- `/admin/API/mnt/Session/IPAddress/{ip}` - Active session by IP

## Device Mappings Configuration

The plugin uses `device_mappings` in settings to determine which devices get ISE tabs and what lookup method to use:

```python
PLUGINS_CONFIG = {
    "netbox_cisco_ise": {
        "ise_url": "https://ise.example.com",
        "ise_username": "admin",
        "ise_password": "password",
        "device_mappings": [
            # NAD lookup for Cisco network devices
            {"manufacturer": r"cisco", "lookup": "nad"},
            # Endpoint lookup for Vocera badges
            {"manufacturer": r"vocera", "lookup": "endpoint"},
            # Endpoint lookup for specific device types
            {"manufacturer": r"cisco", "device_type": r"phone", "lookup": "endpoint"},
        ],
    }
}
```

### Lookup Types:
- **`nad`**: Network Access Device lookup - uses device hostname or management IP
- **`endpoint`**: Endpoint lookup - uses MAC address from device interfaces

## Certification Checklist

Before requesting certification:

- [ ] License file present (Apache 2.0)
- [ ] README complete with all required sections
- [ ] Screenshots included
- [ ] Plugin icon created (48-500px square, CC license)
- [ ] GitHub Wiki documentation created
- [ ] CHANGELOG.md with Keep a Changelog format
- [ ] CI workflow passing (black, isort, flake8, tests)
- [ ] PyPI package published
- [ ] Version compatibility documented

## Contact for Certification

Email: plugincertification@netboxlabs.com

Include:
- Plugin description and certification rationale
- GitHub repository link
- PyPI package entry link
- GitHub and PyPI user IDs

## Reference Implementation

This plugin follows patterns established in `netbox-catalyst-center`:
- `/home/netcomm/development/netbox-catalyst-center/netbox_catalyst_center/catalyst_client.py` - API client pattern
- `/home/netcomm/development/netbox-catalyst-center/netbox_catalyst_center/views.py` - ViewTab registration pattern
