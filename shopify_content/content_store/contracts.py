"""Contracts for the editorial content store (interfaces + value objects).

No backend behaviour lives here; see ``backends.py`` and ``serializers.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Protocol


@dataclass(frozen=True)
class ContentRef:
    """Deterministic, stable reference to one editorial payload.

    Derived entirely from durable DB identity (content type + primary key +
    field + locale). It intentionally does NOT carry the physical path or the
    slug: a path or slug may change, identity must not (INV-PERSIST-001).
    """

    content_type: str  # e.g. "shopify_content.blogpage"
    object_id: str      # stable DB identity (primary key), as text
    field_key: str      # e.g. "description"
    locale: str         # e.g. "en-US"


@dataclass(frozen=True)
class ContentDocument:
    """Normalized, backend-agnostic representation of an editorial payload.

    ``body`` is the domain value (verbatim in Phase B). Consumers operate on
    ``body`` / domain values, never on the file format (INV-PERSIST-003).

    ``checksum`` is integrity / synchronization metadata used to detect drift
    between the authoritative DB row and its mirror. It is NOT content
    authority (HG-001 C-002).
    """

    body: str
    fmt: str = "markdown"          # "markdown" | "json"
    meta: Mapping[str, str] = field(default_factory=dict)
    checksum: str = ""


class ContentNotFound(Exception):
    """Raised when a ref has no stored document."""


class ContentConflict(Exception):
    """Raised on optimistic-concurrency mismatch (expected_version)."""


class ContentSerializer(Protocol):
    """Domain value <-> serialized bytes. One implementation per format."""

    def dumps(self, ref: ContentRef, value: str, *, meta: Mapping[str, str]) -> str:
        """Serialize a domain value to file text (lossless for ``value``)."""
        ...

    def loads(self, ref: ContentRef, raw: str) -> ContentDocument:
        """Parse file text back into a ContentDocument (``body`` == original value)."""
        ...


class ContentRepository(Protocol):
    """Storage boundary. Implementations must not know Django models."""

    def read(self, ref: ContentRef) -> ContentDocument:
        """Return the stored document, or raise ContentNotFound."""
        ...

    def write(
        self,
        ref: ContentRef,
        value: str,
        *,
        meta: Optional[Mapping[str, str]] = None,
        expected_version: Optional[str] = None,
    ) -> ContentDocument:
        """Persist ``value``; return the written document (with checksum)."""
        ...

    def delete(self, ref: ContentRef) -> None:
        """Remove the stored document if present (idempotent)."""
        ...

    def exists(self, ref: ContentRef) -> bool:
        ...
