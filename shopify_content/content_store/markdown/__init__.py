"""Git-native Markdown: parser, directives, references, validation, rendering."""

from .errors import MarkdownRenderError
from .renderer import render_editorial_markdown
from .references import ContentReference, ReferenceResolver

__all__ = [
    "ContentReference",
    "MarkdownRenderError",
    "ReferenceResolver",
    "render_editorial_markdown",
]
