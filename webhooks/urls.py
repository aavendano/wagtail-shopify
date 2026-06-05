from django.urls import path

from . import views

app_name = "webhooks"

urlpatterns = [
    path("app/uninstalled", views.app_uninstalled, name="app-uninstalled"),
    path("app/scopes_update", views.app_scopes_update, name="app-scopes-update"),
]
