from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from shopify_config.models import ShopConfig, ShopMembership

User = get_user_model()


@admin.register(ShopConfig)
class ShopConfigAdmin(admin.ModelAdmin):
    list_display = ("shop", "is_online", "expires", "scope")
    search_fields = ("shop",)


class ShopMembershipInline(admin.TabularInline):
    model = ShopMembership
    extra = 0
    fields = ("shop", "role")


# Re-register User with membership inline when the default UserAdmin is present.
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [ShopMembershipInline]


@admin.register(ShopMembership)
class ShopMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "shop", "role", "updated_at")
    search_fields = ("user__username", "user__email", "shop")
    list_filter = ("role", "shop")
    raw_id_fields = ("user",)
