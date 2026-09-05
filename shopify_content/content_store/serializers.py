"""Lossless editorial serializer: YAML frontmatter + verbatim Markdown body.

Canonical editorial format (D-013): a plain-text ``.md`` file with a YAML
frontmatter block followed by the editorial body, readable by external editors
such as Keystatic and Obsidian without any runtime dependency on them.

Guarantees ``loads(dumps(value)).body == value`` byte-for-byte and performs NO
transformation of the value (no HTML->Markdown). The body may temporarily
contain valid HTML when the source representation is HTML (e.g. Wagtail
RichText ``.source``): lossless preservation takes priority over Markdown
purity, and any semantic HTML->Markdown migration is a separate approved step.

The frontmatter carries only stable identity metadata (never the body). It is
informational for humans/editors; ``ContentRepository`` never relies on it for
identity (identity comes from the path/ref) and tolerates its absence, so an
external editor that rewrites/strips frontmatter cannot break resolution.
"""

from __future__ import annotations

import hashlib
from typing import Mapping

from .contracts import ContentDocument, ContentRef
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


class FrontmatterVerbatimSerializer:
    """Stores the value verbatim beneath a YAML identity frontmatter block."""

    fmt = "markdown"

    def dumps(self, ref: ContentRef, value: str, *, meta: Mapping[str, str]) -> str:
        value = value or ""
        lines = {
            "content_type": ref.content_type,
            "object_id": ref.object_id,
            "field_key": ref.field_key,
            "locale": _content_locale(ref),
            "format": self.fmt,
            **{k: str(v) for k, v in (meta or {}).items()},
        }
        frontmatter = "".join(f"{k}: {v}\n" for k, v in lines.items())
        return f"{_OPEN}{frontmatter}{_CLOSE}{value}"

    def loads(self, ref: ContentRef, raw: str) -> ContentDocument:
        meta: dict[str, str] = {}
        if not raw.startswith(_OPEN):
            body = raw
        else:
            rest = raw[len(_OPEN):]
            if rest.startswith(_CLOSE):
                frontmatter, body = "", rest[len(_CLOSE):]
            else:
                i = rest.find(_MARKER)
                if i == -1:
                    frontmatter, body = "", rest
                else:
                    frontmatter, body = rest[: i + 1], rest[i + len(_MARKER):]
            for line in frontmatter.splitlines():
                if ": " in line:
                    key, val = line.split(": ", 1)
                    meta[key] = val
        return ContentDocument(
            body=body,
            fmt=meta.get("format") or meta.get("fmt") or self.fmt,
            meta=meta,
            # Always derived from the current body: never trust a possibly-stale
            # checksum an external editor may have left behind.
            checksum=checksum(body),
        )
