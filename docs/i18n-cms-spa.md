# i18n — CMS SPA embebida (Polaris)

## Enfoque

| Capa | Mecanismo | Motivo |
|------|-----------|--------|
| SPA React (`/cms/`) | Catálogos JSON + `I18nProvider` | Sin dependencias extra; Vite embebe un solo bundle (`inlineDynamicImports`) |
| Componentes Polaris | `@shopify/polaris/locales/*.json` | Evita mezclas tipo «No registros found» en `IndexTable` |
| Django / Wagtail admin | `gettext` + `.po` en `locale/` | Plantillas y mensajes admin existentes |

No se usan `react-intl` ni `@lingui`: el volumen de cadenas es acotado y JSON + un hook `t()` mantiene el build SPA simple.

## Idiomas por tienda Shopify (no hardcode)

La lista del **conmutador** y el idioma por defecto vienen de la tienda, no de valores fijos en el frontend.

1. **Admin GraphQL** (versión `SHOPIFY_ADMIN_API_VERSION`, p. ej. `2025-04`):

   ```graphql
   {
     shopLocales(published: true) {
       locale
       primary
       published
       name
     }
   }
   ```

   Shopify documenta `shopLocales`, no `shop { primaryLocale }`. El locale principal es el elemento con `primary: true`.

2. **Caché** en `ShopConfig` (`cached_spa_locales`, `cached_spa_primary_locale`, `spa_locales_fetched_at`, TTL ~15 min).
3. **Bootstrap** (`__CMS_BOOTSTRAP__`): campos aditivos `primaryLocale`, `availableLocales`, `localeSource`, `language`, `setLanguageUrl`, `localeStorageKey`.
4. **Resolución de idioma** (orden):
   - cookie `cms_ui_locale` / `localStorage` (elección del usuario)
   - cookie `django_language` / sesión
   - `primaryLocale` de la tienda
   - primer locale disponible o `LANGUAGE_CODE`

5. **Fallback** si no hay token o falla la API: todos los `ALLOWED_LOCALE_CODES` y `source: "fallback"`. Si hay caché antigua: `stale_cache`.

### Mapeo Shopify → Wagtail UI

Solo se exponen códigos definidos en `config.settings.ALLOWED_LOCALE_CODES`:

| Shopify `locale` | Wagtail UI |
|------------------|------------|
| `en`, `en-US` | `en-US` |
| `en-CA` | `en-CA` |
| `es`, `es-US` | `es-US` |
| `fr`, `fr-CA` | `fr-CA` |

Otros idiomas de la tienda se omiten en el conmutador.

## Catálogos SPA

- `cms_ui/frontend/src/i18n/locales/en-US.json` — base en inglés
- `es-US.json` — traducción inicial completa
- `en-CA.json`, `fr-CA.json` — hooks vacíos (heredan `en-US` hasta traducir)

## Cambiar idioma en la SPA

`POST /cms/set-language/` con JSON `{ "language": "es-US" }` (CSRF). Valida contra `availableLocales` de la tienda. Sincroniza cookie Django y recarga la página.

## Operaciones (producción)

Tras cambios en cadenas Django/Wagtail:

```bash
python manage.py makemessages -l es_US -l en_CA -l fr_CA --ignore=cms_ui/frontend
python manage.py compilemessages
```

Tras cambios en el frontend:

```bash
./bin/build_cms_ui.sh
python manage.py collectstatic --noinput
sudo systemctl restart cms-shop-daphne
```

En el flujo de deploy habitual, ejecutar `compilemessages` **antes** de `collectstatic` / reinicio (junto a `migrate`).

## Añadir un idioma nuevo

1. Añadir código en `ALLOWED_LOCALE_CODES` y en `LANGUAGES` / `WAGTAIL_CONTENT_LANGUAGES`.
2. `python manage.py setup_locales` (Wagtail).
3. Crear `cms_ui/frontend/src/i18n/locales/<code>.json` y entrada Polaris si existe (`@shopify/polaris/locales/...`).
4. Extender `_SHOPIFY_TO_WAGTAIL` en `cms_ui/locale_mapping.py` si Shopify usa otra etiqueta.
5. `makemessages` + `compilemessages`, build SPA, tests.
