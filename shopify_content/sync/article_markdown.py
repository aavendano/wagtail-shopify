"""Git-native Markdown adapter for ArticlePage outbound publication.

The legacy Article StreamField remains intact for db/mirror rollback. In
``git_authoritative`` mode, however, Article body is a Git-native editorial
field: ``body.md`` is read through the content-store domain and rendered to HTML
before the Shopify Article mutation. No StreamField conversion is attempted.
"""

from __future__ import annotations

from shopify_content.content_store.accessors import is_git_authoritative, resolve_editorial
from shopify_content.content_store.markdown_renderer import render_editorial_markdown

from . import outbound


def article_body_html(page) -> str:
    """Return the correct Shopify HTML representation for one ArticlePage."""
    if not is_git_authoritative():
        return outbound._render_streamfield_html(page.body)

    # resolve_editorial is the same boundary used by page.editorial.body. We use
    # the function here so the adapter does not require model inheritance during
    # Django app import ordering; ArticlePage exposes the canonical accessor too.
    markdown_source = resolve_editorial(page, "body")
    return render_editorial_markdown(markdown_source)


def _article_mutation_fields(page) -> dict:
    """Build ArticleCreateInput/ArticleUpdateInput with authority-aware body."""
    return {
        'title': page.title,
        'body': article_body_html(page),
        'summary': page.summary or '',
        'author': {'name': page.author or 'Author'},
        'tags': list(page.tags.values_list('name', flat=True)),
        'isPublished': page.live,
    }


def sync_article_page(page):
    """Publish ArticlePage, using Git Markdown body when Git is authoritative."""
    if not page.sync_enabled:
        return False

    parent_blog = page.get_parent().specific
    from ..models import BlogPage

    if not isinstance(parent_blog, BlogPage) or not parent_blog.shopify_id:
        outbound.logger.error(
            'ArticlePage pk=%s parent blog has no shopify_id. '
            'Publish the parent BlogPage first.',
            page.pk,
        )
        return False

    shop = outbound._get_shop()
    primary = outbound._resolve_primary_page(page)
    common_fields = _article_mutation_fields(primary)

    if page.shopify_id:
        variables = {'id': page.shopify_id, 'article': common_fields}
        result = outbound.execute_admin_graphql(
            outbound.ARTICLE_UPDATE,
            shop=shop,
            variables=variables,
        )
        mutation_key = 'articleUpdate'
    else:
        variables = {
            'article': {
                **common_fields,
                'blogId': parent_blog.shopify_id,
            }
        }
        result = outbound.execute_admin_graphql(
            outbound.ARTICLE_CREATE,
            shop=shop,
            variables=variables,
        )
        mutation_key = 'articleCreate'

    if not result.ok:
        detail = outbound._graphql_error_detail(result)
        outbound.logger.error(
            '%s failed shop=%s pk=%s error=%s detail=%s',
            mutation_key, shop, page.pk, result.error_code, detail,
        )
        return False

    mutation_data = (result.data or {}).get(mutation_key, {})
    user_errors = mutation_data.get('userErrors', [])
    if user_errors:
        outbound.logger.error(
            '%s userErrors pk=%s: %s', mutation_key, page.pk, user_errors
        )
        return False

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

    if page.shopify_id:
        outbound._push_seo_metafields(
            shop,
            page.shopify_id,
            primary.get_seo_title(),
            primary.get_seo_description(),
        )

        # Inline metafields remain relational/operational state in Django. The
        # old Article StreamField does not define a metafield block, but keep the
        # legacy extraction in db/mirror mode for backwards compatibility.
        mf_inputs = outbound._collect_inline_metafields(primary, page.shopify_id)
        if not is_git_authoritative():
            mf_inputs += outbound._collect_streamfield_metafields(
                primary.body, page.shopify_id
            )
        outbound._push_metafields(shop, mf_inputs)
        outbound._push_faq_metafield(shop, page.shopify_id, primary.faqs)
        outbound._push_internal_links_metafield(shop, page.shopify_id, primary)
        outbound._push_native_reference_metafields(shop, page.shopify_id, primary)

        from shopify_content.available_locales import default_available_locales_for_page

        locales = primary.available_locales or default_available_locales_for_page(primary)
        outbound._push_available_locales_metafield(shop, page.shopify_id, locales)
        outbound._register_shopify_translations(
            page,
            shop,
            page.shopify_id,
            {
                'title': 'title',
                'body_html': article_body_html,
                'summary_html': 'summary',
            },
        )

    outbound._mark_synced(type(page), page.pk)
    outbound._queue_index_sync_after_content_sync(page)
    return True


def install_article_markdown_sync() -> None:
    """Install the adapter at the existing outbound import surface."""
    if outbound.sync_article_page is not sync_article_page:
        outbound.sync_article_page = sync_article_page
