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


class EditorialReadOnlyFormMixin:
    """Render migrated editorial fields READ_ONLY under git_authoritative mode.

    Representation-compatible fields display the authoritative Git value in the
    disabled legacy form control. Git-native fields (for example Article body
    Markdown replacing a StreamField) keep the old DB widget disabled without
    injecting the Markdown into it, because the two representations are not
    interchangeable.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from shopify_content.content_store.accessors import (
            EDITORIAL_FIELDS,
            GIT_NATIVE_FIELDS,
            is_git_authoritative,
        )

        if not is_git_authoritative():
            return
        instance = self.instance
        label = getattr(getattr(instance, '_meta', None), 'label_lower', None)
        if not label:
            return

        for content_type, field_key in EDITORIAL_FIELDS:
            if content_type != label:
                continue
            field = self.fields.get(field_key)
            if field is None:
                continue

            field.disabled = True
            key = (content_type, field_key)
            if key in GIT_NATIVE_FIELDS:
                field.help_text = (
                    'Read-only legacy field: production-authoritative content is '
                    f'Git Markdown at content/<locale>/…/{field_key}.md. '
                    'The value shown here is rollback/compatibility state only.'
                )
                continue

            field.help_text = (
                'Read-only: authoritative content is managed in Git '
                f'(content/<locale>/…/{field_key}.md). Edit via the Git workflow.'
            )
            if getattr(instance, 'pk', None):
                try:
                    self.initial[field_key] = getattr(instance.editorial, field_key)
                except Exception:
                    # Missing authoritative file: keep DB value as displayed
                    # fallback; authority resolution still raises for consumers.
                    pass


class BlogPageForm(EditorialReadOnlyFormMixin, AvailableLocalesPageForm):
    pass


class ArticlePageForm(EditorialReadOnlyFormMixin, AvailableLocalesPageForm):
    pass


class GlossaryTermPageForm(EditorialReadOnlyFormMixin, WagtailAdminPageForm):
    pass


class LocationPageForm(EditorialReadOnlyFormMixin, WagtailAdminPageForm):
    pass
