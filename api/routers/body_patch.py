"""
Body patch router — POST /api/v1/articles/{page_id}/body/patch/

Capability: update — articles
Structured body editing: insert_after, insert_before, replace, delete, append.
Works with both Wagtail StreamField and RichTextField bodies.
"""
import json
from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from pydantic import Field

from shopify_content.models import ArticlePage
from ..schemas.article import ArticleOut
from ..schemas.common import ErrorSchema
from ..openapi_agent import agent_openapi_extra, capability_docstring

router = Router()


class BodyOperation(Schema):
    op: str = Field(
        ...,
        description="Operation type: insert_after | insert_before | replace | delete | append",
    )
    target: Optional[str] = Field(
        None,
        description=(
            "Selector for the target block/element. "
            "Formats: 'h2:Exact heading text', 'h3:Exact heading text', "
            "'block_index:N' (0-based StreamField index), 'append' (for op=append). "
            "Required for all ops except append."
        ),
    )
    content: Optional[str] = Field(
        None,
        description="HTML string for insert/replace ops. Null for delete.",
    )


class BodyPatchRequest(Schema):
    operations: List[BodyOperation] = Field(..., description="Ordered list of body operations to apply")
    publish: bool = Field(False, description="When true, publish the article after patching")


# ---------------------------------------------------------------------------
# StreamField helpers
# ---------------------------------------------------------------------------

def _stream_find_target(blocks: list, target: str) -> int:
    """Return 0-based index of the matching block or -1."""
    if target.startswith("block_index:"):
        try:
            return int(target.split(":", 1)[1])
        except ValueError:
            return -1

    tag, _, text = target.partition(":")
    tag = tag.lower()
    for i, block in enumerate(blocks):
        block_type = block.get("type", "").lower()
        value = block.get("value", "")
        if isinstance(value, str):
            if block_type == tag and value.strip() == text.strip():
                return i
        elif isinstance(value, dict):
            inner = value.get("text", value.get("value", ""))
            if block_type == tag and str(inner).strip() == text.strip():
                return i
    return -1


def _html_to_stream_block(html: str) -> dict:
    """Wrap an HTML string into a StreamField rich_text block."""
    return {"type": "rich_text", "value": html}


def _apply_stream_ops(raw_blocks: list, operations: list) -> tuple[list, Optional[str]]:
    """Apply all operations to a StreamField block list.

    Returns (new_blocks, error_message). error_message is None on success.
    """
    blocks = list(raw_blocks)

    for op in operations:
        op_type = op.op
        target = op.target
        content = op.content

        if op_type == "append":
            if content is None:
                return blocks, "content is required for append operation"
            blocks.append(_html_to_stream_block(content))
            continue

        if target is None:
            return blocks, f"target is required for op={op_type!r}"

        idx = _stream_find_target(blocks, target)
        if idx == -1:
            return blocks, f"target {target!r} not found in body"

        if op_type == "insert_after":
            if content is None:
                return blocks, "content is required for insert_after"
            blocks.insert(idx + 1, _html_to_stream_block(content))
        elif op_type == "insert_before":
            if content is None:
                return blocks, "content is required for insert_before"
            blocks.insert(idx, _html_to_stream_block(content))
        elif op_type == "replace":
            if content is None:
                return blocks, "content is required for replace"
            blocks[idx] = _html_to_stream_block(content)
        elif op_type == "delete":
            blocks.pop(idx)
        else:
            return blocks, f"unknown op type: {op_type!r}"

    return blocks, None


# ---------------------------------------------------------------------------
# RichTextField (HTML) helpers
# ---------------------------------------------------------------------------

def _apply_html_ops(html: str, operations: list) -> tuple[str, Optional[str]]:
    """Apply operations to an HTML body string using BeautifulSoup4."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html or "", "html.parser")

    for op in operations:
        op_type = op.op
        target = op.target
        content = op.content

        if op_type == "append":
            if content is None:
                return str(soup), "content is required for append operation"
            new_tag = BeautifulSoup(content, "html.parser")
            for child in list(new_tag.contents):
                soup.append(child)
            continue

        if target is None:
            return str(soup), f"target is required for op={op_type!r}"

        # Find element
        element = _html_find_target(soup, target)
        if element is None:
            return str(soup), f"target {target!r} not found in body"

        if op_type == "insert_after":
            if content is None:
                return str(soup), "content is required for insert_after"
            new_nodes = BeautifulSoup(content, "html.parser")
            for child in reversed(list(new_nodes.contents)):
                element.insert_after(child)
        elif op_type == "insert_before":
            if content is None:
                return str(soup), "content is required for insert_before"
            new_nodes = BeautifulSoup(content, "html.parser")
            for child in list(new_nodes.contents):
                element.insert_before(child)
        elif op_type == "replace":
            if content is None:
                return str(soup), "content is required for replace"
            new_nodes = BeautifulSoup(content, "html.parser")
            element.replace_with(new_nodes)
        elif op_type == "delete":
            element.decompose()
        else:
            return str(soup), f"unknown op type: {op_type!r}"

    return str(soup), None


def _html_find_target(soup, target: str):
    """Find first matching element in a BeautifulSoup tree."""
    from bs4 import BeautifulSoup

    if target.startswith("block_index:"):
        try:
            idx = int(target.split(":", 1)[1])
        except ValueError:
            return None
        # Return the N-th direct block-level child
        children = [c for c in soup.children if hasattr(c, "name") and c.name]
        if idx < len(children):
            return children[idx]
        return None

    tag, _, text = target.partition(":")
    tag = tag.lower()
    for element in soup.find_all(tag):
        if element.get_text(strip=True) == text.strip():
            return element
    return None


# ---------------------------------------------------------------------------
# View
# ---------------------------------------------------------------------------

@router.post(
    "/{page_id}/body/patch/",
    response={200: ArticleOut, 400: ErrorSchema, 404: ErrorSchema},
    summary="Patch Article Body",
    operation_id="body_patch_article",
    description=capability_docstring("body_patch_article"),
    openapi_extra=agent_openapi_extra("body_patch_article"),
)
def body_patch_article(request, page_id: int, data: BodyPatchRequest):
    """
    Capability: update — articles
    Modify article body with structured operations without replacing the whole field.
    Supports StreamField and RichTextField bodies automatically.
    """
    if not data.operations:
        return 400, {"detail": "operations list must not be empty"}

    try:
        page = (
            ArticlePage.objects
            .select_related("locale", "featured_image")
            .prefetch_related("metafields", "tagged_items__tag")
            .get(pk=page_id)
        )
    except ArticlePage.DoesNotExist:
        return 404, {"detail": f"Article page {page_id} not found."}

    # Detect field type
    from wagtail.fields import StreamField, RichTextField

    body_field = ArticlePage._meta.get_field("body")
    is_stream = isinstance(body_field, StreamField)

    if is_stream:
        raw_blocks = list(page.body.raw_data) if page.body else []
        new_blocks, error = _apply_stream_ops(raw_blocks, data.operations)
        if error:
            return 400, {"detail": error}
        page.body = json.dumps(new_blocks)
    else:
        html = str(page.body) if page.body else ""
        new_html, error = _apply_html_ops(html, data.operations)
        if error:
            return 400, {"detail": error}
        page.body = new_html

    if data.publish:
        revision = page.save_revision()
        revision.publish()
    else:
        page.save()

    page.refresh_from_db()
    return page
