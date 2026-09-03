import json

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html, escapejs


class VisualEditorAdminMixin:
    """Mixin that embeds a Puck workbench editor for SpaMount.layout."""

    editor_app = "cms"
    change_form_template = "django_react_ui_editor/admin_change_form.html"

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if "layout_editor" not in readonly:
            readonly.append("layout_editor")
        return readonly

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Ensure layout_editor appears even when ModelAdmin uses default fields.
        return fieldsets

    @admin.display(description="Workbench layout (Puck)")
    def layout_editor(self, obj):
        if not obj or not obj.pk:
            return "Guarda el mount una vez para abrir el editor visual."

        visual = getattr(settings, "VISUAL_EDITOR", {}) or {}
        editor_js = visual.get("EDITOR_JS", "cms_ui/editor.js")
        editor_css = visual.get("EDITOR_CSS", "cms_ui/editor.css")
        layout_json = json.dumps(obj.layout or {})
        return format_html(
            '<div id="visual-editor-root" data-editor-app="{}" data-mount-id="{}" '
            'data-layout-json="{}"></div>'
            '<link rel="stylesheet" href="{}{}">'
            '<script type="module" src="{}{}"></script>'
            '<p class="help">Edita el layout del Workbench. El JSON se guarda en el campo layout.</p>',
            self.editor_app,
            obj.pk,
            escapejs(layout_json),
            settings.STATIC_URL,
            editor_css,
            settings.STATIC_URL,
            editor_js,
        )
