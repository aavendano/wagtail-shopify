---
name: theme-root-page-verification
overview: Verificar end-to-end en shopify theme dev la migración de índices CMS (glosario/locations) a entradas del metaobjeto root_page, tras eliminar la dualidad con Pages nativas.
active: true
created: 2026-07-06
---

# Verificación theme — root_page metaobject (glosario/locations)

## Contexto

Se migró la arquitectura de índices CMS de un modelo dual (Shopify Page nativa +
metaobjeto `root_page` como espejo de config) a un modelo unificado: `root_page` ahora
tiene capability `onlineStore` y es la página que el visitante ve directamente en
`/pages/index/{handle}`.

Commits:
- Backend (`wagtail-shopify`): `a07f224` — "Unify root page indexes onto the
  root_page metaobject, drop the Page duality"
- Frontend (`plt-frontend`): `3416eb0` — "Render CMS indexes from the root_page
  metaobject, remove Page duality"

Ambos en la rama `claude/wagtail-root-page-integration-05i6m1` de sus repos
respectivos. Todo el trabajo previo se verificó solo de forma estática (compilación
Python, JSON válido, balance de tags Liquid) — el sandbox donde se implementó no tenía
Django instalado ni Shopify CLI. Este plan cubre la verificación real, end-to-end, en
el repo del theme (`plt-frontend`), y define qué hacer si los datos reales de Shopify
no coinciden con el contrato esperado.

**Regla del rol:** el theme es la fuente de verdad sobre cómo debe verse el dato. Si un
campo del metaobjeto llega vacío, con un tipo distinto, o con una forma de JSON
distinta a la esperada, no se parchea el Liquid para tolerarlo — se diagnostica y se
redacta un prompt de cambio de backend (plantilla incluida abajo) en vez de adivinar
la corrección del lado de Wagtail.

## Fases

- [ ] Fase 1 — Setup backend: correr `ensure_metaobject_definitions`; confirmar en
      Shopify Admin que la definición `root_page` tiene `onlineStore` (`urlHandle:
      index`) y los 4 campos nuevos (`locale`, `index`, `index_alternates`,
      `index_noindex`)
- [ ] Fase 2 — Poblar entradas reales: publicar/forzar sync de al menos un
      `GlossaryTermPage` y un `LocationPage`, o correr `rebuild_glossary_index` /
      `rebuild_location_index`
- [ ] Fase 3 — Confirmar en Admin que una entrada `root_page` tiene URL de storefront
      real (template default bien asignado a la definición)
- [ ] Fase 4 — `shopify theme dev`: verificar listado, layout auto-detectado
      (glosario vs. locations vía `resource_type`), buscador, selector de idioma en
      `/pages/index/glossary-{en,es,fr}` y `/pages/index/locations-{en-us,es-us}`
- [ ] Fase 5 — Verificar `<head>` (hreflang por hermano + x-default, noindex meta
      cuando `index_noindex: true`) y confirmar el valor real de `template.name`
      dentro de una template de metaobjeto `root_page` (punto no verificable con
      documentación oficial durante el desarrollo — bloquea el gate en
      `layout/theme.liquid` y los checks de `snippets/navbar.liquid`)
- [ ] Fase 6 — Verificar breadcrumb y estado activo del navbar; regresión en
      `glossary_term` y `local_page` (no deberían haber cambiado)
- [ ] Fase 7 — `shopify theme check` sobre los archivos tocados + reporte pass/fail
- [ ] Fase 8 — Si todo pasa: limpieza final manual (borrar Pages nativas legacy
      `glossary-en`/etc. + redirects 301 a `/pages/index/...`, documentado, **no
      automatizado**). Si algo falla: uno o más prompts de cambio de backend
      (plantilla abajo)

## Estado

Backend y theme implementados y commiteados; **pendiente verificación real** (Fases
1–7) en un entorno con Shopify CLI y una tienda de prueba conectada al backend
desplegado.

## Prompt de implementación

Copiar el siguiente bloque completo a la sesión/agente que trabaje en `plt-frontend`
con acceso a `shopify theme dev`:

```
# Contexto

Se acaba de migrar la arquitectura de índices CMS (glosario, locations) de un modelo
dual (Shopify Page nativa + metaobjeto root_page como espejo de config) a un modelo
unificado: el metaobjeto `root_page` ahora tiene capability `onlineStore` y es la
página que el visitante ve directamente en `/pages/index/{handle}` (ej.
`/pages/index/glossary-en`, `/pages/index/locations-en-us`).

Commits relevantes:
- Backend (wagtail-shopify): a07f224 "Unify root page indexes onto the root_page
  metaobject, drop the Page duality"
- Frontend (plt-frontend): 3416eb0 "Render CMS indexes from the root_page metaobject,
  remove Page duality"

Ambos están en la rama `claude/wagtail-root-page-integration-05i6m1` de sus
respectivos repos. Todo el trabajo previo fue verificado solo de forma estática
(compilación Python, JSON válido, balance de tags Liquid) porque ese sandbox no tenía
Django instalado ni Shopify CLI. Tu tarea es la verificación real, end-to-end.

# Tu rol: el frontend es la fuente de verdad

No asumas que los datos que llegan desde Shopify (campos del metaobjeto root_page)
están en el formato correcto solo porque el backend "dice" que los envía así. Verifica
contra lo que realmente renderiza shopify theme dev.

Si encuentras que un campo llega vacío, con un tipo distinto al esperado, con una
forma de JSON distinta, o con un valor que no coincide con lo que la sección espera:

1. NO lo arregles parcheando el Liquid para tolerar el dato malformado (eso oculta el
   bug real y crea otra fuente de deuda técnica).
2. Diagnostica exactamente qué campo, qué se esperaba vs. qué llegó, y en qué línea de
   Liquid depende de ese campo.
3. Redacta un prompt de cambio de backend (ver plantilla al final) en vez de adivinar
   la corrección del lado de Wagtail — tú no tienes contexto del código Python, así
   que no lo edites directamente ni intentes replicar su lógica desde el theme.

# Contrato esperado (referencia rápida)

Cada entrada del metaobjeto root_page debe tener:

| Campo | Tipo Shopify | Forma esperada |
|---|---|---|
| locale | single_line_text_field | código simple: en, es, fr, en-US, es-US |
| resource_type | single_line_text_field | exactamente glossary o local-us (case-sensitive; de esto depende el auto-detect de layout en la sección) |
| index | json | {"version":1,"locale":"...","generated_at":"...","count":N,"sections":[{"key":"...","items":[{"label":"...","path":"...","handle":"..."}]}]} |
| index_alternates | json | {"version":1,"include_self":true,"x_default_handle":"...","alternates":[{"hreflang":"...","label":"...","handle":"..."}]} |
| index_noindex | boolean | true/false real (no string "true") |
| title | single_line_text_field | no vacío |

Handles esperados: glossary-{locale} (ej. glossary-en) y locations-{locale en
minúsculas} (ej. locations-en-us).

# Pasos de verificación

1. Setup backend (si tienes acceso a una tienda de prueba con el backend desplegado):
   correr `python manage.py ensure_metaobject_definitions` y confirmar en Shopify
   Admin → Content → Metaobjects → Root Page que la definición tiene onlineStore
   habilitado con urlHandle: index, y que existen los 4 campos nuevos (locale, index,
   index_alternates, index_noindex).
2. Publicar o forzar sync de al menos un GlossaryTermPage y un LocationPage (o correr
   rebuild_glossary_index / rebuild_location_index) para poblar entradas reales
   glossary-en, glossary-es, locations-en-us, etc.
3. En Shopify Admin, abrir una entrada root_page y confirmar que tiene URL de
   storefront (evidencia de que onlineStore + template default están bien
   conectados). Si no tiene URL, ese es un problema de configuración de Shopify
   (falta asignar el template default a la definición), no del Liquid — repórtalo.
4. shopify theme dev contra esa tienda. Navegar:
   - /pages/index/glossary-en, /pages/index/glossary-es, /pages/index/glossary-fr
   - /pages/index/locations-en-us, /pages/index/locations-es-us
5. Para cada una, verificar:
   - El listado se renderiza (items con label + link correcto a la página de detalle).
   - El layout es el correcto (glosario = A-Z + lista; locations = grid + nav por
     estado) — esto depende de metaobject.resource_type.value, confírmalo con las
     herramientas de debug del tema si el layout sale mal.
   - Buscador client-side filtra correctamente.
   - El selector de idioma (locale_alternates) muestra los hermanos correctos y el
     link activo coincide con la entrada actual.
   - Ver código fuente (view-source:) del <head>: debe haber <link rel="alternate"
     hreflang="..."> por cada hermano + x-default. Si index_noindex es true en alguna
     entrada (pruébalo manualmente desde Admin → Custom data), debe aparecer <meta
     name="robots" content="noindex, follow">.
6. Confirmar breadcrumb y navbar: el estado "activo" del link de glosario/locations en
   el navbar debe encenderse solo en esas páginas — esto depende de que
   template.name == 'root_page' sea el valor real dentro de una template de
   metaobjeto de ese tipo. Este punto no se pudo confirmar con documentación oficial
   durante el desarrollo — es lo más importante a verificar empíricamente. Si
   template.name resulta ser otro valor (p. ej. 'metaobject'), avísame: hay que
   ajustar el gate en layout/theme.liquid y los checks en snippets/navbar.liquid.
7. Regresión: visitar una página de detalle glossary_term y local_page existente,
   confirmar que nada se rompió (esas no cambiaron en este trabajo).
8. Correr shopify theme check sobre los archivos tocados.

# Si algo no encaja: plantilla de prompt de cambio de backend

Si detectas un problema real de datos (no de tu Liquid), redacta algo con esta forma
y entrégalo para pasarlo a una sesión con contexto del backend Wagtail:

## Cambio de backend requerido: <título corto>

**Dónde se detectó:** <archivo Liquid + línea que consume el dato>
**Campo afectado:** metaobject.<campo>
**Esperado:** <forma/tipo esperado, según el contrato de docs/shopify_content.md>
**Recibido:** <valor real observado, con ejemplo>
**Impacto:** <qué se rompe en el storefront>
**Sugerencia (opcional):** <función/archivo probable en wagtail-shopify a revisar,
  ej. shopify_content/sync/outbound.py::sync_root_index_locales, o
  shopify_content/glossary/index.py::build_glossary_index_json>

No implementes el fix en Python tú mismo salvo que se te pida explícitamente — tu
entregable en ese caso es el prompt de cambio, no el parche.

# Entregable de esta sesión

- Tabla pass/fail de los pasos de verificación anteriores.
- Si todo pasa: confirmación de que se puede avanzar al paso de limpieza final (borrar
  las Pages nativas legacy glossary-en/etc. en Shopify Admin y crear redirects 301
  hacia /pages/index/..., documentado como paso manual en el plan original — no lo
  automatices).
- Si algo falla: uno o más prompts de cambio de backend usando la plantilla de arriba.
```

## Criterios de aceptación

- [ ] Las 5 entradas `root_page` (`glossary-en/es/fr`, `locations-en-us/es-us`)
      tienen URL de storefront funcionando en `/pages/index/{handle}`
- [ ] `<head>` emite hreflang recíproco + x-default en cada una
- [ ] `index_noindex: true` en una entrada produce `<meta name="robots"
      content="noindex, follow">`
- [ ] Layout glosario vs. locations correcto sin configuración manual por instancia
- [ ] `template.name` dentro de una template de metaobjeto `root_page` confirmado
      empíricamente (documentar el valor real encontrado)
- [ ] Sin regresión en `glossary_term`/`local_page`
- [ ] `shopify theme check` sin errores nuevos

## Planes relacionados

- [`wagtail-root-index-section.plan.md`](wagtail-root-index-section.plan.md) —
  diseño SEO previo (Page-based), superseded por este plan
- [`theme-index-pages.plan.md`](theme-index-pages.plan.md) — implementación
  original de las plantillas Liquid (Page-based), superseded por este plan
