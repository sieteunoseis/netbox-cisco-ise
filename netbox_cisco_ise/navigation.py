"""
Navigation menu items for NetBox Cisco ISE Plugin
"""

from netbox.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_cisco_ise:settings",
        link_text="Cisco ISE",
        permissions=["dcim.view_device"],
    ),
)
