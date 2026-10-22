from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic.base import RedirectView

from oauth2_provider import views as oauth2_views

from api.oauth_discovery import (
    OAuthProtectedResourceMetadataView,
    oauth_authorization_server_metadata,
)
from api.oauth_registration import OAuthDynamicClientRegistrationView
from api.main import api
from django_react_ui_editor.spa_registry import get_spa_urlpatterns
from shopify_admin.views import RootMenuView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls


def _legacy_core_redirect(target: str):
    return RedirectView.as_view(url=target, query_string=True, permanent=False)


urlpatterns = [
    path("", RootMenuView.as_view(), name="root"),
    path("shopify-admin/", include("shopify_admin.urls")),
    path(
        "shopify-admin",
        RedirectView.as_view(url="/shopify-admin/", query_string=True, permanent=False),
    ),
    # Legacy App Home alias (older App URL /app).
    path("app/", _legacy_core_redirect("/shopify-admin/")),
    path("app", _legacy_core_redirect("/shopify-admin/")),
    # Legacy /core/* auth paths → /shopify-admin/* (Partners / bookmarks).
    path("core/install", _legacy_core_redirect("/shopify-admin/install")),
    path("core/install/", _legacy_core_redirect("/shopify-admin/install/")),
    path("core/auth/login", _legacy_core_redirect("/shopify-admin/auth/login")),
    path("core/auth/login/", _legacy_core_redirect("/shopify-admin/auth/login/")),
    path("core/patch-id-token", _legacy_core_redirect("/shopify-admin/patch-id-token")),
    path("core/patch-id-token/", _legacy_core_redirect("/shopify-admin/patch-id-token/")),
    path(
        "core/auth/patch-id-token",
        _legacy_core_redirect("/shopify-admin/patch-id-token"),
    ),
    path(
        "core/auth/patch-id-token/",
        _legacy_core_redirect("/shopify-admin/patch-id-token/"),
    ),
    path(
        "core/auth/embedded/redirect",
        _legacy_core_redirect("/shopify-admin/auth/embedded/redirect"),
    ),
    path(
        "core/auth/embedded/redirect/",
        _legacy_core_redirect("/shopify-admin/auth/embedded/redirect/"),
    ),
    path(
        "core/auth/embedded/parent-redirect",
        _legacy_core_redirect("/shopify-admin/auth/embedded/parent-redirect"),
    ),
    path(
        "core/auth/embedded/parent-redirect/",
        _legacy_core_redirect("/shopify-admin/auth/embedded/parent-redirect/"),
    ),
    path("webhooks/", include("webhooks.urls")),
    # Root OAuth paths expected by MCP clients (Claude uses /authorize, not /o/authorize/).
    path("authorize", oauth2_views.AuthorizationView.as_view(), name="oauth2-authorize-root"),
    path("authorize/", oauth2_views.AuthorizationView.as_view(), name="oauth2-authorize-root-slash"),
    path("token", oauth2_views.TokenView.as_view(), name="oauth2-token-root"),
    path("token/", oauth2_views.TokenView.as_view(), name="oauth2-token-root-slash"),
    path("register", OAuthDynamicClientRegistrationView.as_view(), name="oauth2-register"),
    path("register/", OAuthDynamicClientRegistrationView.as_view(), name="oauth2-register-slash"),
    path(
        ".well-known/oauth-authorization-server",
        oauth_authorization_server_metadata,
        name="oauth2-authorization-server-metadata",
    ),
    path(
        ".well-known/oauth-protected-resource",
        OAuthProtectedResourceMetadataView.as_view(),
        name="oauth2-protected-resource-metadata",
    ),
    path(
        ".well-known/oauth-protected-resource/api/v1/mcp",
        OAuthProtectedResourceMetadataView.as_view(),
        name="oauth2-protected-resource-mcp",
    ),
    path(
        ".well-known/oauth-authorization-server/api/v1/mcp",
        oauth_authorization_server_metadata,
        name="oauth2-authorization-server-mcp",
    ),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("api/v1/", api.urls),
    *get_spa_urlpatterns(),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("admin-django/", admin.site.urls),
]

if "bigquery_gsc" in settings.INSTALLED_APPS:
    urlpatterns.append(path("api/gsc/", include("bigquery_gsc.urls")))


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + "images/", document_root=settings.MEDIA_ROOT / "images"
    )
    urlpatterns += [
        path(
            "favicon.ico",
            RedirectView.as_view(url=settings.STATIC_URL + "myapp/images/favicon.ico"),
        )
    ]
