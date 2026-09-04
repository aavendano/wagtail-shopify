"""Template helpers for authority-aware editorial rendering."""

from django import template
from django.utils.safestring import mark_safe

from shopify_content.sync.article_markdown import article_body_html

register = template.Library()


@register.simple_tag
def render_article_editorial_body(page):
    """Render the same Article body HTML used by Shopify outbound sync."""
    return mark_safe(article_body_html(page))
