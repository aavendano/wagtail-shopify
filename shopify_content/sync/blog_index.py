"""Sync blog index listings metafield to the Shopify Page handle blogs."""

from shopify_content.export_config.blog import blog_listings_consumer


def sync_blog_index_listings(*, dry_run: bool = False) -> dict:
    return blog_listings_consumer.sync(dry_run=dry_run)


def get_blog_index_config():
    return blog_listings_consumer.get_config()
