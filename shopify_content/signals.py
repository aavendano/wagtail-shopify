from wagtail.signals import page_published

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


def register_publish_signals():
    handler = _on_page_published
    for model in get_syncable_page_types():
        page_published.connect(
            handler,
            sender=model,
            dispatch_uid=f'shopify_content_sync_on_publish_{model._meta.label_lower}',
        )
