# API de Contenido de Shopify

## Introducción y Propósito

El módulo `Shopify_Content_API` proporciona una interfaz robusta y programática para gestionar el contenido de Shopify a través de Wagtail CMS. Facilita la sincronización bidireccional de datos de contenido, permitiendo a los usuarios crear, leer, actualizar y eliminar productos, colecciones, blogs, artículos, ubicaciones y términos de glosario, además de gestionar páginas de inicio y enlaces semánticos.

Este módulo es fundamental para integrar Wagtail con Shopify, actuando como el puente entre el potente sistema de gestión de contenido de Wagtail y la plataforma de comercio electrónico de Shopify. Permite una autoría de contenido enriquecida en Wagtail, que luego puede ser sincronizada con Shopify, o bien, importar contenido existente de Shopify a Wagtail para su gestión.

## Visión General de la Arquitectura

La arquitectura de la API de Contenido de Shopify se basa en Django Ninja para construir endpoints RESTful, y se integra con el ecosistema de Wagtail para la gestión de contenido. También incorpora el protocolo MCP (Metaverse Content Protocol) para una comunicación de agente a agente.

```mermaid
graph TD
    subgraph Cliente API
        A[Aplicaciones de Agente / CMS SPA] --> B(Solicitudes HTTP/S)
    end

    subgraph Plataforma de Integración Shopify de Wagtail
        B --> C{Middleware de Autenticación}
        C --> D(Endpoints de la API de Contenido)
        D --> E[Schemas de Validación y Serialización]
        D --> F[Lógica de Negocio de Contenido]
        F --> G[Modelos de Contenido de Wagtail]
        F --> H[Servicios de Sincronización de Shopify]
        H --> I(API GraphQL de Shopify)

        C --> J[Autenticación de Sesión (Editores CMS)]
        C --> K[Autenticación de Token (Claves API / OAuth)]

        D --> L[Integración MCP (Metaverse Content Protocol)]
        L --> M[Transporte SSE / Streamable HTTP]
        M --> N(Servidor MCP Interno)
        N --> D
    end

    G <--> P(Base de Datos PostgreSQL)
    H <--> Q(Metaobjetos de Shopify)

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#fff,stroke:#333,stroke-width:1px
    style C fill:#add8e6,stroke:#333,stroke-width:1px
    style D fill:#90ee90,stroke:#333,stroke-width:1px
    style E fill:#ffcccb,stroke:#333,stroke-width:1px
    style F fill:#ffff99,stroke:#333,stroke-width:1px
    style G fill:#d3d3d3,stroke:#333,stroke-width:1px
    style H fill:#cceeff,stroke:#333,stroke-width:1px
    style I fill:#f0f8ff,stroke:#333,stroke-width:1px
    style J fill:#f8f8ff,stroke:#333,stroke-width:1px
    style K fill:#fffacd,stroke:#333,stroke-width:1px
    style L fill:#ffe4e1,stroke:#333,stroke-width:1px
    style M fill:#e0ffff,stroke:#333,stroke-width:1px
    style N fill:#ffe4e1,stroke:#333,stroke-width:1px
    style P fill:#f5f5dc,stroke:#333,stroke-width:1px
    style Q fill:#f0f8ff,stroke:#333,stroke-width:1px
```

La arquitectura se compone de los siguientes elementos clave:

*   **Cliente API**: Representa las aplicaciones de agente o la SPA del CMS que interactúan con la API de contenido.
*   **Middleware de Autenticación**: Gestiona el acceso a la API, soportando tanto la autenticación basada en sesión para editores de CMS como la autenticación por token (claves API u OAuth) para agentes y otras integraciones.
*   **Endpoints de la API de Contenido**: Implementados utilizando Django Ninja, estos endpoints exponen las funcionalidades CRUD y de sincronización para diferentes tipos de contenido de Shopify.
*   **Schemas de Validación y Serialización**: Definen la estructura de los datos para las solicitudes y respuestas de la API, asegurando la coherencia y validez de los datos.
*   **Lógica de Negocio de Contenido**: Contiene la lógica central para procesar las operaciones de contenido, interactuando con los modelos de Wagtail y los servicios de sincronización.
*   **Modelos de Contenido de Wagtail**: Modelos de Django que representan el contenido de Shopify dentro de Wagtail (por ejemplo, `ArticlePage`, `ProductPage`).
*   **Servicios de Sincronización de Shopify**: Módulos encargados de la comunicación real con la API GraphQL de Shopify para realizar operaciones de pull (importar) y push (exportar) de contenido y metaobjetos.
*   **API GraphQL de Shopify**: La interfaz principal para interactuar con los datos de Shopify.
*   **Base de Datos PostgreSQL**: Almacena los modelos de contenido de Wagtail.
*   **Metaobjetos de Shopify**: Utilizados para almacenar tipos de contenido específicos como ubicaciones y términos de glosario.
*   **Integración MCP (Metaverse Content Protocol)**: Permite la comunicación entre agentes y la API a través de un protocolo de mensajes estandarizado, utilizando transporte SSE (Server-Sent Events) o HTTP streamable.

## Funcionalidad de los Sub-módulos

A continuación, se describen los sub-módulos clave dentro de la API de Contenido de Shopify:

*   **[Shopify_Content_API_Autenticacion](Shopify_Content_API/Shopify_Content_API_Autenticacion.md)**: Gestiona la autenticación de usuarios y agentes, incluyendo la administración de claves API y la integración con sesiones de Django.
*   **[Shopify_Content_API_IntegracionMCP](Shopify_Content_API/Shopify_Content_API_IntegracionMCP.md)**: Implementa la integración con el Metaverse Content Protocol (MCP), facilitando la comunicación asíncrona y basada en eventos con agentes externos.
*   **[Shopify_Content_API_GestionOAuth](Shopify_Content_API/Shopify_Content_API_GestionOAuth.md)**: Maneja el descubrimiento y registro dinámico de clientes OAuth para interactuar con la API de contenido.
*   **[Shopify_Content_API_EsquemasComunes](Shopify_Content_API/Shopify_Content_API_EsquemasComunes.md)**: Define esquemas de datos reutilizables para elementos comunes en la API, como metacampos, enlaces y resultados de sincronización.
*   **[Shopify_Content_API_EsquemasContenido](Shopify_Content_API/Shopify_Content_API_EsquemasContenido.md)**: Proporciona los esquemas de entrada y salida para diferentes tipos de contenido de Shopify, como artículos, blogs, colecciones, glosarios, páginas de inicio, ubicaciones y productos.
*   **[Shopify_Content_API_EsquemasCapacidades](Shopify_Content_API/Shopify_Content_API_EsquemasCapacidades.md)**: Define esquemas para las capacidades de los agentes y las estructuras de las secciones de la página de inicio.
*   **[Shopify_Content_API_RegistroAgente](Shopify_Content_API/Shopify_Content_API_RegistroAgente.md)**: Centraliza la definición y catalogación de las capacidades y flujos de trabajo de los agentes que pueden interactuar con la API.
*   **[Shopify_Content_API_ConfiguracionAplicacion](Shopify_Content_API/Shopify_Content_API_ConfiguracionAplicacion.md)**: Configura la aplicación Django para la API de contenido, incluyendo la carga de módulos internos.

## Cómo el módulo encaja en el sistema general

El módulo `Shopify_Content_API` es un componente crítico de la plataforma de integración Wagtail-Shopify. Se posiciona como una capa de API que expone las funcionalidades de gestión de contenido a aplicaciones externas, incluyendo agentes de IA y la interfaz de usuario del CMS (SPA).

Depende en gran medida de los modelos de contenido definidos en `Wagtail_Content_Management`, utilizando las capacidades de Wagtail para la autoría y gestión de contenido. A su vez, los módulos de la `Application_Core___Shopify_Integration_Platform` (como el cliente API de Shopify y la integración de metaobjetos de Shopify) son utilizados por la lógica de sincronización de este módulo para interactuar con la plataforma de Shopify.

La interacción con el módulo `CMS_UI_Integration` permite que la SPA del CMS utilice esta API para presentar y editar contenido. La autenticación se integra con el sistema de usuarios de Django y OAuth, haciendo que esta API sea segura y extensible.
