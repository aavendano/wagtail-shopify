"""Apply editor-curated related_links as typed semantic FK rows (is_auto=False)."""

from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError
from wagtail.models import Page

from shopify_content.models.blog import ArticlePage, BlogPage
from shopify_content.models.collection import CollectionPage
from shopify_content.models.glossary import GlossaryTermPage
from shopify_content.models.product import ProductPage
from shopify_content.models.semantic_links import (
    get_typed_link_model,
    iter_typed_link_models_for_page,
    relation_for_page_type,
)
from shopify_content.semantic_links.serialization import serialize_semantic_links
from shopify_content.semantic_links.service import (
    page_type_key_for,
    persist_semantic_links_revision,
)

# RelatedLinkSchema.type → page_type_key_for / TYPE_TO_RELATION key
_LINK_TYPE_TO_PAGE_TYPE = {
    'product': 'product',
    'collection': 'collection',
    'article': 'article',
    'metaobject': 'glossary',
}

_SUPPORTED_LINK_TYPES = frozenset(_LINK_TYPE_TO_PAGE_TYPE)


def _as_link_dict(link: Any) -> dict[str, Any]:
    if hasattr(link, 'model_dump'):
        return link.model_dump(exclude_none=True)
    if hasattr(link, 'dict'):
        return link.dict(exclude_none=True)
    return dict(link)


def resolve_related_link_target(link: dict[str, Any], *, locale_id: int) -> Page | None:
    """
    Resolve a RelatedLinkSchema-compatible dict to a Wagtail Page in the given locale.

    Returns None when type/handle are missing or no matching page exists.
    Raises ValidationError for unsupported link types (blog, page, …).
    """
    link_type = link.get('type')
    handle = link.get('handle')
    if not link_type or not handle:
        return None

    if link_type not in _SUPPORTED_LINK_TYPES:
        raise ValidationError(
            f"Unsupported related_links type '{link_type}'. "
            f"Supported: {', '.join(sorted(_SUPPORTED_LINK_TYPES))}."
        )

    if link_type == 'product':
        qs = ProductPage.objects.filter(handle=handle, locale_id=locale_id)
    elif link_type == 'collection':
        qs = CollectionPage.objects.filter(handle=handle, locale_id=locale_id)
    elif link_type == 'article':
        blog_handle = link.get('blog_handle')
        if not blog_handle:
            return None
        try:
            blog = BlogPage.objects.get(handle=blog_handle, locale_id=locale_id)
        except BlogPage.DoesNotExist:
            return None
        qs = ArticlePage.objects.filter(
            handle=handle,
            locale_id=locale_id,
        ).descendant_of(blog)
    elif link_type == 'metaobject':
        qs = GlossaryTermPage.objects.filter(handle=handle, locale_id=locale_id)
    else:
        return None

    page = qs.first()
    if page is None:
        return None
    return Page.objects.get(pk=page.pk)


def apply_manual_related_links(
    page,
    links: list[Any] | None,
    *,
    persist_revision: bool = True,
) -> dict[str, int]:
    """
    Replace is_auto=False semantic links from RelatedLinkSchema-compatible payloads.

    Keeps is_auto=True rows. For GlossaryTermPage, rewrites related_links JSON as a
    cache of all typed FKs (manual + auto).

    Raises ValidationError if any link cannot be resolved or is unsupported.
    """
    if page.pk is None:
        raise ValidationError('Page must be saved before applying related_links.')

    specific = page.specific if isinstance(page, Page) else page
    normalized = [_as_link_dict(link) for link in (links or [])]

    resolved: list[tuple[Page, str]] = []
    errors: list[str] = []
    seen_pks: set[int] = set()

    for index, link in enumerate(normalized):
        try:
            target = resolve_related_link_target(link, locale_id=specific.locale_id)
        except ValidationError as exc:
            messages = exc.messages if hasattr(exc, 'messages') else [str(exc)]
            for message in messages:
                errors.append(f'related_links[{index}]: {message}')
            continue

        if target is None:
            errors.append(
                f'related_links[{index}]: could not resolve '
                f"type={link.get('type')!r} handle={link.get('handle')!r}"
                + (
                    f" blog_handle={link.get('blog_handle')!r}"
                    if link.get('type') == 'article'
                    else ''
                )
            )
            continue

        if target.pk == specific.pk:
            errors.append(f'related_links[{index}]: cannot link a page to itself')
            continue

        type_key = page_type_key_for(target)
        expected = _LINK_TYPE_TO_PAGE_TYPE.get(link.get('type'))
        if type_key is None or (expected and type_key != expected):
            errors.append(
                f'related_links[{index}]: resolved page is not a valid '
                f"{link.get('type')} target"
            )
            continue

        if target.pk in seen_pks:
            continue
        seen_pks.add(target.pk)
        resolved.append((target, type_key))

    if errors:
        raise ValidationError(errors)

    for _relation_name, model_cls in iter_typed_link_models_for_page(specific):
        model_cls.objects.filter(page_id=specific.pk, is_auto=False).delete()

    created = 0
    sort_cursors: dict[str, int] = {}
    for target, type_key in resolved:
        relation_name = relation_for_page_type(type_key)
        model_cls = get_typed_link_model(specific, relation_name)
        if relation_name not in sort_cursors:
            max_sort = (
                model_cls.objects.filter(page_id=specific.pk)
                .order_by('-sort_order')
                .values_list('sort_order', flat=True)
                .first()
            )
            sort_cursors[relation_name] = (max_sort + 1) if max_sort is not None else 0

        model_cls.objects.create(
            page_id=specific.pk,
            related_page=target,
            is_auto=False,
            sort_order=sort_cursors[relation_name],
        )
        sort_cursors[relation_name] += 1
        created += 1

    specific = type(specific).objects.get(pk=specific.pk)
    if isinstance(specific, GlossaryTermPage):
        related_links = serialize_semantic_links(specific)
        type(specific).objects.filter(pk=specific.pk).update(related_links=related_links)
        specific.related_links = related_links
        page.related_links = related_links

    if persist_revision:
        persist_semantic_links_revision(specific, skip_publish_signals=True)

    return {'created': created, 'manual_count': len(resolved)}
