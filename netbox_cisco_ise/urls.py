"""
URL routing for NetBox Cisco ISE Plugin
"""

from django.urls import path

from .views import ENDPOINTS_PLUGIN_INSTALLED, DeviceISEContentView, ISESettingsView, TestConnectionView

urlpatterns = [
    path("settings/", ISESettingsView.as_view(), name="settings"),
    path("test-connection/", TestConnectionView.as_view(), name="test_connection"),
    path("device/<int:pk>/content/", DeviceISEContentView.as_view(), name="device_content"),
]

# Add endpoint URLs if netbox_endpoints is installed
if ENDPOINTS_PLUGIN_INSTALLED:
    from .views import EndpointISEContentView

    urlpatterns.append(
        path("endpoint/<int:pk>/content/", EndpointISEContentView.as_view(), name="endpoint_content"),
    )
