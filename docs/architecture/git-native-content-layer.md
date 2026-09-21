# Capa Git-native Markdown (`content_store`)

Status: implementado en rama `cursor/git-native-content-layer-e08d`  
Coordinación: [`content-layer-coordination.md`](content-layer-coordination.md)

## Resumen

La capa editorial evoluciona desde un serializer lineal y un renderer monolítico hacia:

```text
body.md (YAML + Markdown)
  → FrontmatterVerbatimSerializer (PyYAML)
  → CanonicalDocument (ref + checksum + derived_refs)
  → markdown/ (parser, directives, references, validation, security, renderer)
  → HTML storefront / índice derivado PostgreSQL
```

Git sigue siendo autoridad; Django no ejecuta `git` en lecturas ni saves.

## CanonicalDocument

`FilesystemContentRepository.read_canonical(ref)` devuelve:

- `ref`, `body`, `metadata`, `format`, `checksum`
- `derived_refs`: tokens estables (`product:handle`, `asset:id`, …) extraídos del cuerpo

`read()` conserva `ContentDocument` para consumidores existentes.

## Comandos operativos

```bash
python manage.py content_validate [--json] [--root PATH]
python manage.py content_index_rebuild [--root PATH]
```

`content_validate` es determinista, solo lectura, exit code `1` si hay incidencias.

## Perfiles de render

- `trusted_editorial` (por defecto): HTML crudo en Markdown permitido (revisión Git).
- `restricted`: elimina `<script>`, atributos `on*` y URLs `javascript:`.

## Referencias

- Directivas: `{% product handle="…" %}`, `ref="product:…"` (futuro).
- Assets: `asset:<stable-id>` en Markdown, resolver `PassthroughAssetResolver` intercambiable.

## CI

Workflow `.github/workflows/content-validate.yml`: pytest del content-store y `content_validate` cuando existe el árbol `content/`.
