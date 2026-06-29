from django import template

from shopify_content.semantic_links.serialization import (
    related_link_url,
    serialize_semantic_links_with_urls,
)

register = template.Library()

TYPE_HEADINGS = {
    'product': 'Related products',
    'collection': 'Related collections',
    'article': 'Related articles',
    'metaobject': 'Related glossary terms',
}


@register.inclusion_tag('shopify_content/includes/internal_links.html', takes_context=False)
def render_internal_links(page, group_by_type=True):
    links = serialize_semantic_links_with_urls(page)
    if not group_by_type:
        return {'links': links, 'groups': None}

    groups = []
    by_type: dict[str, list] = {}
    for link in links:
        by_type.setdefault(link['type'], []).append(link)

    for link_type, items in by_type.items():
        groups.append({
            'type': link_type,
            'heading': TYPE_HEADINGS.get(link_type, 'Related pages'),
            'links': items,
        })

    return {'links': links, 'groups': groups}


@register.simple_tag
def internal_link_url(link):
    return related_link_url(link)
