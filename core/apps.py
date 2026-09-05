from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _ensure_test_superuser_on_migrate(sender, **kwargs):
    if sender.name != "django.contrib.auth":
        return
    from core.test_superuser import ensure_test_superuser

    ensure_test_superuser()


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        post_migrate.connect(_ensure_test_superuser_on_migrate)
