"""
Search router — GET /api/v1/search/

Capability: discover — articles/products/collections/blogs/locations/glossary
Cross-resource full-text search with optional resource/locale/live filters.
"""
from typing import Any, Dict, List, Optional

from django.utils import timezone
from ninja import Router, Schema
from pydantic import Field

from ..auth import ApiKeyAuth
from ..openapi_agent import agent_openapi_extra, capability_docstring

router = Router()

RESOURCE_MODEL_MAP = {
    "articles": "shopify_content.ArticlePage",
    "products": "shopify_content.ProductPage",
    "collections": "shopify_content.CollectionPage",
    "blogs": "shopify_content.BlogPage",
    "locations": "shopify_content.LocationPage",
    "glossary": "shopify_content.GlossaryTermPage",
}

# Fields to search per resource (for icontains fallback)
SEARCH_FIELDS: dict[str, list[str]] = {
    "articles": ["title", "seo_title", "search_description"],
    "products": ["title", "seo_title", "search_description"],
    "collections": ["title", "seo_title", "search_description"],
    "blogs": ["title", "seo_title", "search_description"],
    "locations": ["title", "seo_title", "search_description"],
    "glossary": ["title", "term", "definition"],
}

# Body fields to extract excerpts from (may be RichTextField or StreamField)
EXCERPT_FIELDS: dict[str, list[str]] = {
    "articles": ["body", "summary"],
    "products": ["body_content"],
    "collections": ["body_content"],
    "blogs": ["description"],
    "locations": [],
    "glossary": ["definition"],
}


class SearchResultItem(Schema):
    resource: str = Field(..., description="Resource type: article, product, collection, blog, location, glossary")
    page_id: int = Field(..., description="Wagtail page primary key")
    title: str
    slug: str
    locale: str
    live: bool
    url: Optional[str] = Field(None, description="Full public URL, null if site not configured")
    excerpt: str = Field("", description="~160 chars around first match of the search term")
    last_modified: Optional[str] = Field(None, description="ISO 8601 last_published_at or first_published_at")


class SearchResponse(Schema):
    total: int
    results: List[SearchResultItem]


def _get_model(resource_key: str):
    from django.apps import apps
    return apps.get_model(RESOURCE_MODEL_MAP[resource_key])


def _extract_text(page, resource_key: str) -> str:
    """Return plain text from body/rich-text fields for excerpt extraction."""
    parts: list[str] = []
    for field_name in EXCERPT_FIELDS.get(resource_key, []):
        val = getattr(page, field_name, None)
        if val is None:
            continue
        text = str(val)
        # Strip HTML tags simply without importing bs4 at module level
        if "<" in text and ">" in text:
            try:
                from bs4 import BeautifulSoup
                text = BeautifulSoup(text, "html.parser").get_text(" ", strip=True)
            except Exception:
                pass
        parts.append(text)
    return " ".join(parts)


def _make_excerpt(full_text: str, query: str, length: int = 160) -> str:
    """Return a ~160-char excerpt centred on the first occurrence of query."""
    if not full_text:
        return ""
    lower_text = full_text.lower()
    lower_query = query.lower()
    pos = lower_text.find(lower_query)
    if pos == -1:
        return full_text[:length]
    start = max(0, pos - length // 2)
    end = min(len(full_text), start + length)
    return ("..." if start > 0 else "") + full_text[start:end] + ("..." if end < len(full_text) else "")


def _page_to_item(page, resource_key: str, query: str) -> SearchResultItem:
    try:
        url = page.get_full_url()
    except Exception:
        url = None

    locale_str = str(page.locale) if hasattr(page, "locale") else ""
    last_modified = None
    if getattr(page, "last_published_at", None):
        last_modified = page.last_published_at.isoformat()
    elif getattr(page, "first_published_at", None):
        last_modified = page.first_published_at.isoformat()

    body_text = _extract_text(page, resource_key)
    excerpt = _make_excerpt(body_text, query)

    return SearchResultItem(
        resource=resource_key.rstrip("s"),  # "articles" → "article"
        page_id=page.pk,
        title=page.title,
        slug=page.slug,
        locale=locale_str,
        live=page.live,
        url=url,
        excerpt=excerpt,
        last_modified=last_modified,
    )


def _search_resource(resource_key: str, q: str, locale: Optional[str], live: bool) -> list:
    model = _get_model(resource_key)
    qs = model.objects.select_related("locale")
    if live:
        qs = qs.live()
    if locale:
        qs = qs.filter(locale__language_code=locale)

    # Try Wagtail search backend first
    try:
        from wagtail.search.backends import get_search_backend
        backend = get_search_backend()
        results = list(backend.search(q, qs))
        return results
    except Exception:
        pass

    # Fallback: icontains on indexed fields
    from django.db.models import Q
    q_obj = Q()
    for field in SEARCH_FIELDS.get(resource_key, ["title"]):
        q_obj |= Q(**{f"{field}__icontains": q})
    return list(qs.filter(q_obj))


@router.get(
    "/",
    response=SearchResponse,
    summary="Search Content",
    operation_id="search_content",
    description=capability_docstring("search_content"),
    openapi_extra=agent_openapi_extra("search_content"),
)
def search_content(
    request,
    q: str,
    resource: Optional[str] = None,
    locale: Optional[str] = None,
    live: bool = True,
    limit: int = 20,
    offset: int = 0,
):
    """
    Capability: discover — articles
    Full-text cross-resource search. Use before building internal links or to locate pages for editing.
    """
    limit = min(limit, 100)
    resources = [resource] if resource and resource in RESOURCE_MODEL_MAP else list(RESOURCE_MODEL_MAP.keys())

    all_items: list[SearchResultItem] = []
    for res_key in resources:
        try:
            pages = _search_resource(res_key, q, locale, live)
            for page in pages:
                all_items.append(_page_to_item(page, res_key, q))
        except Exception:
            continue

    total = len(all_items)
    page_slice = all_items[offset: offset + limit]
    return SearchResponse(total=total, results=page_slice)
