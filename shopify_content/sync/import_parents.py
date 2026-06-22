"""
Resolve which ShopifyRootPage to use as the import parent per resource type.

When multiple ShopifyRootPage instances exist (e.g. slug=root vs slug=collections),
using .first() by PK sends all imports to the wrong tree branch.
"""

import logging
from typing import Literal, Optional

from wagtail.models import Locale, Page, Site

from ..models import ShopifyRootPage

logger = logging.getLogger(__name__)

ResourceType = Literal['products', 'collections', 'blogs', 'locations', 'glossary']

# Slugs reserved for single-resource ShopifyRootPage containers (not the main catalog root).
RESOURCE_CONTAINER_SLUGS = frozenset({'collections', 'blogs', 'local-us', 'glossary'})

# Preferred ShopifyRootPage slug per resource when multiple roots exist.
IMPORT_ROOT_SLUG = {
    'products': 'root',
    'collections': 'collections',
    'blogs': 'blogs',
    'locations': 'local-us',
    'glossary': 'glossary',
}

IMPORT_ROOT_TITLE = {
    'products': 'Root',
    'collections': 'Collections',
    'blogs': 'Blogs',
    'locations': 'Local US',
    'glossary': 'Glossary',
}


def _get_site_home_page() -> Page:
    """Return the default Wagtail site home page."""
    try:
        site = Site.objects.get(is_default_site=True)
    except Site.DoesNotExist as exc:
        raise RuntimeError(
            'No default Wagtail Site found. Run migrations and configure a site first.'
        ) from exc
    return site.root_page


def _create_shopify_import_root(resource_type: ResourceType) -> ShopifyRootPage:
    """Create and publish a ShopifyRootPage under the site home for the given resource type."""
    slug = IMPORT_ROOT_SLUG[resource_type]
    title = IMPORT_ROOT_TITLE[resource_type]
    home = _get_site_home_page()

    page = ShopifyRootPage(
        title=title,
        slug=slug,
        locale=Locale.get_default(),
    )
    home.add_child(instance=page)
    page.save_revision().publish()

    logger.info(
        'Created ShopifyRootPage slug=%s title=%s for resource_type=%s',
        slug,
        title,
        resource_type,
    )
    return page


def resolve_shopify_import_parent(
    resource_type: ResourceType,
    explicit_parent_id: Optional[int] = None,
    auto_create: bool = True,
) -> Page:
    """
    Return the ShopifyRootPage (or explicit parent) for inbound imports.

    explicit_parent_id overrides slug-based resolution (management command --parent-page-id).
    For locations, settings.LOCATIONS_PARENT_PAGE_ID is used when explicit_parent_id is omitted.
    When auto_create is True (default), creates the expected ShopifyRootPage if missing.
    """
    if explicit_parent_id is None and resource_type == 'locations':
        from django.conf import settings

        explicit_parent_id = getattr(settings, 'LOCATIONS_PARENT_PAGE_ID', None)

    if explicit_parent_id is not None:
        try:
            return Page.objects.get(pk=explicit_parent_id).specific
        except Page.DoesNotExist as exc:
            raise RuntimeError(
                f'Parent page id={explicit_parent_id} not found.'
            ) from exc

    preferred_slug = IMPORT_ROOT_SLUG[resource_type]
    parent = ShopifyRootPage.objects.filter(slug=preferred_slug).first()

    if parent is None and auto_create:
        parent = _create_shopify_import_root(resource_type)
    elif parent is None:
        raise RuntimeError(
            f'No ShopifyRootPage with slug="{preferred_slug}" found. '
            'Create one in Wagtail admin or run the import command without --parent-page-id.'
        )

    return parent


def ensure_child_of_import_parent(page: Page, parent_page: Page) -> bool:
    """
    Move page under parent_page when it was imported under a different root.
    Returns True if a move was performed.
    """
    current_parent = page.get_parent()
    if current_parent.pk == parent_page.pk:
        return False

    page.move(parent_page, pos='last-child')
    return True
