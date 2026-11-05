from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_content', '0024_embeddedcommandrun'),
    ]

    operations = [
        migrations.AddField(
            model_name='glossarytermpage',
            name='image_url',
            field=models.URLField(
                blank=True,
                help_text='Absolute Shopify CDN URL for the glossary image (populated on pull).',
                max_length=500,
            ),
        ),
    ]
