"""Editorial content persistence boundary (Phase B vertical slice).

Explicit ContentRepository boundary that lets selected editorial payloads be
mirrored outside PostgreSQL WITHOUT publication consumers or editing surfaces
knowing the backend.

Phase B invariants (see ADR-PERSIST-001 / HG-001):

* PostgreSQL row is AUTHORITATIVE for the payload; the filesystem file is a
  mirror. Losing the mirror never loses content.
* ``ContentRef`` is DETERMINISTIC (derived from stable DB identity, not from the
  slug or physical path) — no storage key is persisted (HG-001 C-001).
* Checksums are integrity / synchronization metadata only, never content
  authority (HG-001 C-002).
* The serializer round-trips the existing value LOSSLESSLY; no HTML->Markdown
  transformation happens in Phase B (HG-001 C-003).
* Editorial persistence is a content-write workflow, independent of the Shopify
  publish workflow (HG-001 C-004).

Scope: BlogPage.description only.
"""
