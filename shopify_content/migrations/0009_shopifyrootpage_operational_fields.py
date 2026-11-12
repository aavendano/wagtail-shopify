"""Formerly added ShopifyRootPage fields; superseded by 0021 on the main branch.

Kept as a no-op node so historical DBs that applied this leaf remain valid.
On fresh installs, 0021 adds these fields.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_content", "0008_content_index"),
    ]

    operations = []
