"""HomePage editor locale handling for Wagtail page chooser browse/search."""

from __future__ import annotations

import logging
from contextvars import ContextVar

from django.db.models import Q
from django.db.models.query import QuerySet
from wagtail.models import Locale, Page

logger = logging.getLogger(__name__)

_chooser_browse_locale_override: ContextVar[Locale | None] = ContextVar(
    'chooser_browse_locale_override',
    default=None,
)
_include_glossary_root_in_browse: ContextVar[bool] = ContextVar(
    'include_glossary_root_in_browse',
    default=False,
)
_original_queryset_filter = None


def get_homepage_editor_locale(request):
    """Locale of the HomePage being edited (not Wagtail chooser UI ``locale`` param)."""
    code = request.GET.get('homepage_locale')
    if not code and hasattr(request, 'session'):
        code = request.session.get('homepage_locale')
    if not code:
        return None
    try:
        return Locale.objects.get(language_code=code)
    except Locale.DoesNotExist:
        return None


def _desired_includes_glossary(request) -> bool:
    page_type_string = request.GET.get('page_type') or ''
    if not page_type_string:
        return False
    return 'glossarytermpage' in page_type_string.lower()


def _is_glossary_container_page(page) -> bool:
    from shopify_content.models import ShopifyRootPage

    try:
        specific = page.specific
    except Exception:
        specific = page
    return isinstance(specific, ShopifyRootPage) and page.slug == 'glossary'


def _parent_page_id_from_chooser_request(request) -> int | None:
    if request.resolver_match is None:
        return None
    raw = request.resolver_match.kwargs.get('parent_page_id')
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _is_chooser_root_browse(request) -> bool:
    return _parent_page_id_from_chooser_request(request) is None


def maybe_include_glossary_root_at_chooser_root(request) -> None:
    """
    Glossary lives under en-US PlayLoveToys; es-US tree has no glossary folder.
    When browsing the chooser root with ``homepage_locale``, keep the folder visible.
    """
    if not _is_chooser_root_browse(request):
        return
    editor_locale = get_homepage_editor_locale(request)
    if editor_locale is None or not _desired_includes_glossary(request):
        return
    _include_glossary_root_in_browse.set(True)


def maybe_set_glossary_browse_locale_override(request) -> None:
    """
    When browsing the shared ``glossary`` folder during HomePage edit, Wagtail
    filters children by the folder locale (en-US). Override once so children
    match the editor locale (e.g. es-US).
    """
    editor_locale = get_homepage_editor_locale(request)
    if editor_locale is None or not _desired_includes_glossary(request):
        return

    parent_page_id = _parent_page_id_from_chooser_request(request)
    if parent_page_id is None:
        return

    try:
        parent_page = Page.objects.get(pk=parent_page_id)
    except Page.DoesNotExist:
        return

    if not _is_glossary_container_page(parent_page):
        return

    _chooser_browse_locale_override.set(editor_locale)


def glossary_term_page_filter_q(editor_locale: Locale, glossary_ct) -> Q:
    """Filter GlossaryTermPage by Wagtail locale (search-index safe)."""
    return Q(content_type=glossary_ct, locale_id=editor_locale.pk) | ~Q(content_type=glossary_ct)


def _glossary_root_page_ids() -> list[int]:
    from shopify_content.models import ShopifyRootPage

    return list(
        Page.objects.type(ShopifyRootPage).filter(slug='glossary').values_list('pk', flat=True)
    )


def _patched_queryset_filter(self, *args, **kwargs):
    if len(kwargs) == 1 and 'locale' in kwargs and not args:
        include_glossary = _include_glossary_root_in_browse.get()
        if include_glossary:
            _include_glossary_root_in_browse.set(False)
            locale_val = kwargs['locale']
            glossary_pks = _glossary_root_page_ids()
            if glossary_pks:
                return _original_queryset_filter(
                    self,
                    Q(locale=locale_val) | Q(pk__in=glossary_pks),
                )

        override = _chooser_browse_locale_override.get()
        if override is not None:
            _chooser_browse_locale_override.set(None)
            kwargs = {'locale': override}

    return _original_queryset_filter(self, *args, **kwargs)


def install_page_chooser_browse_locale_fix():
    """Patch QuerySet.filter so glossary browse respects ``homepage_locale``."""
    global _original_queryset_filter

    if _original_queryset_filter is not None:
        return

    _original_queryset_filter = QuerySet.filter
    QuerySet.filter = _patched_queryset_filter
