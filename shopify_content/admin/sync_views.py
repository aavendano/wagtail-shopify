"""
Wagtail admin views for manual Shopify inbound sync.
"""

import logging

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from wagtail.admin import messages as wagtail_messages
from wagtail.admin.views.generic import WagtailAdminTemplateMixin

from shopify_content.sync.service import (
    VALID_IMPORT_RESOURCES,
    import_error_count,
    run_shopify_import,
)

logger = logging.getLogger(__name__)


class ShopifySyncView(WagtailAdminTemplateMixin, TemplateView):
    """Settings page to import new Shopify content into Wagtail."""

    template_name = 'wagtailadmin/shopify_sync.html'
    page_title = 'Sincronizar desde Shopify'
    header_icon = 'download'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from core.models import ShopConfig

        config = ShopConfig.objects.first()
        context['shop_configured'] = bool(config and config.access_token)
        context['shop_domain'] = config.shop if config else None
        context['resources'] = [
            ('products', 'Importar productos nuevos'),
            ('collections', 'Importar colecciones nuevas'),
            ('blogs', 'Importar blogs y artículos nuevos'),
            ('all', 'Importar todo lo nuevo'),
        ]
        return context

    def post(self, request, *args, **kwargs):
        resource = request.POST.get('resource')
        if resource not in VALID_IMPORT_RESOURCES:
            wagtail_messages.error(request, 'Recurso de importación no válido.')
            return redirect(reverse('shopify_sync'))

        try:
            result = run_shopify_import(resource, new_only=True)
            stats = result['stats']
            errors = import_error_count(stats, resource)
            if errors > 0:
                wagtail_messages.warning(
                    request,
                    result['message'],
                    extra_tags='shopify-sync',
                )
            else:
                wagtail_messages.success(
                    request,
                    result['message'],
                    extra_tags='shopify-sync',
                )
        except RuntimeError as exc:
            wagtail_messages.error(request, str(exc), extra_tags='shopify-sync-error')
        except Exception:
            logger.exception('Shopify admin sync failed resource=%s', resource)
            wagtail_messages.error(
                request,
                (
                    'Error inesperado durante la importación. '
                    'Consulta los logs del servidor.'
                ),
                extra_tags='shopify-sync-error',
            )

        return redirect(reverse('shopify_sync'))
