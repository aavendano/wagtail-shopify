# Phase E — LocationPage editorial content in Git

Status: implementation branch; review/merge pending  
Scope: `LocationPage` single-value RichText sections only

## Goal

Extend the accepted Git-backed editorial content architecture from
`BlogPage.description` and `GlossaryTermPage.definition` to the simple rich-text
sections of `LocationPage`, without changing database schema or moving operational
location data out of Django.

## Git-authoritative fields

The following fields are externalized:

- `intro`
- `content_2`
- `content_3`
- `brand_section_content`
- `map_content`
- `after_page_content`

Canonical paths remain deterministic and PK-based:

```text
content/<locale>/shopify_content/locationpage/<pk>/<field>.md
```

The current body representation remains the lossless Wagtail RichText HTML
source inside Markdown + YAML frontmatter. No HTML-to-Markdown conversion is
performed by this phase.

## What remains in PostgreSQL

This phase intentionally keeps identity and operational/location structure in
Django/PostgreSQL, including:

- `titulo`, `subtitulo`
- country/state/city
- section titles/subtitles
- locale and canonical handle
- FAQs and relations
- SEO fields
- Shopify IDs and synchronization state
- Wagtail workflow/publication state

Legacy RichText columns also remain temporarily as rollback/compatibility state;
in `git_authoritative` mode they are not the publication authority.

## Publication contract

`LocationPage` exposes `page.editorial.<field>` through `EditorialMixin`.

The existing location Shopify serializer is retained for compatibility in this
phase. A scoped adapter overlays the six authoritative editorial values in-memory
for the duration of `sync_location_page()` and always restores the DB-backed model
values afterwards. Missing authoritative files raise `ContentNotFound`; there is
no silent database fallback unless the existing explicit compatibility setting is
enabled.

The adapter is installed on the existing
`shopify_content.sync.outbound.sync_location_page` import surface from
`AppConfig.ready()`, so Celery, API and management callers keep the same contract.
It performs no model save, Git command, or filesystem write.

## Transition behavior

The content-store post-save mirroring signal is now registry-driven. Therefore
all registered fields — Blog, Glossary and Location — participate consistently in
`mirror` mode without page-specific signal code.

Materialization remains the existing controlled command:

```bash
python manage.py materialize_editorial_content --field intro
python manage.py materialize_editorial_content --field content_2
# ...or omit --field to materialize all registered editorial fields
```

Operators should inspect generated files, commit them to the content repository,
and only then enable `git_authoritative` for an environment.

## Non-goals

This phase does not migrate:

- `ArticlePage.body`, `ProductPage.body`, or `CollectionPage.description`
- Puck layout JSON
- FAQs or typed relations
- images/assets
- database columns
- search/index persistence
- Git writes from Django runtime

The next architectural step remains the structured rich-content schema required
for StreamField content and typed references (internal pages, products,
collections and assets).
