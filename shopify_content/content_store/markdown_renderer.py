"""Render Git-authoritative editorial Markdown to storefront HTML.

The document stays portable Markdown. Custom components are deliberately small
and explicit, using Markdoc-like directives on their own lines:

    {% product handle="satisfyer-pro-2" label="Satisfyer Pro 2" %}
    {% collection handle="vibrators" label="Vibrators" %}
    {% page path="/pages/glossary/lubricant" label="Lubricant" %}

    {% callout type="tip" title="Tip" %}
    Normal **Markdown** inside the callout.
    {% /callout %}

Standard Markdown handles prose, headings, lists, links and images. The custom
renderer only owns components that need a stable semantic contract. It emits
plain HTML with ``plt-*`` classes/data attributes; Shopify does not need to know
about Wagtail StreamField or execute Liquid to render article body content.
"""

from __future__ import annotations

import html
import re
import shlex
from dataclasses import dataclass

import markdown as markdown_lib


class MarkdownRenderError(ValueError):
    """Raised when an editorial component directive is invalid."""


_COMPONENT_RE = re.compile(r"^\{%\s*(product|collection|page)\s*(.*?)\s*%\}\s*$")
_CALLOUT_RE = re.compile(r"^\{%\s*callout\s*(.*?)\s*%\}\s*$")
_CALLOUT_END_RE = re.compile(r"^\{%\s*/callout\s*%\}\s*$")
_DIRECTIVE_PREFIX_RE = re.compile(r"^\{%")
_HANDLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_ALLOWED_CALLOUT_TYPES = frozenset({"note", "info", "tip", "warning"})


@dataclass(frozen=True)
class Component:
    kind: str
    attrs: dict[str, str]


def _parse_attrs(raw: str) -> dict[str, str]:
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


def _only(attrs: dict[str, str], allowed: set[str], *, kind: str) -> None:
    unexpected = sorted(set(attrs) - allowed)
    if unexpected:
        raise MarkdownRenderError(
            f"Unsupported {kind} attributes: {', '.join(unexpected)}"
        )


def _require_handle(attrs: dict[str, str], *, kind: str) -> str:
    handle = (attrs.get("handle") or "").strip()
    if not handle or not _HANDLE_RE.fullmatch(handle):
        raise MarkdownRenderError(
            f"{kind} requires a safe Shopify handle using letters, numbers, '.', '_' or '-'."
        )
    return handle


def _render_component(component: Component) -> str:
    kind = component.kind
    attrs = component.attrs

    if kind == "product":
        _only(attrs, {"handle", "label"}, kind=kind)
        handle = _require_handle(attrs, kind=kind)
        label = (attrs.get("label") or handle).strip() or handle
        return (
            '<aside class="plt-component plt-product-ref" data-component="product" '
            f'data-handle="{html.escape(handle, quote=True)}">\n'
            f'  <a href="/products/{html.escape(handle, quote=True)}">'
            f'{html.escape(label)}</a>\n'
            '</aside>'
        )

    if kind == "collection":
        _only(attrs, {"handle", "label"}, kind=kind)
        handle = _require_handle(attrs, kind=kind)
        label = (attrs.get("label") or handle).strip() or handle
        return (
            '<aside class="plt-component plt-collection-ref" data-component="collection" '
            f'data-handle="{html.escape(handle, quote=True)}">\n'
            f'  <a href="/collections/{html.escape(handle, quote=True)}">'
            f'{html.escape(label)}</a>\n'
            '</aside>'
        )

    if kind == "page":
        _only(attrs, {"path", "label"}, kind=kind)
        path = (attrs.get("path") or "").strip()
        if not path.startswith("/") or path.startswith("//"):
            raise MarkdownRenderError("page requires a root-relative path such as /pages/foo.")
        label = (attrs.get("label") or path).strip() or path
        return (
            '<aside class="plt-component plt-page-ref" data-component="page" '
            f'data-path="{html.escape(path, quote=True)}">\n'
            f'  <a href="{html.escape(path, quote=True)}">{html.escape(label)}</a>\n'
            '</aside>'
        )

    raise MarkdownRenderError(f"Unsupported component kind: {kind}")


def _render_callout(attrs: dict[str, str], body: str, *, depth: int) -> str:
    _only(attrs, {"type", "title"}, kind="callout")
    callout_type = (attrs.get("type") or "note").strip().lower()
    if callout_type not in _ALLOWED_CALLOUT_TYPES:
        allowed = ", ".join(sorted(_ALLOWED_CALLOUT_TYPES))
        raise MarkdownRenderError(f"callout type must be one of: {allowed}")

    title = (attrs.get("title") or "").strip()
    body_html = _render_document(body, depth=depth + 1)
    title_html = (
        f'<div class="plt-callout__title">{html.escape(title)}</div>\n'
        if title
        else ""
    )
    return (
        f'<aside class="plt-callout plt-callout--{callout_type}" '
        f'data-component="callout" data-callout-type="{callout_type}">\n'
        f'{title_html}<div class="plt-callout__body">\n{body_html}\n</div>\n'
        '</aside>'
    )


def _expand_directives(source: str, *, depth: int) -> str:
    if depth > 8:
        raise MarkdownRenderError("Editorial component nesting is too deep.")

    lines = source.splitlines()
    output: list[str] = []
    i = 0

    while i < len(lines):
        raw_line = lines[i]
        stripped = raw_line.strip()

        component_match = _COMPONENT_RE.fullmatch(stripped)
        if component_match:
            kind, attrs_raw = component_match.groups()
            output.append(_render_component(Component(kind, _parse_attrs(attrs_raw))))
            i += 1
            continue

        callout_match = _CALLOUT_RE.fullmatch(stripped)
        if callout_match:
            attrs = _parse_attrs(callout_match.group(1))
            body_lines: list[str] = []
            i += 1
            while i < len(lines) and not _CALLOUT_END_RE.fullmatch(lines[i].strip()):
                if _CALLOUT_RE.fullmatch(lines[i].strip()):
                    raise MarkdownRenderError("Nested callout directives are not supported.")
                body_lines.append(lines[i])
                i += 1
            if i >= len(lines):
                raise MarkdownRenderError("Unclosed callout directive.")
            output.append(_render_callout(attrs, "\n".join(body_lines), depth=depth))
            i += 1
            continue

        if _CALLOUT_END_RE.fullmatch(stripped):
            raise MarkdownRenderError("Unexpected {% /callout %} directive.")

        if _DIRECTIVE_PREFIX_RE.match(stripped):
            raise MarkdownRenderError(f"Unknown or malformed editorial directive: {stripped}")

        output.append(raw_line)
        i += 1

    return "\n".join(output)


def _render_document(source: str, *, depth: int) -> str:
    expanded = _expand_directives(source, depth=depth)
    return markdown_lib.markdown(
        expanded,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )


def render_editorial_markdown(source: str) -> str:
    """Render one authoritative Markdown body to deterministic storefront HTML."""
    if not source or not source.strip():
        return ""
    return _render_document(source, depth=0)
