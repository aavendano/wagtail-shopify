from django.contrib.auth.decorators import login_required
from django.urls import path

from django_react_ui_editor.views import SpaShellView

app_name = "cms_ui"

_shell = login_required(
    SpaShellView.as_view(mount_slug="cms"),
    login_url="/admin-django/login/",
)

urlpatterns = [
    path("", _shell, name="spa-root"),
    path("<path:rest>", _shell, name="spa-rest"),
]
