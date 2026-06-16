
from django.contrib import admin
from django.urls import path, include
from core.views import HomeView, EmbeddedShopifySyncView

from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf import settings


from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from api.main import api

urlpatterns = [
    path("shopify-admin", HomeView.as_view(), name="home"),
    path("shopify-admin/sync", EmbeddedShopifySyncView.as_view(), name="shopify_embedded_sync"),
    path("core/", include("core.urls")),
    path("webhooks/", include("webhooks.urls")),

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