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

## Planes agnósticos de tienda

El proyecto es **single-instance** (una instalación = una tienda), pero **replicable** en cualquier shop. Los planes documentan contratos y handles estables, no datos de un merchant concreto.

| Prohibido en planes | Permitido |
|---------------------|-----------|
| Dominios `*.myshopify.com` reales | Handles canónicos (`glossary-en`, `locations-en-us`) |
| Subdominios de dev store concretos | Placeholders (`gid://shopify/Page/...`, `{shop}.myshopify.com`) |
| GIDs numéricos de una instalación | Comandos que leen `ShopConfig` en runtime |

**Configuración de tienda activa** (fuera de los planes):

- Backend: `ShopConfig` tras OAuth; credenciales en `.env`
- Theme dev: `shopify theme dev --store <dominio>` o `.shopify/project.json`
