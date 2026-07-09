"""Read-only storefront URL data for Wagtail admin panels and tooling."""

from __future__ import annotations

from shopify_content.content_url_index import indexed_paths_for_page
from shopify_content.storefront_urls import all_paths_for_page, storefront_path_for_page


def get_storefront_url_display(page) -> dict:
    """
    Return storefront path data for admin display.

    Keys:
        canonical_path: canonical relative path or None
        paths: list of relative paths (indexed when available, else computed)
        indexed: True when paths come from ContentUrlIndex
    """
    specific = page.specific if hasattr(page, 'specific') else page
    canonical = storefront_path_for_page(specific)
    indexed_paths = indexed_paths_for_page(specific.pk) if specific.pk else []
    paths = indexed_paths or all_paths_for_page(specific)

    return {
        'canonical_path': canonical,
        'paths': paths,
        'indexed': bool(indexed_paths),
    }
