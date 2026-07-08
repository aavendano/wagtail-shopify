from django.db import models
from django.utils import timezone


class EmbeddedCommandRun(models.Model):
    """Tracks async management command jobs dispatched from the embedded Shopify app."""

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

    command_id = models.CharField(max_length=64, db_index=True)
    command_name = models.CharField(max_length=128)
    kwargs = models.JSONField(default=dict, blank=True)
    celery_task_id = models.CharField(max_length=255, blank=True, db_index=True)
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
    )
    message = models.TextField(blank=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    error_detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Embedded command run'
        verbose_name_plural = 'Embedded command runs'

    def __str__(self):
        return f'{self.command_id} ({self.status})'

    def mark_running(self):
        self.status = self.STATUS_RUNNING
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])

    def mark_success(self, message='', stdout='', stderr=''):
        self.status = self.STATUS_SUCCESS
        self.message = message
        self.stdout = stdout
        self.stderr = stderr
        self.error_detail = ''
        self.finished_at = timezone.now()
        self.save(
            update_fields=[
                'status',
                'message',
                'stdout',
                'stderr',
                'error_detail',
                'finished_at',
            ]
        )

    def mark_failed(self, error_detail='', message='', stdout='', stderr=''):
        self.status = self.STATUS_FAILED
        self.error_detail = error_detail
        if message:
            self.message = message
        self.stdout = stdout
        self.stderr = stderr
        self.finished_at = timezone.now()
        self.save(
            update_fields=[
                'status',
                'error_detail',
                'message',
                'stdout',
                'stderr',
                'finished_at',
            ]
        )
