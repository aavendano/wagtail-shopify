---
id: shopify-requests
type: module-design
title: Shopify GraphQL Request Layer
status: draft
parent: wagtail-shopify-architecture
---
# Shopify GraphQL Request Layer

Owns centralized Shopify Admin GraphQL execution, token-provider integration, error translation, and request-level observability. Callers use this seam rather than constructing Shopify clients or embedding token lookup. It is infrastructure for content, admin, webhooks, and API integrations.
