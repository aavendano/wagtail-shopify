# Coordinación — capa Git-native Markdown (`content_store`)

Última actualización: 2026-09-14  
Rama de trabajo: `cursor/git-native-content-layer-e08d`

## Mapa de arquitectura (Agente 1 — inspección previa a CS1)

### Implementado hoy

| Área | Estado | Notas |
|------|--------|-------|
| `ContentRef` + `relative_path` | Estable | PK + locale + field; sin slug en identidad |
| `ContentDocument` | Estable | `body`, `fmt`, `meta`, `checksum` |
| `ContentRepository` / `FilesystemContentRepository` | Estable | Lectura/escritura atómica; sin Django/Git en runtime |
| `FrontmatterVerbatimSerializer` | **CS1** | Frontmatter línea a línea; migrar a PyYAML |
| `page.editorial.<field>` (`EditorialMixin`) | Estable | D-012 |
| Modos `db` / `mirror` / `git_authoritative` | Estable | `GIT_NATIVE_FIELDS` solo `ArticlePage.body` |
| `markdown_renderer.py` | **CS2** | Monolito Python-Markdown + regex directivas |
| Materialize commands | Estable | `materialize_editorial_content`, `materialize_article_markdown` |
| Sync artículo | Estable | `article_markdown.py` → `render_editorial_markdown` |
| Tests content-store | Estable | blog, glossary, location, git, article markdown |

### Contratos públicos (no romper)

- `ref_for(page, field_key)` → `ContentRef`
- `resolve_editorial(page, field_key)` → `str` (cuerpo dominio)
- `FilesystemContentRepository.read/write`
- `render_editorial_markdown(source)` → HTML storefront
- Excepciones: `ContentNotFound`, `ContentConflict`, `MarkdownRenderError`

### Archivos a modificar por change set

| CS | Archivos nuevos / tocados |
|----|---------------------------|
| CS1 | `contracts.py` (`CanonicalDocument`), `serializers.py` (PyYAML), `backends.py`, tests YAML |
| CS2 | `content_store/markdown/*`, refactor `markdown_renderer.py` (facade), tests parser/directivas |
| CS3 | `markdown/references.py`, `markdown/assets.py`, `markdown/security.py`, integración renderer |
| CS4 | `management/commands/content_validate.py`, `content_index_rebuild.py`, modelos índice, CI, docs |

### Riesgos

1. Cambiar parser frontmatter puede alterar archivos re-materializados (mitigar: round-trip byte-identical en cuerpo).
2. Extraer `markdown/` no debe cambiar HTML de artículos (regresión con snapshots de tests existentes).
3. Índice derivado en PostgreSQL: solo reconstrucción explícita; no autoridad editorial.
4. `markdown-it-py` añade dependencia; renderer final sigue usando Python-Markdown para HTML (paridad).

## Tabla de coordinación (9 agentes)

| Área | Agente | Archivos principales | Estado | Dependencias |
|------|--------|----------------------|--------|--------------|
| Arquitectura / dominio | 1 | `contracts.py`, `backends.py` | Completado | — |
| YAML front matter | 2 | `serializers.py`, `tests/test_content_store_yaml.py` | Completado | Agente 1 |
| Parser Markdown | 3 | `content_store/markdown/parser.py`, `validation.py` | Completado | CS1 |
| Directivas / referencias | 4 | `markdown/directives.py`, `references.py`, `renderer.py` | Completado | Agente 3 |
| Assets | 5 | `markdown/assets.py` | Completado | Agente 4 |
| content_validate | 6 | `management/commands/content_validate.py` | Completado | CS1–CS3 |
| ContentIndex | 7 | `models/content_index.py`, `content_index_rebuild.py` | Completado | CS2–CS4 |
| Rendering / seguridad | 8 | `markdown/security.py`, perfiles render | Completado | Agente 3–4 |
| CI / docs | 9 | `.github/workflows/content-validate.yml`, `docs/architecture/*` | Completado | CS6 |

## Criterios de aceptación (checklist 1–15)

1. [x] `ContentRepository` sin acoplamiento Django; sin Git en request/save  
2. [x] `CanonicalDocument` con ref, body, metadata, format, checksum, derived_refs  
3. [x] Front matter YAML real (PyYAML), cuerpo byte-exacto, YAML inválido explícito  
4. [x] Paquete `content_store/markdown/` modular (parser, directives, references, validation, renderer)  
5. [x] Directivas product/collection/page/callout tipadas + `ContentReference` + `ReferenceResolver`  
6. [x] Compat `{% product handle="..." %}` y infra `ref=` para futuro  
7. [x] Contrato `asset:<stable-id>` con resolver desacoplado  
8. [x] Perfiles `trusted_editorial` vs `restricted` + sanitización  
9. [x] `manage.py content_validate` determinista, `--json`, exit ≠ 0, sin git/db write  
10. [x] `ContentIndex` derivado + `content_index_rebuild` reconstruible  
11. [x] Sin HTML→Markdown automático; StreamField legacy intacto  
12. [x] Workflow CI *Editorial content validate* verde (migraciones `0008`–`0010` + catch-up schema)  
13. [x] CI valida `content/**` + tests shopify_content  
14. [x] Docs arquitectura actualizadas  
15. [x] HTML `ArticlePage.body` igual salvo tests justificados (renderer preserva contrato; facade `markdown_renderer.py`)  

## Informe consolidado (entregable)

### Archivos por CS

| CS | Archivos |
|----|----------|
| CS1 | `contracts.py`, `serializers.py`, `backends.py`, `tests/test_content_store_yaml.py` |
| CS2 | `content_store/markdown/*`, `markdown_renderer.py`, `tests/test_content_store_markdown_layer.py` |
| CS3 | `markdown/assets.py`, `markdown/security.py`, ampliación `renderer.py` / `references.py` |
| CS4 | `validation_runner.py`, `content_index_service.py`, commands, `models/content_index.py`, migration `0008`, CI workflow, docs |

### Decisiones

- `CanonicalDocument` vía `read_canonical`; `read()` sin cambio semántico para legacy.
- PyYAML solo en frontmatter; identidad sigue en `ContentRef`/ruta, no en YAML.
- `markdown-it-py` para inspección; HTML sigue con Python-Markdown `extra`.
- Índice PostgreSQL es derivado y reconstruible; no autoridad editorial.

### Deuda

- `0009_shopifyrootpage_operational_fields` cubre drift de `ShopifyRootPage`; suite Wagtail global puede tener deuda adicional fuera de content-store.
- Resolver asset URLs contra CDN real de la tienda (hoy passthrough).
- Validación `content_validate` en árbol `content/` de producción tras materialize.

### Tests ejecutados

```bash
python3 -m pytest shopify_content/tests/test_article_markdown_editorial.py::EditorialMarkdownRendererTests \
  shopify_content/tests/test_content_store_yaml.py \
  shopify_content/tests/test_content_store_markdown_layer.py \
  shopify_content/tests/test_content_validate.py \
  shopify_content/tests/test_content_index_rebuild.py \
  shopify_content/tests/test_content_store_blog.py::SerializerRoundTripTests \
  shopify_content/tests/test_content_store_blog.py::FilesystemRepositoryTests -q
# 33 passed
```

### Riesgos

- Drift de formato frontmatter al re-materializar (cuerpo intacto; diff cosmético en YAML).
- Índice desactualizado si no se corre `content_index_rebuild` tras deploy de contenido.
