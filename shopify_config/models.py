from django.db import models


class ShopConfig(models.Model):
    shop = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    scope = models.TextField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token_expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "core_shopconfig"

    def __str__(self):
        return self.shop
