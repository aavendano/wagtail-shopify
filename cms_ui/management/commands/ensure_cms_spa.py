from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from cms_ui.models import CmsSpaMount, default_cms_layout
from cms_ui.spa_assets import cms_spa_asset_version


class Command(BaseCommand):
    help = "Ensure CMS SPA mount and cms_editors group exist."

    def handle(self, *args, **options):
        mount, created = CmsSpaMount.objects.get_or_create(
            slug="cms",
            defaults={
                "title": "Merchant CMS",
                "url_prefix": "cms",
                "editor_app": "cms",
                "layout": default_cms_layout(),
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created CmsSpaMount slug=cms"))
        else:
            self.stdout.write("CmsSpaMount slug=cms already exists")

        group, g_created = Group.objects.get_or_create(name="cms_editors")
        if g_created:
            self.stdout.write(self.style.SUCCESS("Created group cms_editors"))

        # Staff-level CMS access: grant change on CmsSpaMount is optional;
        # editors use /cms/ via session + is_staff or group membership.
        ct = ContentType.objects.get_for_model(CmsSpaMount)
        for codename in ("view_cmsspamount", "change_cmsspamount"):
            try:
                perm = Permission.objects.get(content_type=ct, codename=codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                pass

        visual = getattr(settings, "VISUAL_EDITOR", {}) or {}
        js_name = visual.get("SPA_PUBLIC_JS", "cms_ui/cms-embedded.js")
        css_name = visual.get("SPA_PUBLIC_CSS", "cms_ui/cms-embedded.css")
        static_dir = Path(settings.BASE_DIR) / "cms_ui" / "static" / "cms_ui"
        js_path = static_dir / Path(js_name).name
        css_path = static_dir / Path(css_name).name
        version = cms_spa_asset_version()

        if js_path.is_file() and css_path.is_file():
            self.stdout.write(
                self.style.SUCCESS(
                    f"Embedded UI assets OK ({js_name}, version {version}, "
                    f"{js_path.stat().st_size // 1024} KiB JS)"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Missing embedded UI assets. Expected:\n"
                    f"  {js_path}\n  {css_path}\n"
                    f"On production (systemd): run ./bin/build_cms_ui.sh then "
                    f"python manage.py collectstatic --noinput"
                )
            )

        self.stdout.write(self.style.SUCCESS("CMS SPA bootstrap complete."))
