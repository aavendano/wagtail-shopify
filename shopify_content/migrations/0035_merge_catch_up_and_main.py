# Merge the obsolete catch-up leaf with the main shopify_content lineage.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_content", "0010_catch_up_schema"),
        ("shopify_content", "0034_alter_homepage_body"),
    ]

    operations = []
