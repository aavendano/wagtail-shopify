---
id: content-store
type: module-design
title: Git-backed Editorial Content Store
status: draft
parent: wagtail-shopify-architecture
---
# Git-backed Editorial Content Store

Owns deterministic editorial content references, repository reads/writes, serialization, Markdown parsing/rendering, validation, and explicit authority modes. It exposes domain-level editorial access and hides paths, frontmatter, and Git representation. Django runtime does not execute Git commands; PostgreSQL remains the authority for non-externalized operational state.
