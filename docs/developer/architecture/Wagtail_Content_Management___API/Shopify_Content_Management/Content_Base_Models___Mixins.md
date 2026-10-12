# Modelos Base y Mixins de Contenido

Este módulo define los modelos base y mixins fundamentales utilizados en la gestión de contenido de Shopify dentro de Wagtail. Proporciona las estructuras de datos esenciales para representar páginas raíz, elementos de FAQ, metacampos, y el seguimiento de operaciones de sincronización y comandos embebidos. Estos componentes son la base para construir tipos de página de contenido más específicos y para integrar la funcionalidad de Wagtail con la plataforma Shopify.

## Arquitectura General

El módulo `Content_Base_Models___Mixins` se encuentra dentro del `Shopify_Content_Management` y establece los cimientos para la estructura de contenido. Se relaciona con otros módulos al proporcionar modelos abstractos y concretos que son extendidos o referenciados por páginas de contenido más específicas, como artículos, colecciones o productos. También interactúa con los servicios de sincronización y comandos embebidos para gestionar el flujo de datos entre Wagtail y Shopify.

```mermaid
C4Context
    title Diagrama de Contexto de Modelos Base y Mixins de Contenido

    System_Ext(shopify, "Plataforma Shopify", "Sistema de comercio electrónico.")
    System_Boundary(wagtail, "Sistema de Gestión de Contenido Wagtail") {

        Container(content_base_models_mixins, "Módulo de Modelos Base y Mixins de Contenido", "Define los modelos fundamentales y mixins para la gestión de contenido de Shopify.")

        Container(specific_content_models, "Módulos de Modelos de Contenido Específicos", "Ej. Modelos de Contenido de Blog, Colección, Producto.")

        Container(sync_services, "Servicios de Sincronización de Contenido", "Gestiona la sincronización de datos entre Wagtail y Shopify.")

        Container(embedded_command_registry, "Registro de Comandos Embebidos", "Gestiona y rastrea la ejecución de comandos asíncronos.")

        Container(content_indexing, "Servicios de Indexación de Contenido", "Indexa el contenido y sus referencias para búsqueda y enlaces semánticos.")

        Container(content_url_management, "Gestión de URLs de Contenido", "Mapea URLs de Shopify a páginas de Wagtail.")
    }

    Rel(content_base_models_mixins, specific_content_models, "Proporciona modelos base y mixins abstractos para")
    Rel(content_base_models_mixins, sync_services, "Almacena el estado de las ejecuciones de sincronización")
    Rel(content_base_models_mixins, embedded_command_registry, "Almacena el estado de las ejecuciones de comandos")
    Rel(content_base_models_mixins, content_indexing, "Almacena índices de contenido y referencias")
    Rel(content_base_models_mixins, content_url_management, "Almacena mapeos de URLs")
    Rel(sync_services, shopify, "Sincroniza datos con")

```

## Funcionalidad de Sub-módulos

Este módulo se descompone en los siguientes sub-módulos, cada uno con responsabilidades específicas:


- [Página Raíz de Shopify](Content_Base_Models___Mixins/Content_Base_Models___Mixins_ShopifyRootPage_Modelo.md): Define la página raíz para el contenido de Shopify, sirviendo como un contenedor para todos los tipos de páginas de contenido de Shopify.
- [Modelos de Indexación de Contenido](Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModelosIndexacionContenido.md): Proporciona modelos para indexar el contenido editorial y sus referencias.
- [Modelo de Índice de URL de Contenido](Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModeloIndiceURLContenido.md): Mapea rutas de URL de Shopify a páginas de Wagtail para correlacionar el tráfico y el contenido del CMS.
- [Modelos de Enlaces Semánticos](Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModelosEnlacesSemanticos.md): Define modelos para enlaces internos tipados entre páginas de Wagtail.
- [Modelo de Ejecución de Comandos Embebidos](Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModeloEjecucionComandoEmbebido.md): Rastrea la ejecución de trabajos de comandos de gestión asíncronos enviados desde la aplicación Shopify.
- [Modelo de Ejecución de Sincronización de Shopify](Content_Base_Models___Mixins/Content_Base_Models___Mixins_ModeloEjecucionSincronizacionShopify.md): Rastrea los trabajos de sincronización asíncronos de Shopify (entrada/salida) enviados a través de Celery.
- [Mixins Base](Content_Base_Models___Mixins/Content_Base_Models___Mixins_MixinsBase.md): Define mixins reutilizables como elementos FAQ y metacampos de Shopify para diferentes tipos de páginas.
