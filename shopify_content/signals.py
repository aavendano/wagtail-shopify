from wagtail.signals import copy_for_translation_done, page_published

from shopify_content.sync.publish_sync import get_syncable_page_types, queue_shopify_sync_on_publish


def _on_page_published(sender, instance, **kwargs):
    queue_shopify_sync_on_publish(instance)


def _on_copy_for_translation_done(sender, source_obj, target_obj, **kwargs):
    """New translation copies inherit sync_enabled=True so locales sync on publish."""
    specific = getattr(target_obj, 'specific', target_obj)
    if not hasattr(specific, 'sync_enabled'):
        return
    if specific.sync_enabled:
        return
    type(specific).objects.filter(pk=specific.pk).update(sync_enabled=True)
    specific.sync_enabled = True


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
