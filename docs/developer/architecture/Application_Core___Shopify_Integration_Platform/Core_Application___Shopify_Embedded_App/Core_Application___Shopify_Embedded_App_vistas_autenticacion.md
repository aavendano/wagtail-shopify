# Módulo Core_Application___Shopify_Embedded_App_vistas_autenticacion

## Introducción

El módulo `Core_Application___Shopify_Embedded_App_vistas_autenticacion` es el encargado de gestionar los flujos de autenticación, la verificación de solicitudes y las diversas funcionalidades de las vistas dentro de la aplicación incrustada de Shopify. Este módulo facilita la integración segura y la interacción con la plataforma Shopify, permitiendo operaciones como la sincronización de contenido, la ejecución de comandos y la gestión de redirecciones.

## Arquitectura

La arquitectura del módulo se centra en la reutilización de código a través de mixins y una clara separación de responsabilidades entre las diferentes vistas. Utiliza el `AppHomeVerifiedMixin` para asegurar que todas las solicitudes que entran a las vistas principales hayan sido verificadas por Shopify App Home, garantizando la seguridad y la procedencia de las interacciones.

### Diagrama de Componentes

```mermaid
graph TD
    A[Navegador del Usuario] -->|Solicitud HTTP| B(Shopify App Home)
    B -->|Verificación e ID Token| C[AppHomeVerifiedMixin]
    C --> D{Vistas de Autenticación y Funcionalidad}
    D --> E[core/views.py]
    E --> F[core/mixins.py]
    E --> G[shopify_content.sync.service]
    E --> H[shopify_content.sync.task_dispatch]
    E --> I[shopify_content.embedded_commands.dispatch]
    E --> J[shopify_content.embedded_commands.registry]
    E --> K[shopify_content.models.command_run]
    E --> L[shopify_content.models.sync_run]
    E --> M[core/forms.py]
    E --> N[core/shop_config_lookup.py]
    E --> O[core/token_service.py]
    E --> P[shopify_requests.domains.shop]
    E --> Q[core/embedded_redirects.py]

    subgraph core/views.py
        D1(AuthLoginView)
        D2(AuthPatchIdTokenView)
        D3(HomeView)
        D4(EmbeddedShopifySyncView)
        D5(EmbeddedCommandDispatchView)
        D6(EmbeddedInAppRedirectView)
        D7(EmbeddedParentRedirectView)
        D8(PublicEntryView)
        D9(RootMenuView)
    end

    subgraph core/mixins.py
        C1(AppHomeVerifiedMixin)
    end

    C1 --> D3
    C1 --> D4
    C1 --> D5
    C1 --> D6
    C1 --> D7
    D1 --> N
    D1 --> M
    D3 --> K
    D3 --> L
    D3 --> J
    D3 --> N
    D3 --> P
    D4 --> G
    D4 --> H
    D5 --> N
    D5 --> I
    D5 --> J
    D6 --> Q
    D7 --> Q
    E --> B

```

### Flujo de Autenticación y Verificación

1.  Una solicitud desde el navegador del usuario llega a Shopify App Home.
2.  Shopify App Home verifica la solicitud y, si es válida, proporciona un token de identificación.
3.  La solicitud es procesada por el `AppHomeVerifiedMixin` en `core/mixins.py`, que valida el token y prepara el contexto para la vista.
4.  Si la verificación es exitosa, se invoca el método `dispatch_after_verified` de la vista correspondiente en `core/views.py`.
5.  Las vistas manejan la lógica de negocio específica, interactuando con otros módulos como `shopify_content` para sincronización y comandos, o `shopify_requests` para interactuar con la API de Shopify.

## Submódulos

Este módulo se descompone en los siguientes submódulos para una mejor organización y gestión de responsabilidades:

*   [AppHomeVerifiedMixin](./Core_Application___Shopify_Embedded_App_vistas_autenticacion/Core_Application___Shopify_Embedded_App_vistas_autenticacion_AppHomeVerifiedMixin.md)
*   [Vistas Funcionales](./Core_Application___Shopify_Embedded_App_vistas_autenticacion/Core_Application___Shopify_Embedded_App_vistas_autenticacion_VistasFuncionales.md)

