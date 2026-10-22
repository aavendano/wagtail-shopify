# Remove ShopConfig from core app state before shopify_config claims it.
# Physical table core_shopconfig is not dropped.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name="ShopConfig"),
            ],
            database_operations=[],
        ),
    ]
