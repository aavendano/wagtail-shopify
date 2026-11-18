from django.urls import path

from .views import CmsSetLanguageView, CmsShellView

app_name = "cms_ui"

_shell = CmsShellView.as_view()

urlpatterns = [
    path("set-language/", CmsSetLanguageView.as_view(), name="set-language"),
    path("", _shell, name="spa-root"),
    path("<path:rest>", _shell, name="spa-rest"),
]
