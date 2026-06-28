"""Sanitize and validate Wagtail RichTextField HTML for Draftail/ContentState."""

from __future__ import annotations

import re
from typing import Iterable

from wagtail.admin.rich_text.converters.contentstate import ContentstateConverter

LOCATION_RICHTEXT_FEATURES = ["bold", "italic", "link", "ol", "ul", "h2", "h3"]
LOCATION_RICHTEXT_FIELDS = (
    "intro",
    "content_2",
    "content_3",
    "brand_section_content",
    "map_content",
    "after_page_content",
)


def _richtext_source(value) -> str:
    if value is None:
        return ""
    return getattr(value, "source", value) or ""


def remove_stray_closing_em_in_list_items(html: str) -> str:
    """Remove an extra </em> inside <li> after the label emphasis is already closed."""

    def fix_li(match: re.Match[str]) -> str:
        inner = match.group(1)
        first_close = inner.find("</em>")
        if first_close == -1:
            return match.group(0)
        rest = inner[first_close + 5 :]
        if "</em>" in rest:
            rest = rest.replace("</em>", "", 1)
            inner = inner[: first_close + 5] + rest
        return f"<li>{inner}</li>"

    return re.sub(r"<li>(.*?)</li>", fix_li, html, flags=re.DOTALL)


def fix_mismatched_paragraph_heading_closers(html: str) -> str:
    """Fix </h3> wrongly closing a <p> block before the next <h3>."""

    return re.sub(
        r"(<p>(?:(?!</p>).)*?)</h3>(\s*<h3>)",
        r"\1</p>\2",
        html,
        flags=re.DOTALL,
    )


def fix_br_in_paragraphs(html: str) -> str:
    """Split <p> blocks that use <br> into separate paragraphs (Draftail-safe)."""

    def fix_p(match: re.Match[str]) -> str:
        inner = match.group(1)
        if not re.search(r"<br\s*/?>", inner):
            return match.group(0)
        parts = re.split(r"<br\s*/?>", inner, maxsplit=1)
        if len(parts) == 2:
            return f"<p>{parts[0]}</p><p>{parts[1]}</p>"
        return match.group(0)

    return re.sub(r"<p>(.*?)</p>", fix_p, html, flags=re.DOTALL)


def sanitize_richtext_html(html: str) -> str:
    html = remove_stray_closing_em_in_list_items(html)
    html = fix_mismatched_paragraph_heading_closers(html)
    html = fix_br_in_paragraphs(html)
    return html


def validate_richtext_html(
    html: str,
    *,
    features: Iterable[str] | None = None,
) -> str | None:
    """Return an error message if HTML cannot be converted to Draftail ContentState."""
    if not (html or "").strip():
        return None
    converter = ContentstateConverter(list(features or LOCATION_RICHTEXT_FEATURES))
    try:
        converter.from_database_format(html)
    except Exception as exc:
        return str(exc)
    return None
