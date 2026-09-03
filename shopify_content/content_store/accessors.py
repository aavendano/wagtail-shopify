"""Domain-facing content accessors.

Publication and editing surfaces call these; they never open files or touch
paths directly (INV-PERSIST-002). In Phase B the PostgreSQL row is authoritative
for the payload and the filesystem file is a mirror.
"""

from __future__ import annotations

import logging
from typing import Optional

from django.conf import settings

from .backends import FilesystemContentRepository
from .contracts import ContentNotFound, ContentRepository
from .refs import ref_for
from .serializers import checksum

logger = logging.getLogger(__name__)

# Scope guard (HG-001): the vertical slice mirrors BlogPage.description only.
MIRRORED_FIELDS = frozenset({("shopify_content.blogpage", "description")})


def is_enabled() -> bool:
    return bool(getattr(settings, "CONTENT_STORE_ENABLED", False))


def _is_mirrored(page, field_key: str) -> bool:
    return (page._meta.label_lower, field_key) in MIRRORED_FIELDS


def get_repository() -> Optional[ContentRepository]:
    root = getattr(settings, "CONTENT_STORE_ROOT", None)
    if not root:
        return None
    return FilesystemContentRepository(root)


def read_editorial_value(page, field_key: str) -> str:
    """Return the authoritative domain value for a mirrored editorial field.

    Phase B: the DB column is authoritative, so this returns the model value
    unchanged (keeping the publication payload identical). When mirroring is
    enabled it performs a best-effort integrity comparison against the mirror
    and logs drift; the checksum is integrity metadata only (C-002), never
    authority.
    """
    value = getattr(page, field_key, "") or ""
    if not (is_enabled() and _is_mirrored(page, field_key)):
        return value
    repo = get_repository()
    if repo is None:
        return value
    ref = ref_for(page, field_key)
    try:
        if repo.exists(ref):
            mirrored = repo.read(ref)
            if mirrored.checksum != checksum(value):
                logger.warning(
                    "content_store drift: DB and mirror differ for %s (%s); "
                    "DB is authoritative in Phase B.",
                    ref.content_type,
                    ref.field_key,
                )
    except Exception:  # integrity check must never break reads/publication
        logger.exception("content_store integrity check failed for %s", ref)
    return value


def mirror_editorial_content(page, field_key: str) -> None:
    """Content-write workflow: mirror the authoritative DB value to a file.

    Independent of Shopify publication (C-004): triggered by content saves, not
    by publish. Idempotent and best-effort — a mirror failure never affects the
    authoritative DB row.
    """
    if not (is_enabled() and _is_mirrored(page, field_key)):
        return
    repo = get_repository()
    if repo is None:
        return
    ref = ref_for(page, field_key)
    value = getattr(page, field_key, "") or ""
    try:
        if not value:
            repo.delete(ref)
        else:
            repo.write(ref, value)
    except Exception:
        logger.exception("content_store mirror write failed for %s", ref)
