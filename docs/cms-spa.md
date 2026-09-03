# Docs for Puck CMS SPA

## Superficies

| URL | Rol |
|-----|-----|
| `/cms/` | SPA Puck para merchants/editores (staff o grupo `cms_editors`) |
| `/admin-django/` | Ops de sistema (ShopConfig, API keys, OAuth, `CmsSpaMount`) |
| `/api/v1/` | Contrato estable (SPA sesión, agentes API key/OAuth) |
| `/admin/` | Wagtail Admin — opcionalmente restringido con `CMS_RESTRICT_WAGTAIL_ADMIN=true` |

## Setup

```bash
# deps Python (incluye paquete local django_react_ui_editor)
pip install -r requirements.txt

# bundles SPA
cd cms_ui/frontend && npm install && npm run build

python manage.py migrate
python manage.py ensure_cms_spa
```

Crea un usuario staff (o añádelo al grupo `cms_editors`) y abre `/cms/`.

## Preview

`GET /api/v1/{resource}/{id}/preview` renderiza el template Wagtail de la última revisión
(draft). La SPA muestra el HTML en un iframe (“Previsualizar”).

## Empaquetado

Este repo se puede instalar como dependencia:

```bash
pip install "wagtail-shopify @ git+https://github.com/aavendano/wagtail-shopify.git"
```
