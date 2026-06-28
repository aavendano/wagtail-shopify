"""
Versioning router — article revision endpoints.

GET  /api/v1/articles/{page_id}/versions/
GET  /api/v1/articles/{page_id}/versions/{revision_id}/
POST /api/v1/articles/{page_id}/revert/{revision_id}/
"""
from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from pydantic import Field

from shopify_content.models import ArticlePage
from ..schemas.article import ArticleOut
from ..schemas.common import ErrorSchema
from ..openapi_agent import agent_openapi_extra, capability_docstring

router = Router()


class RevisionItem(Schema):
    revision_id: int = Field(..., description="Wagtail revision primary key")
    created_at: str = Field(..., description="ISO 8601 timestamp when the revision was created")
    user: Optional[str] = Field(None, description="Username of the editor who created the revision")
    is_latest: bool = Field(..., description="True if this is the most recent revision")


@router.get(
    "/{page_id}/versions/",
    response={200: List[RevisionItem], 404: ErrorSchema},
    summary="List Article Versions",
    operation_id="list_article_versions",
    description=capability_docstring("list_article_versions"),
    openapi_extra=agent_openapi_extra("list_article_versions"),
)
def list_article_versions(request, page_id: int):
    """Capability: read — articles — List Wagtail revisions for an article."""
    try:
        page = ArticlePage.objects.get(pk=page_id)
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}

    revisions = page.revisions.order_by("-created_at").select_related("user")
    if not revisions.exists():
        return 200, []

    latest_id = revisions.first().pk
    items = []
    for rev in revisions:
        items.append(RevisionItem(
            revision_id=rev.pk,
            created_at=rev.created_at.isoformat(),
            user=rev.user.username if rev.user else None,
            is_latest=(rev.pk == latest_id),
        ))
    return 200, items


@router.get(
    "/{page_id}/versions/{revision_id}/",
    response={200: ArticleOut, 404: ErrorSchema},
    summary="Get Article Version",
    operation_id="get_article_version",
    description=capability_docstring("get_article_version"),
    openapi_extra=agent_openapi_extra("get_article_version"),
)
def get_article_version(request, page_id: int, revision_id: int):
    """Capability: read — articles — Return content of a specific revision."""
    try:
        page = ArticlePage.objects.get(pk=page_id)
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}

    try:
        revision = page.revisions.get(pk=revision_id)
    except page.revisions.model.DoesNotExist:
        return 404, {"detail": f"Revision {revision_id} not found for article {page_id}."}

    restored = revision.as_object()
    # Ensure the restored instance has PKs for related lookups
    restored.pk = page.pk
    restored.id = page.id
    return 200, restored


@router.post(
    "/{page_id}/revert/{revision_id}/",
    response={200: ArticleOut, 404: ErrorSchema, 400: ErrorSchema},
    summary="Revert Article to Version",
    operation_id="revert_article_version",
    description=capability_docstring("revert_article_version"),
    openapi_extra=agent_openapi_extra("revert_article_version"),
)
def revert_article_version(request, page_id: int, revision_id: int):
    """Capability: update — articles — Restore a past revision as current draft (does not publish)."""
    try:
        page = ArticlePage.objects.get(pk=page_id)
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}

    try:
        revision = page.revisions.get(pk=revision_id)
    except page.revisions.model.DoesNotExist:
        return 404, {"detail": f"Revision {revision_id} not found for article {page_id}."}

    try:
        restored = revision.as_object()
        restored.pk = page.pk
        restored.id = page.id
        restored.save_revision()
    except Exception as exc:
        return 400, {"detail": f"Revert failed: {exc}"}

    result = (
        ArticlePage.objects
        .select_related("locale", "featured_image")
        .prefetch_related("metafields", "tagged_items__tag")
        .get(pk=page_id)
    )
    return 200, result
