"""Restrict Wagtail Admin to ops when CMS_RESTRICT_WAGTAIL_ADMIN is enabled."""

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden


class RestrictWagtailAdminMiddleware:
    """When enabled, only superusers or cms_ops may use /admin/ (Wagtail)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "CMS_RESTRICT_WAGTAIL_ADMIN", False):
            path = request.path
            if path.startswith("/admin/") and not path.startswith("/admin-django/"):
                user = request.user
                if not user.is_authenticated:
                    return redirect_to_login(request.get_full_path(), login_url=settings.LOGIN_URL)
                if not (user.is_superuser or user.groups.filter(name="cms_ops").exists()):
                    return HttpResponseForbidden(
                        "Wagtail Admin is restricted to system operators. "
                        "Use /cms/ for content editing."
                    )
        return self.get_response(request)
