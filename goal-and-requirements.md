---
id: wagtail-shopify-goal
type: goal-and-requirements
title: Wagtail Shopify CMS
status: draft
---
# Wagtail Shopify CMS

## Overview

Wagtail Shopify is a Django/Wagtail backend that gives Shopify merchants an editorial CMS. Editors manage structured store content in Wagtail and the backend publishes the resulting commerce and editorial projection to Shopify through the Admin GraphQL API. Shopify remains the public commerce runtime; the backend does not render the public storefront.

This description is inferred from the repository README, application layout, and existing architecture documents; the product-owner intent has not been separately confirmed.

## Problem Statement

Merchants need to maintain localized products, collections, blogs, articles, glossary content, and location content without editing Shopify records and storefront-facing content through disconnected workflows. The backend centralizes editorial ownership, validation, localization, tenancy, and publication while preserving Shopify as the channel-facing projection.

## Target Users

- **Editors:** create and review localized editorial and commerce content in Wagtail.
- **Shop administrators:** install and configure the embedded Shopify app, tokens, shop membership, and publication settings.
- **Operators and developers:** run imports, synchronization, indexing, validation, and background jobs.
- **AI agents and integrations:** use the internal API and MCP surfaces for controlled content operations.

## Capabilities

- Manage Wagtail page types for products, collections, blogs, articles, glossary terms, locations, and related editorial structures.
- Synchronize supported content to Shopify Admin through a centralized GraphQL request layer.
- Import Shopify content into Wagtail and run outbound publication asynchronously through Celery where configured.
- Resolve the active shop through deploy-per-shop tenancy, session selection, and membership checks rather than silent tenant guesses.
- Serve embedded Shopify Admin, CMS SPA, internal API/MCP, webhooks, and operational administration surfaces.
- Externalize selected editorial payloads into a Git-backed content store with explicit `db`, `mirror`, and `git_authoritative` authority modes.
- Support the four internal locales (`en-US`, `es-US`, `en-CA`, `fr-CA`) and map them to Shopify language behavior at the integration boundary.

## Non-Goals

- Rendering or replacing Shopify's public storefront; Online Store and Hydrogen remain consumers of Shopify's projection.
- SaaS-style editorial isolation with a shop field on every Wagtail page or separate Site trees per merchant/channel.
- Hidden Git synchronization or Git writes from Django runtime requests, model saves, or publication tasks.
- Moving all operational metadata, relations, workflow state, or Shopify identifiers into Markdown content files.
- Treating the known geo/FAQ synchronization work and region API endpoints as complete capabilities.

## Technology

| Aspect | Choice | Rationale |
|---|---|---|
| Runtime | Python 3.11+, Django, Wagtail | Existing application and editorial platform. |
| Integration | Shopify Admin GraphQL | Central commerce projection and token lifecycle. |
| Async work | Celery, Redis, django-celery-beat | Background sync, imports, and scheduled jobs. |
| Editorial files | Git-backed Markdown/YAML content store | Explicit reviewable authority for migrated editorial fields. |
| API/UI | django-ninja/MCP, embedded Shopify UI, Puck SPA | Internal automation and merchant-facing administration surfaces. |
