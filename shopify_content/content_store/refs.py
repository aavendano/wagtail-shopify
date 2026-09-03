"""Deterministic ContentRef construction and safe path derivation.

The physical path is derived from the ref, keyed by the stable primary key —
never by the slug — so renaming a page does not move or orphan its file
(INV-PERSIST-001). No storage key is persisted (HG-001 C-001).
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .contracts import ContentRef
from .locales import to_content_locale

# Field-format registry for the Phase B slice (BlogPage.description only).
# fmt drives the file extension chosen by the serializer.
_FIELD_FORMAT = {
    ("shopify_content.blogpage", "description"): "markdown",
}

_EXT = {"markdown": "md", "json": "json"}

_SAFE_SEGMENT = re.compile(r"[^A-Za-z0-9._-]")


def field_format(ref: ContentRef) -> str:
    return _FIELD_FORMAT.get((ref.content_type, ref.field_key), "markdown")


def ref_for(page, field_key: str) -> ContentRef:
    """Build a deterministic ref from a Wagtail page and a field name."""
    locale_code = page.locale.language_code if getattr(page, "locale_id", None) else ""
    return ContentRef(
        content_type=page._meta.label_lower,
        object_id=str(page.pk),
        field_key=field_key,
        locale=locale_code,
    )


def _safe(segment: str) -> str:
    """Reject path traversal and normalize a single path segment."""
    cleaned = _SAFE_SEGMENT.sub("-", (segment or "").strip())
    if cleaned in ("", ".", "..") or "/" in cleaned or "\\" in cleaned:
        # Deterministic, collision-resistant fallback that can never traverse.
        cleaned = "h" + hashlib.sha256((segment or "").encode("utf-8")).hexdigest()[:16]
    return cleaned


def relative_path(ref: ContentRef) -> Path:
    """<content-locale>/<app_label>/<model>/<pk>/<field>.<ext> (pk-keyed).

    The locale segment is normalized through the centralized locale policy
    (e.g. ``en-US`` -> ``en-us``); unsupported locales raise UnsupportedLocale.
    The physical path never uses the slug, so renames never move content.
    """
    app_label, model = ref.content_type.split(".", 1)
    ext = _EXT.get(field_format(ref), "md")
    content_locale = to_content_locale(ref.locale)
    return Path(
        _safe(content_locale),
        _safe(app_label),
        _safe(model),
        _safe(ref.object_id),
        f"{_safe(ref.field_key)}.{ext}",
    )
