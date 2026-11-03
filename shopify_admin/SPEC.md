---
id: shopify-admin
type: module-design
title: Shopify Admin Surface
status: draft
parent: wagtail-shopify-architecture
---
# Shopify Admin Surface

Owns the embedded Shopify App Home, OAuth install/login flow, admin redirects, and the `/shopify-admin/` HTTP surface. It may depend on `shopify_config` for shop/token and membership operations and on shared Django infrastructure. It must not own Wagtail content models, Shopify GraphQL transport implementation, or content-store authority.
