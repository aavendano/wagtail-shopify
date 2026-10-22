from django.urls import path

from . import views

app_name = "shopify_admin"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("sync/", views.EmbeddedShopifySyncView.as_view(), name="shopify_embedded_sync"),
    path("sync", views.EmbeddedShopifySyncView.as_view()),
    path(
        "commands/",
        views.EmbeddedCommandDispatchView.as_view(),
        name="shopify_embedded_command",
    ),
    path("commands", views.EmbeddedCommandDispatchView.as_view()),
    path("install", views.PublicEntryView.as_view(), name="install"),
    path("install/", views.PublicEntryView.as_view()),
    path("auth/login", views.AuthLoginView.as_view(), name="auth-login"),
    path("auth/login/", views.AuthLoginView.as_view()),
    path("patch-id-token", views.AuthPatchIdTokenView.as_view(), name="patch-id-token"),
    path("patch-id-token/", views.AuthPatchIdTokenView.as_view()),
    path(
        "auth/embedded/redirect",
        views.EmbeddedInAppRedirectView.as_view(),
        name="auth-embedded-redirect",
    ),
    path("auth/embedded/redirect/", views.EmbeddedInAppRedirectView.as_view()),
    path(
        "auth/embedded/parent-redirect",
        views.EmbeddedParentRedirectView.as_view(),
        name="auth-embedded-parent-redirect",
    ),
    path("auth/embedded/parent-redirect/", views.EmbeddedParentRedirectView.as_view()),
]
