from ninja import NinjaAPI

from .auth import ApiKeyAuth
from .routers.products import router as products_router
from .routers.collections import router as collections_router
from .routers.blogs import router as blogs_router
from .routers.articles import router as articles_router

API_DESCRIPTION = """
# Wagtail-Shopify Content API

An **AI-agent-native tool registry** for autonomous content management across Wagtail CMS and Shopify.

## What This API Does

This API exposes Shopify store content (Products, Collections, Blogs, Articles) managed in Wagtail CMS.
AI agents use these endpoints to autonomously read, create, update, and synchronize content between
Wagtail and the Shopify storefront — without human intervention.

## Core Concepts

### Content Resources
- **Products** — Mirror Shopify Products. Agents update descriptions, SEO, metafields, and sync to storefront.
- **Collections** — Mirror Shopify Collections. Agents manage curated product groupings.
- **Blogs** — Mirror Shopify Blogs (containers for articles). Created in Shopify on first push.
- **Articles** — Mirror Shopify Articles nested inside a Blog. Require a synced parent Blog.

### Sync Model (Bidirectional)
Each resource has a `shopify_id` (Shopify GID) linking it to Shopify, a `sync_enabled` flag,
and a `last_synced_at` timestamp.

**Wagtail → Shopify (Outbound):**
- `PATCH /{resource}/{id}` with `publish=true` auto-syncs if `sync_enabled=true`.
- `POST /{resource}/{id}/push` explicitly pushes to Shopify at any time.

**Shopify → Wagtail (Inbound):**
- `POST /{resource}/pull` imports all resources from Shopify, creating/updating Wagtail pages.

### Typical Agent Workflow
1. `POST /products/pull` — import all Shopify products into Wagtail.
2. `GET /products` — list products, identify those needing content updates.
3. `PATCH /products/{id}` with updated body/SEO/metafields and `publish=true` — update and sync.
4. `GET /products/{id}` — verify `last_synced_at` was updated, confirming success.

## Authentication
Pass your API key as a Bearer token in every request:
```
Authorization: Bearer <your_api_key>
```
API keys are created in Django admin under **API > API Keys**.

## Localization
Content exists in multiple locales: `en-US` (primary), `es-US`, `en-CA`, `fr-CA`.
Filter by `?locale=es-US` to retrieve locale-specific pages.
Translations are registered in Shopify via the translationsRegister mutation on sync.
"""

api = NinjaAPI(
    title="Wagtail-Shopify Content API",
    version="1.0.0",
    description=API_DESCRIPTION,
    auth=ApiKeyAuth(),
    docs_url="/docs/",
    openapi_url="/openapi.json",
)

api.add_router('/products/', products_router, tags=['Products'])
api.add_router('/collections/', collections_router, tags=['Collections'])
api.add_router('/blogs/', blogs_router, tags=['Blogs'])
api.add_router('/articles/', articles_router, tags=['Articles'])
