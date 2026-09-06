# Docs for Puck CMS SPA

## Superficies

| URL | Rol |
|-----|-----|
| `/cms/` | SPA Puck para merchants/editores (staff o grupo `cms_editors`) |
| `/admin-django/` | Ops de sistema (ShopConfig, API keys, OAuth, `CmsSpaMount`) |
| `/api/v1/` | Contrato estable (SPA sesión, agentes API key/OAuth) |
| `/admin/` | Wagtail Admin — opcionalmente restringido con `CMS_RESTRICT_WAGTAIL_ADMIN=true` |

## Setup (producción / tienda conectada)

```bash
# deps Python (incluye paquete local django_react_ui_editor)
pip install -r requirements.txt

# bundles SPA
cd cms_ui/frontend && npm install && npm run build

python manage.py migrate
python manage.py ensure_cms_spa
```

Crea un usuario staff (o añádelo al grupo `cms_editors`) y abre `/cms/`.

## Desarrollo local (SQLite :8083)

Aislado de Postgres. Perfil `config.settings_dev` carga `.env.dev`. Content store en entorno controlado: **`git_authoritative`** (Phase E locations + Phase F article `body.md`).

**Producción** (`:8082` / `.env`) permanece en `db`/`mirror` hasta el checklist de rollout del [contrato F](architecture/article-markdown-contract.md).

```bash
cp .env.dev.example .env.dev
# edita CONTENT_STORE_ROOT / secret si hace falta
# controlado: CONTENT_STORE_MODE=git_authoritative + CONTENT_STORE_GIT_FALLBACK_TO_DB=false

export DJANGO_SETTINGS_MODULE=config.settings_dev
export DEV_SQLITE_NAME=/tmp/cms-shop-dev.sqlite3

.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py ensure_cms_spa
.venv/bin/python manage.py createsuperuser   # usuario solo en SQLite dev

# o Run and Debug → "Daphne dev (8083)"
.venv/bin/daphne -b 127.0.0.1 -p 8083 config.asgi:application
```

Abre `http://127.0.0.1:8083/cms/` (o `/admin/`). Los `.md` viven en `CONTENT_STORE_ROOT` (por defecto `backend/content/`).

Para materializar texto ya en BD hacia archivos (antes del flip o al sembrar):

```bash
DJANGO_SETTINGS_MODULE=config.settings_dev .venv/bin/python manage.py materialize_editorial_content
DJANGO_SETTINGS_MODULE=config.settings_dev .venv/bin/python manage.py materialize_article_markdown
```

**Pytest** sigue usando `config.settings_test` (SQLite `:memory:`, content store forzado a `db`), no `settings_dev`.

## Preview

`GET /api/v1/{resource}/{id}/preview` renderiza el template Wagtail de la última revisión
(draft). La SPA muestra el HTML en un iframe (“Previsualizar”).

## Empaquetado

Este repo se puede instalar como dependencia:

```bash
pip install "wagtail-shopify @ git+https://github.com/aavendano/wagtail-shopify.git"
```
