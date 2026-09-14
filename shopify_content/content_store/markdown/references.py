"""Stable typed references extracted from Markdown directives."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Optional, Protocol

from .directives import _COMPONENT_RE, _CALLOUT_RE, parse_attrs

_HANDLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_ASSET_TOKEN_RE = re.compile(r"asset:([A-Za-z0-9][A-Za-z0-9._-]*)")
_IMG_ASSET_RE = re.compile(
    r"!\[[^\]]*\]\(asset:([A-Za-z0-9][A-Za-z0-9._-]*)(?:\s+\"[^\"]*\")?\)"
)


@dataclass(frozen=True)
class ContentReference:
    """Domain reference token (not a deployment URL)."""

    ref_type: str  # product | collection | page | asset | callout
    identifier: str
    label: str = ""

    def token(self) -> str:
        if self.ref_type == "asset":
            return f"asset:{self.identifier}"
        if self.ref_type == "product":
            return f"product:{self.identifier}"
        if self.ref_type == "collection":
            return f"collection:{self.identifier}"
        if self.ref_type == "page":
            return f"page:{self.identifier}"
        return f"{self.ref_type}:{self.identifier}"


class ReferenceResolver(Protocol):
    def resolve(self, reference: ContentReference) -> str:
        """Map a reference to a storefront URL or HTML fragment."""
        ...


class DefaultReferenceResolver:
    """Built-in resolver for handle/path/asset tokens (no Django)."""

    def resolve(self, reference: ContentReference) -> str:
        if reference.ref_type == "product":
            return f"/products/{reference.identifier}"
        if reference.ref_type == "collection":
            return f"/collections/{reference.identifier}"
        if reference.ref_type == "page":
            path = reference.identifier if reference.identifier.startswith("/") else f"/{reference.identifier}"
            return path
        if reference.ref_type == "asset":
            return f"/cdn/assets/{reference.identifier}"
        return ""


def _refs_from_component(kind: str, attrs: dict[str, str]) -> Optional[ContentReference]:
    if "ref" in attrs:
        raw = attrs["ref"].strip()
        if raw.startswith("asset:"):
            return ContentReference("asset", raw.split(":", 1)[1], attrs.get("label", ""))
        if ":" in raw:
            ref_type, ident = raw.split(":", 1)
            return ContentReference(ref_type, ident, attrs.get("label", ""))

    if kind == "product":
        handle = (attrs.get("handle") or "").strip()
        if handle and _HANDLE_RE.fullmatch(handle):
            return ContentReference("product", handle, attrs.get("label", ""))
    if kind == "collection":
        handle = (attrs.get("handle") or "").strip()
        if handle and _HANDLE_RE.fullmatch(handle):
            return ContentReference("collection", handle, attrs.get("label", ""))
    if kind == "page":
        path = (attrs.get("path") or "").strip()
        if path.startswith("/") and not path.startswith("//"):
            return ContentReference("page", path, attrs.get("label", ""))
    return None


def extract_references(source: str) -> tuple[ContentReference, ...]:
    refs: list[ContentReference] = []
    for line in (source or "").splitlines():
        stripped = line.strip()
        m = _COMPONENT_RE.fullmatch(stripped)
        if m:
            kind, attrs_raw = m.groups()
            ref = _refs_from_component(kind, parse_attrs(attrs_raw))
            if ref:
                refs.append(ref)
            continue
        if _CALLOUT_RE.fullmatch(stripped):
            refs.append(ContentReference("callout", "block", ""))

    for match in _IMG_ASSET_RE.finditer(source or ""):
        refs.append(ContentReference("asset", match.group(1)))

    for match in _ASSET_TOKEN_RE.finditer(source or ""):
        if match.group(0).startswith("asset:"):
            ident = match.group(1)
            if not any(r.ref_type == "asset" and r.identifier == ident for r in refs):
                refs.append(ContentReference("asset", ident))

    return tuple(refs)


def extract_reference_tokens(source: str) -> tuple[str, ...]:
    return tuple(r.token() for r in extract_references(source))
