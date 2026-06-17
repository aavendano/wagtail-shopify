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
"""

import json
import logging
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


def _push_hreflang_metafields(page, shop, owner_gid):
    """
    Push alternate locale URLs as metafields for theme-side hreflang rendering.
    Metafield: namespace=seo, key=hreflang_{locale_code}, type=url, value=full URL.
    Only called when wagtail-localize translations exist.
    """
    try:
        translations = page.get_translations().live().select_related('locale')
        inputs = []
        for t in translations:
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
        # Also include current page's own locale
        current_url = page.full_url
        if current_url:
            current_lang_key = page.locale.language_code.replace('-', '_').lower()
            inputs.append({
                'ownerId': owner_gid,
                'namespace': 'seo',
                'key': f'hreflang_{current_lang_key}',
                'type': 'url',
                'value': current_url,
            })
        _push_metafields(shop, inputs)
    except Exception:
        # Translations may not be set up yet; skip silently
        pass


def _register_shopify_translations(page, shop, resource_id, translatable_fields):
    """
    Push translated field values to Shopify via translationsRegister mutation.

    translatable_fields: dict of {shopify_key: getter}
      getter can be:
        - str  → attribute name on the translation page (field or method)
        - callable(translation_page) → str value

    Shopify locale codes: 'es' (es-US), 'en-CA', 'fr-CA'. Primary locale (en-US) is skipped.
    """
    try:
        translations = page.get_translations().live().select_related('locale')
        for t in translations:
            shopify_locale = _wagtail_locale_to_shopify(t.locale.language_code)
            if not shopify_locale:
                continue

            translation_inputs = []
            for shopify_key, getter in translatable_fields.items():
                if callable(getter):
                    value = getter(t)
                else:
                    value = getattr(t, getter, None) or ''
                    if callable(value):
                        value = value()
                value = str(value) if value else ''
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
    body_html = _render_streamfield_html(page.body)

    variables = {
        'input': {
            'id': page.shopify_id,
            'title': page.title,
            'descriptionHtml': body_html,
            'vendor': page.vendor,
            'productType': page.product_type,
            'tags': list(page.tags.values_list('name', flat=True)),
            'status': page.status,
            'seo': {
                'title': page.get_seo_title(),
                'description': page.get_seo_description(),
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
    mf_inputs = _collect_inline_metafields(page, page.shopify_id)
    mf_inputs += _collect_streamfield_metafields(page.body, page.shopify_id)
    _push_metafields(shop, mf_inputs)

    # hreflang metafields for Liquid theme
    _push_hreflang_metafields(page, shop, page.shopify_id)

    # Register Shopify translations for non-primary locales
    _register_shopify_translations(
        page, shop, page.shopify_id,
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
    description_html = _render_streamfield_html(page.description)

    variables = {
        'input': {
            'id': page.shopify_id,
            'title': page.title,
            'descriptionHtml': description_html,
            'seo': {
                'title': page.get_seo_title(),
                'description': page.get_seo_description(),
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

    mf_inputs = _collect_inline_metafields(page, page.shopify_id)
    _push_metafields(shop, mf_inputs)
    _push_hreflang_metafields(page, shop, page.shopify_id)
    _register_shopify_translations(
        page, shop, page.shopify_id,
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

    if page.shopify_id:
        variables = {
            'id': page.shopify_id,
            'blog': {
                'title': page.title,
                'handle': page.handle or None,
                'commentPolicy': page.comment_policy,
            },
        }
        result = execute_admin_graphql(BLOG_UPDATE, shop=shop, variables=variables)
        mutation_key = 'blogUpdate'
    else:
        variables = {
            'blog': {
                'title': page.title,
                'handle': page.handle or None,
                'commentPolicy': page.comment_policy,
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
        if page.description:
            blog_metafields.append({
                'ownerId': page.shopify_id,
                'namespace': 'descriptors',
                'key': 'description',
                'type': 'multi_line_text_field',
                'value': page.description,
            })
        _push_metafields(shop, blog_metafields)
        _push_seo_metafields(
            shop, page.shopify_id,
            page.get_seo_title(),
            page.get_seo_description(),
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
    common_fields = _article_mutation_fields(page)

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
            page.get_seo_title(),
            page.get_seo_description(),
        )

        # Additional inline metafields
        mf_inputs = _collect_inline_metafields(page, page.shopify_id)
        mf_inputs += _collect_streamfield_metafields(page.body, page.shopify_id)
        _push_metafields(shop, mf_inputs)

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
