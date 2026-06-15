"""
Locale resolution and translation linking for the content API.

Supports market-locale variants: en-US, es-US, en-CA, fr-CA.
"""

from typing import Optional, Type, TypeVar

from ninja.errors import HttpError
from wagtail.models import Locale, Page

ALLOWED_LOCALE_CODES = ('en-US', 'es-US', 'en-CA', 'fr-CA')

LOCALE_FIELD_DESCRIPTION = (
    "Wagtail locale code for this page variant. "
    "Allowed: 'en-US' (English, US), 'es-US' (Spanish, US), "
    "'en-CA' (English, Canada), 'fr-CA' (French, Canada). "
    "Defaults to the site default locale (en-US) when omitted on create."
)

TRANSLATION_OF_FIELD_DESCRIPTION = (
    "Wagtail page ID of an existing variant to link as a translation sibling. "
    "The new/updated page must use a different locale than the source page. "
    "Copies translation_key for hreflang grouping; inherits shopify_id from the "
    "source when the page has no shopify_id set."
)

PageModel = TypeVar('PageModel', bound=Page)


def resolve_locale(language_code: Optional[str]) -> Locale:
    """Return a Locale instance; default locale when language_code is omitted."""
    if language_code is None:
        return Locale.get_default()

    if language_code not in ALLOWED_LOCALE_CODES:
        raise HttpError(
            400,
            f"Invalid locale '{language_code}'. "
            f"Allowed values: {', '.join(ALLOWED_LOCALE_CODES)}.",
        )

    try:
        return Locale.objects.get(language_code=language_code)
    except Locale.DoesNotExist:
        raise HttpError(
            400,
            f"Locale '{language_code}' is not configured. "
            "Run: python manage.py setup_locales",
        )


def apply_locale(page: Page, language_code: Optional[str]) -> None:
    """Set page.locale from an optional language code."""
    if language_code is None:
        return
    page.locale = resolve_locale(language_code)


def apply_translation_link(
    page: Page,
    translation_of_id: Optional[int],
    model_class: Type[PageModel],
) -> Optional[PageModel]:
    """
    Link page to an existing variant via shared translation_key.

    Returns the source page when linked (for shopify_id inheritance), else None.
    """
    if translation_of_id is None:
        return None

    try:
        source = model_class.objects.select_related('locale').get(pk=translation_of_id)
    except model_class.DoesNotExist:
        raise HttpError(
            404,
            f"translation_of page {translation_of_id} not found.",
        )

    target_locale = page.locale or Locale.get_default()
    if source.locale_id == target_locale.id:
        raise HttpError(
            400,
            "translation_of must reference a page in a different locale than this page.",
        )

    conflict = (
        model_class.objects.filter(
            translation_key=source.translation_key,
            locale=target_locale,
        )
        .exclude(pk=page.pk or None)
        .exists()
    )
    if conflict:
        raise HttpError(
            400,
            f"A {model_class._meta.verbose_name} already exists for locale "
            f"'{target_locale.language_code}' in this translation group.",
        )

    page.translation_key = source.translation_key
    return source


def inherit_shopify_id_from_source(page: Page, source: Optional[Page]) -> None:
    """Copy shopify_id from translation source when target has none."""
    if source and not page.shopify_id and source.shopify_id:
        page.shopify_id = source.shopify_id


def resolve_translation_page_ids(obj: Page) -> list[int]:
    """Return all page IDs in the same translation group, including this page."""
    try:
        return list(
            obj.get_translations(inclusive=True)
            .order_by('locale__language_code')
            .values_list('pk', flat=True)
        )
    except Exception:
        return [obj.pk]


def filter_queryset_by_locale(qs, locale_code: Optional[str]):
    """Filter a page queryset by locale code; return empty queryset if locale is invalid."""
    if not locale_code:
        return qs
    try:
        return qs.filter(locale=resolve_locale(locale_code))
    except HttpError:
        return qs.none()
