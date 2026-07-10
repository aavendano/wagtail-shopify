"""Seed or update a single LocationPage from the en-US city template."""

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from wagtail.models import Locale, Page

from shopify_content.content_templates.location_city_en_us import (
    build_location_payload,
    find_forbidden_phrases,
)
from shopify_content.location_slug import location_page_slug
from shopify_content.models import LocationPage, LocationPageFAQ, ShopifyRootPage
from shopify_content.richtext_sanitize import sanitize_richtext_html
from shopify_content.sync.outbound import sync_location_page


class Command(BaseCommand):
    help = 'Create or update a LocationPage from the en-US city content template.'

    def add_arguments(self, parser):
        parser.add_argument('--city', required=True, help='City name (e.g. Anaheim)')
        parser.add_argument('--state', required=True, help='State name (e.g. California)')
        parser.add_argument('--slug', default='', help='Optional legacy slug hint (handle is auto-derived)')
        parser.add_argument('--locale', default='en-US', help='Wagtail locale code')
        parser.add_argument('--push', action='store_true', help='Push to Shopify after publish')
        parser.add_argument('--no-publish', action='store_true', help='Save draft without publishing')
        parser.add_argument('--dry-run', action='store_true', help='Print payload only')

    def handle(self, *args, **options):
        city = options['city']
        state = options['state']
        slug_hint = options['slug'] or None

        payload = build_location_payload(city=city, state=state, slug=slug_hint)

        combined_text = ' '.join(
            str(payload.get(field, ''))
            for field in (
                'intro', 'content_2', 'content_3', 'brand_section_content',
                'map_content', 'after_page_content',
            )
        )
        for faq in payload.get('faqs') or []:
            combined_text += f" {faq.get('question', '')} {faq.get('answer', '')}"

        forbidden = find_forbidden_phrases(combined_text)
        if forbidden:
            self.stderr.write(self.style.WARNING(f'Forbidden phrases in template: {forbidden}'))

        if options['dry_run']:
            self.stdout.write(self.style.SUCCESS('Dry run — payload fields:'))
            for key, value in payload.items():
                if key == 'faqs':
                    self.stdout.write(f'  {key}: {len(value)} items')
                else:
                    preview = str(value)[:120]
                    self.stdout.write(f'  {key}: {preview}')
            return

        locale = Locale.objects.filter(language_code=options['locale']).first()
        if locale is None:
            self.stderr.write(self.style.ERROR(f'Locale {options["locale"]} not found.'))
            return

        parent = ShopifyRootPage.objects.filter(slug='local-us').first()
        if parent is None:
            site_root = Page.get_first_root_node()
            if site_root is None:
                self.stderr.write(self.style.ERROR('No site root found.'))
                return
            parent = ShopifyRootPage(title='Local US', slug='local-us', locale=locale)
            site_root.add_child(instance=parent)
            parent.save_revision().publish()

        # Try to find existing page by city+state under parent
        page = (
            LocationPage.objects.child_of(parent)
            .filter(city__iexact=city, state__iexact=state, locale=locale)
            .first()
        )

        creating = page is None
        if creating:
            page = LocationPage(locale=locale)

        page.titulo = payload['titulo']
        page.title = payload['titulo']
        page.subtitulo = payload['subtitulo']
        page.country = payload['country']
        page.state = payload['state']
        page.city = payload['city']
        page.titulo_2 = payload['titulo_2']
        page.subtitulo_h2 = payload['subtitulo_h2']
        page.titulo_3 = payload['titulo_3']
        page.subtitulo_3 = payload['subtitulo_3']
        page.brand_section_title = payload['brand_section_title']
        page.brand_section_subtitle = payload['brand_section_subtitle']
        page.map_title = payload['map_title']
        page.shopify_locale = payload['shopify_locale']
        page.sync_enabled = payload['sync_enabled']
        page.seo_title = payload['seo_title']
        page.search_description = payload['search_description']

        for field in (
            'intro', 'content_2', 'content_3', 'brand_section_content',
            'map_content', 'after_page_content',
        ):
            setattr(page, field, sanitize_richtext_html(payload.get(field) or ''))

        canonical = location_page_slug(page)
        if canonical:
            page.slug = canonical
            page.handle = canonical

        if creating:
            parent.add_child(instance=page)
        else:
            page.save()

        page.faqs.all().delete()
        for sort_order, faq in enumerate(payload.get('faqs') or []):
            LocationPageFAQ.objects.create(
                page=page,
                question=faq['question'],
                answer=sanitize_richtext_html(faq.get('answer') or ''),
                sort_order=sort_order,
            )

        if not options['no_publish']:
            revision = page.save_revision()
            revision.publish()

        page.refresh_from_db()
        action = 'Created' if creating else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} LocationPage pk={page.pk} slug={page.slug}'))

        if options['push']:
            success, message = sync_location_page(page)
            if success:
                self.stdout.write(self.style.SUCCESS(f'Push OK: {message}'))
            else:
                self.stderr.write(self.style.ERROR(f'Push failed: {message}'))
