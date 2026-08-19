"""Seed editorial home content for home-en-us (PlayLoveToys en-US)."""

from django.core.management.base import BaseCommand

from wagtail.models import Locale

from core.models import ShopConfig
from shopify_content.models import CollectionPage, HomePage
from shopify_content.home_sections_normalization import normalize_sections_json
from shopify_content.home_serialization import sections_json_to_stream_data
from shopify_content.sync.outbound import sync_home_page


def _collection_page_id(handle: str) -> int | None:
    """Resolve CollectionPage Wagtail pk by Shopify handle."""
    page = CollectionPage.objects.filter(handle=handle).first()
    return page.pk if page else None


def _promo_gateway_section() -> dict:
    card1_categories = _collection_page_ids(
        'best-sex-toys',
        'sex-toys-for-women',
        'sexy-lingerie',
        'vibrators',
    )
    card2_categories = _collection_page_ids(
        'male-wand',
        'male-masturbators-strokers',
        'penis-ring-cock-ring-sex-toys-for-men',
        'prostate-massage',
    )
    card3_categories = _collection_page_ids(
        'anal-stimulation',
        'romance',
        'rose-toys',
        'pleasure-enhancers',
    )
    card4_primary = _collection_page_id('bachelorette-party-novelties')

    cards = [
        {
            'title': 'Viral picks',
            'badge': 'Up to 30% off',
            'media_source': 'collection_list',
            'category_page_ids': card1_categories,
            'cta_label': 'Shop trending',
            'cta_url': '',
            'column_span': '1',
        },
        {
            'title': 'Fresh new arrivals',
            'badge': 'Up to 30% off',
            'media_source': 'collection_list',
            'category_page_ids': card2_categories,
            'cta_label': 'Shop trending',
            'cta_url': '',
            'column_span': '1',
        },
        {
            'title': 'Premium picks',
            'badge': '',
            'media_source': 'collection_list',
            'category_page_ids': card3_categories,
            'cta_label': 'Shop trending',
            'cta_url': '',
            'column_span': '1',
        },
    ]
    card4: dict = {
        'title': 'Shop by category',
        'badge': '',
        'media_source': 'collection_products',
        'cta_label': 'Shop trending',
        'cta_url': '',
        'column_span': '1',
    }
    if card4_primary:
        card4['primary_collection_page_id'] = card4_primary
    cards.append(card4)

    return {
        'type': 'promo_gateway',
        'id': 'promo-gateway',
        'value': {'cards': cards},
    }


def _collection_page_ids(*handles: str) -> list[int]:
    ids = []
    for handle in handles:
        page_id = _collection_page_id(handle)
        if page_id:
            ids.append(page_id)
    return ids


def _nav_collection_pills_section() -> dict:
    items = []
    for handle, label in (
        ('vibrators', 'Vibrators'),
        ('lubricants', 'Lubricants'),
        ('anal-stimulation', 'Anal Stimulation'),
        ('penis-ring-cock-ring-sex-toys-for-men', 'For Men'),
    ):
        page_id = _collection_page_id(handle)
        if page_id:
            items.append({'page_id': page_id, 'override_label': label})
    return {
        'type': 'nav_collection_pills',
        'id': 'nav-collection-pills',
        'value': {'items': items},
    }


def _featured_collection_items() -> list[dict]:
    """Four core category cards for the featured grid (lg:grid-cols-4)."""
    items = []
    for handle, title in (
        ('vibrators', 'Vibrators'),
        ('sex-toys-for-couples', 'Couples'),
        ('best-sex-toys', 'Best Sex Toys'),
        ('sex-toys-for-women', 'For Women'),
    ):
        page_id = _collection_page_id(handle)
        if page_id:
            items.append({'page_id': page_id, 'override_title': title})
    return items


def _storefront_url(path: str) -> str:
    """Build absolute URL for Wagtail URLField (storefront-relative path)."""
    path = path if path.startswith('/') else f'/{path}'
    config = ShopConfig.objects.first()
    if config and config.shop:
        return f'https://{config.shop}{path}'
    return f'https://example.myshopify.com{path}'


def _sections_payload() -> dict:
    return {
        'version': 1,
        'sections': [
            {
                'type': 'trust_bar',
                'id': 'trust-bar',
                'value': {
                    'items': [
                        {
                            'icon': 'local_shipping',
                            'title': 'Discreet Shipping',
                            'description': 'Plain packaging, fast delivery',
                        },
                        {
                            'icon': 'verified',
                            'title': 'Body-Safe Materials',
                            'description': 'Curated, quality-tested products',
                        },
                        {
                            'icon': 'lock',
                            'title': 'Secure Checkout',
                            'description': 'Encrypted payments',
                        },
                        {
                            'icon': 'favorite',
                            'title': 'Inclusive Shopping',
                            'description': 'For every body and every desire',
                        },
                    ],
                },
            },
            _promo_gateway_section(),
            _nav_collection_pills_section(),
            {
                'type': 'featured_collections',
                'id': 'featured-collections',
                'value': {
                    'badge': 'TRENDING',
                    'title': 'Core Categories',
                    'intro': 'Shop our most-loved collections, curated for discovery and everyday pleasure.',
                    'items': _featured_collection_items(),
                },
            },
            {
                'type': 'editorial_intro',
                'id': 'editorial-intro',
                'value': {
                    'heading': 'Sexual Wellness for Every Body',
                    'body': (
                        '<p>At PlayLoveToys we believe pleasure is personal. Our editorial team curates '
                        '<a href="/collections/best-sex-toys">body-safe toys</a>, guides, and resources '
                        'so you can shop with confidence—whether you are exploring solo play, shopping with '
                        'a partner, or building a wellness routine. We prioritize inclusive language, '
                        'discreet fulfillment, and products made from medical-grade silicone and other '
                        'non-porous materials.</p>'
                        '<p>Not sure where to start? Browse our buying guides and '
                        '<a href="/pages/glossary/vibrator">glossary</a> to learn about fit, materials, '
                        'and care. Every collection is reviewed for quality, safety, and real-world use—'
                        'because informed shopping leads to better experiences.</p>'
                    ),
                    'alignment': 'left',
                },
            },
            {
                'type': 'best_sellers',
                'id': 'best-sellers',
                'value': {
                    'title': 'Best Sellers',
                    'collection_page_id': 196,
                    'product_limit': 8,
                    'badge': 'HOT',
                    'background': 'contrast',
                },
            },
            {
                'type': 'shop_by_need',
                'id': 'shop-by-need',
                'value': {
                    'title': 'Shop by Need',
                    'cards': [
                        {
                            'title': 'For Beginners',
                            'description': 'Easy starters and approachable picks',
                            'target_page_id': 200,
                            'cta_label': 'Shop',
                            'intent_tag': 'beginners',
                        },
                        {
                            'title': 'For Couples',
                            'description': 'Shared pleasure and connection',
                            'target_page_id': 242,
                            'cta_label': 'Shop',
                            'intent_tag': 'couples',
                        },
                        {
                            'title': 'Solo Play',
                            'description': 'Self-discovery and personal wellness',
                            'target_page_id': 202,
                            'cta_label': 'Shop',
                            'intent_tag': 'solo',
                        },
                        {
                            'title': 'Wellness',
                            'description': 'Pelvic health and relaxation',
                            'target_page_id': 201,
                            'cta_label': 'Shop',
                            'intent_tag': 'wellness',
                        },
                        {
                            'title': 'Gifts',
                            'description': 'Thoughtful picks for any occasion',
                            'target_page_id': 214,
                            'cta_label': 'Shop',
                            'intent_tag': 'gifts',
                        },
                        {
                            'title': 'Anal Play',
                            'description': 'Explore safely with curated essentials',
                            'target_page_id': 211,
                            'cta_label': 'Shop',
                            'intent_tag': 'anal',
                        },
                    ],
                },
            },
            {
                'type': 'educational_hub',
                'id': 'education-hub',
                'value': {
                    'title': 'Learn & Explore',
                    'intro': 'Guides, glossary terms, and articles from our editorial team.',
                    'links': [
                        {
                            'page_id': 7,
                            'label': "Beginner's Guide",
                            'description': 'How to choose your first toy',
                        },
                        {
                            'page_id': 2501,
                            'label': 'Sex Toy',
                            'description': 'Glossary: what counts as a sex toy',
                        },
                        {
                            'page_id': 2489,
                            'label': 'Vibrator',
                            'description': 'Glossary: types and features',
                        },
                        {
                            'page_id': 9,
                            'label': 'Myths & Realities',
                            'description': 'What you need to know about intimate products',
                        },
                    ],
                },
            },
            {
                'type': 'brand_values',
                'id': 'brand-values',
                'value': {
                    'eyebrow': 'Our values',
                    'heading': 'Built for Confidence and Care',
                    'body': (
                        '<p>We built PlayLoveToys for shoppers who want discretion without sacrificing '
                        'quality. Every product page includes material details, care instructions, and '
                        'editorial context so you never have to guess.</p>'
                    ),
                    'media_position': 'left',
                    'values': [
                        {
                            'icon': 'local_shipping',
                            'title': 'Discreet packaging',
                            'description': 'Plain outer boxes with no product names visible.',
                        },
                        {
                            'icon': 'verified',
                            'title': 'Body-safe curation',
                            'description': 'Medical-grade silicone and trusted brands only.',
                        },
                        {
                            'icon': 'favorite',
                            'title': 'Inclusive shopping',
                            'description': 'Shame-free language for every body and identity.',
                        },
                        {
                            'icon': 'shield',
                            'title': 'Privacy-first checkout',
                            'description': 'Encrypted payments and minimal data retention.',
                        },
                    ],
                },
            },
            {
                'type': 'market_block',
                'id': 'market-us',
                'value': {
                    'heading': 'Shipping Across the USA',
                    'body': (
                        '<p>Free shipping on orders over $75. Discreet packaging on every order, '
                        'with tracking from checkout to delivery.</p>'
                    ),
                    'highlights': [
                        'Free shipping over $75',
                        'Discreet plain packaging',
                        'Fast domestic delivery',
                    ],
                    'cta_label': 'Shop now',
                    'cta_url': '/collections/all',
                    'market_code': 'US',
                },
            },
            {
                'type': 'faq',
                'id': 'faq',
                'value': {
                    'heading': 'Frequently Asked Questions',
                    'items': [
                        {
                            'question': 'Is shipping discreet?',
                            'answer': (
                                '<p>Yes — plain packaging with no product names or explicit imagery '
                                'on the outside of the box.</p>'
                            ),
                        },
                        {
                            'question': 'What materials are body-safe?',
                            'answer': (
                                '<p>We prioritize medical-grade silicone, ABS plastic, and other '
                                'non-porous materials. Each product page lists material details.</p>'
                            ),
                        },
                        {
                            'question': 'How do returns work?',
                            'answer': (
                                '<p>Unopened items in original packaging can be returned within 30 days. '
                                'See our returns policy for full details.</p>'
                            ),
                        },
                        {
                            'question': 'Do you ship to all US states?',
                            'answer': (
                                '<p>We ship to all 50 states. Delivery times vary by region; '
                                'tracking is provided at checkout.</p>'
                            ),
                        },
                        {
                            'question': 'How do I choose my first toy?',
                            'answer': (
                                '<p>Start with our beginner guides and glossary, or browse the '
                                '<a href="/collections/best-sex-toys">Best Sex Toys</a> collection '
                                'for curated starter picks.</p>'
                            ),
                        },
                    ],
                },
            },
            {
                'type': 'internal_links',
                'id': 'internal-links',
                'value': {
                    'heading': 'Explore the Store',
                    'groups': [
                        {
                            'title': 'Collections',
                            'links': [
                                {'page_id': 2859, 'label': 'Vibrators'},
                                {'page_id': 242, 'label': 'Couples'},
                                {'page_id': 211, 'label': 'Anal'},
                                {'page_id': 206, 'label': 'Dildos'},
                                {'page_id': 202, 'label': 'For Women'},
                                {'page_id': 207, 'label': 'For Men'},
                                {'page_id': 214, 'label': 'Romance'},
                                {'page_id': 200, 'label': 'Best Sex Toys'},
                            ],
                        },
                        {
                            'title': 'Brands & Best Sellers',
                            'links': [
                                {'page_id': 196, 'label': 'Best Sellers'},
                                {'page_id': 198, 'label': 'Womanizer'},
                                {'page_id': 203, 'label': 'Tenga'},
                                {'page_id': 204, 'label': 'Lelo'},
                                {'page_id': 205, 'label': 'Magic Wand'},
                                {'page_id': 241, 'label': 'Pleasure Enhancers'},
                                {'page_id': 201, 'label': 'Massage & Relaxation'},
                                {'page_id': 2859, 'label': 'All Vibrators'},
                            ],
                        },
                        {
                            'title': 'Guides',
                            'links': [
                                {'page_id': 7, 'label': 'Romantic Interactions'},
                                {'page_id': 8, 'label': 'Breaking Taboos'},
                                {'page_id': 9, 'label': 'Myths & Realities'},
                                {'page_id': 10, 'label': 'Intimate Changes'},
                                {'page_id': 11, 'label': 'Mental Health'},
                                {'page_id': 12, 'label': 'Movies & Wellness'},
                                {'page_id': 13, 'label': 'Social Media'},
                                {'page_id': 14, 'label': 'Sustainable Products'},
                            ],
                        },
                        {
                            'title': 'Glossary',
                            'links': [
                                {'page_id': 2489, 'label': 'Vibrator'},
                                {'page_id': 2501, 'label': 'Sex Toy'},
                                {'page_id': 2506, 'label': 'Dildo'},
                                {'page_id': 2510, 'label': 'Bullet Vibrator'},
                                {'page_id': 2516, 'label': 'Magic Wand'},
                                {'page_id': 2522, 'label': 'G-Spot Dildo'},
                                {'page_id': 2528, 'label': 'Cock Ring'},
                                {'page_id': 2534, 'label': 'Anal Beads'},
                            ],
                        },
                    ],
                },
            },
            {
                'type': 'seo_schema',
                'id': 'seo-schema',
                'value': {
                    'include_faq_schema': True,
                    'include_organization': True,
                },
            },
        ],
    }


class Command(BaseCommand):
    help = 'Seed editorial home content for en-US HomePage (home-en-us).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--push',
            action='store_true',
            help='Push to Shopify metaobject after saving.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print actions without saving.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        push = options['push']

        locale = Locale.objects.filter(language_code='en-US').first()
        if locale is None:
            self.stderr.write(self.style.ERROR('Locale en-US not found.'))
            return

        page = HomePage.objects.filter(locale=locale, slug='home-en-us').first()
        if page is None:
            page = HomePage.objects.filter(locale=locale).first()
        if page is None:
            self.stderr.write(self.style.ERROR('HomePage for en-US not found. Run bootstrap_home_pages first.'))
            return

        self.stdout.write(f'Target: HomePage pk={page.pk} slug={page.slug}')

        hero_updates = {
            'title': 'Adult Toys & Sexual Wellness Products for Every Body',
            'hero_eyebrow': 'PlayLoveToys',
            'hero_heading': 'Adult Toys & Sexual Wellness Products for Every Body',
            'hero_subheading': (
                'Curated pleasure products with discreet shipping, body-safe materials, '
                'and inclusive shopping for every body and every desire.'
            ),
            'hero_primary_cta_label': 'Shop Now',
            'hero_primary_cta_url': _storefront_url('/collections/all'),
            'hero_secondary_cta_label': 'View Collections',
            'hero_secondary_cta_url': _storefront_url('/collections/best-sex-toys'),
            'seo_title': 'Adult Toys & Sexual Wellness | PlayLoveToys',
            'search_description': (
                'Shop body-safe adult toys and sexual wellness products with discreet shipping. '
                'Curated vibrators, couples toys, and guides for every body.'
            ),
            'sections_json': _sections_payload(),
        }

        if dry_run:
            self.stdout.write(self.style.WARNING('Dry run — would update hero + 11 sections.'))
            return

        for field, value in hero_updates.items():
            setattr(page, field, value)

        page.sections_json = normalize_sections_json(page.sections_json)
        page.body = sections_json_to_stream_data(page.sections_json)

        page.save()
        revision = page.save_revision()
        revision.publish()
        page.refresh_from_db()

        self.stdout.write(self.style.SUCCESS(
            f'Updated HomePage pk={page.pk} with hero + {len(page.sections_json["sections"])} sections.'
        ))

        if push:
            success, message = sync_home_page(page)
            if success:
                page.refresh_from_db()
                self.stdout.write(self.style.SUCCESS(f'Pushed to Shopify: {message} shopify_id={page.shopify_id}'))
            else:
                self.stderr.write(self.style.ERROR(f'Push failed: {message}'))
