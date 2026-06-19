"""Shared helpers for Shopify ↔ Wagtail sync."""

import logging

logger = logging.getLogger(__name__)

MAX_PRODUCT_IMAGES = 10


def absolute_shopify_media_url(url: str) -> str:
    """
    Normalize a Shopify media URL to an absolute https URL for img src.

    Returns empty string when the URL is missing or cannot be normalized.
    """
    if not url:
        return ''

    normalized = url.strip()
    if not normalized:
        return ''

    if normalized.startswith('//'):
        return f'https:{normalized}'

    if normalized.startswith('http://') or normalized.startswith('https://'):
        return normalized

    logger.warning('Skipping non-absolute Shopify media URL: %s', normalized)
    return ''
