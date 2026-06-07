# wagtail-shopify

A Django/Wagtail embedded Shopify application that provides a full integration layer between [Wagtail CMS](https://wagtail.org/) and the [Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql). Includes OAuth authentication, a clean GraphQL abstraction layer, a Shopify Metaobjects management toolkit, and webhook handling.

---

## Overview

**wagtail-shopify** is an embedded Shopify app built on Django 4.2 and Wagtail. It allows merchants to install the app in their Shopify store, authenticate via OAuth, and then manage store data — such as Metaobjects — through a Wagtail-powered admin interface or programmatically via Python.

### Key Capabilities

| Capability | Description |
|---|---|
| **OAuth & Token Management** | Full Shopify OAuth 2.0 flow with persistent token storage and automatic refresh |
| **GraphQL API Layer** | Centralized, reusable abstraction over the Shopify Admin GraphQL API |
| **Metaobjects Toolkit** | CRUD operations, CSV batch import/export, and introspection for Shopify Metaobjects |
| **Webhook Handling** | Verified webhook endpoints for `app/uninstalled` and `app/scopes_update` events |
| **Wagtail CMS** | Content management via the Wagtail admin interface |

---

## Architecture

```
wagtail-shopify/
├── config/              # Django project settings and URL routing
├── core/                # OAuth flow, token lifecycle, app home verification
├── shopify_requests/    # Shared GraphQL API layer (token resolution, SDK wrapper)
├── metaobjects/         # Shopify Metaobjects toolkit (CRUD, CSV batch, export)
├── webhooks/            # Shopify event handlers
├── custom/              # Placeholder for custom Wagtail models
└── shopify.app.toml     # Shopify app manifest
```

### Module Responsibilities

**`core`** — Handles the Shopify OAuth flow, stores shop credentials in the `ShopConfig` model, and verifies embedded app sessions. The `token_service` module manages the full token lifecycle (acquisition, refresh, cleanup on authorization errors).

**`shopify_requests`** — A clean abstraction layer over the Shopify Admin GraphQL API. The single public entry point `execute_admin_graphql()` handles token resolution, SDK wrapping, and error normalization. Domain-specific operations live in `shopify_requests/domains/`.

**`metaobjects`** — A self-contained toolkit for managing Shopify Metaobjects. Supports full CRUD operations, introspection of metaobject definitions, CSV batch import with upsert logic, and CSV export.

**`webhooks`** — CSRF-exempt endpoints that receive and verify Shopify webhooks. Currently handles app uninstallation and scope changes.

---

## Tech Stack

- **Python 3.x** / **Django 4.2**
- **Wagtail** — headless CMS and admin interface
- **ShopifyAPI** / **shopifyapp** — Shopify OAuth SDK
- **pandas** — CSV processing for batch Metaobject operations
- **tenacity** — Automatic retry with exponential backoff for API rate limits
- **python-dotenv** — Environment-based configuration
- **SQLite** — Default database (configurable for production)

---

## Getting Started

### 1. Clone and install dependencies

```bash
git clone https://github.com/aavendano/wagtail-shopify.git
cd wagtail-shopify
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```env
DJANGO_SECRET_KEY=your-django-secret-key
SHOPIFY_API_KEY=your-shopify-api-key
SHOPIFY_API_SECRET=your-shopify-api-secret

# For standalone/script usage (without OAuth flow):
SHOPIFY_SHOP_DOMAIN=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_your-admin-api-access-token
```

### 3. Apply migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

---

## GraphQL API Layer

The `shopify_requests` package provides a single, consistent entry point for all Shopify Admin GraphQL operations:

```python
from shopify_requests import execute_admin_graphql

QUERY = """
query {
  shop {
    name
    email
  }
}
"""

result = execute_admin_graphql(QUERY, shop="your-store")

if result.ok:
    print(result.data)
else:
    print(f"Error: {result.error_code}")
    if result.reauthorization_required:
        # Handle re-auth
        pass
```

The `AdminGraphqlResult` response object exposes:

| Field | Type | Description |
|---|---|---|
| `ok` | `bool` | `True` if the request succeeded |
| `data` | `dict` | Parsed GraphQL response data |
| `error_code` | `str \| None` | Error type if `ok` is `False` |
| `reauthorization_required` | `bool` | `True` if the shop needs to re-authenticate |
| `retryable` | `bool` | `True` if the error is transient |

---

## Metaobjects Toolkit

Manage Shopify Metaobjects programmatically or via CSV batch processing.

### Batch import from CSV

```python
from metaobjects.shopify_metaobject_loader import ShopifyMetaobjectLoader

loader = ShopifyMetaobjectLoader(
    shop_domain="your-store.myshopify.com",
    access_token="your-access-token"
)

stats = loader.process_csv(
    file_path="data.csv",
    metaobject_type="my_fabric_type"
)

print(f"Created: {stats['created']}, Updated: {stats['updated']}, Failed: {stats['failed']}")
```

### CSV format

The CSV must have a `handle` column as the first column — it is used as the unique identifier for upsert operations.

```csv
handle,fabric_name,stretch_level,is_organic
main-cotton,Classic Cotton,2,true
stretch-denim,Stretch Denim,8,false
organic-linen,Organic Linen,1,true
```

### Other operations

```python
# Fetch all metaobjects of a type
metaobjects = loader.fetch_metaobjects("my_fabric_type")

# Export to CSV
loader.export_to_csv("my_fabric_type", "output.csv")

# Introspect a metaobject definition
loader.print_metaobject_type_description("my_fabric_type")
description = loader.describe_metaobject_type("my_fabric_type")
```

---

## Webhooks

Configured in `shopify.app.toml` and handled in the `webhooks` app. All endpoints are HMAC-verified.

| Topic | Handler | Description |
|---|---|---|
| `app/uninstalled` | `webhooks/handlers/uninstalled.py` | Cleans up shop data on uninstall |
| `app/scopes_update` | `webhooks/handlers/scopes_update.py` | Handles OAuth scope changes |

---

## Shopify App Manifest

`shopify.app.toml` defines the app configuration for the Shopify CLI:

- **App name:** wagtail-shop
- **API version:** 2026-04
- **Access scopes:** `write_products`
- **Embedded:** yes
- **Webhooks:** `app/uninstalled`, `app/scopes_update`

---

## Error Handling & Resilience

- **Rate limiting:** Automatic retry with exponential backoff via `tenacity`
- **Token errors:** Authorization failures trigger token cleanup and surface `reauthorization_required` to callers
- **GraphQL errors:** Normalized into `AdminGraphqlResult` with typed error codes
- **Logging:** `INFO` for successful operations, `WARNING` for non-critical issues, `ERROR` for failures

---

## Testing

```bash
python manage.py test
```

Unit tests for the GraphQL layer are in `shopify_requests/tests/`. The recommended mocking target is `shopify_requests.graphql_client.raw_admin_graphql` — this keeps tests decoupled from the Shopify SDK.

---

## Contributing

Issues and pull requests are welcome.
