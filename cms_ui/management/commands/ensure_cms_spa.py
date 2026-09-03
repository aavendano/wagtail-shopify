from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from cms_ui.models import CmsSpaMount, default_cms_layout


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

        self.stdout.write(self.style.SUCCESS("CMS SPA bootstrap complete."))
