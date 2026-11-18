---
id: shopify-admin
type: module-design
title: Shopify Admin Surface
status: draft
parent: wagtail-shopify-architecture
---
# Shopify Admin Surface

Owns the embedded Shopify App Home, OAuth install/login flow, admin redirects, and the `/shopify-admin/` HTTP surface. It may depend on `shopify_config` for shop/token and membership operations and on shared Django infrastructure. It must not own Wagtail content models, Shopify GraphQL transport implementation, or content-store authority.

## Ops hub vs CMS SPA

- With `CMS_REDIRECT_EMBEDDED_HOME_TO_SPA=true` (default), `/shopify-admin/` redirects merchants to the Polaris CMS at `/cms/`.
- The operations hub (import, allowlisted management commands, recent runs) remains at `/shopify-admin/?ops=1`.
- The embedded nav (`core/navbar.html`) exposes **Operaciones** → that ops URL while keeping Home/CMS as the default editorial path.
