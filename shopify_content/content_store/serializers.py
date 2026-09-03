"""Lossless editorial serializer: YAML-ish frontmatter + verbatim body.

Phase B guarantees ``loads(dumps(value)).body == value`` byte-for-byte and does
NOT transform the value (no HTML->Markdown) — HG-001 C-003.

The frontmatter carries only stable identity + integrity metadata (never the
body), so parsing the leading block and keeping the remainder verbatim is exact.
"""

from __future__ import annotations

import hashlib
from typing import Mapping

from .contracts import ContentDocument, ContentRef

_OPEN = "---\n"
_MARKER = "\n---\n"


def checksum(value: str) -> str:
    """Integrity / synchronization checksum (NOT content authority, C-002)."""
    return hashlib.sha256((value or "").encode("utf-8")).hexdigest()


class FrontmatterVerbatimSerializer:
    """Stores the value verbatim beneath a minimal identity frontmatter block."""

    fmt = "markdown"

    def dumps(self, ref: ContentRef, value: str, *, meta: Mapping[str, str]) -> str:
        value = value or ""
        lines = {
            "content_type": ref.content_type,
            "object_id": ref.object_id,
            "field_key": ref.field_key,
            "locale": ref.locale,
            "fmt": self.fmt,
            "checksum": checksum(value),
            **{k: str(v) for k, v in (meta or {}).items()},
        }
        frontmatter = "".join(f"{k}: {v}\n" for k, v in lines.items())
        return f"{_OPEN}{frontmatter}{_MARKER[1:]}{value}"

    def loads(self, ref: ContentRef, raw: str) -> ContentDocument:
        meta: dict[str, str] = {}
        if not raw.startswith(_OPEN):
            body = raw
        else:
            rest = raw[len(_OPEN):]
            if rest.startswith("---\n"):
                frontmatter, body = "", rest[len("---\n"):]
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
            fmt=meta.get("fmt", self.fmt),
            meta=meta,
            checksum=meta.get("checksum") or checksum(body),
        )
