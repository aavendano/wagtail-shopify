# Aplicación Central de Shopify

## Introducción

El módulo `Core_Shopify_App` constituye el esqueleto central de la aplicación Shopify, proporcionando la infraestructura fundamental para la autenticación, la configuración de la tienda y la gestión de la interfaz de usuario incrustada. Actúa como el puente principal entre el framework Django y el ecosistema de Shopify, asegurando una interacción fluida y segura. Este módulo gestiona el ciclo de vida de los tokens de acceso, las redirecciones dentro y fuera de la aplicación incrustada, y las operaciones de sincronización de contenido iniciales.

## Arquitectura General

La arquitectura del módulo `Core_Shopify_App` se centra en la integración con la plataforma Shopify, utilizando un modelo de aplicación incrustada. Se compone de varias capas clave que colaboran para gestionar la configuración de la tienda, la autenticación y las interacciones del usuario.


*Diagrama 1: Arquitectura General de `Core_Shopify_App`*

La aplicación se inicializa a través de `CoreConfig` y utiliza `ShopifyLocalProxyMiddleware` para manejar las solicitudes del proxy local de Shopify CLI. El corazón de la aplicación incrustada reside en las diferentes vistas que manejan la autenticación (`AuthLoginView`, `AuthPatchIdTokenView`), la página de inicio (`HomeView`, `PublicEntryView`, `RootMenuView`), las redirecciones (`EmbeddedInAppRedirectView`, `EmbeddedParentRedirectView`) y el despacho de comandos (`EmbeddedCommandDispatchView`, `EmbeddedShopifySyncView`).

El modelo `ShopConfig` almacena la información de la tienda y los tokens de acceso, gestionado por `ShopConfigForm` y sus migraciones asociadas. `AppHomeVerifiedMixin` asegura que las solicitudes a las vistas incrustadas estén verificadas por Shopify.

## Componentes y Funcionalidades Principales

Los componentes de `Core_Shopify_App` se agrupan en las siguientes sub-secciones para una mejor comprensión:

### [Configuración de la Aplicación y de la Tienda](Core_Shopify_App/Core_Shopify_App_Configuracion.md)
Este sub-módulo se encarga de la configuración inicial de la aplicación Django y de la gestión de la información esencial de la tienda Shopify, incluyendo los tokens de acceso.

### [Autenticación de la Aplicación Incrustada](Core_Shopify_App/Core_Shopify_App_Autenticacion.md)
Gestiona el flujo de autenticación para la aplicación incrustada de Shopify, asegurando que las interacciones sean seguras y verificadas.

### [Vistas y Lógica de la Interfaz de Usuario Incrustada](Core_Shopify_App/Core_Shopify_App_Vistas_Incrustadas.md)
Contiene las vistas principales que renderizan la interfaz de usuario dentro de la aplicación incrustada de Shopify, así como la lógica para la sincronización de contenido y el despacho de comandos.

### [Middleware y Utilidades](Core_Shopify_App/Core_Shopify_App_Middleware_y_Utilidades.md)
Proporciona funcionalidades de middleware específicas, como el manejo de encabezados `X-Forwarded-Proto` para el proxy local de Shopify CLI.

### [Pruebas Unitarias y de Integración](Core_Shopify_App/Core_Shopify_App_Pruebas.md)
Este sub-módulo contiene las pruebas que verifican la funcionalidad y el comportamiento correcto de los componentes principales de la aplicación Shopify.

## Relaciones con Otros Módulos

El módulo `Core_Shopify_App` se interconecta con varios otros módulos clave en el sistema:

*   **[Shopify_API___Schemas](Shopify_API___Schemas.md)**: El módulo `Core_Shopify_App` interactúa con los esquemas de la API de Shopify para la autenticación y para realizar operaciones de la API. La gestión de `ShopConfig` (que almacena `access_token` y `refresh_token`) es crucial para realizar llamadas autenticadas a la API.
*   **[Shopify_Content_Management](Shopify_Content_Management.md)**: La `EmbeddedShopifySyncView` y la `EmbeddedCommandDispatchView` en `Core_Shopify_App` son los puntos de entrada para las operaciones de sincronización de contenido y el despacho de comandos de gestión definidos en `shopify_content`. Por ejemplo, `enqueue_shopify_import` y `enqueue_embedded_command` de `shopify_content.sync.task_dispatch` y `shopify_content.embedded_commands.dispatch` respectivamente.
*   **[Shopify_API_Client](Shopify_API_Client.md)**: Las vistas de `Core_Shopify_App` utilizan la funcionalidad del cliente de la API de Shopify (por ejemplo, `fetch_shop_admin_graphql`) para interactuar con la API GraphQL de Shopify.
*   **[Webhooks](Webhooks.md)**: Aunque no hay una dependencia directa visible en el código proporcionado, es muy probable que `Core_Shopify_App` configure o gestione de alguna manera la suscripción a webhooks de Shopify, que luego serían manejados por el módulo `Webhooks`.

Esta interacción asegura que la aplicación pueda autenticarse con Shopify, gestionar los datos de la tienda, sincronizar contenido y responder a eventos de la plataforma.
