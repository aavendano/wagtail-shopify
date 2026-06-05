# Uso del paquete `shopify_requests`

Este documento describe cómo consumir el paquete [`shopify_requests`](../shopify_requests/) para llamar al **Shopify Admin API** vía GraphQL desde cualquier parte del proyecto Django, sin acoplar vistas o jobs al SDK `shopify_app`.

## Rol del paquete

- **Infraestructura compartida**: centraliza transporte GraphQL, resolución de token persistido y normalización de resultados.
- **Regla de arquitectura**: la única implementación que debe invocar `ShopifyApp.admin_graphql_request` es [`shopify_requests/graphql_client.py`](../shopify_requests/graphql_client.py) (función `raw_admin_graphql`). El resto del código debe usar la API pública del paquete o capas de dominio bajo `shopify_requests/domains/`.

## Dependencias con `core`

`shopify_requests` importa modelos y servicios de la app `core` (por ejemplo `ShopConfig`, `core.token_service`, `get_shopify_app`). La app `core` **no** debe importar `shopify_requests` desde módulos que ya consuma `shopify_requests` en sentido inverso, para evitar importaciones circulares.

## Configuración

| Variable | Ubicación | Descripción |
|----------|-----------|-------------|
| `SHOPIFY_ADMIN_API_VERSION` | [`config/settings.py`](../config/settings.py) | Versión de la API Admin usada en GraphQL. Por defecto `2025-04`. Se puede sobreescribir con la variable de entorno homónima. |
| `SHOPIFY_API_KEY` / `SHOPIFY_API_SECRET` | `settings` / entorno | Credenciales de la app; las usa `get_shopify_app()` en [`core/utils.py`](../core/utils.py). |

## API pública

Definida en [`shopify_requests/__init__.py`](../shopify_requests/__init__.py):

### `execute_admin_graphql`

Punto de entrada genérico para ejecutar cualquier documento GraphQL contra el Admin API.

**Firma (resumen):**

```python
execute_admin_graphql(
    query,
    *,
    shop,
    api_version=None,
    variables=None,
    headers=None,
    max_retries=None,
    verification_result=None,
    invalid_token_response=None,
    shopify_app=None,
)
```

| Parámetro | Descripción |
|-----------|-------------|
| `query` | Cadena con el documento GraphQL. |
| `shop` | Identificador de tienda persistido con el token (mismo valor que en `ShopConfig.shop`, p. ej. `"mi-tienda"`). |
| `api_version` | Opcional; si se omite, se usa `settings.SHOPIFY_ADMIN_API_VERSION`. |
| `variables` | Diccionario de variables GraphQL; opcional. |
| `headers` | Cabeceras HTTP adicionales; opcional. |
| `max_retries` | Reintentos para el cliente SDK; opcional. |
| `verification_result` | Resultado de `verify_app_home_req` (u otro flujo con intercambio de token). Permite obtener token vía `ensure_offline_token_lifecycle` si aún no hay `access_token` en base de datos. |
| `invalid_token_response` | Objeto de respuesta para reintentos controlados en contexto embebido (típicamente `verification_result.new_id_token_response`). En jobs en segundo plano suele ser `None`. |
| `shopify_app` | Instancia opcional de `ShopifyApp`; por defecto se obtiene con `get_shopify_app()`. Útil en tests o para reutilizar la misma instancia que en la vista. |

**Retorno:** instancia de `AdminGraphqlResult` (ver más abajo).

### `fetch_shop_admin_graphql`

Operación de dominio de ejemplo en [`shopify_requests/domains/shop.py`](../shopify_requests/domains/shop.py): ejecuta una consulta mínima que devuelve el `id` GraphQL de la tienda (`shop { id }`).

Misma idea de parámetros opcionales: `verification_result`, `invalid_token_response`, `shopify_app`.

Para nuevas funcionalidades, se recomienda añadir módulos bajo `shopify_requests/domains/` que internamente llamen a `execute_admin_graphql`.

### `AdminGraphqlResult`

Dataclass con el resultado normalizado:

| Campo | Significado |
|-------|-------------|
| `ok` | Éxito lógico de la operación (alineado con el resultado del SDK). |
| `shop` | Dominio de tienda asociado al resultado. |
| `data` | Carga útil GraphQL (`dict`) o `None` si falló. |
| `extensions` | Extensiones GraphQL (p. ej. coste), si existen. |
| `error_code` | Código del log del SDK o `missing_access_token` si no hubo token. |
| `log_detail` | Texto de detalle del log. |
| `reauthorization_required` | `True` cuando el error indica que hay que reautorizar (p. ej. códigos alineados con `TOKEN_ERROR_CODES` en `core.token_service` o `unauthorized`). |
| `retryable` | Reservado para errores transitorios (p. ej. `throttled`); en la implementación actual es acotado. |
| `raw` | Resultado crudo del SDK cuando la llamada provino del cliente GraphQL o del lifecycle; puede ser `None` si solo falló la resolución de token sin objeto SDK. Sirve para traducir la respuesta HTTP con `shopify_result_to_django_response` en [`core/utils.py`](../core/utils.py). |

## Cómo se resuelve el access token

La lógica vive en [`shopify_requests/token_provider.py`](../shopify_requests/token_provider.py) (`resolve_access_token_for_admin`):

1. Se busca `ShopConfig` para el `shop` dado.
2. Si hay `access_token` guardado:
   - Solo se intenta **refresh** si el registro tiene `refresh_token` y `expires`, y `expires` ya pasó (respecto a `timezone.now()`).
3. Si no hay token usable y se pasó `verification_result`, se delega en `ensure_offline_token_lifecycle` de [`core/token_service.py`](../core/token_service.py) (intercambio o refresh según corresponda).
4. Si no hay token y no hay contexto de verificación, se devuelve `(None, None)` y `execute_admin_graphql` construye un `AdminGraphqlResult` con `error_code="missing_access_token"`.

Tras errores GraphQL con códigos críticos (`TOKEN_ERROR_CODES` o `unauthorized`), `execute_admin_graphql` llama a `clear_shop_tokens(shop)` para alinear el estado local con la política de reautorización.

## Contexto HTTP embebido (App Home) frente a jobs

| Escenario | `verification_result` | `invalid_token_response` |
|-----------|------------------------|---------------------------|
| Vista o request con sesión App Home recién verificada | Pasar el objeto devuelto por `verify_app_home_req` cuando haga falta intercambiar o completar token. | Suele ser `verification_result.new_id_token_response` para permitir al SDK generar respuestas de reintento acordes a Shopify. |
| Tarea en segundo plano, comando, webhook que solo tiene `shop` | Normalmente `None` (el token debe existir ya en `ShopConfig`). | `None`: si el token es inválido, la petición falla sin flujo de retry embebido. |

## Ejemplo en una vista

Patrón alineado con [`core/views.py`](../core/views.py) (`HomeView`):

```python
from shopify_requests.domains.shop import fetch_shop_admin_graphql

gql = fetch_shop_admin_graphql(
    shop,
    verification_result=verification_result,
    invalid_token_response=getattr(verification_result, "new_id_token_response", None),
    shopify_app=shopify_app,
)
if gql.ok and gql.data:
    shop_gid = (gql.data.get("shop") or {}).get("id")
```

Si `not gql.ok` y `gql.raw` es el resultado del SDK, se puede devolver la respuesta HTTP esperada por Shopify:

```python
from core.utils import shopify_result_to_django_response

if not gql.ok and gql.raw is not None:
    return shopify_result_to_django_response(gql.raw)
```

## Ejemplo de consulta arbitraria

```python
from shopify_requests import execute_admin_graphql

QUERY = """
query {
  shop {
    name
    primaryDomain { host }
  }
}
"""

result = execute_admin_graphql(
    QUERY,
    shop="mi-tienda",
    invalid_token_response=None,
)
if result.ok:
    nombre = (result.data or {}).get("shop", {}).get("name")
```

## Pruebas automatizadas

Para simular el Admin API sin red ni credenciales reales, parchea el cliente de bajo nivel en el **módulo** donde está definido (así `graphql_service` usa la versión mockeada):

```python
from unittest.mock import patch, SimpleNamespace

@patch("shopify_requests.graphql_client.raw_admin_graphql")
def test_algo(mock_raw):
    mock_raw.return_value = SimpleNamespace(
        ok=True,
        shop="mi-tienda",
        data={"shop": {"id": "gid://shopify/Shop/1"}},
        extensions=None,
        log=SimpleNamespace(code="success", detail="ok"),
        response=SimpleNamespace(status=200, body="", headers={}),
    )
    ...
```

No mockees `admin_graphql_request` del SDK directamente salvo que estés probando `graphql_client` de forma aislada.

## Qué no hacer

- No importes ni llames `shopify_app.admin_graphql_request` fuera de `shopify_requests/graphql_client.py`.
- No dupliques lógica de refresh o intercambio de token: usa `execute_admin_graphql` / `verification_result` o extiende `core.token_service` si falta una política nueva, en lugar de copiar código en vistas.
- No asumas que siempre habrá refresh en cada llamada: el refresh automático en el proveedor de token está condicionado a `expires` vencido (ver sección anterior).

## Más lectura en el código

| Archivo | Contenido |
|---------|-----------|
| [`shopify_requests/graphql_service.py`](../shopify_requests/graphql_service.py) | Orquestación y DTO. |
| [`shopify_requests/exceptions.py`](../shopify_requests/exceptions.py) | Excepciones de dominio (poco uso obligatorio si se prefiere el DTO). |
| [`core/token_service.py`](../core/token_service.py) | `TOKEN_ERROR_CODES`, `clear_shop_tokens`, `ensure_offline_token_lifecycle`, `refresh_stored_token_if_possible`. |
