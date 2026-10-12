# Lógica de Enlaces Semánticos y Resolución de URL de Contenido de Shopify

Este módulo es fundamental para gestionar cómo se resuelven y enlazan los contenidos dentro del ecosistema de Shopify, centrándose en la creación de una experiencia de usuario fluida y optimizada para SEO. Proporciona mecanismos para reescribir enlaces de productos en el contenido, resolver URLs de la tienda a páginas de Wagtail, validar referencias de páginas basadas en la configuración regional y generar enlaces internos semánticos.

## Arquitectura General

El módulo `Content_URL___Semantic_Linking_Logic` se integra con el sistema de gestión de contenido de Wagtail y la API de Shopify para asegurar que los enlaces de contenido sean consistentes y funcionales. Utiliza varios componentes interconectados para lograr sus objetivos:

```mermaid
graph TD
    A[Contenido de Wagtail] --> B{Lógica de Enlaces Semánticos y Resolución de URL de Contenido};
    B --> C[Resolución de URL de Contenido]
    B --> D[Enlaces de Producto en Artículos]
    B --> E[Validación de Configuración Regional de Página de Inicio]
    B --> F[Servicio de Enlaces Semánticos]
    B --> G[Ayudantes de URL de la Tienda]
    C --> H[Índice de URL de Contenido (Base de Datos)];
    D --> I[Páginas de Producto de Shopify];
    E --> J[Páginas de Inicio de Wagtail];
    F --> K[Índice de Páginas (pgvector)];
    F --> L[Modelos de Enlaces Semánticos];
    G --> M[Convenciones de Rutas de Shopify];

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#ccf,stroke:#333,stroke-width:2px
    style E fill:#ccf,stroke:#333,stroke-width:2px
    style F fill:#ccf,stroke:#333,stroke-width:2px
    style G fill:#ccf,stroke:#333,stroke-width:2px
    style H fill:#f9f,stroke:#333,stroke-width:1px
    style I fill:#f9f,stroke:#333,stroke-width:1px
    style J fill:#f9f,stroke:#333,stroke-width:1px
    style K fill:#f9f,stroke:#333,stroke-width:1px
    style L fill:#f9f,stroke:#333,stroke-width:1px
    style M fill:#f9f,stroke:#333,stroke-width:1px
```

## Sub-módulos

A continuación, se detalla la funcionalidad de los sub-módulos que componen la lógica de enlaces semánticos y resolución de URL de contenido:

*   **[Lógica de Enlaces de Producto en Artículos](Content_URL___Semantic_Linking_Logic/Content_URL___Semantic_Linking_Logic_Article_Product_Linking.md)**: Se encarga de analizar y reescribir los enlaces de productos en el contenido HTML de los artículos de Wagtail para asegurar que apunten a los manejadores de productos en vivo correctos.
*   **[Resolución de URL de Contenido](Content_URL___Semantic_Linking_Logic/Content_URL___Semantic_Linking_Logic_URL_Resolution.md)**: Proporciona la capacidad de resolver URLs de la tienda a páginas de contenido específicas de Wagtail, normalizando las rutas y gestionando prefijos de localización.
*   **[Validación de Configuración Regional de Página de Inicio](Content_URL___Semantic_Linking_Logic/Content_URL___Semantic_Linking_Logic_Home_Locale_Validation.md)**: Asegura que las referencias de páginas dentro de las secciones de las páginas de inicio de Wagtail coincidan con la configuración regional esperada.
*   **[Servicio de Enlaces Semánticos](Content_URL___Semantic_Linking_Logic/Content_URL___Semantic_Linking_Logic_Semantic_Link_Service.md)**: Ofrece funcionalidades para generar y mantener enlaces internos semánticos entre diferentes tipos de páginas de contenido, mejorando la navegación y el SEO.
*   **[Ayudantes de URL de la Tienda](Content_URL___Semantic_Linking_Logic/Content_URL___Semantic_Linking_Logic_Storefront_URL_Helpers.md)**: Contiene funciones de utilidad para construir rutas canónicas relativas a la tienda Shopify para diferentes tipos de páginas de contenido, incluyendo la gestión de prefijos de localización.
