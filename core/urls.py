from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("install", views.PublicEntryView.as_view(), name="install"),
    path("auth/login", views.AuthLoginView.as_view(), name="auth-login"),
    path("patch-id-token", views.AuthPatchIdTokenView.as_view(), name="patch-id-token"),
    path("auth/embedded/redirect", views.EmbeddedInAppRedirectView.as_view(), name="auth-embedded-redirect",),
    path("auth/embedded/parent-redirect", views.EmbeddedParentRedirectView.as_view(), name="auth-embedded-parent-redirect",),
]
