from django.contrib import admin

from shopify_content.models.sync_run import ShopifySyncRun


@admin.register(ShopifySyncRun)
class ShopifySyncRunAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'kind',
        'resource',
        'page',
        'status',
        'new_only',
        'created_at',
        'finished_at',
    )
    list_filter = ('kind', 'status', 'resource', 'new_only')
    search_fields = ('celery_task_id', 'message', 'error_detail')
    readonly_fields = (
        'kind',
        'resource',
        'page',
        'new_only',
        'celery_task_id',
        'status',
        'message',
        'stats',
        'error_detail',
        'created_at',
        'started_at',
        'finished_at',
    )
