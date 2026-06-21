
from django.contrib import admin
from django.urls import path, include
from core.views import HomeView, EmbeddedShopifySyncView

from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf import settings

from oauth2_provider import views as oauth2_views

from api.oauth_discovery import (
    OAuthProtectedResourceMetadataView,
    oauth_authorization_server_metadata,
)


from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from api.main import api

urlpatterns = [
    path("shopify-admin/", HomeView.as_view(), name="home"),
    path("shopify-admin", HomeView.as_view()),
    path("shopify-admin/sync/", EmbeddedShopifySyncView.as_view(), name="shopify_embedded_sync"),
    path("shopify-admin/sync", EmbeddedShopifySyncView.as_view()),
    path("core/", include("core.urls")),
    path("webhooks/", include("webhooks.urls")),
    # Root OAuth paths expected by MCP clients (Claude uses /authorize, not /o/authorize/).
    path("authorize", oauth2_views.AuthorizationView.as_view(), name="oauth2-authorize-root"),
    path("authorize/", oauth2_views.AuthorizationView.as_view(), name="oauth2-authorize-root-slash"),
    path("token", oauth2_views.TokenView.as_view(), name="oauth2-token-root"),
    path("token/", oauth2_views.TokenView.as_view(), name="oauth2-token-root-slash"),
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
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),

    path('api/v1/', api.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('admin-django/', admin.site.urls),
]



if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=settings.MEDIA_ROOT / 'images')
    urlpatterns += [
        path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'myapp/images/favicon.ico'))
    ]