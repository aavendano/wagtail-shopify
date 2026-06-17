"""
Enqueue Shopify sync jobs as Celery tasks.
"""

from shopify_content.models.sync_run import ShopifySyncRun
from shopify_content.sync.service import VALID_IMPORT_RESOURCES, ImportResource


def enqueue_shopify_import(resource: ImportResource, *, new_only: bool = False) -> ShopifySyncRun:
    if resource not in VALID_IMPORT_RESOURCES:
        raise ValueError(f'Unknown resource: {resource}')

    sync_run = ShopifySyncRun.objects.create(
        kind=ShopifySyncRun.KIND_INBOUND,
        resource=resource,
        new_only=new_only,
        message='Importación en cola.',
    )

    from shopify_content.tasks import run_shopify_import_task

    async_result = run_shopify_import_task.delay(
        sync_run.pk,
        resource,
        new_only=new_only,
    )
    sync_run.celery_task_id = async_result.id or ''
    sync_run.save(update_fields=['celery_task_id'])
    return sync_run


def enqueue_page_outbound_sync(page) -> ShopifySyncRun | None:
    specific = page.specific
    if not getattr(specific, 'sync_enabled', True):
        return None

    sync_run = ShopifySyncRun.objects.create(
        kind=ShopifySyncRun.KIND_OUTBOUND,
        page=page,
        message='Sincronización con Shopify en cola.',
    )

    from shopify_content.tasks import sync_page_to_shopify_task

    async_result = sync_page_to_shopify_task.delay(sync_run.pk, page.pk)
    sync_run.celery_task_id = async_result.id or ''
    sync_run.save(update_fields=['celery_task_id'])
    return sync_run


def sync_run_to_task_response(sync_run: ShopifySyncRun) -> dict:
    return {
        'sync_run_id': sync_run.pk,
        'celery_task_id': sync_run.celery_task_id,
        'status': sync_run.status,
        'message': sync_run.message,
    }
