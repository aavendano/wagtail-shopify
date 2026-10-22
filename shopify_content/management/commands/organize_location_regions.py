"""
Move location pages under their region page (province or state).

A location hangs directly off its root (``local-us``) until this runs. For each group of
loose locations (same root, locale and state/province) it creates a RegionPage next to
them and moves the locations underneath. Only the Wagtail tree changes: nothing is sent to
Shopify, and handles (so storefront URLs) are not touched.

Dry run by default. Safe to re-run: regions that exist are reused and locations already
under a region are left alone.

Usage:
    python manage.py organize_location_regions              # dry run
    python manage.py organize_location_regions --apply
"""

from collections import Counter, defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from shopify_content.models import LocationPage, RegionPage, ShopifyRootPage
from shopify_content.region_codes import region_code_for
from shopify_content.shopify_languages import shopify_country


def _loose_locations():
    """Locations whose parent is a root page, not a region."""
    for page in LocationPage.objects.all().order_by('path'):
        parent = page.get_parent()
        if parent is not None and isinstance(parent.specific, ShopifyRootPage):
            yield page, parent.specific


def region_slug(locale_code: str, state: str) -> str:
    """Locale-prefixed, like location handles: slugs are unique among siblings of every locale."""
    return f'{slugify(locale_code)}-{slugify(state)}'


class Command(BaseCommand):
    help = 'Create RegionPages and move location pages under them (Wagtail tree only)'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Write changes (default is a dry run).')

    def handle(self, *args, **options):
        apply_changes = options['apply']
        groups = defaultdict(list)
        skipped = []
        for page, root in _loose_locations():
            state = (page.state or '').strip()
            if not state:
                skipped.append(page)
                continue
            groups[(root.pk, page.locale_id, state)].append(page)

        created = reused = moved = 0
        mode = 'Applying' if apply_changes else 'Dry run'
        self.stdout.write(f'{mode}: {sum(len(v) for v in groups.values())} loose location(s) in {len(groups)} region group(s)')

        with transaction.atomic():
            for (root_pk, locale_id, state), pages in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][2])):
                root = ShopifyRootPage.objects.get(pk=root_pk)
                locale = pages[0].locale
                countries = Counter(p.country for p in pages if p.country)
                country = (countries.most_common(1)[0][0] if countries
                           else shopify_country(locale.language_code) or '')
                slug = region_slug(locale.language_code, state)
                code = region_code_for(country, state)

                existing = RegionPage.objects.child_of(root).filter(slug=slug, locale=locale).first()
                self.stdout.write(
                    f'  {locale.language_code} {state} ({country or "?"}, {code or "no code"}): '
                    f'{len(pages)} location(s) -> {"existing" if existing else "new"} region "{slug}"'
                )
                if not apply_changes:
                    reused += 1 if existing else 0
                    created += 0 if existing else 1
                    moved += len(pages)
                    continue

                if existing:
                    region = existing
                    reused += 1
                else:
                    region = RegionPage(
                        title=state, slug=slug, locale=locale, country=country, region_code=code,
                    )
                    root.add_child(instance=region)
                    region.save_revision().publish()
                    created += 1
                for page in pages:
                    page.move(region, pos='last-child')
                    moved += 1

        for page in skipped:
            self.stdout.write(self.style.WARNING(f'  skipped "{page.title}" (pk={page.pk}): no state or province'))
        self.stdout.write(self.style.SUCCESS(
            f'{"Done" if apply_changes else "Would do"}: {created} region(s) created, '
            f'{reused} reused, {moved} location(s) moved, {len(skipped)} skipped.'
        ))
        if not apply_changes:
            self.stdout.write('Dry run: nothing was written. Use --apply to move pages.')
