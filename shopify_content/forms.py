"""Wagtail admin forms for shopify_content page types."""

from django import forms
from wagtail.admin.forms import WagtailAdminPageForm

from config.settings import ALLOWED_LOCALE_CODES


LOCALE_CHOICES = list(ALLOWED_LOCALE_CODES.items())


class AvailableLocalesPageForm(WagtailAdminPageForm):
    """Checkbox multi-select backed by the available_locales JSONField."""

    available_locales = forms.MultipleChoiceField(
        choices=LOCALE_CHOICES,
        required=False,
        label='Available locales',
        help_text='Markets/locales where this content should be available in the storefront.',
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if instance and getattr(instance, 'pk', None):
            current = getattr(instance, 'available_locales', None) or []
            if current:
                self.initial.setdefault('available_locales', current)
            elif instance.locale_id:
                self.initial.setdefault(
                    'available_locales',
                    [instance.locale.language_code],
                )

    def save(self, commit=True):
        page = super().save(commit=False)
        page.available_locales = list(self.cleaned_data.get('available_locales') or [])
        if commit:
            page.save()
        return page


class BlogPageForm(AvailableLocalesPageForm):
    pass


class ArticlePageForm(AvailableLocalesPageForm):
    pass
