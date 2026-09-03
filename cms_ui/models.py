from django_react_ui_editor.models import SpaMount, default_layout


class CmsSpaMount(SpaMount):
    """SPA mount for the merchant CMS workbench at /cms/."""

    class Meta:
        verbose_name = "CMS SPA"
        verbose_name_plural = "CMS SPAs"

    def get_bootstrap(self, request=None):
        return {
            "apiBase": "/api/v1",
            "loginUrl": "/admin-django/login/?next=/cms/",
            "adminDjangoUrl": "/admin-django/",
            "wagtailAdminUrl": "/admin/",
        }


def default_cms_layout():
    layout = default_layout()
    layout["pages"] = {
        "/": {"version": 1, "content": []},
        "/glossary": {"version": 1, "content": []},
        "/glossary/:id": {"version": 1, "content": []},
    }
    return layout
