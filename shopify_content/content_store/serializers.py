"""Lossless editorial serializer: YAML frontmatter + verbatim Markdown body.

Canonical editorial format (D-013): a plain-text ``.md`` file with a YAML
frontmatter block followed by the editorial body, readable by external editors
such as Keystatic and Obsidian without any runtime dependency on them.

Guarantees ``loads(dumps(value)).body == value`` byte-for-byte and performs NO
transformation of the value (no HTML->Markdown).
"""

from __future__ import annotations

import hashlib
from typing import Any, Mapping

import yaml

from .contracts import (
    ContentDocument,
    ContentRef,
    InvalidEditorialFrontmatter,
)
from .locales import UnsupportedLocale, to_content_locale

_OPEN = "---\n"
_CLOSE = "---\n"
_MARKER = "\n---\n"


def checksum(value: str) -> str:
    """Integrity / synchronization checksum (NOT content authority, C-002)."""
    return hashlib.sha256((value or "").encode("utf-8")).hexdigest()


def _content_locale(ref: ContentRef) -> str:
    try:
        return to_content_locale(ref.locale)
    except UnsupportedLocale:
        return ref.locale


def _meta_to_strings(data: Mapping[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, val in data.items():
        if val is None:
            continue
        if isinstance(val, (dict, list)):
            out[str(key)] = yaml.safe_dump(val, default_flow_style=True).strip()
        else:
            out[str(key)] = str(val)
    return out


def split_frontmatter(raw: str) -> tuple[dict[str, str], str, bool]:
    """Return (metadata, body, had_opening_delimiter).

    If YAML frontmatter is present but invalid, raises
    ``InvalidEditorialFrontmatter``.
    """
    if not raw.startswith(_OPEN):
        return {}, raw, False

    rest = raw[len(_OPEN) :]
    if rest.startswith(_CLOSE):
        return {}, rest[len(_CLOSE) :], True

    i = rest.find(_MARKER)
    if i == -1:
        # Opening --- without closing: treat as body (legacy tolerance).
        return {}, raw, False

    frontmatter_text = rest[:i]
    body = rest[i + len(_MARKER) :]
    if not frontmatter_text.strip():
        return {}, body, True

    try:
        parsed = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        raise InvalidEditorialFrontmatter(str(exc)) from exc

    if parsed is None:
        return {}, body, True
    if not isinstance(parsed, dict):
        raise InvalidEditorialFrontmatter(
            "YAML frontmatter must be a mapping at the document root."
        )
    return _meta_to_strings(parsed), body, True


class FrontmatterVerbatimSerializer:
    """Stores the value verbatim beneath a YAML identity frontmatter block."""

    fmt = "markdown"

    def dumps(self, ref: ContentRef, value: str, *, meta: Mapping[str, str]) -> str:
        value = value or ""
        lines: dict[str, Any] = {
            "content_type": ref.content_type,
            "object_id": ref.object_id,
            "field_key": ref.field_key,
            "locale": _content_locale(ref),
            "format": self.fmt,
            **{k: v for k, v in (meta or {}).items()},
        }
        frontmatter = yaml.safe_dump(
            lines,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        ).strip()
        return f"{_OPEN}{frontmatter}\n{_CLOSE}{value}"

    def loads(self, ref: ContentRef, raw: str) -> ContentDocument:
        meta, body, _ = split_frontmatter(raw)
        return ContentDocument(
            body=body,
            fmt=meta.get("format") or meta.get("fmt") or self.fmt,
            meta=meta,
            checksum=checksum(body),
        )
