"""
Outbound sync: push Wagtail page content to Shopify Admin on publish.

Single-tenant design: shop is resolved from ShopConfig.objects.first().shop.
If sync fails, we log and return False — the publish is NOT blocked.

StreamField → HTML: each block is rendered via its template. HtmlBlock values
are used verbatim. MetafieldBlock blocks are extracted separately.

Article SEO: Shopify's Admin API has no native seo field on Article.
SEO is pushed as metafields: namespace=global, key=title_tag / description_tag.

hreflang metafields: after each sync, all live locale translations of a page
are pushed as metafields (namespace=seo, keys=hreflang_en_us, etc.) so the
Shopify Liquid theme can render <link rel="alternate"> tags.

Primary locale (en-US): outbound sync always pushes en-US content to the
primary Shopify resource, even when triggered from another locale. Non-primary
locales are registered via translationsRegister for every live variant in the
translation group (including the page that triggered sync).
"""

import json
import logging
import re
from django.utils import timezone
from django.utils.functional import SimpleLazyObject

from shopify_requests.graphql_service import execute_admin_graphql
from .mutations import (
    PRODUCT_UPDATE,
    COLLECTION_UPDATE,
    BLOG_CREATE,
    BLOG_UPDATE,
    ARTICLE_CREATE,
    ARTICLE_UPDATE,
    METAFIELDS_SET,
    TRANSLATIONS_REGISTER,
)

logger = logging.getLogger(__name__)


def _wagtail_field_value(value):
    """Normalize Wagtail RichText / plain values to a sync-ready scalar."""
    if value is None:
        return None
    source = getattr(value, 'source', None)
    if source is not None:
        return source
    return value


def _has_meaningful_sync_value(value) -> bool:
    coerced = _wagtail_field_value(value)
    if coerced is None:
        return False
    if isinstance(coerced, str):
        return bool(re.sub(r'<[^>]+>', '', coerced).strip())
    return bool(coerced)

PRIMARY_LOCALE = 'en-US'


def _graphql_error_detail(result):
    """Extract GraphQL error messages from SDK http_logs when available."""
    raw = getattr(result, "raw", None)
    if raw is None:
        return result.log_detail or ""
    for http_log in getattr(raw, "http_logs", None) or []:
        res = getattr(http_log, "res", None)
        body = getattr(res, "body", None) if res is not None else None
        if not body:
            continue
        try:
            payload = json.loads(body)
        except (TypeError, json.JSONDecodeError):
            continue
        errors = payload.get("errors") or []
        if errors:
            return "; ".join(
                err.get("message", str(err)) for err in errors if isinstance(err, dict)
            )
    return result.log_detail or ""


def _article_mutation_fields(page):
    """
    Build ArticleCreateInput / ArticleUpdateInput fields.

    Shopify does not accept publishedAt on write inputs; use isPublished only.
    published_at is kept on the Wagtail page for editorial use.
    """
    return {
        'title': page.title,
        'body': _render_streamfield_html(page.body),
        'summary': page.summary or '',
        'author': {'name': page.author or 'Author'},
        'tags': list(page.tags.values_list('name', flat=True)),
        'isPublished': page.live,
    }


def _get_shop():
    """Resolve shop from ShopConfig (single-tenant: always the first/only record)."""
    from core.models import ShopConfig
    config = ShopConfig.objects.first()
    if not config:
        raise RuntimeError(
            'No ShopConfig found. Install the app on a Shopify store first.'
        )
    return config.shop


def _render_streamfield_html(streamfield_value):
    """
    Render a StreamField value to an HTML string.
    MetafieldBlock blocks are excluded (they are sent via metafieldsSet separately).
    HtmlBlock values are included verbatim.
    """
    parts = []
    for block in streamfield_value:
        if block.block_type == 'metafield':
            continue
        try:
            parts.append(str(block.render_as_block()))
        except Exception:
            parts.append(str(block.value))
    return ''.join(parts)


def _collect_inline_metafields(page, owner_gid):
    """Collect InlinePanel metafield rows and format for metafieldsSet."""
    return [
        {
            'ownerId': owner_gid,
            'namespace': mf.namespace,
            'key': mf.key,
            'type': mf.type,
            'value': str(mf.value),
        }
        for mf in page.metafields.all()
    ]


def _collect_streamfield_metafields(body_value, owner_gid):
    """Extract MetafieldBlock blocks from a StreamField value."""
    inputs = []
    for block in body_value:
        if block.block_type == 'metafield':
            v = block.value
            inputs.append({
                'ownerId': owner_gid,
                'namespace': str(v.get('namespace', 'custom')),
                'key': str(v['key']),
                'type': str(v.get('type', 'single_line_text_field')),
                'value': str(v['value']),
            })
    return inputs


def _push_metafields(shop, metafield_inputs):
    """Issue metafieldsSet mutation. Returns True on success."""
    if not metafield_inputs:
        return True
    result = execute_admin_graphql(
        METAFIELDS_SET,
        shop=shop,
        variables={'metafields': metafield_inputs},
    )
    if not result.ok:
        logger.error('metafieldsSet failed shop=%s error=%s', shop, result.error_code)
        return False
    user_errors = (result.data or {}).get('metafieldsSet', {}).get('userErrors', [])
    if user_errors:
        logger.error('metafieldsSet userErrors: %s', user_errors)
        return False
    return True


def _push_faq_metafield(shop, owner_gid, faq_queryset):
    """
    Push FAQ items as a single JSON metafield custom.faqs.
    Value: [{"question": "...", "answer": "..."}, ...]
    """
    items = list(faq_queryset.order_by('sort_order'))
    if not items:
        return True
    faq_data = [{'question': f.question, 'answer': f.answer} for f in items]
    return _push_metafields(shop, [{
        'ownerId': owner_gid,
        'namespace': 'custom',
        'key': 'faqs',
        'type': 'json',
        'value': json.dumps(faq_data, ensure_ascii=False),
    }])


def _push_internal_links_metafield(shop, owner_gid, page):
    """Push semantic internal links as JSON metafield (default custom.internal_links)."""
    from django.conf import settings

    from shopify_content.semantic_links.serialization import serialize_semantic_links

    links = serialize_semantic_links(page)
    if not links:
        return True
    namespace = getattr(settings, 'SEMANTIC_LINKS_METAFIELD_NAMESPACE', 'custom')
    key = getattr(settings, 'SEMANTIC_LINKS_METAFIELD_KEY', 'internal_links')
    return _push_metafields(shop, [{
        'ownerId': owner_gid,
        'namespace': namespace,
        'key': key,
        'type': 'json',
        'value': json.dumps(links, ensure_ascii=False),
    }])


def _push_seo_metafields(shop, owner_gid, seo_title, seo_description):
    """
    Push SEO data as Shopify metafields.
    Used for Article and Blog which have no native seo field in Admin API.
    """
    inputs = []
    if seo_title:
        inputs.append({
            'ownerId': owner_gid,
            'namespace': 'global',
            'key': 'title_tag',
            'type': 'single_line_text_field',
            'value': seo_title,
        })
    if seo_description:
        inputs.append({
            'ownerId': owner_gid,
            'namespace': 'global',
            'key': 'description_tag',
            'type': 'single_line_text_field',
            'value': seo_description,
        })
    return _push_metafields(shop, inputs)


def _resolve_primary_page(page):
    """
    Return the en-US variant for primary Shopify resource content.

    When sync is triggered from a translated page (e.g. es-US), the primary
    Shopify resource should still receive en-US content. Falls back to `page`
    when no live en-US sibling exists in the translation group.
    """
    if page.locale.language_code == PRIMARY_LOCALE:
        return page
    try:
        en_us = (
            page.get_translations(inclusive=True)
            .filter(locale__language_code=PRIMARY_LOCALE, live=True)
            .select_related('locale')
            .first()
        )
        if en_us is not None:
            return en_us.specific
    except Exception:
        pass
    return page


def _live_translation_variants(page):
    """All live pages in the translation group, including the given page."""
    return page.get_translations(inclusive=True).live().select_related('locale')


def _translation_field_value(variant_page, getter):
    if callable(getter):
        return getter(variant_page)
    value = getattr(variant_page, getter, None) or ''
    if callable(value):
        value = value()
    return str(value) if value else ''


def _push_hreflang_metafields(page, shop, owner_gid):
    """
    Push alternate locale URLs as metafields for theme-side hreflang rendering.
    Metafield: namespace=seo, key=hreflang_{locale_code}, type=url, value=full URL.
    Only called when wagtail-localize translations exist.
    """
    try:
        inputs = []
        for t in _live_translation_variants(page):
            lang_key = t.locale.language_code.replace('-', '_').lower()
            url = t.full_url
            if url:
                inputs.append({
                    'ownerId': owner_gid,
                    'namespace': 'seo',
                    'key': f'hreflang_{lang_key}',
                    'type': 'url',
                    'value': url,
                })
        _push_metafields(shop, inputs)
    except Exception:
        # Translations may not be set up yet; skip silently
        pass


def _register_shopify_translations(page, shop, resource_id, translatable_fields):
    """
    Push translated field values to Shopify via translationsRegister mutation.

    Registers every live non-primary locale in the translation group, including
    the page that triggered sync (not only its siblings).

    translatable_fields: dict of {shopify_key: getter}
      getter can be:
        - str  → attribute name on the translation page (field or method)
        - callable(translation_page) → str value

    Shopify locale codes: 'es' (es-US), 'en-CA', 'fr-CA'. Primary locale (en-US) is skipped.
    """
    try:
        for variant in _live_translation_variants(page):
            shopify_locale = _wagtail_locale_to_shopify(variant.locale.language_code)
            if not shopify_locale:
                continue

            specific = variant.specific
            translation_inputs = []
            for shopify_key, getter in translatable_fields.items():
                value = _translation_field_value(specific, getter)
                if value:
                    translation_inputs.append({
                        'key': shopify_key,
                        'locale': shopify_locale,
                        'value': value,
                    })

            if translation_inputs:
                result = execute_admin_graphql(
                    TRANSLATIONS_REGISTER,
                    shop=shop,
                    variables={
                        'resourceId': resource_id,
                        'translations': translation_inputs,
                    },
                )
                if not result.ok:
                    logger.warning(
                        'translationsRegister failed locale=%s resource=%s error=%s',
                        shopify_locale, resource_id, result.error_code,
                    )
    except Exception as exc:
        logger.warning('Translation push skipped: %s', exc)


def _wagtail_locale_to_shopify(language_code):
    """
    Convert Wagtail locale code to Shopify locale code.
    Shopify uses BCP 47 but often just 2-letter: en, es, fr.
    en-US → en (primary, not registered as translation)
    es-US → es
    en-CA → en-CA
    fr-CA → fr-CA
    Returns None for the primary locale (should not be registered as translation).
    """
    mapping = {
        'en-US': None,   # primary — skip
        'es-US': 'es',
        'en-CA': 'en-CA',
        'fr-CA': 'fr-CA',
    }
    return mapping.get(language_code)


def _mark_synced(model_class, pk):
    """Update last_synced_at without triggering signals."""
    model_class.objects.filter(pk=pk).update(last_synced_at=timezone.now())


# ---------------------------------------------------------------------------
# Public sync functions — called from wagtail_hooks.py
# ---------------------------------------------------------------------------

def sync_product_page(page):
    """
    Push ProductPage → Shopify productUpdate.
    Products must already exist in Shopify (inbound import populates shopify_id).
    Returns True on success, False on failure.
    """
    if not page.shopify_id:
        logger.warning(
            'ProductPage pk=%s has no shopify_id; skipping sync. '
            'Run import_shopify_products first.',
            page.pk,
        )
        return False
    if not page.sync_enabled:
        return False

    shop = _get_shop()
    primary = _resolve_primary_page(page)
    shopify_id = page.shopify_id
    body_html = _render_streamfield_html(primary.body)

    variables = {
        'input': {
            'id': shopify_id,
            'title': primary.title,
            'descriptionHtml': body_html,
            'vendor': primary.vendor,
            'productType': primary.product_type,
            'tags': list(primary.tags.values_list('name', flat=True)),
            'status': primary.status,
            'seo': {
                'title': primary.get_seo_title(),
                'description': primary.get_seo_description(),
            },
        }
    }

    result = execute_admin_graphql(PRODUCT_UPDATE, shop=shop, variables=variables)
    if not result.ok:
        logger.error(
            'productUpdate failed shop=%s pk=%s error=%s detail=%s',
            shop, page.pk, result.error_code, result.log_detail,
        )
        return False

    user_errors = (result.data or {}).get('productUpdate', {}).get('userErrors', [])
    if user_errors:
        logger.error('productUpdate userErrors pk=%s: %s', page.pk, user_errors)
        return False

    # Metafields (inline panel + streamfield blocks)
    mf_inputs = _collect_inline_metafields(primary, shopify_id)
    mf_inputs += _collect_streamfield_metafields(primary.body, shopify_id)
    _push_metafields(shop, mf_inputs)
    _push_faq_metafield(shop, shopify_id, primary.faqs)
    _push_internal_links_metafield(shop, shopify_id, primary)
    _push_hreflang_metafields(page, shop, shopify_id)
    _register_shopify_translations(
        page, shop, shopify_id,
        {
            'title': 'title',
            'body_html': lambda t: _render_streamfield_html(t.body),
        },
    )

    _mark_synced(type(page), page.pk)
    return True


def sync_collection_page(page):
    """Push CollectionPage → Shopify collectionUpdate."""
    if not page.shopify_id:
        logger.warning('CollectionPage pk=%s has no shopify_id; skipping.', page.pk)
        return False
    if not page.sync_enabled:
        return False

    shop = _get_shop()
    primary = _resolve_primary_page(page)
    shopify_id = page.shopify_id
    description_html = _render_streamfield_html(primary.description)

    variables = {
        'input': {
            'id': shopify_id,
            'title': primary.title,
            'descriptionHtml': description_html,
            'seo': {
                'title': primary.get_seo_title(),
                'description': primary.get_seo_description(),
            },
        }
    }

    result = execute_admin_graphql(COLLECTION_UPDATE, shop=shop, variables=variables)
    if not result.ok:
        detail = _graphql_error_detail(result)
        logger.error(
            'collectionUpdate failed shop=%s pk=%s error=%s detail=%s',
            shop, page.pk, result.error_code, detail,
        )
        return False

    user_errors = (result.data or {}).get('collectionUpdate', {}).get('userErrors', [])
    if user_errors:
        logger.error('collectionUpdate userErrors pk=%s: %s', page.pk, user_errors)
        return False

    mf_inputs = _collect_inline_metafields(primary, shopify_id)
    _push_metafields(shop, mf_inputs)
    _push_faq_metafield(shop, shopify_id, primary.faqs)
    _push_internal_links_metafield(shop, shopify_id, primary)
    _push_hreflang_metafields(page, shop, shopify_id)
    _register_shopify_translations(
        page, shop, shopify_id,
        {
            'title': 'title',
            'body_html': lambda t: _render_streamfield_html(t.description),
        },
    )
    _mark_synced(type(page), page.pk)
    return True


def sync_blog_page(page):
    """
    Push BlogPage → Shopify blogCreate or blogUpdate.
    Creates in Shopify if shopify_id is empty, updates otherwise.
    """
    if not page.sync_enabled:
        return False

    shop = _get_shop()
    primary = _resolve_primary_page(page)

    if page.shopify_id:
        variables = {
            'id': page.shopify_id,
            'blog': {
                'title': primary.title,
                'handle': primary.handle or None,
                'commentPolicy': primary.comment_policy,
            },
        }
        result = execute_admin_graphql(BLOG_UPDATE, shop=shop, variables=variables)
        mutation_key = 'blogUpdate'
    else:
        variables = {
            'blog': {
                'title': primary.title,
                'handle': primary.handle or None,
                'commentPolicy': primary.comment_policy,
            },
        }
        result = execute_admin_graphql(BLOG_CREATE, shop=shop, variables=variables)
        mutation_key = 'blogCreate'

    if not result.ok:
        logger.error(
            '%s failed shop=%s pk=%s error=%s',
            mutation_key, shop, page.pk, result.error_code,
        )
        return False

    mutation_data = (result.data or {}).get(mutation_key, {})
    user_errors = mutation_data.get('userErrors', [])
    if user_errors:
        logger.error('%s userErrors pk=%s: %s', mutation_key, page.pk, user_errors)
        return False

    # Persist shopify_id on first create
    if not page.shopify_id:
        returned = mutation_data.get('blog', {})
        new_id = returned.get('id')
        new_handle = returned.get('handle')
        if new_id:
            type(page).objects.filter(pk=page.pk).update(
                shopify_id=new_id,
                handle=new_handle or page.handle,
            )
            page.shopify_id = new_id

    # Blog has no native description or seo fields — push as metafields
    if page.shopify_id:
        blog_metafields = []
        if primary.description:
            blog_metafields.append({
                'ownerId': page.shopify_id,
                'namespace': 'descriptors',
                'key': 'description',
                'type': 'rich_text_field',
                'value': primary.description,
            })
        _push_metafields(shop, blog_metafields)
        _push_faq_metafield(shop, page.shopify_id, primary.faqs)
        _push_seo_metafields(
            shop, page.shopify_id,
            primary.get_seo_title(),
            primary.get_seo_description(),
        )

    _mark_synced(type(page), page.pk)
    return True


def sync_article_page(page):
    """
    Push ArticlePage → Shopify articleCreate or articleUpdate.
    Creates in Shopify if shopify_id is empty.
    Requires parent BlogPage to have a shopify_id.
    """
    if not page.sync_enabled:
        return False

    # Ensure parent blog is synced first
    parent_blog = page.get_parent().specific
    from ..models import BlogPage
    if not isinstance(parent_blog, BlogPage) or not parent_blog.shopify_id:
        logger.error(
            'ArticlePage pk=%s parent blog has no shopify_id. '
            'Publish the parent BlogPage first.',
            page.pk,
        )
        return False

    shop = _get_shop()
    primary = _resolve_primary_page(page)
    common_fields = _article_mutation_fields(primary)

    if page.shopify_id:
        variables = {'id': page.shopify_id, 'article': common_fields}
        result = execute_admin_graphql(ARTICLE_UPDATE, shop=shop, variables=variables)
        mutation_key = 'articleUpdate'
    else:
        variables = {
            'article': {
                **common_fields,
                'blogId': parent_blog.shopify_id,
            }
        }
        result = execute_admin_graphql(ARTICLE_CREATE, shop=shop, variables=variables)
        mutation_key = 'articleCreate'

    if not result.ok:
        detail = _graphql_error_detail(result)
        logger.error(
            '%s failed shop=%s pk=%s error=%s detail=%s',
            mutation_key, shop, page.pk, result.error_code, detail,
        )
        return False

    mutation_data = (result.data or {}).get(mutation_key, {})
    user_errors = mutation_data.get('userErrors', [])
    if user_errors:
        logger.error('%s userErrors pk=%s: %s', mutation_key, page.pk, user_errors)
        return False

    # Persist shopify_id on first create
    if not page.shopify_id:
        returned = mutation_data.get('article', {})
        new_id = returned.get('id')
        new_handle = returned.get('handle')
        if new_id:
            type(page).objects.filter(pk=page.pk).update(
                shopify_id=new_id,
                handle=new_handle or page.handle,
            )
            page.shopify_id = new_id

    # SEO via metafields (Article has no native seo in Shopify API)
    if page.shopify_id:
        _push_seo_metafields(
            shop, page.shopify_id,
            primary.get_seo_title(),
            primary.get_seo_description(),
        )

        # Additional inline metafields
        mf_inputs = _collect_inline_metafields(primary, page.shopify_id)
        mf_inputs += _collect_streamfield_metafields(primary.body, page.shopify_id)
        _push_metafields(shop, mf_inputs)
        _push_faq_metafield(shop, page.shopify_id, primary.faqs)
        _push_internal_links_metafield(shop, page.shopify_id, primary)

        _push_hreflang_metafields(page, shop, page.shopify_id)
        _register_shopify_translations(
            page, shop, page.shopify_id,
            {
                'title': 'title',
                'body_html': lambda t: _render_streamfield_html(t.body),
                'summary_html': 'summary',
            },
        )

    _mark_synced(type(page), page.pk)
    return True


def _location_page_definition():
    """
    Build the MetaobjectDefinitionSpec for the merchant-owned local_page type.
    Called lazily so the import only happens at sync time.
    """
    from metaobjects.shopify_metaobjects.definition import MetaobjectDefinitionSpec, MetaobjectFieldSpec
    return MetaobjectDefinitionSpec(
        type='local_page',
        name='Location Page',
        description='Location-specific page content managed in Wagtail CMS',
        display_name_field='city',
        capabilities={
            'publishable': {'enabled': True},
            'onlineStore': {'enabled': True, 'data': {'urlHandle': 'location'}},
            'renderable': {'enabled': True, 'data': {
                'metaTitleKey': 'meta_titulo',
                'metaDescriptionKey': 'meta_descripcion',
            }},
        },
        access={'storefront': 'PUBLIC_READ'},
        fields=[
            MetaobjectFieldSpec(key='titulo',                 name='Título',                type='single_line_text_field', required=True),
            MetaobjectFieldSpec(key='subtitulo',              name='Subtítulo',             type='single_line_text_field'),
            MetaobjectFieldSpec(key='intro',                  name='Intro',                 type='rich_text_field'),
            MetaobjectFieldSpec(key='country',                name='Country',               type='single_line_text_field'),
            MetaobjectFieldSpec(key='state',                  name='State / Province',      type='single_line_text_field'),
            MetaobjectFieldSpec(key='city',                   name='City',                  type='single_line_text_field'),
            MetaobjectFieldSpec(key='slug',                   name='Slug',                  type='single_line_text_field'),
            MetaobjectFieldSpec(key='titulo_2',               name='Título 2',              type='single_line_text_field'),
            MetaobjectFieldSpec(key='subtitulo_h2',           name='Subtítulo H2',          type='single_line_text_field'),
            MetaobjectFieldSpec(key='content_2',              name='Content 2',             type='rich_text_field'),
            MetaobjectFieldSpec(key='titulo_3',               name='Título 3',              type='single_line_text_field'),
            MetaobjectFieldSpec(key='subtitulo_3',            name='Subtítulo 3',           type='single_line_text_field'),
            MetaobjectFieldSpec(key='content_3',              name='Content 3',             type='rich_text_field'),
            MetaobjectFieldSpec(key='brand_section_title',    name='Brand Section Title',   type='single_line_text_field'),
            MetaobjectFieldSpec(key='brand_section_subtitle', name='Brand Section Subtitle',type='single_line_text_field'),
            MetaobjectFieldSpec(key='brand_section_content',  name='Brand Section Content', type='rich_text_field'),
            MetaobjectFieldSpec(key='map_title',              name='Map Title',             type='single_line_text_field'),
            MetaobjectFieldSpec(key='map_content',            name='Map Content',           type='rich_text_field'),
            MetaobjectFieldSpec(key='after_page_content',     name='After Page Content',    type='rich_text_field'),
            MetaobjectFieldSpec(key='faqs',                   name='FAQs',                  type='json'),
            MetaobjectFieldSpec(key='locale',                 name='Locale',               type='single_line_text_field'),
            MetaobjectFieldSpec(key='meta_titulo',            name='Meta Título',          type='single_line_text_field'),
            MetaobjectFieldSpec(key='meta_descripcion',       name='Meta Descripción',     type='single_line_text_field'),
        ],
    )


def _resolve_location_shopify_id(client, page, canonical: str) -> str | None:
    """
    Resolve the Shopify metaobject GID to update in place.

    When shopify_id is stored, always update that record (including handle renames).
    Otherwise, look up a legacy handle still stored on the Wagtail page.
    """
    if page.shopify_id:
        return page.shopify_id

    legacy_handle = (page.handle or page.slug or '').strip()
    if not legacy_handle or legacy_handle == canonical:
        return None

    existing = client.get_by_handle('local_page', legacy_handle)
    if existing and existing.id:
        return existing.id
    return None


def sync_location_page(page):
    """
    Push LocationPage → Shopify merchant-owned metaobject (type: local_page).

    Returns (success, message). Message is human-readable and safe for API clients.

    Uses MetaobjectClient.sync() which calls ensure_definition() on every sync
    (one extra GET per publish — safe and self-healing if definition is deleted).
    Handle and slug field are always derived as <locale>-<city>[-<state>] (e.g. en-us-glendale-arizona).
    When a Shopify GID or legacy handle exists, updates the same metaobject via
    metaobjectUpdate instead of creating a duplicate on handle rename.
    Rich text fields (RichTextField HTML) are converted to Shopify rich_text_field JSON.
    FAQs list is detected by to_shopify_fields() and serialized as json.dumps().
    """
    if not page.sync_enabled:
        return False, "Sync disabled: enable sync_enabled on this location page."

    try:
        shop = _get_shop()
    except RuntimeError as exc:
        return False, str(exc)

    from shopify_content.location_slug import location_page_slug

    canonical = location_page_slug(page)
    if not canonical:
        logger.error(
            'LocationPage sync aborted pk=%s: city and locale required for slug',
            page.pk,
        )
        return False, "Sync aborted: city and locale are required to build location slug."

    handle = canonical

    if not _has_meaningful_sync_value(page.titulo):
        logger.error('LocationPage sync aborted pk=%s: titulo is required', page.pk)
        return False, "Sync aborted: titulo is required."

    # Build field dict; always keep handle + slug + required titulo
    data: dict = {
        'handle': handle,
        'slug': handle,
        'titulo': str(_wagtail_field_value(page.titulo)).strip(),
    }
    for key, value in [
        ('subtitulo', page.subtitulo),
        ('intro', page.intro),
        ('country', page.country),
        ('state', page.state),
        ('city', page.city),
        ('titulo_2', page.titulo_2),
        ('subtitulo_h2', page.subtitulo_h2),
        ('content_2', page.content_2),
        ('titulo_3', page.titulo_3),
        ('subtitulo_3', page.subtitulo_3),
        ('content_3', page.content_3),
        ('brand_section_title', page.brand_section_title),
        ('brand_section_subtitle', page.brand_section_subtitle),
        ('brand_section_content', page.brand_section_content),
        ('map_title', page.map_title),
        ('map_content', page.map_content),
        ('after_page_content', page.after_page_content),
        ('meta_titulo', page.get_seo_title()),
        ('meta_descripcion', page.get_seo_description()),
    ]:
        if _has_meaningful_sync_value(value):
            data[key] = _wagtail_field_value(value)
    if page.shopify_locale:
        data['locale'] = page.shopify_locale
    faq_items = list(page.faqs.order_by('sort_order'))
    if faq_items:
        # Metaobject.to_shopify_fields() detects list → json.dumps() automatically
        data['faqs'] = [{'question': f.question, 'answer': f.answer} for f in faq_items]

    from metaobjects.shopify_metaobjects.client import MetaobjectClient
    from metaobjects.shopify_metaobjects.exceptions import DefinitionError, UpsertError

    spec = _location_page_definition()
    client = MetaobjectClient(shop=shop)
    existing_id = _resolve_location_shopify_id(client, page, canonical)

    try:
        result = client.sync(
            data,
            definition=spec,
            ensure_definition=True,
            validate=False,
            existing_id=existing_id,
        )
    except (DefinitionError, UpsertError) as exc:
        detail = str(exc)
        logger.error('LocationPage sync failed pk=%s: %s', page.pk, detail)
        return False, f"Shopify metaobject error: {detail}"

    updates = {}
    resolved_id = result.id or existing_id
    if resolved_id and page.shopify_id != resolved_id:
        updates['shopify_id'] = resolved_id
        page.shopify_id = resolved_id
    if page.slug != canonical:
        updates['slug'] = canonical
        page.slug = canonical
    if page.handle != canonical:
        updates['handle'] = canonical
        page.handle = canonical
    if updates:
        type(page).objects.filter(pk=page.pk).update(**updates)

    _mark_synced(type(page), page.pk)
    return True, "Location synced to Shopify metaobject successfully."


def _glossary_term_definition():
    """
    Build the MetaobjectDefinitionSpec for the merchant-owned glossary_term type.
    Called lazily so the import only happens at sync time.
    """
    from metaobjects.shopify_metaobjects.definition import MetaobjectDefinitionSpec, MetaobjectFieldSpec
    return MetaobjectDefinitionSpec(
        type='glossary_term',
        name='Glossary Term',
        description='Glossary term managed in Wagtail CMS',
        display_name_field='term',
        capabilities={
            'publishable': {'enabled': True},
            'onlineStore': {'enabled': True, 'data': {'urlHandle': 'glossary'}},
            'renderable': {'enabled': True, 'data': {
                'metaTitleKey': 'term',
                'metaDescriptionKey': 'definition',
            }},
        },
        access={'storefront': 'PUBLIC_READ'},
        fields=[
            MetaobjectFieldSpec(key='term', name='Term', type='single_line_text_field', required=True),
            MetaobjectFieldSpec(key='definition', name='Definition', type='rich_text_field'),
            MetaobjectFieldSpec(key='locale', name='Locale', type='single_line_text_field'),
            MetaobjectFieldSpec(key='related_links', name='Related Links', type='json'),
            MetaobjectFieldSpec(key='external_links', name='External Links', type='json'),
            MetaobjectFieldSpec(key='synonyms', name='Synonyms', type='list.single_line_text_field'),
            MetaobjectFieldSpec(key='same_as', name='Same As', type='list.url'),
        ],
    )


def sync_glossary_term_page(page):
    """
    Push GlossaryTermPage → Shopify merchant-owned metaobject (type: glossary_term).

    Returns (success, message). Message is human-readable and safe for API clients.

    Handle defaults to slugified term if page.handle is not set.
    related_links, external_links, synonyms, and same_as are omitted when empty.
    """
    if not page.sync_enabled:
        return False, "Sync disabled: enable sync_enabled on this glossary term page."

    try:
        shop = _get_shop()
    except RuntimeError as exc:
        return False, str(exc)

    from django.utils.text import slugify

    handle = page.handle or slugify(page.term)

    if not _has_meaningful_sync_value(page.term):
        logger.error('GlossaryTermPage sync aborted pk=%s: term is required', page.pk)
        return False, "Sync aborted: term is required."

    data: dict = {
        'handle': handle,
        'term': str(_wagtail_field_value(page.term)).strip(),
    }
    if _has_meaningful_sync_value(page.definition):
        data['definition'] = _wagtail_field_value(page.definition)
    if page.locale_code:
        data['locale'] = page.locale_code
    from shopify_content.semantic_links.serialization import serialize_semantic_links

    related_links = serialize_semantic_links(page)
    if related_links:
        data['related_links'] = related_links
    elif page.related_links:
        data['related_links'] = page.related_links
    if page.external_links:
        data['external_links'] = page.external_links
    if page.synonyms:
        data['synonyms'] = page.synonyms
    if page.same_as:
        data['same_as'] = page.same_as

    from metaobjects.shopify_metaobjects.client import MetaobjectClient
    from metaobjects.shopify_metaobjects.exceptions import DefinitionError, UpsertError

    spec = _glossary_term_definition()
    client = MetaobjectClient(shop=shop)

    try:
        result = client.sync(data, definition=spec, ensure_definition=True, validate=False)
    except (DefinitionError, UpsertError) as exc:
        detail = str(exc)
        logger.error('GlossaryTermPage sync failed pk=%s: %s', page.pk, detail)
        return False, f"Shopify metaobject error: {detail}"

    if result.id and not page.shopify_id:
        type(page).objects.filter(pk=page.pk).update(shopify_id=result.id)
        page.shopify_id = result.id

    _mark_synced(type(page), page.pk)
    return True, "Glossary term synced to Shopify metaobject successfully."
