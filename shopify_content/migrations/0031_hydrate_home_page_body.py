from django.db import migrations


def hydrate_home_body(apps, schema_editor):
    HomePage = apps.get_model('shopify_content', 'HomePage')
    from shopify_content.home_serialization import sections_json_to_stream_data
    from shopify_content.home_sections_normalization import normalize_sections_json

    for page in HomePage.objects.all().iterator():
        normalized = normalize_sections_json(page.sections_json or {})
        page.sections_json = normalized
        page.body = sections_json_to_stream_data(normalized)
        page.save(update_fields=['body', 'sections_json'])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_content', '0030_home_page_body_streamfield'),
    ]

    operations = [
        migrations.RunPython(hydrate_home_body, noop_reverse),
    ]
