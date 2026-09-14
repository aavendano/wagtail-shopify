from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_content", "0007_shopify_sync_run"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContentIndex",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content_type", models.CharField(db_index=True, max_length=128)),
                ("object_id", models.CharField(db_index=True, max_length=64)),
                ("field_key", models.CharField(db_index=True, max_length=64)),
                ("locale", models.CharField(db_index=True, max_length=16)),
                ("checksum", models.CharField(blank=True, max_length=64)),
                ("reference_count", models.PositiveIntegerField(default=0)),
                ("relative_path", models.CharField(blank=True, max_length=512)),
                ("indexed_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ContentReferenceIndex",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ref_type", models.CharField(db_index=True, max_length=32)),
                ("identifier", models.CharField(db_index=True, max_length=255)),
                ("token", models.CharField(max_length=512)),
                (
                    "content_index",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="references",
                        to="shopify_content.contentindex",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="contentindex",
            constraint=models.UniqueConstraint(
                fields=("content_type", "object_id", "field_key", "locale"),
                name="uniq_content_index_ref",
            ),
        ),
        migrations.AddIndex(
            model_name="contentreferenceindex",
            index=models.Index(fields=["ref_type", "identifier"], name="content_ref_type_ident_idx"),
        ),
    ]
