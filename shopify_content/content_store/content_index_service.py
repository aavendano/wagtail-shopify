"""Rebuild derived ContentIndex rows from the filesystem (no Git commands)."""

from __future__ import annotations

from pathlib import Path

from django.db import transaction

from shopify_content.content_store.backends import FilesystemContentRepository
from shopify_content.content_store.contracts import ContentRef
from shopify_content.content_store.locales import to_wagtail_locale
from shopify_content.content_store.markdown.references import extract_references
from shopify_content.content_store.refs import relative_path
from shopify_content.models.content_index import ContentIndex, ContentReferenceIndex


def _ref_from_relative(rel: Path) -> ContentRef | None:
    parts = rel.parts
    if len(parts) < 5:
        return None
    content_locale, app_label, model, object_id, filename = parts[0], parts[1], parts[2], parts[3], parts[4]
    if not filename.endswith(".md"):
        return None
    field_key = filename[:-3]
    try:
        wagtail_locale = to_wagtail_locale(content_locale)
    except Exception:
        wagtail_locale = content_locale
    return ContentRef(
        content_type=f"{app_label}.{model}",
        object_id=object_id,
        field_key=field_key,
        locale=wagtail_locale,
    )


def rebuild_content_index(root: str | Path) -> dict[str, int]:
    repo = FilesystemContentRepository(root)
    root_path = Path(root)
    stats = {"files": 0, "references": 0}

    with transaction.atomic():
        ContentReferenceIndex.objects.all().delete()
        ContentIndex.objects.all().delete()

        for path in sorted(root_path.rglob("*.md")):
            rel = path.relative_to(root_path)
            ref = _ref_from_relative(rel)
            if ref is None:
                continue
            canonical = repo.read_canonical(ref)
            stats["files"] += 1
            row = ContentIndex.objects.create(
                content_type=ref.content_type,
                object_id=ref.object_id,
                field_key=ref.field_key,
                locale=ref.locale,
                checksum=canonical.checksum,
                reference_count=len(canonical.derived_refs),
                relative_path=relative_path(ref).as_posix(),
            )
            for cref in extract_references(canonical.body):
                ContentReferenceIndex.objects.create(
                    content_index=row,
                    ref_type=cref.ref_type,
                    identifier=cref.identifier,
                    token=cref.token(),
                )
                stats["references"] += 1

    return stats
