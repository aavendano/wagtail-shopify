# ADR 0003: Dual-channel storefronts + editorial form authority

## Status

Accepted (documentation; no runtime sync change in this ADR).

## Context

PlayLoveToys is **one** Shopify merchant with two public reading surfaces:

1. **Online Store** — Liquid theme (`plt-frontend-liquid`).
2. **Headless Hydrogen** — `tina-hydrogen-frontstore` (Oxygen; staging documented in that repo).

Wagtail (`wagtail-shopify`) is a headless CMS that syncs outbound to Shopify Admin
(GraphQL). After ADR 0001 (app split) and ADR 0002 (deploy-per-shop +
`ShopMembership`), shop resolution is sole-`ShopConfig` / session — not a field
on every page.

An earlier draft assumed **two Wagtail Sites / two brands**. Merchant inventory
shows **one shop and two channels**. Duplicating trees would force handle
prefixes and double sync without benefit.

Separately, document **shape** (fields, paths, public URL patterns, blocks) is
owned by [`aavendano/plt-editorial-schema`](https://github.com/aavendano/plt-editorial-schema)
(`contractVersion` **1.1.0** in `registry.json`). That contract does **not**
own Shopify metaobject GraphQL `type` strings, Wagtail page classes, or tokens.

## Decision

1. **One merchant, one Wagtail deploy, one default Site.** No second
   `ShopConfig`, no second `wagtailcore.Site` solely to separate Online Store
   from Hydrogen. Both channels read the **same** Shopify projection after a
   single publish/sync path (ADR 0002).

2. **Two storefront channels, not two brands.** Online Store (Liquid) and
   Hydrogen are consumers. Wagtail does not render the public storefront.

3. **Form authority:** `plt-editorial-schema` defines canonical document types
   (`home`, `page`, `product`, `collection`, `blog`, `article`,
   `glossary_term`, `location`, `region`) and block schemas. Producers
   (Wagtail, Tina/`plt-content`) and channels map onto those types; they may
   use different Shopify type handles until a geo unification decision lands
   (see inventory P1).

4. **Shopify is the commerce/runtime projection.** Hydrogen is not an
   editorial source of truth while AGENTS.md in that repo states Shopify
   metaobjects first (Tina/`plt-content` as fallback). Wagtail authors into
   Shopify; it does not replace the schema contract.

5. **Glossary / location indexes for Liquid:** agreed contract remains
   Wagtail → precomputed JSON on Shopify (`root_page` per locale and/or Page
   metafields such as `custom.index_listings`) → Liquid
   (`wagtail-root-index`). Treat as contract + smoke checklist, not as
   “production-verified” without a recorded run. Hydrogen glossary/geo loaders
   may diverge (direct `glossary_term` / `location_page` / `region` queries).

6. **Supersedes** the “Site-per-brand / dual Site” approach for this merchant.
   Channel-exclusive trees remain out of scope until a future ADR.

## Consequences

- Inventory and backlog live in
  [`docs/content-inventory-playlovetoys.md`](../content-inventory-playlovetoys.md)
  (P0–P4 as **decisions-open**, no mass corporate Page sync in this cycle).
- Geo naming stays a known triangle until product chooses aliases or
  unification: schema `location`/`region` vs Shopify H2 `location_page`/`region`
  vs Wagtail sync `local_page` (no `RegionPage` yet).
- Call sites must not invent a second Site or ShopConfig to “support Hydrogen.”

## Related

- ADR 0001 — `core` → `shopify_admin` / `shopify_config` / `core` ops
- ADR 0002 — deploy-per-shop tenancy + `ShopMembership`
- `plt-editorial-schema` `registry.json` (`contractVersion` 1.1.0)
- `docs/shopify_content.md` — sync models and index rebuild commands
