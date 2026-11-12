# Docs for Puck CMS SPA

## Superficies

| URL | Rol |
|-----|-----|
| `/cms/` | SPA Puck para merchants/editores (staff o grupo `cms_editors`) |
| `/admin-django/` | Ops de sistema (ShopConfig, API keys, OAuth, `CmsSpaMount`) |
| `/api/v1/` | Contrato estable (SPA sesión, agentes API key/OAuth) |
| `/admin/` | Wagtail Admin — opcionalmente restringido con `CMS_RESTRICT_WAGTAIL_ADMIN=true` |

## Setup (producción / tienda conectada)

Producción típica: **systemd** + `git pull` en `/home/alejandro/apps/cms-shop/backend`
(ver README «Despliegue y reinicio»). No usa Coolify; el `Dockerfile` del repo es opcional.

```bash
pip install -r requirements.txt

# Bundles Polaris embebidos (obligatorio tras cambios en cms_ui/frontend o primer deploy Polaris)
./bin/build_cms_ui.sh   # escribe cms_ui/static/cms_ui/cms-embedded.{js,css}

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py ensure_cms_spa   # verifica cms-embedded.* y monta CmsSpaMount
sudo systemctl restart cms-shop-daphne
```

En el HTML de `/cms/` debe verse `cms-embedded.js?v=…` y `data-cms-spa-ui="polaris"`.
La URL del Admin de Shopify (`…/apps/…/cms/`) carga ese mismo `/cms/` en el iframe.

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
