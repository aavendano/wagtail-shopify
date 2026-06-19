from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'Content API'

    def ready(self):
        import api.ninja_compat  # noqa: F401
