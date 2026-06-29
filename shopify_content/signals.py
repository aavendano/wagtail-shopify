from django.db import transaction

from wagtail.signals import copy_for_translation_done, page_published

from shopify_content.sync.publish_sync import get_syncable_page_types, queue_shopify_sync_on_publish


def get_semantic_linkable_page_types():
    from shopify_content.models import (
        ArticlePage,
        CollectionPage,
        GlossaryTermPage,
        ProductPage,
    )

    return (ProductPage, CollectionPage, ArticlePage, GlossaryTermPage)


def _queue_semantic_links_when_sync_disabled(page):
    from django.conf import settings

    from shopify_content.semantic_links.service import is_semantic_linkable_page

    if not getattr(settings, 'SEMANTIC_LINKS_ENABLED', False):
        return
    if not getattr(settings, 'SEMANTIC_LINKS_AUTO_ON_PUBLISH', True):
        return
    if not is_semantic_linkable_page(page):
        return

    specific = page.specific
    if getattr(specific, 'sync_enabled', True):
        return

    page_id = page.pk

    def dispatch():
        from shopify_content.tasks import refresh_semantic_links_task

        refresh_semantic_links_task.delay(page_id)

    transaction.on_commit(dispatch)


def _on_page_published(sender, instance, **kwargs):
    queue_shopify_sync_on_publish(instance)
    _queue_semantic_links_when_sync_disabled(instance)


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

    for model in get_semantic_linkable_page_types():
        if model in get_syncable_page_types():
            continue
        page_published.connect(
            handler,
            sender=model,
            dispatch_uid=f'shopify_content_semantic_links_on_publish_{model._meta.label_lower}',
        )

    copy_for_translation_done.connect(
        _on_copy_for_translation_done,
        dispatch_uid='shopify_content_sync_enabled_on_translation',
    )
