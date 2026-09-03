from django.apps import AppConfig


class CmsUiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cms_ui"
    verbose_name = "CMS UI (Puck)"

    def ready(self):
        from django_react_ui_editor.spa_registry import register_spa

        from .models import CmsSpaMount

        register_spa(
            app_label="cms_ui",
            url_prefix="cms",
            urlconf="cms_ui.urls",
            mount_model=CmsSpaMount,
            mount_slug="cms",
        )
