# Convención de planes

Planes versionados en Git para continuidad entre sesiones y dispositivos.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `<feature>.plan.md` | Plan de una feature o iniciativa |
| `active.plan.md` | Plan en curso (copia o symlink del activo) |
| `../PROGRESS.md` | Ledger global — última fase, siguiente paso, historial |

## Crear un plan

1. Plan Mode → **Save to workspace** → `.cursor/plans/<nombre>.plan.md`
2. Copiar a `active.plan.md`
3. Registrar en `PROGRESS.md`
4. Commitear (cuando el usuario lo pida)

## Retomar trabajo

Invocar `/continue-work` o pedir "continúa el plan activo".

## Formato

Ver rule `.cursor/rules/plans-convention.mdc`.
