# Article Markdown Editorial Contract

Status: **Phase F completed** (implementation verified 2026-09-05; `git_authoritative` on `settings_dev` only)  
Scope: `ArticlePage.body`  
Authority target: Git

## Decision

`ArticlePage.body` does not need a Git representation of Wagtail `StreamField`.

The new editorial contract is:

```text
Git body.md
   -> ContentRepository
   -> page.editorial.body        # Markdown source
   -> editorial Markdown renderer
   -> HTML
   -> Shopify Article.body
```

The existing Wagtail `StreamField` remains temporarily as rollback/compatibility
state. It is not the content model to reproduce in Git.

## Why Git-native instead of mirror

The old and new representations have different semantics:

```text
PostgreSQL: Wagtail StreamField JSON / StreamValue
Git:        Markdown document
```

Therefore `ArticlePage.body` is registered as a **Git-native editorial field**,
not a mirrored field.

Consequences:

- no checksum/drift comparison between StreamField and Markdown;
- no automatic DB fallback if `body.md` is missing;
- no `mirror` signal for Article body;
- `page.editorial.body` is valid when `CONTENT_STORE_MODE=git_authoritative`;
- in `db` / `mirror`, legacy publication continues to render `page.body`;
- in `git_authoritative`, publication reads only Git Markdown.

A missing `body.md` in Git-authoritative mode is an integrity error and aborts
publication.

## Path

```text
content/<locale>/shopify_content/articlepage/<pk>/body.md
```

Example:

```text
content/en-us/shopify_content/articlepage/42/body.md
```

Identity remains locale + content type + stable PK + field name. Slug changes do
not move content.

## Markdown contract

Normal content uses normal Markdown:

```md
## Choosing the right vibrator

Start with **comfort** and choose the intensity that works for you.

- Body-safe materials
- Easy cleaning
- Discreet storage

![Product close-up](https://cdn.example.com/image.jpg)
```

Standard Markdown owns:

- headings
- paragraphs
- emphasis
- lists
- links
- images
- tables / fenced code through Python-Markdown `extra`

Raw HTML remains accepted by the Markdown engine. This is intentional during
migration because existing StreamField output can be moved to Git without a
lossy HTML-to-Markdown rewrite.

## Custom components

Only content that needs explicit storefront semantics uses directives. Directives
must appear on their own line.

### Product

```md
{% product handle="satisfyer-pro-2" label="Satisfyer Pro 2" %}
```

Renders semantic HTML with:

```text
data-component="product"
data-handle="satisfyer-pro-2"
```

and a canonical `/products/<handle>` link.

### Collection

```md
{% collection handle="vibrators" label="Shop Vibrators" %}
```

### Internal page

```md
{% page path="/pages/glossary/lubricant" label="Lubricant" %}
```

The path must be root-relative. Deployment-specific absolute URLs are not used
as identity.

### Callout

```md
{% callout type="tip" title="Tip" %}
Use plenty of **water-based lubricant**.
{% /callout %}
```

Allowed callout types:

```text
note
info
tip
warning
```

The body is Markdown and is rendered recursively. Nested callouts are currently
rejected deliberately to keep the grammar small.

## Renderer output

The renderer emits normal HTML plus stable `plt-*` classes and `data-component`
attributes. It does not emit Liquid and it does not require client-side React.

Examples:

```text
plt-component
plt-product-ref
plt-collection-ref
plt-page-ref
plt-callout
plt-callout--tip
```

The Shopify theme may style these classes. The content contract does not depend
on a particular CSS framework.

## Validation and safety

Custom directives are allow-listed. Unknown directives fail explicitly.

Component labels are HTML-escaped. Shopify handles are restricted to a safe
handle grammar. Internal page references must be root-relative. A malformed
component aborts rendering instead of silently emitting ambiguous HTML.

Raw HTML in ordinary Markdown remains a trusted-editor capability and is governed
by the Git review workflow.

## Existing StreamField migration

The initial authority flip should preserve storefront output before attempting
semantic cleanup.

Run:

```bash
python manage.py materialize_article_markdown --dry-run
python manage.py materialize_article_markdown
```

The command renders the existing StreamField using the current production
renderer and writes that HTML verbatim inside each `body.md` file.

This is intentional:

```text
StreamField
   -> current rendered HTML
   -> body.md containing raw HTML
   -> Markdown renderer
   -> same HTML
```

No automatic HTML-to-Markdown transformation occurs during the authority flip.
After the files are committed and Git authority is validated, humans or agents
can progressively replace raw HTML sections with semantic Markdown and custom
components.

The materializer is controlled and idempotent:

- existing identical files are left unchanged;
- divergent Git files are never overwritten unless `--force` is explicit;
- `--dry-run` reports without writing;
- empty bodies still get an explicit `body.md`, because a missing authoritative
  file has different semantics from an intentionally empty document.

## Write surfaces

Under `git_authoritative`:

- Wagtail Admin shows the old StreamField disabled;
- REST create/update rejects `body` StreamField writes;
- authoritative edits happen through Git branch -> commit -> PR -> merge;
- Django runtime performs no Git commit/push/pull operations.

Other Article fields remain in Django/PostgreSQL, including:

- identity and hierarchy
- title / handle
- author
- summary
- tags
- featured image metadata
- SEO fields
- FAQs
- semantic relations
- Shopify IDs
- workflow / publication state

## Rollout

Recommended sequence:

```text
1. deploy code while CONTENT_STORE_MODE=db/mirror
2. run materialize_article_markdown --dry-run
3. run materialize_article_markdown
4. commit generated content/<locale>/.../body.md files
5. review and merge content PR
6. deploy the authoritative Git revision
7. set CONTENT_STORE_MODE=git_authoritative
8. publish a test Article and verify Shopify body HTML
9. keep StreamField columns for rollback until production validation is complete
10. progressively normalize legacy HTML to semantic Markdown
```

Rollback is configuration-only while the StreamField is retained:

```text
CONTENT_STORE_MODE=db
```

## Non-goals for Phase F

- deleting the StreamField column;
- recreating StreamField block schemas in Markdown;
- automatic HTML-to-Markdown conversion;
- moving relational metadata into Markdown;
- making Keystatic a runtime dependency;
- client-side React rendering;
- automatic Git writes from Django.

The central rule is intentionally small:

```text
Markdown is the editorial model.
Custom directives are exceptions, not a replacement block system.
```
