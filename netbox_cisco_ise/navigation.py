"""
Navigation menu items for NetBox Cisco ISE Plugin
"""

from django.conf import settings
from netbox.plugins import PluginMenu, PluginMenuItem

_menu = PluginMenu(
    label="Cisco ISE",
    groups=(
        (
            "Settings",
            (
                PluginMenuItem(
                    link="plugins:netbox_cisco_ise:settings",
                    link_text="Configuration",
                    permissions=["netbox_cisco_ise.configure_ciscoise"],
                ),
            ),
        ),
    ),
    icon_class="mdi mdi-shield-account",
)


# top_level_menu=False puts this plugin's items under the shared "Plugins" menu
# (grouped by plugin name) instead of its own top-level sidebar menu.
if settings.PLUGINS_CONFIG.get("netbox_cisco_ise", {}).get("top_level_menu", True):
    menu = _menu
else:
    menu_items = tuple(item for group in _menu.groups for item in group.items)
