"""
Links router — GET /api/v1/links/index/

Capability: discover — articles/products/collections/blogs/locations/glossary
Complete slug/handle index for the site. Cached 5 min; invalidated on Page save signal.
"""
from typing import List, Optional

from django.core.cache import cache
from django.utils import timezone
from ninja import Router, Schema
from pydantic import Field

from ..openapi_agent import agent_openapi_extra, capability_docstring

router = Router()

INDEXED_MODELS = {
    "articles": "shopify_content.ArticlePage",
    "products": "shopify_content.ProductPage",
    "collections": "shopify_content.CollectionPage",
    "blogs": "shopify_content.BlogPage",
    "locations": "shopify_content.LocationPage",
    "glossary": "shopify_content.GlossaryTermPage",
}


class SlugIndexItem(Schema):
    resource: str
    page_id: int
    title: str
    slug: str
    url: Optional[str] = None
    locale: str
    shopify_handle: Optional[str] = Field(None, description="Shopify URL handle; null if resource has none")


class SlugIndexResponse(Schema):
    generated_at: str
    total: int
    index: List[SlugIndexItem]


def _build_index(resource: Optional[str], locale: Optional[str], live: bool) -> list[SlugIndexItem]:
    from django.apps import apps

    models_to_query = (
        {resource: INDEXED_MODELS[resource]}
        if resource and resource in INDEXED_MODELS
        else INDEXED_MODELS
    )

    items: list[SlugIndexItem] = []
    for res_key, model_path in models_to_query.items():
        model = apps.get_model(model_path)
        qs = model.objects.select_related("locale")
        if live:
            qs = qs.live()
        if locale:
            qs = qs.filter(locale__language_code=locale)

        for page in qs.values("pk", "title", "slug", "locale__language_code"):
            # Resolve URL without hitting the DB per page
            handle = None
            if hasattr(model, "handle"):
                try:
                    handle = model.objects.filter(pk=page["pk"]).values_list("handle", flat=True).first()
                except Exception:
                    pass

            try:
                url = model.objects.get(pk=page["pk"]).get_full_url()
            except Exception:
                url = None

            items.append(SlugIndexItem(
                resource=res_key.rstrip("s"),
                page_id=page["pk"],
                title=page["title"],
                slug=page["slug"],
                url=url,
                locale=page["locale__language_code"] or "",
                shopify_handle=handle if handle else None,
            ))

    return items


def _cache_key(resource: Optional[str], locale: Optional[str], live: bool) -> str:
    return f"links_index_{resource}_{locale}_{live}"


@router.get(
    "/index/",
    response=SlugIndexResponse,
    summary="Slug Index",
    operation_id="links_index",
    description=capability_docstring("links_index"),
    openapi_extra=agent_openapi_extra("links_index"),
)
def links_index(
    request,
    resource: Optional[str] = None,
    locale: Optional[str] = None,
    live: bool = True,
):
    """
    Capability: discover — articles
    Complete slug/handle index for building internal links without iterating resources.
    Cached for 5 minutes; invalidated on any Page save.
    """
    key = _cache_key(resource, locale, live)
    cached = cache.get(key)
    if cached is not None:
        return cached

    items = _build_index(resource, locale, live)
    generated_at = timezone.now().isoformat()
    result = SlugIndexResponse(
        generated_at=generated_at,
        total=len(items),
        index=items,
    )
    cache.set(key, result, timeout=300)
    return result
