# Editorial Content Architecture Decisions

Status: Accepted architecture through HG-003  
Last updated: 2026-09-03  
Scope: Git-backed editorial content in `wagtail-shopify`

## Purpose

This document records the architectural decisions accepted during the design and implementation of the flat-file editorial content system. It is intentionally independent from any single editor UI or deployment provider.

The central architectural boundary is:

```text
Git owns authoritative editorial payloads.
Django/PostgreSQL owns operational application state.
ContentRepository joins both at the domain boundary.
```

## Authority boundary

### D-009 — Git is authoritative for externalized editorial payloads

**Status:** Approved and implemented for `BlogPage.description`.

The authoritative source for editorial fields explicitly migrated to the content store is the approved Git repository revision, not the corresponding PostgreSQL column.

PostgreSQL remains authoritative for:

- Django/Wagtail model identity
- relations
- workflow state
- Wagtail publication state
- Shopify identifiers
- operational metadata
- synchronization state

Git is authoritative for:

- externalized editorial prose and other editorial payloads explicitly placed behind `ContentRepository`

This does **not** make Git authoritative for the entire Django domain.

### Authoritative transition

Editorial changes follow this governance path:

```text
edit
  -> branch
  -> commit
  -> pull request
  -> review / approval
  -> merge to authoritative branch
  -> CI/CD deployment
  -> deployed Git revision
  -> ContentRepository
  -> Django domain
  -> Shopify publication
```

An unmerged branch is proposed content, not production-authoritative content.

The deployed worktree is a materialization of the authoritative Git revision. A stale server checkout is not a separate source of truth.

## Domain fields versus Django ORM fields

### D-011 — Editorial content is a domain field, not `django.db.models.Field`

**Status:** Approved.

Externally persisted editorial content MUST be represented as a domain concept and MUST NOT be implemented as a custom `django.db.models.Field` that performs filesystem or Git I/O.

Example:

```python
page.slug
# Django ORM / PostgreSQL

page.shopify_id
# Django ORM / PostgreSQL

page.editorial.description
# Editorial domain / ContentRepository / Git
```

Consequences:

- Django ORM continues to provide identity, relations, filtering and operational state.
- Editorial values outside PostgreSQL are not automatically queryable using ORM lookup syntax.
- Search/indexing of externalized editorial content requires an explicit indexing strategy if needed.
- Persistence representation MUST NOT become the content domain API.

## Canonical domain access

### D-012 — `page.editorial.<field>` is the canonical editorial API

**Status:** Approved and implemented for `BlogPage.description`.

The canonical access pattern is:

```python
page.editorial.description
```

Semantics:

```text
page
  = Django/Wagtail domain object

page.editorial
  = domain-level editorial accessor

page.editorial.<field>
  = authoritative editorial value resolved through ContentRepository
```

New consumers of migrated editorial fields MUST use `page.editorial.<field>` rather than reading legacy PostgreSQL columns directly.

Physical file paths, frontmatter representation and editor-specific conventions MUST remain hidden behind the content-store/domain boundary.

## Content identity and paths

Content identity is deterministic and independent of slugs.

The current identity components are conceptually:

```text
content_type + object_id + field_key + locale
```

A slug rename MUST NOT change the authoritative content identity or file path.

For the current vertical slice:

```text
content/<locale>/shopify_content/blogpage/<pk>/description.md
```

Example:

```text
content/en-us/shopify_content/blogpage/15/description.md
```

## Localization topology

**Status:** Approved and implemented.

Canonical locale roots are:

```text
content/
├── en-us/
├── en-ca/
├── fr-ca/
└── es-us/
```

Locale normalization is centralized. Current mappings are:

```text
en-US -> en-us
en-CA -> en-ca
fr-CA -> fr-ca
es-US -> es-us
```

Unsupported locales MUST fail explicitly rather than silently writing into an unintended directory.

The locale directory is part of `ContentRef` resolution.

## Runtime Git isolation

**Status:** Approved and verified in HG-003.

Django runtime code MUST NOT perform Git synchronization as a hidden side effect.

The following operations MUST NOT occur inside model saves, domain accessors, HTTP requests or Shopify publication tasks:

```text
git pull
git commit
git push
git merge
```

Deployment/CI infrastructure owns checkout and synchronization of the approved Git revision.

Runtime only reads the deployed authoritative content tree.

## ContentRepository boundary

`ContentRepository` is the persistence boundary between editorial domain access and the deployed Git-backed files.

Domain consumers MUST NOT:

- construct filesystem paths directly
- parse editor-specific metadata directly
- execute Git commands
- depend on the physical content representation

Publication consumers MUST read the domain value through the editorial accessor.

For migrated content:

```text
Git checkout
    -> ContentRepository
    -> page.editorial.<field>
    -> Shopify synchronization / other domain consumers
```

## Authority modes and transition compatibility

Current modes provide an explicit migration boundary:

```text
db
mirror
git_authoritative
```

Semantics:

### `db`

PostgreSQL is authoritative. This preserves legacy behavior.

### `mirror`

PostgreSQL is authoritative and content files are a mirror.

### `git_authoritative`

Git-backed content is authoritative. The legacy PostgreSQL editorial column is compatibility/rollback state only.

When PostgreSQL and Git disagree in `git_authoritative` mode, Git wins.

A missing authoritative file is an integrity error and MUST raise an explicit repository/domain error such as `ContentNotFound`.

A database fallback, when temporarily supported, MUST be:

- explicitly configured
- observable
- disabled by default in Git-authoritative operation
- never mistaken for the normal authority model

## Editorial writes

The first Git-authoritative implementation uses a **READ_ONLY** runtime policy for migrated content.

Django Admin/runtime MUST NOT directly mutate production-authoritative content outside Git governance.

A future workflow in which Django Admin creates branches/commits/pull requests is a separate architectural capability and requires a new decision.

Conceptually that future capability would be a proposal service/workspace, not hidden mutation inside `Model.save()`.

## Shopify publication

Existing Shopify publication remains a domain consumer; only the source of migrated editorial values changes.

For `BlogPage.description`, publication MUST consume:

```python
page.editorial.description
```

It MUST NOT:

- open content files directly
- construct repository paths
- execute Git
- silently prefer `page.description`

HG-003 demonstrated:

```text
PostgreSQL description = A
Git description        = B
page.editorial.description = B
Shopify payload            = B
```

This proves that Git is the effective editorial authority for the migrated field.

## Materialization and migration of legacy content

Migration from database-authoritative content to Git content is an explicit operational action, not a schema migration or application startup side effect.

The materialization process MUST be controlled and should be idempotent where practical.

It MUST:

- enumerate target domain objects
- derive deterministic `ContentRef` values
- preserve existing content verbatim unless a separate format migration is approved
- detect existing identical files
- detect divergent files
- avoid destructive overwrite without explicit force
- report results

The current implementation uses a Django management command for this responsibility.

## Database column lifecycle

Legacy PostgreSQL content columns MAY remain temporarily after the authority flip for rollback/compatibility.

Their continued presence does not make them authoritative.

Removing a legacy column requires a separate architectural decision and HumanGate.

## Canonical editorial file format

### D-013 — Markdown files readable by Keystatic

**Status:** Approved.

Canonical editorial documents are plain-text Markdown files that are compatible with Keystatic as an external editor.

Reference implementation/editor compatibility target:

```text
Thinkmill/keystatic
https://github.com/Thinkmill/keystatic
```

The architectural rule is:

```text
Keystatic-readable != Keystatic-owned
```

Keystatic MAY provide an editor UI over the Git repository, but it is not part of the Django runtime and does not own domain semantics.

### Document convention

The canonical direction is:

```text
container: Markdown (.md)
metadata: YAML frontmatter
prose: Markdown
structured rich content: Keystatic-readable Markdown/Markdoc-compatible constructs where required
```

The format MUST remain:

- plain text
- Git-versionable
- readable without Keystatic
- parseable by `ContentRepository` independently of Keystatic
- usable by external editors such as Obsidian where the Markdown subset allows it

No editor-specific runtime dependency is permitted.

### Rich content and references

Future complex editorial documents may contain:

- multiple text fields
- paragraphs and headings
- images/assets
- links to internal pages
- Shopify products
- Shopify collections
- repeated/structured sections

These SHOULD use stable typed references rather than embedding deployment URLs as identity.

Conceptual reference types include:

```text
internal_page
product
collection
asset
```

The exact reference syntax and structured-block schema are intentionally not finalized by D-013 and require validation against the chosen Keystatic-readable schema before broad migration.

### Existing HTML content

Existing verbatim HTML content MUST NOT be automatically transformed into Markdown merely because Markdown is now the canonical target format.

HTML -> Markdown conversion is a content migration and requires separate approval and tests for losslessness/semantic preservation.

## Current validated vertical slice

### `BlogPage.description`

Status: Phase C completed; HG-003 approved.

Validated properties include:

- Git authority
- canonical `page.editorial.description` domain access
- Git wins over stale database state
- Shopify publication consumes Git value
- explicit `ContentNotFound`
- locale topology
- slug-independent identity
- runtime Git isolation
- controlled materialization
- rollback to `mirror` or `db`

### `GlossaryTermPage.definition`

Status: Phase D implemented; HG-004 pending review.

This slice reuses the same domain/content-store architecture for a Wagtail
`RichTextField` and begins exercising the canonical Markdown (`.md`) format
(D-013). Validated properties include:

- Git authority via `page.editorial.definition`
- Git wins over stale PostgreSQL `definition`
- Shopify metaobject `definition` field consumes the Git value
- explicit `ContentNotFound` on missing file (opt-in DB fallback only)
- locale topology and slug-independent identity
- runtime Git isolation
- controlled materialization (extended, not duplicated) with verbatim preservation

Interim representation note: the current PostgreSQL value is Wagtail RichText
HTML (`.source`). To remain lossless (D-013 non-goal: no automatic HTML→Markdown
conversion), the `.md` body currently contains that HTML verbatim. The file is
still valid Markdown-with-YAML-frontmatter and Keystatic/Obsidian-readable. A
semantic migration to pure Markdown is a separate, approval-gated content
migration (see "Existing HTML content").

## Next vertical slice

With two fields migrated (a plain `TextField` and a `RichTextField`), the
architecture is proven for both simple and rich single-value editorial fields.

The recommended next targets, each under its own scoped WorkOrder/HumanGate, are
the remaining single-value RichText fields (e.g. `LocationPage` rich-text
sections) before any multi-field/structured document such as `ArticlePage.body`
(`StreamField`), which first requires finalizing the Keystatic-readable
rich-content/reference schema (open decision 5).

## Invariants

The following invariants are accepted architectural constraints:

### INV-PERSIST-001

Database row/domain identity MUST NOT depend on a physical file path.

### INV-PERSIST-002

Publication consumers MUST read domain content rather than filesystem paths.

### INV-PERSIST-003

File format MUST NOT become the domain API.

### INV-PERSIST-004

Git MUST NOT execute implicitly as a side effect of ordinary Django model saves or domain reads.

### INV-PERSIST-005

Puck layout JSON and editorial prose are independent persistence concerns.

### INV-EDITORIAL-001

Migrated editorial fields MUST be accessed through `page.editorial.<field>`.

### INV-EDITORIAL-002

An unmerged content change MUST NOT become authoritative production content.

### INV-EDITORIAL-003

In Git-authoritative mode, stale PostgreSQL editorial content MUST NOT silently override Git.

### INV-EDITORIAL-004

Keystatic or any other editor MUST remain replaceable without changing the editorial domain contract.

## Explicit non-goals / not yet approved

The following are not authorized merely by the decisions above:

- migrating Puck layout persistence to Git
- migrating all `StreamField` content
- removing legacy database columns
- direct Git writes from Django model save hooks
- automatic Git commit/push/merge from runtime
- Admin-driven PR generation
- automatic HTML-to-Markdown conversion
- changing storefront technology
- making Keystatic a production runtime dependency

## Open architectural decisions

The following remain unresolved and should be handled independently:

1. **Django migration policy debt** — the repository currently ignores `*/migrations/*`; migrations should be treated as version-controlled source artifacts, but the catch-up/fix should be a dedicated change.
2. **Deployment contract** — define authoritative repository/branch, deployment checkout strategy, environment mapping, immutable deployed commit SHA and rollback procedure.
3. **Proposal-generation workflow** — if Admin editing should generate Git branches/PRs, define an explicit editorial workspace/change service.
4. **Legacy column retirement** — decide when database editorial columns can be removed after sufficient production validation.
5. **Rich-content schema** — finalize the Keystatic-readable conventions for typed references, images, repeated sections, products, collections and internal-page links before migrating complex content such as `ArticlePage.body`.
6. **Editorial indexing/search** — define a separate index if SQL-style querying over Git-authoritative prose becomes a requirement.

## Architectural summary

```text
                               +----------------------+
                               | External editors     |
                               | Keystatic / Obsidian |
                               +----------+-----------+
                                          |
                                          v
                                Git branch / PR
                                          |
                                    merge / CI-CD
                                          |
                                          v
+------------------+            deployed Git revision
| PostgreSQL       |                     |
| identity         |                     v
| relations        |              ContentRepository
| workflow         |                     |
| Shopify IDs      |                     v
+--------+---------+           page.editorial.<field>
         |                                |
         +----------------+---------------+
                          |
                          v
                    Django domain
                          |
                          v
                  Shopify publication
```

The domain contract remains stable even if the external editor, file parser implementation, deployment provider or storefront renderer changes.
