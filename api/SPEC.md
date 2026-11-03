---
id: internal-api
type: module-design
title: Internal API and MCP Surface
status: draft
parent: wagtail-shopify-architecture
---
# Internal API and MCP Surface

Owns django-ninja endpoints, agent authentication/registration, preview and sync API delivery, and MCP exposure. It is a delivery surface that delegates tenancy, content, and Shopify operations to their owning modules. It must preserve explicit authorization and must not introduce a second source of truth.
