"""Structural validation for editorial Markdown (no rendering)."""

from __future__ import annotations

from .directives import parse_directive_line
from .errors import MarkdownRenderError


def validate_directive_structure(source: str) -> None:
    """Ensure callouts are balanced and directives are syntactically valid."""
    depth = 0
    for i, line in enumerate((source or "").splitlines()):
        stripped = line.strip()
        if not stripped.startswith("{%"):
            continue
        directive = parse_directive_line(stripped, line=i)
        if directive is None:
            continue
        if directive.kind == "callout":
            depth += 1
        elif directive.kind == "/callout":
            depth -= 1
            if depth < 0:
                raise MarkdownRenderError("Unexpected {% /callout %} directive.")
    if depth > 0:
        raise MarkdownRenderError("Unclosed callout directive.")
