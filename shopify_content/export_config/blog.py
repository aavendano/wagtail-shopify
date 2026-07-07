"""Blog index listings export_config consumer."""

from __future__ import annotations

from django.db import transaction

from shopify_content.blogs.index import build_blog_index_listings
from shopify_content.export_config.single_page import SinglePageListingsConsumer


class BlogListingsConsumer(SinglePageListingsConsumer):
    """Push custom.index_listings to a single Shopify Page (handle blogs)."""

    root_slug = 'blogs'
    config_key = 'blog_index'

    def build_payload(self) -> dict:
        return build_blog_index_listings()

    def locale_codes_for_page(self, page) -> list[str] | None:
        """Return the article locale to rebuild when content changes."""
        from shopify_content.models import ArticlePage

        specific = page.specific if hasattr(page, 'specific') else page
        if not isinstance(specific, ArticlePage):
            return None
        if not specific.locale_id:
            return None
        return [specific.locale.language_code]

    def queue_sync(self, *, locale_codes: list[str] | None = None) -> None:
        from shopify_content.tasks import sync_blog_index_task

        def dispatch():
            sync_blog_index_task.delay()

        transaction.on_commit(dispatch)


blog_listings_consumer = BlogListingsConsumer()
