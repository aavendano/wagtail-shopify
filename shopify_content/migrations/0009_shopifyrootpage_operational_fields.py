"""Add ShopifyRootPage operational fields missing from 0001 (catch-up migration)."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_content", "0008_content_index"),
    ]

    operations = [
        migrations.AddField(
            model_name="shopifyrootpage",
            name="shopify_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="Shopify metaobject GID (populated after first upsert)",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="shopifyrootpage",
            name="handle",
            field=models.SlugField(
                blank=True,
                help_text="Shopify metaobject handle (defaults to Wagtail slug)",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="shopifyrootpage",
            name="sync_enabled",
            field=models.BooleanField(db_default=True, default=True),
        ),
        migrations.AddField(
            model_name="shopifyrootpage",
            name="last_synced_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="shopifyrootpage",
            name="export_config",
            field=models.JSONField(blank=True, db_default={}, default=dict),
        ),
    ]
