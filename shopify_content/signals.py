from wagtail.signals import page_published

from shopify_content.sync.publish_sync import get_syncable_page_types, queue_shopify_sync_on_publish


def _on_page_published(sender, instance, **kwargs):
    queue_shopify_sync_on_publish(instance)


def register_publish_signals():
    handler = _on_page_published
    for model in get_syncable_page_types():
        page_published.connect(
            handler,
            sender=model,
            dispatch_uid=f'shopify_content_sync_on_publish_{model._meta.label_lower}',
        )
