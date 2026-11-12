from django.urls import path

from .views import CmsShellView

app_name = "cms_ui"

_shell = CmsShellView.as_view()

urlpatterns = [
    path("", _shell, name="spa-root"),
    path("<path:rest>", _shell, name="spa-rest"),
]
