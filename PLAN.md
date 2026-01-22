# NetBox Cisco ISE Plugin Plan

## Overview
Create a new NetBox plugin `netbox-cisco-ise` that displays Cisco Identity Services Engine (ISE) endpoint and session information for devices in NetBox. The plugin will show real-time endpoint status, authentication details, profiling data, and network access device (NAD) information.

## NetBox Plugin Certification Program

This plugin targets the [NetBox Plugin Certification Program](https://github.com/netbox-community/netbox/wiki/Plugin-Certification-Program). All development must adhere to these requirements:

### Certification Checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| **License** | | |
| Apache 2.0 license file at root | [ ] | `LICENSE` |
| License matches PyPI designation | [ ] | In `pyproject.toml` |
| **Documentation** | | |
| README headline + introduction | [ ] | Plugin value proposition |
| Version compatibility matrix | [ ] | NetBox 4.0+ / Python 3.10+ |
| Dependency list with versions | [ ] | `requests>=2.28.0` |
| Screenshots demonstrating value | [ ] | Endpoint tab, NAD tab |
| Installation instructions | [ ] | pip install + config |
| Support/engagement info | [ ] | GitHub issues |
| Square icon (48-500px, CC license) | [ ] | `docs/icon.png` |
| CHANGELOG.md (Keep a Changelog) | [ ] | Breaking changes in **bold** |
| GitHub Wiki documentation | [ ] | Expanded docs |
| **Code Quality** | | |
| GitHub Actions CI workflow | [ ] | `.github/workflows/ci.yml` |
| Tests for Python 3.10, 3.11, 3.12 | [ ] | pytest + responses |
| Code formatted with black | [ ] | `black netbox_cisco_ise/` |
| Imports sorted with isort | [ ] | `isort netbox_cisco_ise/` |
| Linted with flake8 | [ ] | max-line-length=120 |
| **Packaging** | | |
| pyproject.toml with metadata | [ ] | Build configuration |
| PyPI package published | [ ] | netbox-cisco-ise |
| Version compatibility metadata | [ ] | min_version/max_version |

### Contact for Certification
- Email: plugincertification@netboxlabs.com
- Include: GitHub repo, PyPI link, GitHub ID, PyPI ID

## Key Requirements
1. **Dual purpose** - Show endpoint data (by MAC) for wireless clients AND NAD data for network devices
2. **MAC-based lookup for endpoints** - Uses device interface MAC addresses
3. **IP/Hostname lookup for NADs** - Uses device management IP or hostname
4. **Configurable manufacturer pattern** - Default: show tab for all devices with MAC or for Cisco NADs
5. **ERS API** - Primary API for configuration data (port 9060 or 443 via API Gateway)
6. **Monitoring API** - For real-time session data

## Data Flow

```
NetBox Device
    │
    ├── Has MAC address on interface?
    │       │
    │       ▼
    │   Endpoint API (by MAC)
    │       ├── Endpoint profile/group
    │       ├── Identity group membership
    │       └── Custom attributes
    │               │
    │               ▼
    │       Session API (if connected)
    │           ├── Authentication status
    │           ├── Authorization policy
    │           ├── Connected switch/port
    │           └── Session duration
    │
    └── Is Cisco network device?
            │
            ▼
        NAD API (by IP/hostname)
            ├── Device name & description
            ├── Network device groups
            ├── Authentication settings
            └── RADIUS/TACACS config
```

## Plugin Configuration

```python
PLUGINS_CONFIG = {
    'netbox_cisco_ise': {
        # ISE Connection
        'ise_url': 'https://ise.example.com',
        'ise_username': 'ersadmin',
        'ise_password': 'your-password',

        # API Settings
        'verify_ssl': False,  # For self-signed certs
        'timeout': 30,
        'cache_timeout': 60,  # Cache results for 60 seconds

        # Device mappings - which devices show the ISE tab
        # endpoint: Lookup by MAC (for wireless clients, badges, phones)
        # nad: Lookup as network access device (for Cisco switches, routers)
        'device_mappings': [
            {'manufacturer': 'vocera', 'lookup': 'endpoint'},
            {'manufacturer': 'cisco', 'device_type': '.*phone.*', 'lookup': 'endpoint'},
            {'manufacturer': 'cisco', 'lookup': 'nad'},
        ],
    }
}
```

## Tab Visibility Logic

```python
def should_show_ise_tab(device):
    """
    Show ISE tab if device matches a mapping AND has required data:
    - endpoint lookup: requires MAC address on interface
    - nad lookup: requires management IP or hostname
    """
    config = settings.PLUGINS_CONFIG.get('netbox_cisco_ise', {})
    mappings = config.get('device_mappings', [])

    for mapping in mappings:
        if device_matches_mapping(device, mapping):
            lookup = mapping.get('lookup', 'endpoint')
            if lookup == 'endpoint':
                return device_has_mac(device)
            elif lookup == 'nad':
                return device.primary_ip4 or device.name
    return False
```

## Plugin Structure

```
/home/netcomm/development/netbox-cisco-ise/
├── netbox_cisco_ise/
│   ├── __init__.py              # PluginConfig
│   ├── views.py                 # DeviceISEView with ViewTab
│   ├── ise_client.py            # ISE ERS/Monitoring API client
│   ├── forms.py                 # Settings form
│   ├── navigation.py            # Plugin menu
│   ├── urls.py                  # URL routes
│   └── templates/
│       └── netbox_cisco_ise/
│           ├── endpoint_tab.html    # Endpoint/session view
│           ├── nad_tab.html         # Network device view
│           └── settings.html        # Settings page
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
└── docs/
    └── icon.png
```

## ISE API Client

```python
class ISEClient:
    """Client for Cisco ISE ERS and Monitoring APIs"""

    def __init__(self, base_url, username, password, verify_ssl=False, timeout=30):
        self.base_url = base_url.rstrip('/')
        self.auth = (username, password)
        self.verify_ssl = verify_ssl
        self.timeout = timeout

    # === Endpoint APIs (ERS) ===

    def get_endpoint_by_mac(self, mac_address):
        """
        GET /ers/config/endpoint?filter=mac.EQ.{mac}
        Returns: Endpoint details with profile, group, custom attributes
        """

    def get_endpoint_groups(self):
        """
        GET /ers/config/endpointgroup
        Returns: All endpoint identity groups
        """

    def get_endpoint_profile(self, profile_id):
        """
        GET /ers/config/profilerprofile/{id}
        Returns: Profiler profile details
        """

    # === Session APIs (Monitoring) ===

    def get_active_session_by_mac(self, mac_address):
        """
        GET /admin/API/mnt/Session/MACAddress/{mac}
        Returns: Active session details if connected
        """

    def get_session_details(self, session_id):
        """
        GET /admin/API/mnt/Session/Active/SessionID/{id}
        Returns: Full session attributes
        """

    # === Network Device APIs (ERS) ===

    def get_network_device_by_ip(self, ip_address):
        """
        GET /ers/config/networkdevice?filter=ipaddress.EQ.{ip}
        Returns: NAD configuration in ISE
        """

    def get_network_device_by_name(self, name):
        """
        GET /ers/config/networkdevice?filter=name.CONTAINS.{name}
        Returns: NAD configuration in ISE
        """

    def get_network_device_groups(self):
        """
        GET /ers/config/networkdevicegroup
        Returns: All network device groups
        """

    # === Utility ===

    def test_connection(self):
        """Test ISE connectivity by fetching version info"""
```

## Template Sections

### Endpoint Tab (endpoint_tab.html)

#### Section 1: Endpoint Identity
| Field | Source |
|-------|--------|
| MAC Address | `endpoint.mac` |
| Endpoint Profile | `endpoint.profileName` |
| Identity Group | `endpoint.groupName` |
| Static Group | Yes/No badge |
| Portal User | `endpoint.portalUser` (if set) |

#### Section 2: Profiling Data
| Field | Source |
|-------|--------|
| Profile Match | `endpoint.profileName` |
| Static Assignment | Yes/No |
| Custom Attributes | Key-value table |

#### Section 3: Active Session (if connected)
| Field | Source | Color Coding |
|-------|--------|--------------|
| Status | Connected/Disconnected | Green/Gray badge |
| Authentication | `session.authMethod` | |
| Authorization | `session.authorizationPolicy` | |
| Connected To | `session.nasIpAddress` + port | |
| Session Start | `session.startTimestamp` | |
| Session Duration | Calculated | |
| IP Address | `session.ipAddress` | |
| VLAN | `session.vlan` | |

#### Section 4: Authentication History (last 5)
| Column | Data |
|--------|------|
| Timestamp | Time of auth attempt |
| Result | Pass/Fail badge |
| Policy | Applied policy |
| Source | Switch/port |

### NAD Tab (nad_tab.html)

#### Section 1: Device Registration
| Field | Source |
|-------|--------|
| NAD Name | `device.name` |
| Description | `device.description` |
| IP Address | `device.networkDeviceIpList` |
| Profile | `device.profileName` |
| Status | Active in ISE badge |

#### Section 2: Network Device Groups
| Group Type | Value |
|------------|-------|
| Location | `networkDeviceGroupList[location]` |
| Device Type | `networkDeviceGroupList[type]` |
| IPSEC | `networkDeviceGroupList[ipsec]` |

#### Section 3: Authentication Settings
| Protocol | Status |
|----------|--------|
| RADIUS | Enabled/Disabled + shared secret status |
| TACACS | Enabled/Disabled + shared secret status |
| SNMP | Settings summary |
| TrustSec | Enabled/Disabled |

## API Response Examples

### Endpoint Response
```json
{
    "ERSEndPoint": {
        "id": "abc123",
        "name": "00:11:22:33:44:55",
        "mac": "00:11:22:33:44:55",
        "profileId": "profile-id-123",
        "profileName": "Vocera-Badge",
        "staticGroupAssignment": true,
        "groupId": "group-id-456",
        "groupName": "Vocera-Badges",
        "portalUser": "",
        "customAttributes": {
            "customAttribute1": "value1"
        }
    }
}
```

### Active Session Response
```json
{
    "activeSession": {
        "session_id": "session123",
        "user_name": "00:11:22:33:44:55",
        "nas_ip_address": "10.1.1.1",
        "nas_port": "GigabitEthernet1/0/1",
        "framed_ip_address": "10.10.10.50",
        "audit_session_id": "audit123",
        "acct_session_id": "acct123",
        "acct_session_time": 3600,
        "calling_station_id": "00:11:22:33:44:55",
        "selected_authorization_profile": "PermitAccess"
    }
}
```

### Network Device Response
```json
{
    "NetworkDevice": {
        "id": "nad-id-123",
        "name": "switch01",
        "description": "Access switch - Building A",
        "authenticationSettings": {
            "radiusSharedSecret": "********",
            "enableKeyWrap": false
        },
        "networkDeviceIPList": [
            {"ipaddress": "10.1.1.1", "mask": 32}
        ],
        "networkDeviceGroupList": [
            "Location#All Locations#Building-A",
            "Device Type#All Device Types#Switch"
        ],
        "profileName": "Cisco"
    }
}
```

## What Can We Learn from ISE?

### Endpoint Data (Wireless Clients, Phones, Badges)
| Data Point | API Source | Value for NetBox |
|------------|------------|------------------|
| MAC Address | ERS Endpoint | Device identifier |
| Endpoint Profile | ERS Endpoint | Device type classification (Vocera, Phone, etc.) |
| Identity Group | ERS Endpoint | Organizational grouping |
| Custom Attributes | ERS Endpoint | Asset tag, department, owner, etc. |
| Current IP Address | Session/Monitoring | Real-time IP assignment |
| Connected Switch/Port | Session/Monitoring | Physical location tracking |
| Authentication Status | Session/Monitoring | Network access status |
| VLAN Assignment | Session/Monitoring | Network segment |
| First Seen Date | ERS Endpoint | Device discovery date |
| Last Seen Date | Session/Monitoring | Activity tracking |
| Profiler Classification | ERS Profiler | Hardware/OS detection |

### Network Device Data (Switches, Routers, WLCs)
| Data Point | API Source | Value for NetBox |
|------------|------------|------------------|
| Device Name | ERS NAD | Device identity |
| IP Addresses | ERS NAD | Management IPs |
| Description | ERS NAD | Location/purpose |
| Device Groups | ERS NAD | Location, Type, IPSEC groups |
| RADIUS Settings | ERS NAD | Authentication config |
| TACACS Settings | ERS NAD | Command authorization |
| SNMP Settings | ERS NAD | Monitoring config |
| TrustSec Status | ERS NAD | SGT/SXP capability |

## Sync Capabilities (ISE → NetBox)

### Endpoint Sync (Read-only from ISE)
```python
# Sync from ISE endpoint to NetBox device
sync_fields = {
    'ip_address': session.framed_ip_address,    # Update primary IP
    'custom_fields.ise_profile': endpoint.profileName,
    'custom_fields.ise_group': endpoint.groupName,
    'custom_fields.last_seen': session.timestamp,
    'comments': f"Connected to {session.nas_ip}:{session.nas_port}",
}
```

### NAD Sync (Read-only from ISE)
```python
# Sync from ISE NAD to NetBox device
sync_fields = {
    'comments': nad.description,  # ISE NAD description
    'custom_fields.ise_registered': True,
    'custom_fields.ise_location_group': nad.location_group,
    'custom_fields.ise_device_type': nad.device_type_group,
}
```

## Import Capabilities (ISE → NetBox)

### Import Endpoints from ISE
Could search ISE for all endpoints matching criteria and import to NetBox:

```python
# Search ISE for endpoints by profile
endpoints = ise_client.search_endpoints(profile='Vocera-Badge')

# For each endpoint, create NetBox device if not exists
for ep in endpoints:
    if not Device.objects.filter(interfaces__mac_address=ep.mac).exists():
        device = Device(
            name=ep.mac,  # or custom attribute for name
            device_type=get_device_type_for_profile(ep.profileName),
            role=get_role_for_profile(ep.profileName),
            site=get_site_from_ise_location(ep),
        )
        # Create interface with MAC
        Interface(device=device, mac_address=ep.mac, name='wlan0')
```

### Import NADs from ISE
Could import ISE NADs (network devices) to NetBox:

```python
# Get all NADs from ISE
nads = ise_client.get_all_network_devices()

# For each NAD, create NetBox device if not exists
for nad in nads:
    if not Device.objects.filter(primary_ip4__address__net_host=nad.ip).exists():
        device = Device(
            name=nad.name,
            device_type=guess_device_type(nad.profileName),
            role=get_role_from_device_group(nad.device_type_group),
            site=get_site_from_location_group(nad.location_group),
            comments=nad.description,
        )
```

### Import Page Features (Similar to Catalyst Center)
- **Search by**: MAC address pattern, Profile name, Identity group, Location group
- **Bulk import**: Select multiple endpoints/NADs to import
- **Duplicate detection**: Show devices already in NetBox
- **Auto-mapping**: Map ISE profiles to NetBox device types/roles
- **Site mapping**: Map ISE location groups to NetBox sites

## Implementation Phases

### Phase 1: Repository Setup
1. Create `/home/netcomm/development/netbox-cisco-ise/` directory structure
2. Copy base structure from netbox-catalyst-center
3. Update pyproject.toml, README.md, LICENSE
4. Create basic `__init__.py` with PluginConfig

### Phase 2: ISE API Client
1. Create `ise_client.py` with Basic Auth
2. Implement `get_endpoint_by_mac()` first
3. Add `get_active_session_by_mac()` for session data
4. Implement `test_connection()` for settings page
5. Add caching using Django cache framework

### Phase 3: Endpoint View + Tab
1. Create `views.py` with ViewTab registration for endpoints
2. Implement `should_show_ise_tab()` with device_mappings
3. Create `endpoint_tab.html` template
4. Test with Vocera device MAC lookup

### Phase 4: NAD View
1. Add NAD lookup methods to ise_client.py
2. Create `nad_tab.html` template
3. Update views.py to select correct template
4. Test with Cisco switch lookup

### Phase 5: Settings & Navigation
1. Create settings page with connection test
2. Add navigation menu (Settings link)
3. Create forms.py for settings form

### Phase 6: Polish & Publish
1. Add comprehensive README documentation
2. Create icon for plugin
3. Set up CI/CD workflows (black, flake8, isort)
4. Tag version 1.0.0 and publish

## Files to Create

| File | Based On | Key Changes |
|------|----------|-------------|
| `__init__.py` | netbox-catalyst-center | ISE-specific settings |
| `ise_client.py` | catalyst_client.py | ISE ERS + Monitoring APIs, Basic Auth |
| `views.py` | netbox-catalyst-center | Endpoint + NAD lookup, template selection |
| `forms.py` | netbox-catalyst-center | ISE fields |
| `navigation.py` | netbox-catalyst-center | New name |
| `urls.py` | netbox-catalyst-center | New name |
| `endpoint_tab.html` | client_tab.html | ISE endpoint/session data |
| `nad_tab.html` | network_device_tab.html | ISE NAD data |
| `settings.html` | netbox-catalyst-center | ISE config display |

## Key Differences from Catalyst Center Plugin

| Aspect | Catalyst Center | Cisco ISE |
|--------|-----------------|-----------|
| Auth Method | Token-based (POST /auth/token) | Basic Auth (username:password) |
| API Ports | 443 only | 9060 (ERS) + 443 (Gateway) |
| Endpoint Lookup | Client API by MAC | ERS Endpoint by MAC |
| Session Data | Client health/connection | Session attributes, auth policy |
| Network Device | Inventory lookup | NAD registration status |
| Groups | N/A | Identity Groups, Device Groups |

## Feature Priority for v1.0

### Must Have (v1.0)
1. Endpoint tab showing profile, group, and active session data
2. NAD tab showing ISE registration and group membership
3. Settings page with connection test
4. Basic sync: Update device comments with ISE session info

### Nice to Have (v1.1)
1. Import endpoints from ISE to NetBox
2. Import NADs from ISE to NetBox
3. Custom field sync for ISE-specific attributes
4. Search/filter by ISE profile in NetBox

### Future (v2.0)
1. pxGrid real-time session updates
2. Posture compliance status
3. ANC quarantine actions from NetBox
4. Bidirectional NAD sync (NetBox → ISE)

## Notes
- ISE ERS API requires ERS Admin or ERS Operator role
- Monitoring API uses same credentials but different endpoint base
- Some ISE deployments may have API Gateway enabled (port 443 for all APIs)
- Session data only available for actively connected endpoints
- Import feature would be one-way (ISE → NetBox) similar to Catalyst Center plugin
