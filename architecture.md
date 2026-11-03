---
id: wagtail-shopify-architecture
type: architecture-design
title: Wagtail Shopify Architecture
status: draft
parent: wagtail-shopify-goal
references:
  - article-markdown-contract
  - content-layer-coordination
  - editorial-content-decisions
  - git-native-content-layer
  - location-editorial-git-migration
---
# Wagtail Shopify Architecture

## Shape

The system is a deploy-per-shop Django/Wagtail application. Wagtail owns editorial and operational domain state; Shopify Admin is the outbound commerce/content projection; Shopify storefront channels consume that projection.

```text
Shopify Admin / embedded app
        │
        ▼
shopify_admin ── shopify_config (tenancy, membership, tokens)
        │
        ▼
Wagtail + shopify_content ── content store (selected editorial fields)
        │                         │
        └───────────────┬─────────┘
                        ▼
              shopify_requests
                        ▼
             Shopify Admin GraphQL
                        ▼
             Online Store / Hydrogen
```

## Boundaries

- `shopify_admin` owns embedded app routes, OAuth/install/login, and admin-facing redirects. It must not own content or tenant persistence.
- `shopify_config` owns `ShopConfig`, tokens, membership, and shop resolution. It has no dependency on UI or content modules.
- `shopify_content` owns Wagtail content models, editorial projections, import/export orchestration, indexing, and publication mapping.
- `shopify_requests` owns the centralized Shopify GraphQL transport and token-provider seam.
- `content` / content-store code owns the persistence boundary for explicitly migrated editorial payloads; runtime reads deployed files and does not run Git.
- `api`, `cms_ui`, `webhooks`, and `django_react_ui_editor` are delivery/integration surfaces over domain capabilities, not alternative domain authorities.

## Dependency rules

Dependencies point toward shared infrastructure and domain services. Domain code must not import embedded UI concerns. Shopify calls go through `shopify_requests`; tenant resolution goes through `shopify_config`; migrated editorial values go through the editorial accessor and `ContentRepository`.

## Invariants

- A deployment represents one Shopify merchant; non-request sync paths fail closed unless exactly one installed shop is resolvable or an explicit shop is supplied.
- One merchant/deployment has one default Wagtail site and may serve both Online Store and Hydrogen consumers through the same Shopify projection.
- Git is authoritative only for fields explicitly registered in the content store; PostgreSQL remains authoritative for identity, relations, workflow, Shopify IDs, and operational state.
- Missing authoritative content is an integrity error, not an implicit database fallback.
- Shopify schema changes and risky definition application are explicitly gated and are not silently performed during ordinary publication.
- Known limitation: unified region/location/FAQ synchronization and region API endpoints remain incomplete and must stay behind explicit operational decisions.
