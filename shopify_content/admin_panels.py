from wagtail.admin.panels import InlinePanel


def semantic_links_panel(relation_name='semantic_links', heading='Internal Links'):
    from django.conf import settings

    if getattr(settings, 'WAGTAIL_AI_PGVECTOR', False):
        from wagtail_ai.panels import AIMultipleChooserPanel

        return AIMultipleChooserPanel(
            relation_name,
            chooser_field_name='related_page',
            heading=heading,
            label='Page',
            vector_index='PageIndex',
        )
    return InlinePanel(relation_name, label=heading)
