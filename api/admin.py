from django.contrib import admin

from .models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'last_used_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'key')
    readonly_fields = ('key', 'created_at', 'last_used_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ('created_at', 'last_used_at')
