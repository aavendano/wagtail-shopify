from django.contrib import admin

from django_react_ui_editor.admin import VisualEditorAdminMixin

from .models import CmsSpaMount


@admin.register(CmsSpaMount)
class CmsSpaMountAdmin(VisualEditorAdminMixin, admin.ModelAdmin):
    editor_app = "cms"
    list_display = ("slug", "title", "url_prefix", "editor_app", "is_active")
    list_filter = ("is_active",)
    search_fields = ("slug", "title", "url_prefix")
    fields = (
        "slug",
        "title",
        "url_prefix",
        "editor_app",
        "is_active",
        "layout",
        "layout_editor",
    )
    readonly_fields = ("layout_editor",)
