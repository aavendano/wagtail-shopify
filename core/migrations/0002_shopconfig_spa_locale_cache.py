from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shopconfig",
            name="cached_spa_locales",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="shopconfig",
            name="cached_spa_primary_locale",
            field=models.CharField(blank=True, default="", max_length=32),
        ),
        migrations.AddField(
            model_name="shopconfig",
            name="spa_locales_fetched_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
