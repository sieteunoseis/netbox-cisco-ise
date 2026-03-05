from django.db import models


class CiscoIse(models.Model):
    """Unmanaged model to register custom permissions for the Cisco ISE plugin."""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (("configure_ciscoise", "Can configure Cisco ISE plugin settings"),)
