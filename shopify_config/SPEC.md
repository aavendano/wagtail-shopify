---
id: shopify-config
type: module-design
title: Shop Configuration and Tenancy
status: draft
parent: wagtail-shopify-architecture
---
# Shop Configuration and Tenancy

Owns `ShopConfig`, token lifecycle helpers, deploy-per-shop resolution, `ShopMembership`, session-shop selection, and fail-closed tenancy rules. It may depend on Django authentication and Shopify SDK/request seams. It must not depend on embedded UI or content modules.
