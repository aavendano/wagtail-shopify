from django.contrib import admin

from shopify_config.models import ShopConfig


@admin.register(ShopConfig)
class ShopConfigAdmin(admin.ModelAdmin):
    list_display = ("shop", "is_online", "expires", "scope")
    search_fields = ("shop",)
