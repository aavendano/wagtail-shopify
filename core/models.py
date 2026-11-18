from django.db import models


class ShopConfig(models.Model):
    shop = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    is_online = models.BooleanField(default=False)  # Field name made lowercase.
    scope = models.TextField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)  # Field name made lowercase.
    refresh_token = models.CharField(max_length=255, blank=True, null=True)  # Field name made lowercase.
    refresh_token_expires = models.DateTimeField(blank=True, null=True)  # Field name made lowercase.
    cached_spa_locales = models.JSONField(default=list, blank=True)
    cached_spa_primary_locale = models.CharField(max_length=32, blank=True, default="")
    spa_locales_fetched_at = models.DateTimeField(null=True, blank=True)
