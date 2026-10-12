# Resolución de URLs de Contenido

Este módulo, `Content_URL___Link_Management_resolucion_urls`, es fundamental para la gestión de URLs dentro del sistema de gestión de contenido (CMS) basado en Wagtail, especialmente en su integración con Shopify. Su propósito principal es normalizar y resolver URLs de escaparates o de Google Search Console (GSC) a páginas de contenido específicas en Wagtail.

## Propósito y Funcionalidad Principal

El módulo se encarga de:
1.  **Normalización de URLs**: Convertir URLs brutas (raw_url) en rutas normalizadas y detectar prefijos de localización (locale_prefix).
2.  **Resolución de URLs**: Buscar una URL normalizada en el índice de URLs de contenido para identificar la página Wagtail correspondiente.
3.  **Proporcionar Información de Coincidencia**: Devolver un objeto `ContentUrlMatch` que encapsula la información de la página Wagtail encontrada, incluyendo su ID, tipo de contenido, título, ruta normalizada y el prefijo de localización.

### Componentes Principales

El módulo se compone de los siguientes elementos clave:

*   `ContentUrlMatch`: Una dataclass que representa el resultado de una coincidencia de URL.
*   `normalize_url(raw_url: str, *, property_url: str = '') -> tuple[str, str]`: Función que normaliza una URL.
*   `resolve_url(raw_url: str, *, property_url: str = '') -> ContentUrlMatch | None`: Función que resuelve una URL a una página de contenido Wagtail.

### `ContentUrlMatch`

Esta dataclass se utiliza para estructurar los datos resultantes de una operación de resolución de URL exitosa.

```python
@dataclass(frozen=True)
class ContentUrlMatch:
    wagtail_page_id: int
    content_type: str
    title: str
    normalized_path: str
    locale_prefix: str | None
    match_quality: str  # exact | unmapped
```

**Campos:**
*   `wagtail_page_id`: El ID de la página Wagtail que coincide.
*   `content_type`: El tipo de contenido de la página Wagtail (ej. 'article', 'product').
*   `title`: El título de la página Wagtail.
*   `normalized_path`: La ruta URL normalizada de la página.
*   `locale_prefix`: El prefijo de localización detectado (ej. 'es-us', 'en-ca') o `None` si no hay.
*   `match_quality`: Indica la calidad de la coincidencia (actualmente 'exact' o 'unmapped').

### `normalize_url`

Esta función es responsable de limpiar y estandarizar las URLs de entrada.

**Funcionalidad:**
*   Elimina el dominio, la cadena de consulta, el fragmento y la barra final.
*   Detecta prefijos de localización de Shopify Markets (ej. `/es-us/`, `/en-ca/`) utilizando la constante `KNOWN_LOCALE_PREFIXES` de [shopify_content/storefront_urls.py](../storefront_urls.md).
*   Asegura que la ruta siempre comience con `/`.

### `resolve_url`

Esta función es el punto de entrada para buscar y emparejar URLs con contenido Wagtail.

**Funcionalidad:**
*   Primero normaliza la `raw_url` utilizando `normalize_url`.
*   Consulta el modelo `ContentUrlIndex` (definido en [Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModeloIndiceURLContenido.md](../Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModeloIndiceURLContenido.md)) para encontrar una coincidencia.
*   Prioriza las coincidencias con `locale_prefix`. Si no se encuentra una, intenta buscar sin `locale_prefix`.
*   Si se encuentra una entrada en el índice, recupera la página Wagtail asociada y construye un objeto `ContentUrlMatch`.
*   Retorna `None` si no se encuentra ninguna página indexada que coincida con la URL.

## Arquitectura y Relaciones de Componentes

El módulo `Content_URL___Link_Management_resolucion_urls` es un componente clave en la capa de resolución de URLs del CMS. Se interconecta con la base de datos a través del modelo `ContentUrlIndex` y utiliza configuraciones de URL desde `shopify_content/storefront_urls.py`.

```mermaid
graph TD
    A[URL Externa<br>(GSC / Escaparate)] --> B{normalize_url};
    B --> C{Ruta Normalizada & Prefijo de Localización};
    C --> D[resolve_url];
    D -- Consulta --> E[ContentUrlIndex<br>(Base de Datos)];
    E -- Contiene --> F[Página Wagtail];
    D -- Utiliza --> G[KNOWN_LOCALE_PREFIXES<br>(shopify_content/storefront_urls.py)];
    D -- Produce --> H[ContentUrlMatch];
    F --> H;

    subgraph M["Módulo Content_URL___Link_Management_resolucion_urls"]
        B
        C
        D
        H
    end

    subgraph N["Módulo Content_Base_Models___Mixins_ModeloIndiceURLContenido"]
        E
    end

    subgraph O["Módulo Content_URL___Link_Management"]
        G
    end

    M --- Depende de ---> N
    M --- Depende de ---> O
```

**Relaciones Clave:**
*   **`normalize_url`**: Consume `raw_url` y `property_url`, y `KNOWN_LOCALE_PREFIXES` para producir una ruta normalizada y un prefijo de localización.
*   **`resolve_url`**: Consume la salida de `normalize_url` y consulta el modelo `ContentUrlIndex`. Recupera el objeto `wagtail_page` asociado a la entrada del índice.
*   **`ContentUrlIndex`**: Este modelo (definido en [Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModeloIndiceURLContenido.md](../Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModeloIndiceURLContenido.md)) actúa como una tabla de búsqueda para las URLs de contenido, almacenando las rutas normalizadas y sus correspondientes IDs de página Wagtail.
*   **`shopify_content/storefront_urls.py`**: Proporciona la lista de `KNOWN_LOCALE_PREFIXES` que son cruciales para la detección de la localización en las URLs.

## Cómo el Módulo Encaja en el Sistema General

Este módulo es una parte integral de la [Gestión de URLs y Enlaces de Contenido](../Content_URL___Link_Management.md) dentro de la [API y Gestión de Contenido de Wagtail para Shopify](../../Shopify_Content_Management.md). Su funcionalidad de resolución de URLs es utilizada por varios subsistemas para:

*   **Enrutamiento de Solicitudes**: Dirigir las solicitudes entrantes de URLs a las páginas Wagtail correctas, permitiendo que el sistema responda con el contenido editorial adecuado.
*   **SEO y Analíticas**: Al normalizar y resolver URLs, facilita el seguimiento y la integración con herramientas como Google Search Console, asegurando que el contenido sea correctamente atribuido y analizado.
*   **Experiencia de Usuario**: Asegura que los usuarios sean dirigidos al contenido localizado y correcto, incluso si acceden a URLs con variaciones o con diferentes prefijos de localización.

Al centralizar la lógica de resolución de URLs, este módulo proporciona una base robusta y consistente para manejar las URLs de contenido en un entorno complejo como el de Shopify con soporte para múltiples localizaciones.
