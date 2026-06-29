from wagtail.admin.panels import InlinePanel, MultiFieldPanel


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
