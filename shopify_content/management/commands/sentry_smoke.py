"""Send a test event to Sentry to verify the integration."""

from django.core.management.base import BaseCommand

import sentry_sdk


class Command(BaseCommand):
    help = "Send a test event to Sentry."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fail-celery",
            action="store_true",
            help="Also enqueue a deliberately failing Celery task to test worker reporting.",
        )

    def handle(self, *args, **options):
        sentry_sdk.capture_message("sentry_smoke: test event", level="info")
        self.stdout.write(self.style.SUCCESS("Test event sent to Sentry."))

        if options["fail_celery"]:
            from shopify_content.tasks import run_shopify_import_task

            # sync_run_id=0 does not exist → the task raises and Sentry captures it.
            run_shopify_import_task.delay(0, "products")
            self.stdout.write("Enqueued a failing Celery task (sync_run_id=0).")
