"""Create default django-celery-beat periodic tasks for Shopify sync."""
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    help = 'Create or update default Celery Beat schedules for Shopify sync (disabled by default).'

    def handle(self, *args, **options):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='3',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone=ZoneInfo(settings.TIME_ZONE),
        )

        task, created = PeriodicTask.objects.update_or_create(
            name='Importar contenido nuevo desde Shopify',
            defaults={
                'task': 'shopify_content.tasks.scheduled_import_new_content',
                'crontab': schedule,
                'enabled': False,
            },
        )

        verb = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{verb} periodic task "{task.name}" (enabled={task.enabled}). '
                'Enable it in Django Admin → Periodic tasks.'
            )
        )

        backfill_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='4',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone=ZoneInfo(settings.TIME_ZONE),
        )

        backfill_enabled = (
            getattr(settings, 'SEMANTIC_LINKS_ENABLED', False)
            and getattr(settings, 'SEMANTIC_LINKS_BACKFILL_SCHEDULE_ENABLED', True)
        )
        backfill_task, backfill_created = PeriodicTask.objects.update_or_create(
            name='Backfill semantic internal links',
            defaults={
                'task': 'shopify_content.tasks.backfill_semantic_links_task',
                'crontab': backfill_schedule,
                'enabled': backfill_enabled,
                'kwargs': '{"model": "all", "only_missing": true}',
            },
        )

        backfill_verb = 'Created' if backfill_created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{backfill_verb} periodic task "{backfill_task.name}" '
                f'(enabled={backfill_task.enabled}).'
            )
        )
