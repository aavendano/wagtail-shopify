# Configuración de Exportación de Contenido

Este módulo, `Content_Export_Configuration`, es responsable de definir la lógica para la exportación de diferentes tipos de contenido de Wagtail a Shopify. Actúa como un puente entre el sistema de gestión de contenido (CMS) y la plataforma de comercio electrónico, asegurando que el contenido editorial, como artículos de blog, términos de glosario y páginas de ubicación, se indexe y se exporte correctamente a Shopify.

## Propósito
El propósito principal de este módulo es proporcionar una estructura configurable y extensible para generar payloads de índice precomputados, manejar la localización (hreflang) y las directivas de noindex para el contenido exportado. Esto permite que el contenido se sincronice con Shopify, donde puede ser consumido por la tienda en línea.

## Arquitectura General
El módulo se basa en un patrón de "consumidores" (`Consumer`) que encapsulan la lógica específica para cada tipo de contenido a exportar. Existe una clase base `RootIndexConsumer` que establece las propiedades y métodos comunes, y luego clases derivadas para tipos de contenido específicos como blogs, glosarios y ubicaciones.

El flujo de trabajo general es el siguiente:
1. **Configuración**: Las páginas raíz de Shopify en Wagtail (ej. `ShopifyRootPage`) almacenan la configuración de exportación, incluyendo qué tipos de contenido están habilitados para la exportación y sus locales asociados.
2. **Construcción de Payload**: Cada consumidor de índice es responsable de construir el payload JSON que representa el índice del contenido para un locale específico.
3. **Sincronización**: Una vez que el payload está construido, se puede poner en cola una tarea de sincronización para enviar este payload a Shopify, generalmente actualizando los metafields de una página de Shopify designada o metaobjects.

```mermaid
graph TD
    A[Página Raíz de Shopify (Wagtail)] -->|`export_config`| B{Configuración de Exportación};
    B -->|Habilitado, `locales`| C{Consumidor de Índice (Ej. `BlogListingsConsumer`)};
    C -->|`build_payload(locale)`| D[Payload JSON del Índice];
    D -->|`queue_sync()`| E[Tarea de Sincronización (Celery)];
    E -->|Actualizar Metafields/Metaobjects| F[Shopify];

    subgraph Componentes del Módulo
        C1[`RootIndexConsumer`]
        C2[`BlogListingsConsumer`]
        C3[`GlossaryIndexConsumer`]
        C4[`LocationIndexConsumer`]
        C5[`SinglePageListingsConsumer`]
    end

    C --> C1;
    C --> C2;
    C --> C3;
    C --> C4;
    C --> C5;
```
*Diagrama 1: Arquitectura General del Módulo de Configuración de Exportación de Contenido.*

## Sub-módulos

A continuación, se describen los sub-módulos clave dentro de `Content_Export_Configuration`:

*   [Consumidor Base de Índice de Contenido](Content_Export_Configuration/Content_Export_Configuration_BaseConsumer.md)
*   [Consumidor de Listados de Blog](Content_Export_Configuration/Content_Export_Configuration_BlogListings.md)
*   [Consumidor de Índice de Glosario](Content_Export_Configuration/Content_Export_Configuration_Content_Export_Configuration_GlossaryIndex.md)
*   [Consumidor de Índice de Ubicaciones](Content_Export_Configuration/Content_Export_Configuration_LocationIndexConsumer.md)
*   [Consumidor de Listados de Página Única](Content_Export_Configuration/Content_Export_Configuration_Content_Export_Configuration_SinglePageListingsConsumer.md)
