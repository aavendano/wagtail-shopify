"""
Creates the four Wagtail Locale objects required for hreflang support.
Run once after initial migrations.
"""
from django.core.management.base import BaseCommand
from wagtail.models import Locale

REQUIRED_LOCALES = ['en-US', 'es-US', 'en-CA', 'fr-CA']


class Command(BaseCommand):
    help = 'Create Wagtail Locale objects for en-US, es-US, en-CA, fr-CA.'

    def handle(self, *args, **options):
        for lang in REQUIRED_LOCALES:
            obj, created = Locale.objects.get_or_create(language_code=lang)
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'{status}: {lang}')
        self.stdout.write(self.style.SUCCESS('Locale setup complete.'))
