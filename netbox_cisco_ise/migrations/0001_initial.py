from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CiscoIse",
            fields=[],
            options={
                "managed": False,
                "default_permissions": (),
                "permissions": (
                    ("configure_ciscoise", "Can configure Cisco ISE plugin settings"),
                ),
            },
        ),
    ]
