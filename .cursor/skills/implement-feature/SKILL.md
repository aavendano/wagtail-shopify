---
name: implement-feature
description: >-
  Workflow reutilizable para implementar features Django/Wagtail en wagtail-shopify.
  Use when implementing a new feature, adding API endpoints, sync logic, or Wagtail page types.
---

# Implement Feature

Workflow estándar para features en este repo.

## Checklist

```
Task Progress:
- [ ] Descubrir — entender spec y apps afectadas
- [ ] Planificar — crear o extender plan
- [ ] Implementar — diff mínimo siguiendo patrones existentes
- [ ] Verificar — make test
- [ ] Documentar — solo si cambia comportamiento
```

## Fase 1 — Descubrir

1. Leer spec (issue, prompt, sección del plan)
2. Identificar apps: `shopify_content`, `api`, `metaobjects`, `core`, etc.
3. Buscar código similar existente antes de crear abstracciones nuevas

Docs de referencia:
- [docs/shopify_content.md](../../../docs/shopify_content.md) — modelos, sync, jerarquía de páginas
- [docs/api-agents.md](../../../docs/api-agents.md) — endpoints, MCP, workflows agente

## Fase 2 — Planificar

Si no hay plan:
1. Crear `.cursor/plans/<feature>.plan.md` con fases y criterios de aceptación
2. Symlink o copiar a `active.plan.md`
3. Registrar en `PROGRESS.md`

Formato mínimo del plan:

```markdown
---
name: feature-name
overview: Una línea
active: true
created: YYYY-MM-DD
---

# Feature Name

## Fases
- [ ] Fase 1 — ...
- [ ] Fase 2 — ...

## Criterios de aceptación
- ...
```

## Fase 3 — Implementar

Patrones por tipo de cambio:

| Cambio | Dónde mirar |
|--------|-------------|
| Nuevo tipo de página | `shopify_content/models/`, mixin, sync outbound |
| Endpoint API | `api/routers/`, `api/schemas/`, `api/agent_registry.py` |
| Endpoint GSC API | `services/bigquery_gsc/bigquery_gsc/api/routers/`, `agent_registry.py` |
| Sync Shopify | `shopify_content/sync/`, `shopify_requests/` |
| Metaobject | `metaobjects/shopify_metaobjects/` |
| Management command | `shopify_content/management/commands/` |

Principios:
- Diff mínimo; una preocupación por commit lógico
- Reutilizar `ShopifyPageMixin`, `MetaobjectClient`, patrones de router existentes
- Registrar capacidades en `agent_registry.py` para endpoints nuevos

## Fase 4 — Verificar

```bash
make test
# o tests específicos:
.venv/bin/python -m pytest shopify_content/tests/test_<area>.py -v
```

Corregir fallos antes de marcar fase completada.

## Fase 5 — Documentar

Cualquier cambio en `api/` debe actualizar la documentación en el mismo cambio. Ver [`.cursor/rules/api-documentation.mdc`](../../rules/api-documentation.mdc).

Checklist mínimo (API):
- [ ] `agent_registry.py` actualizado (content o GSC según API)
- [ ] Router con `capability_docstring` + `agent_openapi_extra`
- [ ] `docs/api-agents.md` o `docs/api-gsc.md` si afecta consumidores externos
- [ ] `API_DESCRIPTION` en `api/main.py` si cambia matriz/workflows/auth
- [ ] `make test` pasa (paridad MCP/OpenAPI)

Otros cambios de comportamiento público:
- `README.md` — setup o arquitectura
- `docs/shopify_content.md` — modelos/sync

Al terminar, invocar lógica de `continue-work` para actualizar plan y PROGRESS.
