from django.db import transaction

from wagtail.signals import copy_for_translation_done, page_published, page_unpublished

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


def _queue_content_url_index_on_publish(page):
    page_id = page.pk

    def dispatch():
        from shopify_content.content_url_index import rebuild_index_for_page
        from wagtail.models import Page

        try:
            rebuild_index_for_page(Page.objects.get(pk=page_id))
        except Page.DoesNotExist:
            pass

    transaction.on_commit(dispatch)


def _on_content_url_index_unpublished(sender, instance, **kwargs):
    from shopify_content.content_url_index import clear_index_for_page

    clear_index_for_page(instance.pk)


def _on_page_published(sender, instance, **kwargs):
    queue_shopify_sync_on_publish(instance)
    _queue_semantic_links_when_sync_disabled(instance)
    _queue_content_url_index_on_publish(instance)


def _on_copy_for_translation_done(sender, source_obj, target_obj, **kwargs):
    """New translation copies inherit sync_enabled=True so locales sync on publish."""
    specific = getattr(target_obj, 'specific', target_obj)
    if not hasattr(specific, 'sync_enabled'):
        return
    if specific.sync_enabled:
        return
    type(specific).objects.filter(pk=specific.pk).update(sync_enabled=True)
    specific.sync_enabled = True


def _on_glossary_term_changed(sender, instance, **kwargs):
    from shopify_content.export_config.registry import on_content_page_changed

    on_content_page_changed(instance)


def _on_location_page_changed(sender, instance, **kwargs):
    from shopify_content.export_config.registry import on_content_page_changed

    on_content_page_changed(instance)


def _on_article_page_changed(sender, instance, **kwargs):
    from shopify_content.export_config.registry import on_content_page_changed

    on_content_page_changed(instance)


def _on_export_root_published(sender, instance, **kwargs):
    from shopify_content.export_config.registry import on_root_published

    on_root_published(instance)


def register_publish_signals():
    handler = _on_page_published
    for model in get_syncable_page_types():
        page_published.connect(
            handler,
            sender=model,
            dispatch_uid=f'shopify_content_sync_on_publish_{model._meta.label_lower}',
        )
        page_unpublished.connect(
            _on_content_url_index_unpublished,
            sender=model,
            dispatch_uid=f'shopify_content_url_index_on_unpublish_{model._meta.label_lower}',
        )

    for model in get_semantic_linkable_page_types():
        if model in get_syncable_page_types():
            continue
        page_published.connect(
            handler,
            sender=model,
            dispatch_uid=f'shopify_content_semantic_links_on_publish_{model._meta.label_lower}',
        )

    from shopify_content.models import ArticlePage, GlossaryTermPage, LocationPage, ShopifyRootPage

    page_unpublished.connect(
        _on_glossary_term_changed,
        sender=GlossaryTermPage,
        dispatch_uid='shopify_content_glossary_index_on_term_unpublish',
    )
    page_unpublished.connect(
        _on_location_page_changed,
        sender=LocationPage,
        dispatch_uid='shopify_content_location_index_on_unpublish',
    )
    page_unpublished.connect(
        _on_article_page_changed,
        sender=ArticlePage,
        dispatch_uid='shopify_content_blog_index_on_article_unpublish',
    )
    page_published.connect(
        _on_export_root_published,
        sender=ShopifyRootPage,
        dispatch_uid='shopify_content_export_config_on_root_publish',
    )

    copy_for_translation_done.connect(
        _on_copy_for_translation_done,
        dispatch_uid='shopify_content_sync_enabled_on_translation',
    )
