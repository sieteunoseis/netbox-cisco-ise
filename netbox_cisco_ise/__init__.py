"""
NetBox Cisco ISE Plugin

Display Cisco Identity Services Engine (ISE) endpoint and NAD information in Device detail pages.
Shows endpoint identity, profiling data, active session status, and network access device details.
"""

import logging

from netbox.plugins import PluginConfig

__version__ = "0.1.8"

logger = logging.getLogger(__name__)


class CiscoISEConfig(PluginConfig):
    """Plugin configuration for NetBox Cisco ISE integration."""

    name = "netbox_cisco_ise"
    verbose_name = "Cisco ISE"
    description = "Display Cisco ISE endpoint and NAD information in device pages"
    version = __version__
    author = "sieteunoseis"
    author_email = "jeremy.worden@gmail.com"
    base_url = "cisco-ise"
    min_version = "4.0.0"
    max_version = "4.99"

    # Required settings - plugin won't load without these
    required_settings = []

    # Default configuration values
    default_settings = {
        # ISE Connection Settings
        "ise_url": "",  # e.g., "https://ise.example.com"
        "ise_username": "",  # ERS Admin username
        "ise_password": "",  # ERS Admin password
        "timeout": 30,  # API timeout in seconds
        "cache_timeout": 60,  # Cache results for 60 seconds
        "verify_ssl": False,  # Skip SSL verification for self-signed certs
        # Device mappings - determines which devices show ISE tab and lookup method
        # Format: list of dicts with manufacturer (regex), device_type (regex, optional), lookup method
        #
        # lookup types:
        #   "endpoint" - MAC address lookup (for wireless clients, phones, badges)
        #   "nad" - Network Access Device lookup (for switches, routers, WLCs)
        #
        # Example:
        # "device_mappings": [
        #     {"manufacturer": "cisco", "lookup": "nad"},  # Cisco network devices as NADs
        #     {"manufacturer": "vocera", "lookup": "endpoint"},  # Vocera badges by MAC
        #     {"manufacturer": "cisco", "device_type": ".*phone.*", "lookup": "endpoint"},  # Cisco phones by MAC
        # ]
        "device_mappings": [
            {
                "manufacturer": r"cisco",
                "lookup": "nad",
            },  # Default: Cisco devices as NADs
        ],
        # Endpoint mappings (requires netbox-endpoints plugin)
        # Format: list of dicts with manufacturer (regex), endpoint_type (regex, optional)
        # All endpoints use MAC lookup since they're endpoint devices
        #
        # Example:
        # "endpoint_mappings": [
        #     {"manufacturer": "vocera"},  # All Vocera endpoints
        #     {"manufacturer": "cisco", "endpoint_type": ".*phone.*"},  # Cisco phones
        # ]
        # If empty, shows tab for ALL endpoints with a MAC address
        "endpoint_mappings": [],
    }

    def ready(self):
        """Register endpoint view if netbox_endpoints is available."""
        super().ready()
        self._register_endpoint_views()

    def _register_endpoint_views(self):
        """Register Cisco ISE tab for Endpoints if plugin is installed."""
        import sys

        # Quick check if netbox_endpoints is available
        if "netbox_endpoints" not in sys.modules:
            try:
                import importlib.util

                if importlib.util.find_spec("netbox_endpoints") is None:
                    logger.debug("netbox_endpoints not installed, skipping endpoint view registration")
                    return
            except Exception:
                logger.debug("netbox_endpoints not available, skipping endpoint view registration")
                return

        try:
            from django.shortcuts import render
            from netbox.views import generic
            from netbox_endpoints.models import Endpoint
            from utilities.views import ViewTab, register_model_view

            from .views import should_show_ise_tab_endpoint

            @register_model_view(Endpoint, name="cisco_ise", path="cisco-ise")
            class EndpointISEView(generic.ObjectView):
                """Display Cisco ISE endpoint details for a netbox Endpoint."""

                queryset = Endpoint.objects.all()
                template_name = "netbox_cisco_ise/netbox_endpoint_tab.html"

                tab = ViewTab(
                    label="Cisco ISE",
                    weight=9001,
                    permission="netbox_endpoints.view_endpoint",
                    hide_if_empty=False,
                    visible=should_show_ise_tab_endpoint,
                )

                def get(self, request, pk):
                    endpoint = Endpoint.objects.get(pk=pk)
                    return render(
                        request,
                        self.template_name,
                        {
                            "object": endpoint,
                            "tab": self.tab,
                            "loading": True,
                        },
                    )

            logger.info("Registered Cisco ISE tab for Endpoint model")
        except ImportError:
            logger.debug("netbox_endpoints not installed, skipping endpoint view registration")
        except Exception as e:
            logger.warning(f"Could not register endpoint views: {e}")


config = CiscoISEConfig
