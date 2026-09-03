from django.db import models


def default_layout():
    """Default Puck layout envelope for a Workbench SPA."""
    return {
        "root": {"props": {}},
        "content": [],
        "zones": {},
        "pages": {
            "/": {"version": 1, "content": []},
        },
    }


class SpaMount(models.Model):
    """Abstract-ish base for mounting a merchant SPA under a URL prefix.

    Concrete subclasses (e.g. CmsSpaMount) own the table so each product can
    customize bootstrap / layout without multi-tenant coupling.
    """

    slug = models.SlugField(unique=True, max_length=64)
    title = models.CharField(max_length=255, blank=True, default="")
    url_prefix = models.SlugField(
        max_length=64,
        help_text="URL prefix without leading/trailing slashes (e.g. 'cms').",
    )
    editor_app = models.SlugField(
        max_length=64,
        default="cms",
        help_text="Frontend editor app key used by VisualEditorAdminMixin.",
    )
    layout = models.JSONField(default=default_layout, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["slug"]

    def __str__(self):
        return self.title or self.slug

    def get_bootstrap(self, request=None):
        """JSON payload injected into the SPA shell."""
        return {
            "slug": self.slug,
            "urlPrefix": self.url_prefix,
            "layout": self.layout or default_layout(),
        }
