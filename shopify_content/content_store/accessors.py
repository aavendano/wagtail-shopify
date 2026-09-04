"""Editorial resolution + content-write mirroring, mode-aware.

Authority strategy is selected by ``CONTENT_STORE_MODE`` (see settings):

* ``db``                -> PostgreSQL authoritative (legacy)
* ``mirror``            -> PostgreSQL authoritative + filesystem mirror
* ``git_authoritative`` -> Git-backed ContentRepository authoritative

Consumers use the domain accessor (``page.editorial.<field>``); this module
implements the resolution behind it. It performs NO Git commands — runtime only
reads the already-deployed worktree (Git sync is deployment infrastructure).
"""

from __future__ import annotations

import logging
from typing import Optional

from django.conf import settings

from .backends import FilesystemContentRepository
from .contracts import ContentNotFound, ContentRepository
from .locales import UnsupportedLocale
from .refs import ref_for
from .serializers import checksum

logger = logging.getLogger(__name__)

# Migrated editorial fields (scoped, per HumanGate):
#   BlogPage.description                         (HG-003, Phase C)
#   GlossaryTermPage.definition                  (HG-004, Phase D)
#   LocationPage single-value RichText sections  (Phase E)
MIRRORED_FIELDS = frozenset({
    ("shopify_content.blogpage", "description"),
    ("shopify_content.glossarytermpage", "definition"),
    ("shopify_content.locationpage", "intro"),
    ("shopify_content.locationpage", "content_2"),
    ("shopify_content.locationpage", "content_3"),
    ("shopify_content.locationpage", "brand_section_content"),
    ("shopify_content.locationpage", "map_content"),
    ("shopify_content.locationpage", "after_page_content"),
})

MODE_DB = "db"
MODE_MIRROR = "mirror"
MODE_GIT = "git_authoritative"
_VALID_MODES = {MODE_DB, MODE_MIRROR, MODE_GIT}


def get_mode() -> str:
    """Resolve the active content-store mode.

    Explicit CONTENT_STORE_MODE wins. Otherwise fall back to the legacy boolean
    (CONTENT_STORE_ENABLED=true -> mirror) so Phase B behavior is preserved.
    """
    mode = (getattr(settings, "CONTENT_STORE_MODE", "") or "").strip().lower()
    if mode in _VALID_MODES:
        return mode
    if getattr(settings, "CONTENT_STORE_ENABLED", False):
        return MODE_MIRROR
    return MODE_DB


def is_git_authoritative() -> bool:
    return get_mode() == MODE_GIT


def _is_mirrored(page, field_key: str) -> bool:
    return (page._meta.label_lower, field_key) in MIRRORED_FIELDS


def db_text(page, field_key: str) -> str:
    """Lossless string form of a field's DB value.

    Wagtail ``RichTextField`` exposes ``.source`` (the stored HTML), which is
    the lossless representation. Plain text/char fields are already strings.
    Never renders or transforms the value.
    """
    value = getattr(page, field_key, "")
    source = getattr(value, "source", None)
    if source is not None:
        return source
    return value or ""


def get_repository() -> Optional[ContentRepository]:
    root = getattr(settings, "CONTENT_STORE_ROOT", None)
    if not root:
        return None
    return FilesystemContentRepository(root)


def resolve_editorial(page, field_key: str) -> str:
    """Return the authoritative editorial value for a migrated field.

    ``db`` / ``mirror``: PostgreSQL is authoritative (returns the model value;
    ``mirror`` additionally logs drift against the mirror).

    ``git_authoritative``: the Git-backed file is authoritative. If the file is
    missing, raise ContentNotFound (data-integrity error) unless the explicit,
    off-by-default compatibility fallback is enabled. PostgreSQL never overrides
    Git; on drift, Git wins.
    """
    db_value = db_text(page, field_key)
    mode = get_mode()

    if mode == MODE_DB or not _is_mirrored(page, field_key):
        return db_value

    repo = get_repository()
    ref = ref_for(page, field_key)

    if mode == MODE_MIRROR:
        if repo is not None:
            try:
                if repo.exists(ref) and repo.read(ref).checksum != checksum(db_value):
                    logger.warning(
                        "content_store drift (mirror): DB/mirror differ for %s.%s; "
                        "DB authoritative.",
                        ref.content_type, ref.field_key,
                    )
            except Exception:
                logger.exception("content_store mirror integrity check failed for %s", ref)
        return db_value

    # git_authoritative
    if repo is None:
        raise ContentNotFound(f"No content repository configured for {ref}")
    if repo.exists(ref):
        git_value = repo.read(ref).body
        if git_value != db_value:
            logger.info(
                "content_store drift (git_authoritative): Git wins for %s.%s "
                "(db_checksum=%s git_checksum=%s).",
                ref.content_type, ref.field_key, checksum(db_value), checksum(git_value),
            )
        return git_value

    logger.error(
        "content_store missing authoritative file for %s.%s locale=%s pk=%s",
        ref.content_type, ref.field_key, ref.locale, ref.object_id,
    )
    if getattr(settings, "CONTENT_STORE_GIT_FALLBACK_TO_DB", False):
        logger.warning(
            "content_store compatibility fallback: returning DB value for %s "
            "(CONTENT_STORE_GIT_FALLBACK_TO_DB enabled).", ref,
        )
        return db_value
    raise ContentNotFound(f"Authoritative editorial file missing for {ref}")


# Backwards-compatible alias (Phase B callers).
def read_editorial_value(page, field_key: str) -> str:
    return resolve_editorial(page, field_key)


def mirror_editorial_content(page, field_key: str) -> None:
    """Content-write workflow: mirror the DB value to a file (``mirror`` mode).

    Independent of Shopify publication (C-004). No-op unless mode == mirror, so
    ``git_authoritative`` never turns runtime edits into authoritative content
    via hidden filesystem writes (authoritative writes go through Git).
    """
    if get_mode() != MODE_MIRROR or not _is_mirrored(page, field_key):
        return
    repo = get_repository()
    if repo is None:
        return
    ref = ref_for(page, field_key)
    value = db_text(page, field_key)
    try:
        if not value:
            repo.delete(ref)
        else:
            repo.write(ref, value)
    except UnsupportedLocale:
        logger.warning("content_store mirror skipped: unsupported locale for %s", ref)
    except Exception:
        logger.exception("content_store mirror write failed for %s", ref)
