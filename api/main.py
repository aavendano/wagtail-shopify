import api.ninja_compat  # noqa: F401 — patch URL converters before ninja import

from ninja import NinjaAPI

from .auth import ApiKeyAuth
from .openapi_agent import build_openapi_tags
from .routers.products import router as products_router
from .routers.collections import router as collections_router
from .routers.blogs import router as blogs_router
from .routers.articles import router as articles_router
from .routers.locations import router as locations_router
from .routers.glossary import router as glossary_router
from .routers.capabilities import router as capabilities_router

API_DESCRIPTION = """
# Wagtail-Shopify Content API (AI Agent Tool Registry)

Autonomous content management across Wagtail CMS and Shopify. Every endpoint runs **synchronously**
and returns final results in the HTTP response — no Celery jobs, no polling.

OpenAPI spec: `/api/v1/openapi.json` · Agent catalog: `GET /api/v1/capabilities/` · Interactive docs: `/api/v1/docs/`

## Authentication

All endpoints require a bearer token. Existing API keys and OAuth access tokens issued
for MCP clients are both accepted:

```
Authorization: Bearer <api_key_or_oauth_access_token>
```

Create API keys in **Django Admin → API → API Keys** (`/admin-django/`). Create OAuth
clients in **Django Admin → Django OAuth Toolkit → Applications** and request the
`mcp` scope through `/o/authorize/` and `/o/token/`. Missing or invalid tokens return **401**.

## Tool Matrix

| Resource | List | Get | Create | Update | Delete | Pull (Shopify→Wagtail) | Push (Wagtail→Shopify) |
|----------|------|-----|--------|--------|--------|------------------------|------------------------|
| Products | GET /products/ | GET /products/{id} | POST /products/ | PATCH /products/{id} | DELETE /products/{id} | POST /products/pull | POST /products/{id}/push |
| Collections | GET /collections/ | GET /collections/{id} | POST /collections/ | PATCH /collections/{id} | DELETE /collections/{id} | POST /collections/pull | POST /collections/{id}/push |
| Blogs | GET /blogs/ | GET /blogs/{id} | POST /blogs/ | PATCH /blogs/{id} | DELETE /blogs/{id} | POST /blogs/pull | POST /blogs/{id}/push |
| Articles | GET /articles/ | GET /articles/{id} | POST /articles/ | PATCH /articles/{id} | DELETE /articles/{id} | POST /articles/pull | POST /articles/{id}/push |
| Locations | GET /locations/ | GET /locations/{id} | POST /locations/ | PATCH /locations/{id} | DELETE /locations/{id} | — (Wagtail-only) | POST /locations/{id}/push |
| Glossary | GET /glossary/ | GET /glossary/{id} | POST /glossary/ | PATCH /glossary/{id} | DELETE /glossary/{id} | — (Wagtail-only) | POST /glossary/{id}/push |

**Pull** returns HTTP 200 with `{created, updated, skipped, errors, message}` immediately.
**Push** returns HTTP 200 with `{success, message, shopify_id}` immediately.

## Agent Workflows

### Products / Collections (existing Shopify catalog)

1. `POST /products/pull` — import all products; read stats in response body.
2. `GET /products/?locale=en-US` — list pages; note `id` and `shopify_id`.
3. `PATCH /products/{id}` with content + `"publish": true` — save and sync if `sync_enabled=true`.
4. `GET /products/{id}` — verify `last_synced_at` updated.

### Blogs and Articles

1. `POST /blogs/pull` — imports blogs **and** articles in one call.
2. `GET /articles/?blog_id={blog_page_id}` — filter articles by parent blog.
3. `PATCH /articles/{id}` with `"publish": true` — parent BlogPage must have `shopify_id`.

### Locations (Wagtail-origin metaobjects)

Locations have **no pull** — content is authored in Wagtail and pushed to Shopify metaobject type `local_page`.

1. `POST /locations/` with `titulo` and content fields.
2. `PATCH /locations/{id}` with `"publish": true` (optional).
3. `POST /locations/{id}/push` — upserts metaobject; `shopify_id` saved on first success.
4. `GET /locations/{id}` — verify `last_synced_at` and `shopify_id`.

### Glossary (Wagtail-origin metaobjects)

Glossary terms have **no pull** — content is authored in Wagtail and pushed to Shopify metaobject type `glossary_term`.
The `/pages/glossary` list page is managed by the Shopify theme in Liquid.

1. `POST /glossary/` with `term`, `locale_code`, and optional `definition` / link fields.
2. `PATCH /glossary/{id}` with `"publish": true` (optional).
3. `POST /glossary/{id}/push` — upserts metaobject; `shopify_id` saved on first success.
4. `GET /glossary/{id}` — verify `last_synced_at` and `shopify_id`.

Note: `locale_code` (en/es/fr) is the Shopify metaobject locale, distinct from Wagtail `locale`.

## Sync Model

- `shopify_id` — Shopify GID linking Wagtail page to Shopify resource.
- `sync_enabled` — when true, `publish=true` triggers outbound sync via Wagtail publish hook.
- `last_synced_at` — UTC timestamp of last successful push; null if never synced.
- `translation_of` / `translation_page_ids` — link locale variants; shared `shopify_id` on translations.

## Localization

Markets: `en-US` (primary), `es-US`, `en-CA`, `fr-CA`. Filter lists with `?locale=es-US`.
Set `locale` on create; use `translation_of` (Wagtail page ID) to link variants.

## Common Errors

| Status | Meaning |
|--------|---------|
| 401 | Missing or invalid bearer token |
| 400 | ShopConfig/token missing, validation error, or sync failure detail |
| 404 | Page ID not found |

## Notes

- API operations are **synchronous only**. Wagtail admin and embedded app UI may still use background Celery jobs.
- DELETE removes Wagtail pages only — Shopify resources are not deleted.
- Use `operation_id` values in OpenAPI for stable AI tool names.
"""

api = NinjaAPI(
    title="Wagtail-Shopify Content API",
    version="1.1.0",
    description=API_DESCRIPTION,
    auth=ApiKeyAuth(),
    docs_url="/docs/",
    openapi_url="/openapi.json",
    openapi_extra={"tags": build_openapi_tags()},
)

api.add_router('/products/', products_router, tags=['Products'])
api.add_router('/collections/', collections_router, tags=['Collections'])
api.add_router('/blogs/', blogs_router, tags=['Blogs'])
api.add_router('/articles/', articles_router, tags=['Articles'])
api.add_router('/locations/', locations_router, tags=['Locations'])
api.add_router('/glossary/', glossary_router, tags=['Glossary'])
api.add_router('/capabilities/', capabilities_router, tags=['Capabilities'])

from .mcp import setup_mcp  # noqa: E402

setup_mcp(api, API_DESCRIPTION)
