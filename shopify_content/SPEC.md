---
id: shopify-content
type: module-design
title: Shopify Content and Editorial Projection
status: draft
parent: wagtail-shopify-architecture
---
# Shopify Content and Editorial Projection

Owns Wagtail page models and editorial behavior for Shopify-backed content, localization, imports, outbound synchronization orchestration, indexes, and content validation. It depends on `shopify_config` for shop resolution, `shopify_requests` for transport, and the content-store boundary for migrated editorial fields. It must not bypass those boundaries with direct token or filesystem/Git access.
