"""Backward-compatible facade for editorial Markdown rendering."""

from shopify_content.content_store.markdown.errors import MarkdownRenderError
from shopify_content.content_store.markdown.renderer import render_editorial_markdown
from shopify_content.content_store.markdown.security import RenderProfile

__all__ = ["MarkdownRenderError", "RenderProfile", "render_editorial_markdown"]
