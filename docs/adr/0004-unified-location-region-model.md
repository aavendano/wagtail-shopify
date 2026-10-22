# ADR 0004: One location model, with a region page as the parent

## Status

Accepted. Code only: nothing in this ADR writes to Shopify, and no Shopify data or
definition changes until the project is operational.

## Context

The store has two location systems:

- **United States** — the `local_page` metaobject (`/pages/location/{handle}`), no region.
- **Canada** — `location_page` (`/pages/canada-location/{handle}`) and `region`
  (`/pages/canada/{handle}`). A region is a published web page whose `location_pages` list links
  to the individual location pages. The parent/child link lives only on the region side.

Wagtail knew only `local_page`, as a flat `LocationPage` under a root.

## Decision

1. **One model.** `LocationPage` keeps its name (git paths and handles depend on it) and gains the
   Canadian service-messaging fields (`discreet_shipping`, `quality_focus`, `body_safe_materials`,
   `seo_keyword`). Equivalent fields are not duplicated: `titulo` = `header1`,
   `subtitulo` = `header2`, `intro` = `greeting`, `state` = province.
2. **Region is the parent.** `RegionPage` (a province or state, with `country`, `region_code`,
   hero fields and SEO) holds `LocationPage` children. Its link list (`location_pages`) is derived
   from the Wagtail tree. A location may still hang off a root during the transition.
   `LocationPage.clean()` takes `state` and `country` from its region.
3. **Shopify is the source of truth for languages.** Shopify has `en` (primary), `es` and `fr`;
   the markets are `ca` and `usa`. Wagtail's four locales (`en-US`, `es-US`, `en-CA`, `fr-CA`) are
   internal; at the Shopify boundary only the language is used (`shopify_languages.py`). `en-CA`
   and `en-US` share `en`, so neither is registered as a translation. This fixes translation
   registration, which previously sent the invalid `en-CA` / `fr-CA`: `fr-CA` now registers `fr`.
4. **FAQs are not JSON metafields.** The target is `faq` metaobject entries referenced from
   content. The existing JSON pushes are untouched until that sync exists.
5. **Missing definitions are metaobjects**, not metafields: `content_links` carries the related
   products, collections, articles, glossary terms, internal links and FAQs. Legacy metafield keys
   (`custom.faqs`, `custom.json_faqs`, `faqs`) are not reused.
6. **Definitions are code, applied later.** `shopify_content/sync/unified_definitions.py` declares
   the generalized `faq`, `location_page`, `region` and `content_links` definitions. They only add
   to the live ones (every live field and URL handle is kept). `SHOPIFY_SCHEMA_CHANGES_ENABLED`
   is off by default and `apply_definitions` refuses to run without it. Because
   `sync_location_page` ensures its definition on every publish, the new definitions are not wired
   into any sync flow.
7. **Routing follows Shopify Liquid.** The live URL handles stay (`canada`, `canada-location`).
   Moving US locations onto `location_page` needs a neutral URL handle and redirects; that is an
   open routing/SEO decision.

## Tools

- `python manage.py unified_location_definitions [--live] [--json]` — renders the definitions
  offline, or prints a read-only plan against the store. `--apply` is refused unless the flag is on.
- `python manage.py organize_location_regions [--apply]` — creates a `RegionPage` per
  (root, locale, state) and moves loose locations under it. Wagtail tree only; dry run by default;
  idempotent.

## Consequences

- Moving locations changes Wagtail paths, not handles, so storefront URLs do not change.
- The region ↔ location reference is circular, so applying the definitions takes two passes.
- Canada's `province_page` is empty in the live data; importing Canada must derive the parent from
  `region.location_pages`.
- Not done yet: syncing `region` / unified `location_page` and `faq` entries (behind a flag, off
  until operational), grouping the locations index by region, and region API endpoints.
