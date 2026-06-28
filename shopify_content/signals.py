from wagtail.signals import copy_for_translation_done, page_published
from django.db.models.signals import post_save

from shopify_content.sync.publish_sync import get_syncable_page_types, queue_shopify_sync_on_publish


def _on_page_published(sender, instance, **kwargs):
    # #region agent log
    from shopify_content.publish_debug import debug_log

    debug_log(
        "B",
        "signals.py:_on_page_published",
        "page_published signal received",
        {
            "page_id": getattr(instance, "pk", None),
            "page_type": type(instance.specific).__name__,
            "title": getattr(instance, "title", "")[:80],
        },
    )
    # #endregion
    result = queue_shopify_sync_on_publish(instance)
    # #region agent log
    debug_log(
        "B",
        "signals.py:_on_page_published",
        "queue_shopify_sync_on_publish finished",
        {
            "page_id": getattr(instance, "pk", None),
            "sync_run_id": getattr(result, "pk", None) if result else None,
        },
    )
    # #endregion


def _on_copy_for_translation_done(sender, source_obj, target_obj, **kwargs):
    """New translation copies inherit sync_enabled=True so locales sync on publish."""
    specific = getattr(target_obj, 'specific', target_obj)
    if not hasattr(specific, 'sync_enabled'):
        return
    if specific.sync_enabled:
        return
    type(specific).objects.filter(pk=specific.pk).update(sync_enabled=True)
    specific.sync_enabled = True


def _invalidate_links_cache(sender, instance, **kwargs):
    """Invalidate all links_index cache keys when any relevant Page is saved."""
    from django.core.cache import cache
    from itertools import product as iterproduct

    resources = [None, "articles", "products", "collections", "blogs", "locations", "glossary"]
    locales = [None]
    live_options = [True, False]

    for resource, locale, live in iterproduct(resources, locales, live_options):
        key = f"links_index_{resource}_{locale}_{live}"
        cache.delete(key)


def register_publish_signals():
    handler = _on_page_published
    for model in get_syncable_page_types():
        page_published.connect(
            handler,
            sender=model,
            dispatch_uid=f'shopify_content_sync_on_publish_{model._meta.label_lower}',
        )

    copy_for_translation_done.connect(
        _on_copy_for_translation_done,
        dispatch_uid='shopify_content_sync_enabled_on_translation',
    )


def register_cache_invalidation_signals():
    """Register post_save signals to invalidate the links_index cache."""
    from wagtail.models import Page
    post_save.connect(
        _invalidate_links_cache,
        sender=Page,
        dispatch_uid='api_links_cache_invalidate_page',
    )
    # Also connect to specific page subclasses for direct saves
    from shopify_content.models import (
        ArticlePage, ProductPage, CollectionPage,
        BlogPage, LocationPage, GlossaryTermPage,
    )
    for model in (ArticlePage, ProductPage, CollectionPage, BlogPage, LocationPage, GlossaryTermPage):
        post_save.connect(
            _invalidate_links_cache,
            sender=model,
            dispatch_uid=f'api_links_cache_invalidate_{model._meta.label_lower}',
        )
