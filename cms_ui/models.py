from django.conf import settings
from django.urls import reverse

from django_react_ui_editor.models import SpaMount, default_layout

from .shop_locales import fetch_shop_spa_locales
from .spa_locale import activate_request_language


class CmsSpaMount(SpaMount):
    """SPA mount for the merchant CMS workbench at /cms/."""

    class Meta:
        verbose_name = "CMS SPA"
        verbose_name_plural = "CMS SPAs"

    def get_bootstrap(self, request=None):
        data = super().get_bootstrap(request)
        locale_payload = fetch_shop_spa_locales()
        language = settings.LANGUAGE_CODE
        if request is not None:
            language = activate_request_language(request)
        data.update(
            {
                "apiBase": "/api/v1",
                "loginUrl": "/admin-django/login/?next=/cms/",
                "adminDjangoUrl": "/admin-django/",
                "wagtailAdminUrl": "/admin/",
                "resources": [
                    {"key": "glossary", "label": "Glossary", "path": "/glossary"},
                    {"key": "products", "label": "Products", "path": "/products"},
                    {"key": "collections", "label": "Collections", "path": "/collections"},
                    {"key": "blogs", "label": "Blogs", "path": "/blogs"},
                    {"key": "articles", "label": "Articles", "path": "/articles"},
                    {"key": "locations", "label": "Locations", "path": "/locations"},
                ],
                "language": language,
                "primaryLocale": locale_payload.get("primaryLocale"),
                "availableLocales": locale_payload.get("availableLocales") or [],
                "localeSource": locale_payload.get("source", "fallback"),
                "setLanguageUrl": reverse("cms_ui:set-language"),
                "localeStorageKey": "cms_ui_locale",
            }
        )
        return data


def default_cms_layout():
    layout = default_layout()
    layout["pages"] = {
        "/": {"version": 1, "content": []},
        "/glossary": {"version": 1, "content": []},
        "/glossary/:id": {"version": 1, "content": []},
        "/products": {"version": 1, "content": []},
        "/products/:id": {"version": 1, "content": []},
        "/collections": {"version": 1, "content": []},
        "/collections/:id": {"version": 1, "content": []},
        "/blogs": {"version": 1, "content": []},
        "/blogs/:id": {"version": 1, "content": []},
        "/articles": {"version": 1, "content": []},
        "/articles/:id": {"version": 1, "content": []},
        "/locations": {"version": 1, "content": []},
        "/locations/:id": {"version": 1, "content": []},
    }
    return layout
