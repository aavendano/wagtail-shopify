---
id: cms-ui
type: module-design
title: CMS SPA Surface
status: draft
parent: wagtail-shopify-architecture
---
# CMS SPA Surface

Owns the `/cms/` SPA integration, middleware, models needed by that surface, and Wagtail-facing UI delivery. It consumes domain contracts and membership/authentication rules; it does not own page synchronization or Shopify transport.
