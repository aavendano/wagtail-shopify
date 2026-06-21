"""Wagtail admin shortcuts to Django admin (API keys and OAuth applications)."""

from wagtail import hooks
from wagtail.admin.menu import MenuItem

DJANGO_ADMIN = "/admin-django"


@hooks.register("register_settings_menu_item")
def register_api_keys_menu_item():
    return MenuItem(
        "API Keys",
        f"{DJANGO_ADMIN}/api/apikey/",
        icon_name="key",
        order=200,
    )


@hooks.register("register_settings_menu_item")
def register_oauth_applications_menu_item():
    return MenuItem(
        "OAuth Applications",
        f"{DJANGO_ADMIN}/oauth2_provider/application/",
        icon_name="lock",
        order=201,
    )
