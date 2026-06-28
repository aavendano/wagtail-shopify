"""
Bulk router — POST /api/v1/bulk/update/

Capability: update — articles/products/collections/blogs/locations/glossary
Update up to 50 pages in a single call; each operation runs in its own atomic transaction.
"""
from typing import Any, Dict, List, Optional

from django.db import transaction
from ninja import Router, Schema
from pydantic import Field

from ..openapi_agent import agent_openapi_extra, capability_docstring

router = Router()

RESOURCE_MODEL_MAP = {
    "article": "shopify_content.ArticlePage",
    "product": "shopify_content.ProductPage",
    "collection": "shopify_content.CollectionPage",
    "blog": "shopify_content.BlogPage",
    "location": "shopify_content.LocationPage",
    "glossary": "shopify_content.GlossaryTermPage",
}

RESOURCE_PATCH_MAP = {
    "article": ("api.routers.articles", "update_article"),
    "product": ("api.routers.products", "update_product"),
    "collection": ("api.routers.collections", "update_collection"),
    "blog": ("api.routers.blogs", "update_blog"),
    "location": ("api.routers.locations", "update_location"),
    "glossary": ("api.routers.glossary", "update_glossary_term"),
}


class BulkOperation(Schema):
    resource: str = Field(
        ...,
        description="Resource type: article | product | collection | blog | location | glossary",
    )
    page_id: int = Field(..., description="Wagtail page primary key to update")
    fields: Dict[str, Any] = Field(
        ...,
        description="Fields to update (same schema as PATCH for each resource)",
    )
    publish: bool = Field(False, description="When true, publish after saving")


class BulkUpdateRequest(Schema):
    operations: List[BulkOperation] = Field(
        ...,
        description="List of update operations; max 50",
    )


class BulkOperationResult(Schema):
    page_id: int
    resource: str
    status: str = Field(..., description="ok | error")
    error: Optional[str] = Field(None, description="Error detail if status=error")


class BulkUpdateResponse(Schema):
    total: int
    succeeded: int
    failed: int
    results: List[BulkOperationResult]


def _apply_operation(operation: BulkOperation) -> BulkOperationResult:
    """Apply a single bulk operation inside its own atomic transaction."""
    resource = operation.resource
    if resource not in RESOURCE_MODEL_MAP:
        return BulkOperationResult(
            page_id=operation.page_id,
            resource=resource,
            status="error",
            error=f"Unknown resource type: {resource!r}",
        )

    from django.apps import apps
    model = apps.get_model(RESOURCE_MODEL_MAP[resource])

    try:
        with transaction.atomic():
            try:
                page = model.objects.get(pk=operation.page_id)
            except model.DoesNotExist:
                return BulkOperationResult(
                    page_id=operation.page_id,
                    resource=resource,
                    status="error",
                    error=f"{resource} page {operation.page_id} not found.",
                )

            # Apply each field using setattr (same logic as individual PATCH)
            fields = operation.fields
            _apply_fields(page, resource, fields)

            if operation.publish:
                revision = page.save_revision()
                revision.publish()
            else:
                page.save()

        return BulkOperationResult(
            page_id=operation.page_id,
            resource=resource,
            status="ok",
            error=None,
        )
    except Exception as exc:
        return BulkOperationResult(
            page_id=operation.page_id,
            resource=resource,
            status="error",
            error=str(exc),
        )


# Simple field application — covers the common scalar fields shared by all models.
# Complex fields (tags, metafields, body) are handled with type-specific logic.
_COMMON_FIELDS = [
    "title", "shopify_id", "handle", "slug", "seo_title", "search_description",
    "sync_enabled", "author", "summary", "published_at", "vendor", "product_type",
    "status", "titulo", "city", "country", "term", "definition", "locale_code",
    "description", "comment_policy",
]


def _apply_fields(page, resource: str, fields: dict) -> None:
    from django.utils.text import slugify
    from api.locale_utils import resolve_locale

    for field_name, value in fields.items():
        if field_name == "locale":
            page.locale = resolve_locale(value)
        elif field_name == "handle":
            page.handle = value
            page.slug = slugify(value)
        elif field_name == "tags":
            if hasattr(page, "tags"):
                page.tags.set(value)
        elif field_name == "metafields":
            if hasattr(page, "metafields"):
                page.metafields.all().delete()
                _create_metafields(page, resource, value)
        elif field_name == "body":
            import json
            page.body = json.dumps(value)
        elif field_name in _COMMON_FIELDS:
            setattr(page, field_name, value)
        # Silently skip unknown fields rather than erroring on the whole op


def _create_metafields(page, resource: str, metafields_data: list) -> None:
    from django.apps import apps
    metafield_models = {
        "article": "shopify_content.ArticlePageMetafield",
        "product": "shopify_content.ProductPageMetafield",
        "collection": "shopify_content.CollectionPageMetafield",
    }
    if resource not in metafield_models:
        return
    model = apps.get_model(metafield_models[resource])
    for mf in metafields_data:
        model.objects.create(
            page=page,
            namespace=mf.get("namespace", "custom"),
            key=mf["key"],
            type=mf.get("type", "single_line_text_field"),
            value=mf["value"],
        )


@router.post(
    "/update/",
    response={200: BulkUpdateResponse, 400: dict},
    summary="Bulk Update Pages",
    operation_id="bulk_update",
    description=capability_docstring("bulk_update"),
    openapi_extra=agent_openapi_extra("bulk_update"),
)
def bulk_update(request, data: BulkUpdateRequest):
    """
    Capability: update — articles
    Batch-update up to 50 pages. Each operation is independent; a failure in one does not stop others.
    """
    if len(data.operations) > 50:
        return 400, {"detail": f"Too many operations: {len(data.operations)}. Maximum is 50."}

    results: list[BulkOperationResult] = []
    for operation in data.operations:
        results.append(_apply_operation(operation))

    succeeded = sum(1 for r in results if r.status == "ok")
    failed = sum(1 for r in results if r.status == "error")

    return 200, BulkUpdateResponse(
        total=len(results),
        succeeded=succeeded,
        failed=failed,
        results=results,
    )
