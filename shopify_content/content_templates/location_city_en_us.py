"""Content templates for en-US LocationPage city landing pages.

See docs/local-page-content-spec.md for editorial rules.
"""

from __future__ import annotations

from typing import Any


FORBIDDEN_PHRASES = (
    'visit our store',
    'come see us',
    'our local shop',
    'stop by',
    'in-store pickup',
)


def _p(text: str) -> str:
    return f'<p>{text}</p>'


def build_location_payload(
    *,
    city: str,
    state: str,
    slug: str | None = None,
    local_intro_paragraphs: list[str] | None = None,
    shipping_zones: list[str] | None = None,
    faqs: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """
    Build API/Wagtail field dict for a US city location page (en-US).

    Rich HTML fields use scaffold copy when local_intro_paragraphs / zones / faqs
    are omitted — replace with LLM-generated local content before production publish.
    """
    city = city.strip()
    state = state.strip()

    if local_intro_paragraphs is None:
        local_intro_paragraphs = [
            (
                f'Shoppers in {city}, {state} choose PlayLoveToys for body-safe vibrators, '
                f'dildos, and couples toys — delivered in plain packaging with no retail storefront.'
            ),
            (
                f'Whether you are downtown or in the suburbs, discreet shipping keeps your '
                f'order private across {city} and surrounding communities.'
            ),
            (
                'Curated for every body with inclusive language, quality-tested materials, '
                'and expert buying guides.'
            ),
        ]

    intro = ''.join(_p(paragraph) for paragraph in local_intro_paragraphs)

    zones = shipping_zones or [
        f'Downtown {city}',
        f'North {city}',
        f'South {city}',
        f'East {city}',
        f'West {city}',
        f'{city} metro suburbs',
    ]
    zones_html = ''.join(f'<li>{zone}</li>' for zone in zones)

    default_faqs = faqs or [
        {
            'question': f'Do you have a physical store in {city}?',
            'answer': (
                f'<p>No — PlayLoveToys is 100% online. We ship discreetly to {city}, {state} '
                'addresses with plain outer packaging.</p>'
            ),
        },
        {
            'question': 'How discreet is the packaging?',
            'answer': '<p>Orders arrive in plain boxes with no adult branding or product names on the outside.</p>',
        },
        {
            'question': f'How fast is shipping to {city}?',
            'answer': (
                f'<p>Most {city} orders ship within 1–2 business days. Delivery times vary by carrier '
                'and destination within the metro area.</p>'
            ),
        },
        {
            'question': 'What materials are your toys made from?',
            'answer': '<p>We prioritize medical-grade silicone and other body-safe, non-porous materials.</p>',
        },
        {
            'question': f'Can I shop for couples toys in {city}?',
            'answer': '<p>Yes — browse couples toys, vibrators, and accessories curated for shared pleasure.</p>',
        },
        {
            'question': 'Is billing discreet?',
            'answer': '<p>Yes — charges appear under a neutral merchant descriptor on your statement.</p>',
        },
        {
            'question': f'Do you ship across all of {state}?',
            'answer': f'<p>We ship throughout {state} and nationwide within the United States.</p>',
        },
        {
            'question': 'What if I need help choosing a product?',
            'answer': '<p>Explore our buying guides, glossary, and collection pages for expert recommendations.</p>',
        },
    ]

    seo_description = (
        f'Shop sex toys in {city}, {state}. Premium vibrators, dildos & couples toys '
        f'with discreet shipping. PlayLoveToys — your online adult store alternative.'
    )[:160]

    return {
        'titulo': f'Sex Toys in {city} — Premium Adult Toys Delivered Discreetly',
        'subtitulo': (
            f"{city}'s Trusted Online Adult Store for Vibrators, Dildos, "
            'Couples Toys & Sexual Wellness'
        ),
        'intro': intro,
        'country': 'United States',
        'state': state,
        'city': city,
        'titulo_2': f"The Best Adult Toys for {city}'s Shoppers",
        'subtitulo_h2': f'Vibrators, dildos & couples toys — delivered across {city}',
        'content_2': (
            _p(
                f'Explore bestselling vibrators, dildos, and couples toys selected for {city} lifestyles — '
                'from compact travel-friendly picks to premium silicone collections.'
            )
            + '<ul>'
            '<li>Body-safe medical-grade silicone</li>'
            '<li>Discreet billing and packaging</li>'
            f'<li>Fast shipping across {city} and {state}</li>'
            '<li>Inclusive sizing and expert guides</li>'
            '<li>Curated bestsellers updated regularly</li>'
            '</ul>'
        ),
        'titulo_3': f'Why an Online Adult Store Is the Smarter Choice in {city}',
        'subtitulo_3': 'Privacy, selection, and shopping from home',
        'content_3': (
            _p(
                f'Skip crowded errands — shop from home with total privacy. An online adult store '
                f'beats brick-and-mortar for selection, reviews, and discreet fulfillment in {city}.'
            )
            + _p(
                f'PlayLoveToys ships to addresses throughout {city} and the wider {state} area '
                'with no showroom visits required.'
            )
        ),
        'brand_section_title': f"PlayLoveToys — {city}'s Trusted Online Adult Store",
        'brand_section_subtitle': 'Premium sex toys. Discreet shipping. Total privacy.',
        'brand_section_content': (
            _p(
                f'We serve {city} and all of {state} from our online fulfillment network — '
                'no physical adult boutique, no awkward in-person purchases.'
            )
            + _p('Every order is packed with care and shipped in unmarked outer boxes.')
            + '<ul>'
            '<li><em>Discreet plain packaging</em></li>'
            '<li><em>Body-safe curated products</em></li>'
            '<li><em>Inclusive shopping for every body</em></li>'
            '<li><em>Secure encrypted checkout</em></li>'
            '</ul>'
        ),
        'map_title': f'Shipping Sex Toys Across {city}',
        'map_content': (
            _p(f'We deliver to neighborhoods and communities across {city} and the surrounding area.')
            + f'<ul>{zones_html}</ul>'
            + _p('Every order ships in plain, unmarked packaging — no adult branding on the outside.')
        ),
        'after_page_content': '',
        'seo_title': f'Sex Toys in {city} | Adult Toys, Vibrators & Dildos | PlayLoveToys',
        'search_description': seo_description,
        'shopify_locale': 'en-US',
        'locale': 'en-US',
        'sync_enabled': True,
        'faqs': default_faqs,
        'slug': slug,
    }


def find_forbidden_phrases(text: str) -> list[str]:
    """Return forbidden phrase substrings found in text (case-insensitive)."""
    if not text:
        return []
    lowered = text.lower()
    return [phrase for phrase in FORBIDDEN_PHRASES if phrase in lowered]
