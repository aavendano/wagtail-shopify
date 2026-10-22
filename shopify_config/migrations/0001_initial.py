# State-only claim of ShopConfig after core removes it from state.
# Physical table remains core_shopconfig (Meta.db_table); no ALTER TABLE.

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0002_remove_shopconfig_state"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="ShopConfig",
                    fields=[
                        (
                            "id",
                            models.BigAutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        ("shop", models.CharField(max_length=255, unique=True)),
                        (
                            "state",
                            models.CharField(blank=True, max_length=255, null=True),
                        ),
                        ("is_online", models.BooleanField(default=False)),
                        ("scope", models.TextField(blank=True, null=True)),
                        ("expires", models.DateTimeField(blank=True, null=True)),
                        (
                            "access_token",
                            models.CharField(blank=True, max_length=255, null=True),
                        ),
                        (
                            "refresh_token",
                            models.CharField(blank=True, max_length=255, null=True),
                        ),
                        (
                            "refresh_token_expires",
                            models.DateTimeField(blank=True, null=True),
                        ),
                    ],
                    options={
                        "db_table": "core_shopconfig",
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
