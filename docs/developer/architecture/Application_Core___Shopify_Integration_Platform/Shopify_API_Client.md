# Cliente de la API de Shopify

Este módulo, `Shopify_API_Client`, es un componente crucial dentro de la Plataforma de Integración de Shopify. Su propósito principal es facilitar la comunicación bidireccional y robusta con la API de administración de Shopify, específicamente a través de consultas GraphQL. Proporciona una capa de abstracción para manejar las solicitudes, la autenticación y la gestión de errores, asegurando una interacción fluida y resiliente con la plataforma Shopify.

## Propósito y Funcionalidad Principal

El `Shopify_API_Client` está diseñado para:
*   **Centralizar las interacciones con la API de Shopify:** Sirve como el punto de entrada principal para todas las operaciones que requieren comunicarse con la API de administración de Shopify.
*   **Manejar la ejecución de consultas GraphQL:** Permite enviar consultas y mutaciones GraphQL a la API de Shopify, procesando las respuestas y manejando posibles errores.
*   **Gestionar la autenticación:** Se encarga de resolver y utilizar los tokens de acceso necesarios para autenticar las solicitudes a la API de Shopify, incluyendo la lógica de reautorización cuando sea necesario.
*   **Proporcionar manejo de errores estructurado:** Define excepciones específicas para errores de integración, facilitando la identificación y el manejo de problemas como la reautorización requerida o la limitación de tasas (throttling).

## Arquitectura y Componentes

La arquitectura del `Shopify_API_Client` se compone principalmente de dos áreas funcionales clave: la gestión de errores y el servicio GraphQL.

```mermaid
graph TD
    A(Plataforma de Integración de Shopify) --> B(Shopify_API_Client);

    subgraph Shopify_API_Client
        B1(Servicio GraphQL) --> B2(Gestión de Errores);
    end

    B --> C(API de Administración de Shopify (GraphQL));

    style A fill:#f9f,stroke:#333,stroke-width:2px;
    style C fill:#ccf,stroke:#333,stroke-width:2px;
    style B1 fill:#bbf,stroke:#333,stroke-width:2px;
    style B2 fill:#fbc,stroke:#333,stroke-width:2px;
```

### Descripción de Sub-módulos

A continuación, se describen los sub-módulos que componen el `Shopify_API_Client`:

*   **[Servicio GraphQL](Shopify_API_Client/Shopify_API_Client_Servicio_GraphQL.md)**: Este sub-módulo se encarga de la construcción y ejecución de las solicitudes GraphQL a la API de Shopify. Gestiona la resolución de tokens de acceso, el manejo de versiones de la API y la interpretación de las respuestas.
*   **[Gestión de Errores](Shopify_API_Client/Shopify_API_Client_Gestion_Errores.md)**: Este sub-módulo define las excepciones personalizadas que se utilizan para señalar problemas específicos durante la integración con Shopify, como la necesidad de reautorización o errores generales de la integración.

Los detalles de cada sub-módulo se encuentran en sus respectivos archivos de documentación.
