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
    """Blog admin form.

    Under git_authoritative mode, `description` is READ_ONLY (D-012 / WRITE
    SEMANTICS): the authoritative value lives in Git and is edited through the
    Git workflow. The field is displayed disabled from the domain accessor so
    admin edits never become authoritative content.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from shopify_content.content_store.accessors import is_git_authoritative
        from shopify_content.content_store.contracts import ContentNotFound

        field = self.fields.get('description')
        if field is not None and is_git_authoritative():
            field.disabled = True
            field.help_text = (
                'Read-only: authoritative content is managed in Git '
                '(content/<locale>/…/description.md). Edit via the Git workflow.'
            )
            instance = self.instance
            if instance and getattr(instance, 'pk', None):
                try:
                    self.initial['description'] = instance.editorial.description
                except (ContentNotFound, Exception):
                    # Missing authoritative file: leave DB value as displayed
                    # fallback; authority resolution still raises for consumers.
                    pass


class ArticlePageForm(AvailableLocalesPageForm):
    pass
