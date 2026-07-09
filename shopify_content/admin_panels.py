from wagtail.admin.panels import InlinePanel, MultiFieldPanel, Panel


class StorefrontUrlsPanel(Panel):
    """Read-only panel listing Shopify storefront paths for the current page."""

    def __init__(self, **kwargs):
        kwargs.setdefault('heading', 'Storefront URLs')
        kwargs.setdefault('classname', 'storefront-urls-panel')
        kwargs.setdefault(
            'help_text',
            (
                'Rutas públicas en la tienda Shopify (no la URL del CMS Wagtail). '
                'El dominio depende de Markets; usa estas rutas para correlacionar con GSC.'
            ),
        )
        super().__init__(**kwargs)

    class BoundPanel(Panel.BoundPanel):
        template_name = 'shopify_content/panels/storefront_urls.html'

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)
            from shopify_content.storefront_url_display import get_storefront_url_display

            context['storefront_display'] = get_storefront_url_display(self.instance)
            return context


def _typed_ai_chooser_panel(relation_name, *, heading, label, type_key, vector_index='PageIndex'):
    from wagtail_ai.panels import AIMultipleChooserPanel

    class TypedAIMultipleChooserPanel(AIMultipleChooserPanel):
        _relation_name = relation_name
        _heading = heading
        _label = label
        _type_key = type_key
        _vector_index = vector_index

        def __init__(self, *args, **kwargs):
            relation_name = kwargs.pop('relation_name', self._relation_name)
            kwargs.setdefault('chooser_field_name', 'related_page')
            kwargs.setdefault('heading', self._heading)
            kwargs.setdefault('label', self._label)
            kwargs.setdefault('vector_index', self._vector_index)
            super().__init__(relation_name, *args, **kwargs)
            self.attrs = {
                **self.attrs,
                'data-wai-filter-type': self._type_key,
            }

    return TypedAIMultipleChooserPanel()


def semantic_links_panels():
    from django.conf import settings

    from shopify_content.semantic_links.constants import RELATION_CONFIG, SEMANTIC_LINK_RELATION_NAMES

    children = []
    for relation_name in SEMANTIC_LINK_RELATION_NAMES:
        config = RELATION_CONFIG[relation_name]
        if getattr(settings, 'WAGTAIL_AI_PGVECTOR', False):
            children.append(
                _typed_ai_chooser_panel(
                    relation_name,
                    heading=config['heading'],
                    label=config['label'],
                    type_key=config['type_key'],
                )
            )
        else:
            children.append(InlinePanel(relation_name, label=config['heading']))

    return MultiFieldPanel(children, heading='Internal Links')
