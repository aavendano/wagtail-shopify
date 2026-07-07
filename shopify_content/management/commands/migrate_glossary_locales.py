"""Assign Wagtail Locale objects to glossary terms from locale_code."""

from django.core.management.base import BaseCommand

from shopify_content.glossary_locale_utils import wagtail_locale_code_for_glossary
from shopify_content.models import GlossaryTermPage
from wagtail.models import Locale


class Command(BaseCommand):
    help = 'Assign Wagtail Locale to GlossaryTermPage rows based on locale_code (en→en-US, etc.).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report changes without saving.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        updated = 0
        skipped = 0

        for term in GlossaryTermPage.objects.all().select_related('locale'):
            target_code = wagtail_locale_code_for_glossary(term.locale_code or 'en')
            target_locale, _ = Locale.objects.get_or_create(language_code=target_code)
            if term.locale_id == target_locale.pk:
                skipped += 1
                continue
            self.stdout.write(
                f'  {term.term!r} (pk={term.pk}): '
                f'{term.locale.language_code} → {target_code}'
            )
            if not dry_run:
                term.locale = target_locale
                term.save(update_fields=['locale'])
            updated += 1

        style = self.style.SUCCESS if not dry_run else self.style.WARNING
        self.stdout.write(style(
            f'Done. updated={updated}, skipped={skipped}, dry_run={dry_run}.'
        ))
