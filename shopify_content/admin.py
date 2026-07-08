from django.contrib import admin

from shopify_content.models.command_run import EmbeddedCommandRun
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


@admin.register(EmbeddedCommandRun)
class EmbeddedCommandRunAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'command_id',
        'command_name',
        'status',
        'created_at',
        'finished_at',
    )
    list_filter = ('status', 'command_name')
    search_fields = ('command_id', 'command_name', 'celery_task_id', 'message', 'error_detail')
    readonly_fields = (
        'command_id',
        'command_name',
        'kwargs',
        'celery_task_id',
        'status',
        'message',
        'stdout',
        'stderr',
        'error_detail',
        'created_at',
        'started_at',
        'finished_at',
    )
