import re

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import ShopConfig


SHOP_DOMAIN_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.myshopify\.com$")


class ShopConfigForm(ModelForm):
    shop = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "my-shop-domain.myshopify.com",
                "autocomplete": "on",
                "pattern": r"^[a-z0-9][a-z0-9-]*\.myshopify\.com$",
                "title": "Use format: your-store.myshopify.com",
                "style": "width: 100%; max-width: 420px; padding: 0.5rem; margin-bottom: 0.75rem;",
            }
        ),
    )

    class Meta:
        model = ShopConfig
        fields = ["shop"]

    def clean_shop(self):
        shop = (self.cleaned_data.get("shop") or "").strip().lower()
        if not SHOP_DOMAIN_RE.match(shop):
            raise ValidationError("Shop domain must match *.myshopify.com.")
        return shop