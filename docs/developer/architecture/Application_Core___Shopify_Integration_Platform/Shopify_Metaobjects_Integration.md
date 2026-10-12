# Integración de Metaobjetos de Shopify

Este módulo es responsable de la interacción con la API de Metaobjetos de Shopify. Proporciona funcionalidades para definir, crear, actualizar y gestionar metaobjetos y sus definiciones dentro de la plataforma Shopify. Facilita la sincronización de estructuras de datos personalizadas y contenido entre la aplicación y Shopify.

## Arquitectura General

El módulo `Shopify_Metaobjects_Integration` se integra con el cliente GraphQL de administración de Shopify para realizar operaciones CRUD en metaobjetos y sus definiciones. Se compone de varias unidades lógicas que manejan la definición de esquemas, la serialización de datos, la gestión de clientes API y el manejo de errores.

```mermaid
graph TD
    A[Aplicación Cliente/Administración Wagtail] -->|Solicitud de gestión de Metaobjetos| B(Módulo Shopify_Metaobjects_Integration)
    B --> C{Cliente de Metaobjetos}
    C --> D[Definiciones de Metaobjetos] 
    C --> E[Modelo de Metaobjetos]
    C --> F[Serialización de Metaobjetos]
    C --> G[Manejo de Excepciones]
    C --> H[Servicio GraphQL de Shopify] 
    H --> I[API de Shopify]

    D -- Define --> E
    F -- Serializa/Deserializa --> E
    C -- Utiliza --> D
    C -- Utiliza --> E
    C -- Utiliza --> F
    C -- Utiliza --> G
    C -- Realiza Operaciones --> H

    subgraph Módulo Shopify_Metaobjects_Integration
        C
        D
        E
        F
        G
    end

    classDef default fill:#EEE,stroke:#333,stroke-width:2px;
    classDef submodule fill:#DFF,stroke:#009,stroke-width:1px;

    linkStyle 0 stroke-width:2px,fill:none,stroke:green;

```

## Sub-módulos

A continuación se describen los principales sub-módulos y sus responsabilidades:

*   [Cliente de Metaobjetos](Shopify_Metaobjects_Integration/Shopify_Metaobjects_Integration_Cliente_Metaobjetos.md)
*   [Definición de Metaobjetos](Shopify_Metaobjects_Integration/Shopify_Metaobjects_Integration_Definicion_Metaobjetos.md)
*   [Excepciones de Metaobjetos](Shopify_Metaobjects_Integration/Shopify_Metaobjects_Integration_Excepciones_Metaobjetos.md)
*   [Modelo de Metaobjetos](Shopify_Metaobjects_Integration/Shopify_Metaobjects_Integration_Modelo_Metaobjetos.md)