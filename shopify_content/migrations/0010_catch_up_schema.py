"""Formerly a catch-up schema dump that duplicated the main migration lineage.

Kept as a no-op leaf so existing environments that recorded this migration stay
consistent. Fresh installs get schema from 0008_location…0034 instead.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_content", "0009_shopifyrootpage_operational_fields"),
    ]

    operations = []
