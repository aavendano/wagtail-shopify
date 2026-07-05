---
name: continue-work
description: >-
  Retoma el plan activo leyendo PROGRESS.md y .cursor/plans/active.plan.md.
  Use when resuming work, continuing a plan, starting a new session, or when
  the user says continúa, retoma, or where were we.
---

# Continue Work

Retoma trabajo en cualquier sesión sin depender de transcripts locales ni del botón Build de Plan Mode.

## Workflow

```
Task Progress:
- [ ] Step 1: Leer PROGRESS.md
- [ ] Step 2: Leer plan activo
- [ ] Step 3: Identificar siguiente fase pendiente
- [ ] Step 4: Ejecutar la fase
- [ ] Step 5: Actualizar plan y PROGRESS
```

### Step 1 — Leer PROGRESS.md

Buscar en la raíz del repo:
- Archivo del plan activo (default: `.cursor/plans/active.plan.md`)
- Última fase completada
- Siguiente paso indicado

Si `PROGRESS.md` no existe, usar `.cursor/plans/active.plan.md` directamente.

### Step 2 — Leer plan activo

Abrir el plan indicado en PROGRESS (o `active.plan.md`).
Extraer: contexto, fases con checkboxes, criterios de aceptación.

### Step 3 — Identificar siguiente fase

Buscar la primera línea con checkbox pendiente: `- [ ] Fase N — ...`
Si todas están marcadas, reportar plan completado y preguntar si archivar.

### Step 4 — Ejecutar la fase

Implementar solo lo descrito en esa fase. No avanzar a fases posteriores sin confirmación si son grandes.

### Step 5 — Actualizar progreso

Al completar una fase:

1. Cambiar `- [ ]` → `- [x]` en el `.plan.md`
2. Actualizar `PROGRESS.md`:

```markdown
## Plan activo
- **Archivo:** `.cursor/plans/active.plan.md`
- **Última fase completada:** Fase N (YYYY-MM-DD)
- **Siguiente:** Fase N+1 — descripción breve

## Historial reciente
| Fecha | Plan | Fase | Notas |
|-------|------|------|-------|
| YYYY-MM-DD | nombre-plan | N | resumen 1-2 líneas |
```

## Prompts de ejemplo

- "Continúa el plan activo"
- "Retoma donde lo dejamos"
- "¿Cuál es la siguiente fase del plan?"

## Limitaciones

- El botón Build de Plan Mode no viaja entre máquinas; el markdown + PROGRESS son la fuente de verdad.
- Commitear cambios de plan/PROGRESS solo si el usuario lo pide.
