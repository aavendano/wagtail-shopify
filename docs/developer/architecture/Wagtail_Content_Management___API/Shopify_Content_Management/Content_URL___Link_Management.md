# Gestión de URLs y Enlaces de Contenido

Este módulo, `Content_URL___Link_Management`, es fundamental para la gestión y resolución de URLs y enlaces dentro de la plataforma de contenido Wagtail, especialmente en su integración con Shopify. Proporciona las herramientas necesarias para normalizar URLs, resolverlas a páginas de contenido específicas, gestionar la reescritura de enlaces de productos en artículos y facilitar la generación y persistencia de enlaces semánticos.

## Arquitectura General

El módulo se compone de varios servicios y utilidades que trabajan en conjunto para asegurar la coherencia y funcionalidad de los enlaces de contenido. A continuación, se presenta un diagrama de componentes que ilustra las interacciones principales:

```mermaid
graph TD
    A[Sistema de Gestión de Contenido Wagtail] --> B(Módulo Content_URL___Link_Management)
    B --> C(Resolución de URLs)
    B --> D(Utilidades de URLs de Tienda)
    B --> E(Reescritura de Enlaces de Artículo a Producto)
    B --> F(Servicio de Enlaces Semánticos)
    C --> G[Índice de URLs de Contenido (ContentUrlIndex)]
    D --> G
    E --> H[Información de Productos de Shopify]
    F --> I[Índice de Páginas (PageIndex) / Pgvector]
    F --> J[Modelos de Enlaces Semánticos]
    C --> K[Páginas de Contenido Wagtail]
    D --> K
    E --> K
    F --> K
```

### Componentes Principales

*   **Resolución de URLs**: Encargado de tomar una URL cruda (por ejemplo, de Google Search Console o una URL de tienda) y normalizarla para resolverla a una página de contenido Wagtail específica, utilizando el índice de URLs.
*   **Utilidades de URLs de Tienda**: Proporciona funciones y constantes para generar rutas canónicas de Shopify para diferentes tipos de páginas de Wagtail (productos, colecciones, blogs, artículos, términos de glosario, páginas de inicio y ubicaciones). También gestiona los prefijos de localización de Shopify Markets.
*   **Reescritura de Enlaces de Artículo a Producto**: Se encarga de analizar el contenido HTML de los artículos de Wagtail y reescribir los enlaces que apuntan a productos de Shopify, asegurando que utilicen los handles de producto correctos y actualizados.
*   **Servicio de Enlaces Semánticos**: Facilita la generación automática de enlaces internos semánticamente relevantes entre páginas de contenido, utilizando capacidades de búsqueda vectorial y persistiendo estas relaciones en el grafo de revisión de Wagtail.

## Sub-módulos

A continuación, se detalla la funcionalidad de los sub-módulos que componen `Content_URL___Link_Management`:

*   [Resolución y Normalización de URLs](Content_URL___Link_Management/Content_URL___Link_Management_resolucion_urls.md): Describe cómo el sistema normaliza y resuelve URLs a páginas de contenido Wagtail.
*   [Utilidades de URLs de Tienda](Content_URL___Link_Management/Content_URL___Link_Management_utilidades_urls_tienda.md): Detalla las funciones para generar y gestionar las rutas de URLs canónicas de Shopify.
*   [Reescritura de Enlaces de Artículo a Producto](Content_URL___Link_Management/Content_URL___Link_Management_reescritura_enlaces_articulos_productos.md): Explica el proceso de reescritura de enlaces de productos en el contenido de los artículos.
*   [Servicio de Enlaces Semánticos](Content_URL___Link_Management/Content_URL___Link_Management_servicio_enlaces_semanticos.md): Describe la funcionalidad de generación y gestión de enlaces internos semánticos.
