"""Typed editorial directives (Markdoc-like, own-line grammar)."""

from __future__ import annotations

import re
import shlex
from dataclasses import dataclass
from typing import Optional

from .errors import MarkdownRenderError

_COMPONENT_RE = re.compile(r"^\{%\s*(product|collection|page)\s*(.*?)\s*%\}\s*$")
_CALLOUT_RE = re.compile(r"^\{%\s*callout\s*(.*?)\s*%\}\s*$")
_CALLOUT_END_RE = re.compile(r"^\{%\s*/callout\s*%\}\s*$")
_REF_ATTR_RE = re.compile(r"^ref=")


@dataclass(frozen=True)
class Component:
    kind: str
    attrs: dict[str, str]


def parse_attrs(raw: str) -> dict[str, str]:
    if not raw.strip():
        return {}
    try:
        tokens = shlex.split(raw, posix=True)
    except ValueError as exc:
        raise MarkdownRenderError(f"Invalid directive attributes: {exc}") from exc

    attrs: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            raise MarkdownRenderError(
                f"Directive attribute {token!r} must use key=value syntax."
            )
        key, value = token.split("=", 1)
        key = key.strip().lower()
        if not key or not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise MarkdownRenderError(f"Invalid directive attribute name: {key!r}")
        if key in attrs:
            raise MarkdownRenderError(f"Duplicate directive attribute: {key}")
        attrs[key] = value
    return attrs


def parse_directive_line(stripped: str, *, line: int = 0) -> Optional[Component]:
    component_match = _COMPONENT_RE.fullmatch(stripped)
    if component_match:
        kind, attrs_raw = component_match.groups()
        return Component(kind, parse_attrs(attrs_raw))

    callout_match = _CALLOUT_RE.fullmatch(stripped)
    if callout_match:
        return Component("callout", parse_attrs(callout_match.group(1)))

    if _CALLOUT_END_RE.fullmatch(stripped):
        return Component("/callout", {})

    if stripped.startswith("{%") and not stripped.startswith("{%-"):
        raise MarkdownRenderError(f"Unknown or malformed editorial directive: {stripped}")

    return None


def supports_ref_attribute(attrs: dict[str, str]) -> bool:
    """Future ``ref=`` identity alongside handle/path (not required today)."""
    return "ref" in attrs or any(_REF_ATTR_RE.match(k) for k in attrs)
