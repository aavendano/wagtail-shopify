---
id: webhooks
type: module-design
title: Shopify Webhook Receivers
status: draft
parent: wagtail-shopify-architecture
---
# Shopify Webhook Receivers

Owns Shopify webhook routing, verification/normalization, and dispatch into domain operations. It must remain thin: tenant resolution, persistence, and synchronization behavior belong to their owning modules.
