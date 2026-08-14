"""Ensure ShopifyRootPage cms-home and one HomePage per allowed locale."""

from django.conf import settings
from django.core.management.base import BaseCommand

from wagtail.models import Locale

from shopify_content.models import HomePage, ShopifyRootPage
from shopify_content.home_sections_normalization import normalize_sections_json
from shopify_content.home_serialization import sections_json_to_stream_data
from shopify_content.sync.import_parents import resolve_shopify_import_parent


class Command(BaseCommand):
    help = (
        'Create ShopifyRootPage slug=cms-home (if missing) and HomePage rows '
        'for each ALLOWED_LOCALE_CODES locale.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--publish',
            action='store_true',
            help='Publish created HomePage rows (triggers Shopify sync when sync_enabled).',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report actions without writing.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        publish = options['publish']

        if dry_run:
            self.stdout.write(self.style.WARNING('Dry run — no changes will be saved.'))

        parent = resolve_shopify_import_parent('home', auto_create=not dry_run)
        if not isinstance(parent, ShopifyRootPage):
            self.stderr.write(self.style.ERROR(f'Expected ShopifyRootPage, got {type(parent).__name__}'))
            return

        self.stdout.write(f'Home root: {parent.title} (pk={parent.pk}, slug={parent.slug})')
        self.stdout.write(
            f'  Explorer: Site root → {parent.title} (slug={parent.slug}) → HomePage per locale'
        )

        created = 0
        skipped = 0
        created_pages = []
        for locale_code in settings.ALLOWED_LOCALE_CODES:
            locale, _ = Locale.objects.get_or_create(language_code=locale_code)
            existing = HomePage.objects.child_of(parent).filter(locale=locale).first()
            if existing:
                skipped += 1
                self.stdout.write(
                    f'  skip {locale_code}: HomePage pk={existing.pk} slug={existing.slug} '
                    f'live={existing.live} edit=/admin/pages/{existing.pk}/edit/'
                )
                continue

            label = settings.ALLOWED_LOCALE_CODES[locale_code]
            hero_heading = f'Home ({label})'
            self.stdout.write(f'  create {locale_code}: {hero_heading!r}')

            if dry_run:
                created += 1
                continue

            page = HomePage(
                title=hero_heading,
                hero_heading=hero_heading,
                locale=locale,
                shopify_locale=locale_code,
            )
            page.sections_json = normalize_sections_json({})
            page.body = sections_json_to_stream_data(page.sections_json)
            parent.add_child(instance=page)
            revision = page.save_revision()
            if publish:
                revision.publish()
            page.refresh_from_db()

            created += 1
            created_pages.append(page)
            self.stdout.write(self.style.SUCCESS(
                f'    → pk={page.pk} slug={page.slug} live={page.live} '
                f'edit=/admin/pages/{page.pk}/edit/'
            ))

        self.stdout.write(self.style.SUCCESS(
            f'Done. created={created}, skipped={skipped}, dry_run={dry_run}, publish={publish}.'
        ))
        if created_pages and not publish:
            self.stdout.write(self.style.WARNING(
                'Pages saved as drafts. Re-run with --publish to publish and sync to Shopify.'
            ))
        elif created_pages and publish:
            self.stdout.write(
                'Published pages enqueue Shopify sync when sync_enabled=true and Celery is running.'
            )
