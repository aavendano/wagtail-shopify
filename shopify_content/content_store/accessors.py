"""Editorial resolution + content-write mirroring, mode-aware.

Authority strategy is selected by ``CONTENT_STORE_MODE`` (see settings):

* ``db``                -> PostgreSQL authoritative (legacy)
* ``mirror``            -> PostgreSQL authoritative + filesystem mirror
* ``git_authoritative`` -> Git-backed ContentRepository authoritative

Two migration classes are explicit:

``MIRRORED_FIELDS``
    Legacy DB and Git carry the same representation, so db/mirror/git modes can
    be compared directly during transition.

``GIT_NATIVE_FIELDS``
    The Git representation intentionally differs from the legacy DB field. The
    first example is ``ArticlePage.body``: Git contains Markdown while the DB
    keeps the old Wagtail StreamField JSON. These fields are resolved through
    ``page.editorial.<field>`` only in git_authoritative mode and are never
    silently converted, mirrored, or compared to the legacy representation.

Runtime performs NO Git commands; it only reads the deployed worktree.
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

# Fields whose DB and Git payloads share the same representation.
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

# Fields born in the Git editorial model. Their legacy DB representation is not
# semantically equivalent and therefore must not participate in mirror/drift
# comparison or automatic DB fallback.
GIT_NATIVE_FIELDS = frozenset({
    ("shopify_content.articlepage", "body"),
})

EDITORIAL_FIELDS = MIRRORED_FIELDS | GIT_NATIVE_FIELDS

MODE_DB = "db"
MODE_MIRROR = "mirror"
MODE_GIT = "git_authoritative"
_VALID_MODES = {MODE_DB, MODE_MIRROR, MODE_GIT}


def get_mode() -> str:
    """Resolve the active content-store mode."""
    mode = (getattr(settings, "CONTENT_STORE_MODE", "") or "").strip().lower()
    if mode in _VALID_MODES:
        return mode
    if getattr(settings, "CONTENT_STORE_ENABLED", False):
        return MODE_MIRROR
    return MODE_DB


def is_git_authoritative() -> bool:
    return get_mode() == MODE_GIT


def _field_key(page, field_key: str) -> tuple[str, str]:
    return page._meta.label_lower, field_key


def _is_mirrored(page, field_key: str) -> bool:
    return _field_key(page, field_key) in MIRRORED_FIELDS


def _is_git_native(page, field_key: str) -> bool:
    return _field_key(page, field_key) in GIT_NATIVE_FIELDS


def db_text(page, field_key: str) -> str:
    """Lossless string form of a legacy DB editorial value.

    Wagtail ``RichTextField`` exposes ``.source`` (stored HTML), which is the
    lossless representation. This helper is intentionally for representation-
    compatible mirrored fields; Git-native fields such as StreamField-backed
    Article body never call it for authority resolution.
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


def _read_required_git(page, field_key: str) -> str:
    repo = get_repository()
    ref = ref_for(page, field_key)
    if repo is None:
        raise ContentNotFound(f"No content repository configured for {ref}")
    if repo.exists(ref):
        return repo.read(ref).body
    logger.error(
        "content_store missing authoritative file for %s.%s locale=%s pk=%s",
        ref.content_type, ref.field_key, ref.locale, ref.object_id,
    )
    raise ContentNotFound(f"Authoritative editorial file missing for {ref}")


def resolve_editorial(page, field_key: str) -> str:
    """Return the domain editorial value for a registered field.

    Mirrored fields preserve the Phase C-E transition semantics. Git-native
    fields intentionally have no DB/mirror representation in this API: callers
    use the legacy model field while running in db/mirror mode, and switch to
    ``page.editorial.<field>`` once ``git_authoritative`` is enabled.
    """
    mode = get_mode()

    if _is_git_native(page, field_key):
        if mode != MODE_GIT:
            raise ContentNotFound(
                f"Git-native editorial field {_field_key(page, field_key)!r} is only "
                "available through page.editorial in git_authoritative mode."
            )
        # Deliberately no CONTENT_STORE_GIT_FALLBACK_TO_DB: Markdown and the
        # legacy StreamField are different representations and cannot be mixed.
        return _read_required_git(page, field_key)

    db_value = db_text(page, field_key)

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

    # git_authoritative for representation-compatible fields.
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
    """Mirror a representation-compatible DB value in ``mirror`` mode.

    Git-native fields are never mirrored because their Git payload has different
    semantics from the legacy DB representation.
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
