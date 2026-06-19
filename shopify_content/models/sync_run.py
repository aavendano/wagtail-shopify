from django.db import models
from django.utils import timezone
from wagtail.models import Page


class ShopifySyncRun(models.Model):
    """Tracks async Shopify inbound/outbound sync jobs dispatched via Celery."""

    KIND_INBOUND = 'inbound'
    KIND_OUTBOUND = 'outbound'
    KIND_CHOICES = [
        (KIND_INBOUND, 'Inbound (Shopify → Wagtail)'),
        (KIND_OUTBOUND, 'Outbound (Wagtail → Shopify)'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
    ]

    kind = models.CharField(max_length=16, choices=KIND_CHOICES)
    resource = models.CharField(
        max_length=32,
        blank=True,
        help_text='products, collections, blogs, or all (inbound only)',
    )
    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='shopify_sync_runs',
    )
    new_only = models.BooleanField(default=False)
    celery_task_id = models.CharField(max_length=255, blank=True, db_index=True)
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
    )
    message = models.TextField(blank=True)
    stats = models.JSONField(null=True, blank=True)
    error_detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Shopify sync run'
        verbose_name_plural = 'Shopify sync runs'

    def __str__(self):
        label = self.resource or f'page:{self.page_id}'
        return f'{self.kind} {label} ({self.status})'

    def mark_running(self):
        self.status = self.STATUS_RUNNING
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])

    def mark_success(self, message='', stats=None):
        self.status = self.STATUS_SUCCESS
        self.message = message
        self.stats = stats
        self.error_detail = ''
        self.finished_at = timezone.now()
        self.save(update_fields=['status', 'message', 'stats', 'error_detail', 'finished_at'])

    def mark_failed(self, error_detail='', message=''):
        self.status = self.STATUS_FAILED
        self.error_detail = error_detail
        if message:
            self.message = message
        self.finished_at = timezone.now()
        self.save(update_fields=['status', 'error_detail', 'message', 'finished_at'])
