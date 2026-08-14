"""Migrate legacy wagtailcore.Page home rows to HomePage under cms-home root."""

from django.core.management.base import BaseCommand

from wagtail.models import Page

from shopify_content.models import HomePage, ShopifyRootPage
from shopify_content.home_sections_normalization import normalize_sections_json
from shopify_content.home_serialization import sections_json_to_stream_data
from shopify_content.sync.import_parents import resolve_shopify_import_parent


LEGACY_SLUG_PREFIXES = ('home', 'home-')


class Command(BaseCommand):
    help = (
        'Create HomePage copies from legacy wagtailcore.Page rows (slug home / home-*). '
        'Legacy pages are left in place for manual review.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report migrations without creating pages.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        parent = resolve_shopify_import_parent('home', auto_create=not dry_run)
        if not isinstance(parent, ShopifyRootPage):
            self.stderr.write(self.style.ERROR(f'Expected ShopifyRootPage, got {type(parent).__name__}'))
            return

        legacy_qs = (
            Page.objects
            .filter(slug__startswith='home')
            .exclude(id__in=HomePage.objects.values_list('id', flat=True))
        )

        migrated = 0
        skipped = 0
        for legacy in legacy_qs:
            specific = legacy.specific
            if isinstance(specific, (HomePage, ShopifyRootPage)):
                skipped += 1
                continue

            if HomePage.objects.child_of(parent).filter(locale=legacy.locale).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'  skip legacy pk={legacy.pk} ({legacy.slug}): '
                        f'HomePage already exists for locale {legacy.locale.language_code}'
                    )
                )
                skipped += 1
                continue

            hero_heading = legacy.title or 'Home'
            self.stdout.write(
                f'  migrate pk={legacy.pk} slug={legacy.slug} locale={legacy.locale.language_code} '
                f'→ HomePage'
            )

            if dry_run:
                migrated += 1
                continue

            page = HomePage(
                title=hero_heading,
                hero_heading=hero_heading,
                locale=legacy.locale,
                shopify_locale=legacy.locale.language_code,
                seo_title=legacy.seo_title or '',
                search_description=legacy.search_description or '',
            )
            page.sections_json = normalize_sections_json({})
            page.body = sections_json_to_stream_data(page.sections_json)
            parent.add_child(instance=page)
            migrated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. migrated={migrated}, skipped={skipped}, dry_run={dry_run}. '
            'Legacy pages were not deleted.'
        ))
