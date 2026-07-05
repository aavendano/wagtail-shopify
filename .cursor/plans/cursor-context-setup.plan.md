---
name: cursor-context-setup
overview: Bootstrap de contexto persistente — rules, skills y convención de planes
active: false
created: 2026-07-05
completed: 2026-07-05
---

# Contexto persistente en el repo

Setup inicial de rules, skills y convención de planes versionados en Git.

## Contexto

Plan de referencia: contexto persistente para wagtail-shopify.
Ledger de progreso: `PROGRESS.md` (solo repo, sin Notion).

## Fases

- [x] Fase 0 — Limpieza `.cursor/` (debug logs, instrumentación API, .gitignore)
- [x] Fase 1 — Rules (`project.mdc`, `python-django.mdc`, `plans-convention.mdc`)
- [x] Fase 2 — Skills (`continue-work`, `implement-feature`)
- [x] Fase 3 — Documentar convención en `plans/README.md`
- [x] Fase 4 — Verificar flujo en sesión nueva

## Criterios de aceptación

- `.cursor/rules/`, `.cursor/skills/`, `.cursor/plans/` versionados en Git
- `PROGRESS.md` actualizado con checkpoint actual
- Sin writes a `.cursor/debug-*.log` en runtime normal
- Skill `continue-work` puede retomar desde Fase 3
