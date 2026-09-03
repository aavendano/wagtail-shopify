from __future__ import annotations

import json

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

from .spa_registry import get_registered_spas


class SpaShellView(TemplateView):
    """Serve the public SPA shell for a registered mount slug."""

    template_name = "django_react_ui_editor/spa_shell.html"
    mount_slug: str = ""

    def get_mount(self):
        slug = self.mount_slug or self.kwargs.get("mount_slug")
        if not slug:
            raise Http404("SPA mount slug not configured.")

        for reg in get_registered_spas().values():
            model = reg.mount_model
            try:
                mount = model.objects.get(slug=slug, is_active=True)
            except model.DoesNotExist:
                continue
            return mount, reg

        raise Http404(f"SPA mount '{slug}' not found.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mount, reg = self.get_mount()
        visual = getattr(settings, "VISUAL_EDITOR", {}) or {}
        public_js = visual.get("SPA_PUBLIC_JS", "cms_ui/spa-public.js")
        public_css = visual.get("SPA_PUBLIC_CSS", "cms_ui/spa-public.css")

        bootstrap = mount.get_bootstrap(self.request)
        bootstrap.setdefault("user", None)
        if self.request.user.is_authenticated:
            bootstrap["user"] = {
                "id": self.request.user.pk,
                "username": self.request.user.get_username(),
                "isStaff": self.request.user.is_staff,
                "isSuperuser": self.request.user.is_superuser,
            }

        context.update(
            {
                "mount": mount,
                "spa_title": mount.title or mount.slug,
                "spa_public_js": public_js,
                "spa_public_css": public_css,
                "spa_bootstrap_json": json.dumps(bootstrap),
                "url_prefix": reg.url_prefix,
            }
        )
        return context
