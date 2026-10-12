# Vistas Funcionales de Autenticación de la Aplicación Incrustada de Shopify

Este módulo, `Core_Application___Shopify_Embedded_App_vistas_autenticacion_VistasFuncionales`, contiene las vistas de Django que gestionan la autenticación y las interacciones clave dentro de una aplicación incrustada de Shopify. Estas vistas son fundamentales para la experiencia del usuario, el flujo de autenticación OAuth, la sincronización de datos y el despacho de comandos, operando tanto dentro como fuera del iframe de la aplicación incrustada.

## Propósito y Funcionalidad Principal

El objetivo principal de este módulo es proporcionar los puntos de entrada y la lógica de negocio para las interacciones del usuario con la aplicación incrustada de Shopify. Esto incluye la gestión del proceso de inicio de sesión y autenticación OAuth, la visualización de la página de inicio de la aplicación, el manejo de la sincronización de contenido con Wagtail, la ejecución de comandos personalizados y la gestión de redireccionamientos dentro y fuera del contexto incrustado de Shopify.

Las vistas en este módulo garantizan que las operaciones se realicen en un contexto de sesión de Shopify verificado y manejan la lógica de ciclo de vida del token.

## Arquitectura y Relación entre Componentes

Las vistas funcionales se construyen sobre una base común y se relacionan de la siguiente manera:

*   **Autenticación**: `AuthLoginView` inicia el flujo OAuth, mientras que `AuthPatchIdTokenView` maneja la actualización del token de identidad.
*   **Puntos de Entrada**: `PublicEntryView` sirve como punto de entrada público, y `RootMenuView` es el hub de navegación principal.
*   **Página de Inicio y Sincronización**: `HomeView` es la página de inicio central para la aplicación incrustada, que integra funcionalidades de sincronización y despacho de comandos a través de `EmbeddedShopifySyncView` y `EmbeddedCommandDispatchView`.
*   **Redireccionamientos**: `EmbeddedInAppRedirectView` y `EmbeddedParentRedirectView` controlan los flujos de navegación dentro y fuera del iframe de Shopify, respectivamente.

La mayoría de estas vistas (`HomeView`, `EmbeddedShopifySyncView`, `EmbeddedCommandDispatchView`, `EmbeddedInAppRedirectView`, `EmbeddedParentRedirectView`) heredan de `AppHomeVerifiedMixin` (documentado en [AppHomeVerifiedMixin](Core_Application___Shopify_Embedded_App_vistas_autenticacion_AppHomeVerifiedMixin.md)), lo que les proporciona una capa de verificación de autenticación y un contexto de Shopify.

### Diagrama de Componentes y Flujo de Datos

\`\`\`mermaid
graph TD
    subgraph Puntos de Entrada
        A[PublicEntryView] --> B{Solicitud de Login}
        A --> C[AuthLoginView]
        C -- Redirige a OAuth --> D[Shopify Admin/OAuth]
        D -- Redirige a app incrustada --> E[HomeView]
    end

    subgraph Vistas de la Aplicación Incrustada
        E[HomeView] -- Muestra estado y opciones --> F[EmbeddedShopifySyncView]
        E -- Muestra estado y opciones --> G[EmbeddedCommandDispatchView]
        E -- Actualización de token --> H[AuthPatchIdTokenView]
        E -- Redirecciones internas --> I[EmbeddedInAppRedirectView]
        E -- Redirecciones externas --> J[EmbeddedParentRedirectView]
    end

    subgraph Servicios y Utilidades
        K[ShopConfigForm]
        L[shop_config_lookup]
        M[token_service]
        N[shopify_content.sync.task_dispatch]
        O[shopify_content.embedded_commands.dispatch]
        P[embedded_redirects]
        Q[utils]
        R[shopify_requests.domains.shop]
        S[AppHomeVerifiedMixin]
        T[shopify_content.models.command_run.EmbeddedCommandRun]
        U[shopify_content.models.sync_run.ShopifySyncRun]
    end

    C -- Usa --> K
    A -- Usa --> K

    E -- Usa --> L
    F -- Usa --> L
    G -- Usa --> L

    E -- Usa --> M
    F -- Usa --> M
    G -- Usa --> M

    F -- Encola Importación --> N
    F -- Registra --> U

    G -- Encola Comando --> O
    G -- Registra --> T

    I -- Valida Rutas --> P
    J -- Valida URLs --> P

    C -- Utilidades Shopify --> Q
    E -- Utilidades Shopify --> Q
    H -- Utilidades Shopify --> Q
    I -- Utilidades Shopify --> Q
    J -- Utilidades Shopify --> Q

    E -- Fetch Shop Data --> R

    E -- Extiende --> S
    F -- Extiende --> S
    G -- Extiende --> S
    I -- Extiende --> S
    J -- Extiende --> S
\`\`\`

### Descripción Detallada de Vistas Funcionales:

*   **`RootMenuView`**: Una `TemplateView` simple que renderiza el menú raíz de la aplicación. Es un punto de partida para la navegación principal, especialmente útil en un contexto de CMS headless donde la raíz no es una página de Wagtail.
*   **`PublicEntryView`**: `TemplateView` que muestra la página de entrada pública. Proporciona un formulario (`ShopConfigForm`) para que los usuarios introduzcan el nombre de su tienda Shopify, iniciando así el proceso de instalación de la aplicación.
*   **`AuthLoginView`**: Extiende `TemplateView`. Maneja las solicitudes POST para iniciar el flujo de instalación de OAuth de Shopify. Redirige al usuario a la URL de instalación de Shopify después de validar el dominio de la tienda con `ShopConfigForm`.
*   **`HomeView`**: La vista principal de la aplicación incrustada. Hereda de `AppHomeVerifiedMixin` para asegurar que el usuario esté autenticado. Muestra opciones para sincronizar recursos de Shopify (productos, colecciones, blogs, glosario), una lista de comandos disponibles y el historial de ejecución de comandos y sincronizaciones recientes. También gestiona el ciclo de vida del token offline y puede realizar llamadas a la API de GraphQL de administración de Shopify.
*   **`EmbeddedShopifySyncView`**: Hereda de `AppHomeVerifiedMixin`. Responde a solicitudes POST para encolar tareas de importación de contenido de Shopify a Wagtail. Valida el recurso a importar y utiliza el servicio de sincronización (`enqueue_shopify_import`) para procesar la importación en segundo plano. Muestra mensajes de éxito o error al usuario.
*   **`EmbeddedCommandDispatchView`**: Hereda de `AppHomeVerifiedMixin`. Permite a los usuarios encolar comandos de gestión permitidos desde la página de inicio de la aplicación incrustada. Verifica si hay un token de acceso configurado, valida el ID del comando y los argumentos adicionales (como `page_id`), y luego encola el comando utilizando `enqueue_embedded_command`. Muestra mensajes de estado.
*   **`AuthPatchIdTokenView`**: Una `TemplateView` que gestiona la actualización del token de identidad de la sesión de Shopify. Utiliza `app_home_patch_id_token` del SDK de Shopify para asegurar que la sesión del usuario esté siempre actualizada.
*   **`EmbeddedInAppRedirectView`**: Hereda de `AppHomeVerifiedMixin`. Facilita redireccionamientos dentro del iframe de la aplicación incrustada. Valida la ruta de destino relativa para evitar redireccionamientos maliciosos y utiliza la funcionalidad de redireccionamiento del SDK de Shopify.
*   **`EmbeddedParentRedirectView`**: Hereda de `AppHomeVerifiedMixin`. Maneja redireccionamientos que sacan la aplicación del iframe incrustado, por ejemplo, para redirigir a una URL en la administración de Shopify o a un sitio externo permitido. Valida la URL de destino contra una lista de hosts permitidos (`SHOPIFY_PARENT_REDIRECT_ALLOWED_HOSTS`) para prevenir vulnerabilidades de seguridad y utiliza la funcionalidad `app_home_parent_redirect` del SDK de Shopify.

## Cómo el Módulo Encaja en el Sistema General

Este módulo es una parte central del [Core_Application___Shopify_Embedded_App](../Core_Application___Shopify_Embedded_App.md), sirviendo como la interfaz principal para la interacción del usuario y la gestión del contenido dentro del entorno de Shopify.

Se integra con:
*   **[Core_Application___Shopify_Embedded_App_vistas_autenticacion_AppHomeVerifiedMixin](Core_Application___Shopify_Embedded_App_vistas_autenticacion_AppHomeVerifiedMixin.md)**: Proporciona la lógica de verificación de la aplicación incrustada, que es crucial para la seguridad y el contexto de todas las vistas de la aplicación.
*   **[Core_Application___Shopify_Embedded_App_configuracion_modelos](../../Core_Application___Shopify_Embedded_App_configuracion_modelos.md)**: A través de `ShopConfigForm` y `ShopConfig`, gestiona la configuración de la tienda y el estado de los tokens de acceso.
*   **[Wagtail_Content_Management___API/Shopify_Content_Management](../../../../Wagtail_Content_Management___API/Shopify_Content_Management.md)**: Coordina las operaciones de sincronización y despacho de comandos con los modelos de contenido y servicios de Wagtail, como `ShopifySyncRun` y `EmbeddedCommandRun`, y los servicios de sincronización.
*   **[Shopify_API_Client/Shopify_API_Client_Servicio_GraphQL](../../../Shopify_API_Client/Shopify_API_Client_Servicio_GraphQL.md)**: Permite a `HomeView` interactuar con la API de GraphQL de administración de Shopify para obtener información de la tienda.

Este módulo es esencial para la funcionalidad del "front-end" de la aplicación, facilitando una experiencia de usuario fluida y segura dentro de la plataforma Shopify, al tiempo que orquesta las interacciones con el backend de Wagtail para la gestión de contenido.
