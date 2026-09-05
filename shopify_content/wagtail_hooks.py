"""
Wagtail hooks for shopify_content.

Outbound sync is queued via the page_published signal (all publish paths,
including bulk actions and API publish). These hooks only surface admin feedback.
"""

import logging

from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin import messages as wagtail_messages
from wagtail.admin.menu import MenuItem

from .admin.sync_views import ShopifySyncView
from .models.sync_run import ShopifySyncRun
from .sync.publish_sync import is_syncable_page

logger = logging.getLogger(__name__)


@hooks.register('insert_global_admin_js', order=1000)
def shopify_wai_chooser_patch_js():
    from django.utils.html import format_html
    from wagtail.admin.staticfiles import versioned_static

    return format_html(
        '<script src="{}"></script>',
        versioned_static('shopify_content/wai_chooser_patch.js'),
    )


@hooks.register('register_admin_urls')
def register_shopify_sync_urls():
    return [
        path('shopify-sync/', ShopifySyncView.as_view(), name='shopify_sync'),
    ]


@hooks.register('register_settings_menu_item')
def register_shopify_sync_menu_item():
    return MenuItem(
        'Shopify Sync',
        reverse('shopify_sync'),
        icon_name='download',
        order=100,
    )


def _latest_outbound_sync_run(page):
    return (
        page.shopify_sync_runs.filter(kind=ShopifySyncRun.KIND_OUTBOUND)
        .order_by('-created_at')
        .first()
    )


def _notify_sync_queued(request, page):
    sync_run = _latest_outbound_sync_run(page)
    if sync_run and sync_run.status in (
        ShopifySyncRun.STATUS_PENDING,
        ShopifySyncRun.STATUS_RUNNING,
        ShopifySyncRun.STATUS_SUCCESS,
    ):
        wagtail_messages.success(
            request,
            (
                f'"{page.title}" encolado para sincronizar con Shopify '
                f'(job id={sync_run.pk}).'
            ),
            extra_tags='shopify-sync',
        )
        return

    wagtail_messages.error(
        request,
        (
            f'No se pudo encolar la sincronización con Shopify para "{page.title}". '
            'La página se publicó localmente. Consulta los logs del servidor.'
        ),
        extra_tags='shopify-sync-error',
    )


@hooks.register('after_publish_page')
def notify_shopify_sync_on_publish(request, page):
    """Show admin feedback after single-page publish (sync queued via page_published)."""
    try:
        specific_page = page.specific
        if not is_syncable_page(page):
            return
        if not getattr(specific_page, 'sync_enabled', True):
            return

        _notify_sync_queued(request, page)
    except Exception:
        logger.exception(
            'after_publish_page feedback failed for page pk=%s',
            getattr(page, 'pk', None),
        )


@hooks.register('after_bulk_action')
def notify_shopify_sync_after_bulk_publish(request, action_type, objects, action_class_instance):
    """Show admin feedback after bulk publish (sync queued via page_published per page)."""
    if action_type != 'publish':
        return

    queued = 0
    failed = 0
    for page in objects:
        if not is_syncable_page(page):
            continue
        if not getattr(page.specific, 'sync_enabled', True):
            continue

        sync_run = _latest_outbound_sync_run(page)
        if sync_run and sync_run.status in (
            ShopifySyncRun.STATUS_PENDING,
            ShopifySyncRun.STATUS_RUNNING,
            ShopifySyncRun.STATUS_SUCCESS,
        ):
            queued += 1
        else:
            failed += 1
            logger.error(
                'Bulk publish: Shopify sync not queued for page pk=%s title=%r',
                page.pk,
                page.title,
            )

    if queued:
        wagtail_messages.success(
            request,
            (
                f'{queued} página(s) encolada(s) para sincronizar con Shopify '
                'tras la publicación masiva.'
            ),
            extra_tags='shopify-sync',
        )
    if failed:
        wagtail_messages.error(
            request,
            (
                f'No se pudo encolar la sincronización con Shopify para {failed} '
                'página(s). Consulta los logs del servidor.'
            ),
            extra_tags='shopify-sync-error',
        )


# ---------------------------------------------------------------------------
# HomePage: Locale-aware page chooser for GlossaryTermPage
# ---------------------------------------------------------------------------

from wagtail.admin.views.pages.edit import EditView


class HomePageEditView(EditView):
    """
    Custom edit view for HomePage that stores the page's locale in the request
    so that LocaleAwarePageChooserBlock can access it when rendering StreamField blocks.
    """

    def get_edit_handler_class(self, request, instance):
        if instance and hasattr(instance, 'locale') and instance.locale:
            request.homepage_locale = instance.locale.language_code
            if hasattr(request, 'session'):
                request.session['homepage_locale'] = instance.locale.language_code
        return super().get_edit_handler_class(request, instance)


@hooks.register('register_page_editing_view')
def use_home_page_edit_view(page):
    """Register HomePageEditView for HomePage instances."""
    from shopify_content.models.home_page import HomePage
    if isinstance(page, HomePage):
        return HomePageEditView
    return None


@hooks.register('construct_page_chooser_queryset')
def filter_page_chooser_by_locale(pages, request):
    """
    Filter PageChooserBlock queryset by the current page's locale for HomePage editing.
    Only applies when editing a HomePage and only filters GlossaryTermPage.
    """
    from django.contrib.contenttypes.models import ContentType
    from wagtail.models import Page

    from shopify_content.models.glossary import GlossaryTermPage

    # Editor locale from HomePageEditView, session, or homepage_locale query param.
    # Do not use Wagtail chooser UI ``locale`` — that controls browse tree i18n.
    page_locale = getattr(request, 'homepage_locale', None)
    if not page_locale and hasattr(request, 'session'):
        page_locale = request.session.get('homepage_locale')
    if not page_locale:
        page_locale = request.GET.get('homepage_locale')

    if not page_locale:
        return pages

    from shopify_content.page_chooser_locale import (
        get_homepage_editor_locale,
        glossary_term_page_filter_q,
        maybe_include_glossary_root_at_chooser_root,
        maybe_set_glossary_browse_locale_override,
    )

    maybe_include_glossary_root_at_chooser_root(request)
    maybe_set_glossary_browse_locale_override(request)

    page_type_string = request.GET.get('page_type', '')
    desired_classes = []
    if page_type_string:
        for page_type in page_type_string.split(','):
            page_type = page_type.strip()
            if page_type == 'wagtailcore.page':
                desired_classes = [Page]
                break
            try:
                app_label, model_name = page_type.split('.')
                from django.apps import apps
                model = apps.get_model(app_label, model_name)
                if model and issubclass(model, Page):
                    desired_classes.append(model)
            except (ValueError, LookupError, ImportError):
                pass

    if not desired_classes:
        desired_classes = [Page]

    if GlossaryTermPage in desired_classes:
        editor_locale = get_homepage_editor_locale(request)
        if editor_locale is None:
            return pages

        glossary_ct = ContentType.objects.get_for_model(GlossaryTermPage)
        pages = pages.filter(glossary_term_page_filter_q(editor_locale, glossary_ct))

    return pages
