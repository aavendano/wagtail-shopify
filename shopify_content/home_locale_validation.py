"""Locale-aware validation for HomePage sections_json page references."""

from __future__ import annotations

from typing import Any, Protocol

from django.core.exceptions import ValidationError
from wagtail.models import Page

from shopify_content.glossary_locale_utils import glossary_locale_code_for_wagtail
from shopify_content.models.blog import ArticlePage
from shopify_content.models.glossary import GlossaryTermPage


class HomePageLocaleSource(Protocol):
    locale: Any
    sections_json: dict | None


def _append_page_id(target: set[int], value: Any) -> None:
    if value is None:
        return
    try:
        target.add(int(value))
    except (TypeError, ValueError):
        return


def collect_sections_page_ids(sections_json: dict | None) -> list[int]:
    """Collect all Wagtail page IDs referenced in sections_json."""
    ids: set[int] = set()
    sections = (sections_json or {}).get('sections') or []
    for section in sections:
        if not isinstance(section, dict):
            continue
        block_type = section.get('type')
        value = section.get('value') or {}
        if not isinstance(value, dict):
            continue

        if block_type == 'featured_collections':
            for item in value.get('items') or []:
                if isinstance(item, dict):
                    _append_page_id(ids, item.get('page_id'))

        elif block_type == 'best_sellers':
            _append_page_id(ids, value.get('collection_page_id'))

        elif block_type == 'shop_by_need':
            for card in value.get('cards') or []:
                if isinstance(card, dict):
                    _append_page_id(ids, card.get('target_page_id'))

        elif block_type == 'educational_hub':
            for link_item in value.get('links') or []:
                if isinstance(link_item, dict):
                    _append_page_id(ids, link_item.get('page_id'))

        elif block_type == 'internal_links':
            for group in value.get('groups') or []:
                if not isinstance(group, dict):
                    continue
                for link_item in group.get('links') or []:
                    if isinstance(link_item, dict):
                        _append_page_id(ids, link_item.get('page_id'))

        elif block_type == 'promo_gateway':
            for card in value.get('cards') or []:
                if not isinstance(card, dict):
                    continue
                _append_page_id(ids, card.get('primary_collection_page_id'))
                for category_id in card.get('category_page_ids') or []:
                    _append_page_id(ids, category_id)

    return sorted(ids)


def is_page_valid_for_home_locale(home_page: HomePageLocaleSource, page: Page) -> bool:
    """Return True when page reference is allowed for the home locale."""
    try:
        specific = page.specific
    except Exception:
        specific = page

    home_locale = home_page.locale.language_code

    if isinstance(specific, ArticlePage):
        return specific.locale.language_code == home_locale

    if isinstance(specific, GlossaryTermPage):
        expected = glossary_locale_code_for_wagtail(home_locale)
        return specific.locale_code == expected

    return True


def validate_sections_json_locale(home_page: HomePageLocaleSource) -> list[ValidationError]:
    """Validate that locale-sensitive references match the HomePage locale."""
    page_ids = collect_sections_page_ids(home_page.sections_json)
    if not page_ids:
        return []

    pages = {
        page.pk: page
        for page in Page.objects.filter(pk__in=page_ids).select_related('locale')
    }

    errors: list[ValidationError] = []
    home_locale = home_page.locale.language_code

    for page_id in page_ids:
        page = pages.get(page_id)
        if page is None:
            errors.append(
                ValidationError(
                    f'sections_json references unknown page_id={page_id}.',
                    code='invalid_page_reference',
                )
            )
            continue

        if is_page_valid_for_home_locale(home_page, page):
            continue

        try:
            specific = page.specific
        except Exception:
            specific = page

        if isinstance(specific, ArticlePage):
            errors.append(
                ValidationError(
                    (
                        f'Article page_id={page_id} has locale '
                        f'{specific.locale.language_code}; HomePage locale is {home_locale}.'
                    ),
                    code='locale_mismatch',
                )
            )
        elif isinstance(specific, GlossaryTermPage):
            expected = glossary_locale_code_for_wagtail(home_locale)
            errors.append(
                ValidationError(
                    (
                        f'Glossary term page_id={page_id} has locale_code '
                        f'{specific.locale_code}; expected {expected} for HomePage {home_locale}.'
                    ),
                    code='locale_mismatch',
                )
            )

    return errors
