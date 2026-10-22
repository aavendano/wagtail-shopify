"""Map editorial schema types to the Shopify type each channel uses.

ADR 0003 keeps one Wagtail site and two readers. Type strings live only here
so outbound sync does not keep a second copy. ``index`` is not a schema
``document.type``; it is the Liquid ``root_page`` contract. ``seo_collection``
is intentionally absent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ResourceClass = Literal['metaobject', 'native', 'none']


@dataclass(frozen=True)
class ChannelProjection:
    """One schema type (or the Liquid index key) on Wagtail and both channels.

    ``None`` means that surface does not write or read the type. Location keeps
    distinct handles on purpose (Wagtail/Liquid ``local_page``, Hydrogen
    ``location_page``). ``article`` is the native Article resource, not the
    merchant metaobject of the same name.
    """

    wagtail_model: str | None
    resource_class: ResourceClass
    wagtail_type: str | None
    hydrogen_type: str | None
    liquid_type: str | None
    wagtail_sync: bool


PROJECTIONS: dict[str, ChannelProjection] = {
    'location': ChannelProjection(
        wagtail_model='LocationPage',
        resource_class='metaobject',
        wagtail_type='local_page',
        hydrogen_type='location_page',
        liquid_type='local_page',
        wagtail_sync=True,
    ),
    'region': ChannelProjection(
        wagtail_model=None,
        resource_class='metaobject',
        wagtail_type=None,
        hydrogen_type='region',
        liquid_type=None,
        wagtail_sync=False,
    ),
    'glossary_term': ChannelProjection(
        wagtail_model='GlossaryTermPage',
        resource_class='metaobject',
        wagtail_type='glossary_term',
        hydrogen_type='glossary_term',
        liquid_type='glossary_term',
        wagtail_sync=True,
    ),
    'index': ChannelProjection(
        wagtail_model='ShopifyRootPage',
        resource_class='metaobject',
        wagtail_type='root_page',
        hydrogen_type=None,
        liquid_type='root_page',
        wagtail_sync=True,
    ),
    'home': ChannelProjection(
        wagtail_model='HomePage',
        resource_class='metaobject',
        wagtail_type='home_page',
        hydrogen_type='home_page',
        liquid_type='home_page',
        wagtail_sync=True,
    ),
    'product': ChannelProjection(
        wagtail_model='ProductPage',
        resource_class='native',
        wagtail_type='Product',
        hydrogen_type='Product',
        liquid_type='Product',
        wagtail_sync=True,
    ),
    'collection': ChannelProjection(
        wagtail_model='CollectionPage',
        resource_class='native',
        wagtail_type='Collection',
        hydrogen_type='Collection',
        liquid_type='Collection',
        wagtail_sync=True,
    ),
    'blog': ChannelProjection(
        wagtail_model='BlogPage',
        resource_class='native',
        wagtail_type='Blog',
        hydrogen_type='Blog',
        liquid_type='Blog',
        wagtail_sync=True,
    ),
    'article': ChannelProjection(
        wagtail_model='ArticlePage',
        resource_class='native',
        wagtail_type='Article',
        hydrogen_type='Article',
        liquid_type='Article',
        wagtail_sync=True,
    ),
    'page': ChannelProjection(
        wagtail_model=None,
        resource_class='native',
        wagtail_type=None,
        hydrogen_type='Page',
        liquid_type='Page',
        wagtail_sync=False,
    ),
}


def projection(schema_type: str) -> ChannelProjection:
    """Return the row for a schema ``document.type`` or the ``index`` key.

    Unknown keys raise KeyError so a merchant metaobject that is not in this
    matrix (for example ``seo_collection``) cannot be treated as synced.
    """
    return PROJECTIONS[schema_type]
