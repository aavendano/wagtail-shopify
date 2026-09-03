from django.contrib import admin

from django_react_ui_editor.admin import VisualEditorAdminMixin

from .models import CmsSpaMount


@admin.register(CmsSpaMount)
class CmsSpaMountAdmin(VisualEditorAdminMixin, admin.ModelAdmin):
    editor_app = "cms"
    list_display = ("slug", "url_prefix", "editor_app")
    search_fields = ("slug", "url_prefix")
    readonly_fields = ()
