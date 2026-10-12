# Integración de la UI del CMS

Este módulo, `CMS_UI_Integration`, es fundamental para integrar la interfaz de usuario del Sistema de Gestión de Contenidos (CMS) basado en Wagtail con una aplicación de una sola página (SPA) construida con React, utilizando el marco `django_react_ui_editor`. Su propósito principal es proporcionar el montaje y la configuración necesarios para que los editores de contenido puedan interactuar con el CMS a través de una experiencia de usuario moderna y dinámica.

## Propósito y Funcionalidad Principal

El módulo facilita la creación y gestión de una SPA que sirve como la interfaz de edición para el contenido del comercio electrónico. Permite la visualización y edición visual del contenido de Wagtail, aprovechando las capacidades de un frontend React. Además, incluye mecanismos para proteger el acceso al panel de administración de Wagtail y herramientas para inicializar la configuración de la SPA en el CMS.

## Arquitectura General

La arquitectura del módulo `CMS_UI_Integration` se centra en la integración entre el backend de Django/Wagtail y un frontend React. Utiliza `django_react_ui_editor` como un puente para montar la SPA y gestionar su configuración desde el lado del servidor.

```mermaid
graph TD
    A[Navegador del Usuario] --> B(Aplicación React SPA del CMS)
    B --> C{Servidor Django/Wagtail}
    C --> D[Base de Datos]
    C --> E[Django_React_UI_Editor Framework]
    C --> F[Middleware de Autenticación/Restricción]
    B -- Peticiones API --> G[Shopify Content API]
    G --> C
    subgraph CMS_UI_Integration
        CmsSpaMount[Modelo CmsSpaMount]
        CmsSpaMountAdmin[Administración CmsSpaMount]
        CmsUiConfig[Configuración de la Aplicación]
        RestrictWagtailAdminMiddleware[Middleware de Restricción del Admin de Wagtail]
        FrontendAssets[Activos Frontend (React/Vite)]
    end
    CmsUiConfig --> CmsSpaMount
    CmsSpaMountAdmin --> CmsSpaMount
    RestrictWagtailAdminMiddleware --> C
    FrontendAssets --> B
    E --> CmsSpaMount
    E --> CmsSpaMountAdmin
    G --> B
    D --- CmsSpaMount
```

*Diagrama 1: Arquitectura de Integración de la UI del CMS*

### Componentes Clave y Relaciones:

*   **Aplicación React SPA del CMS**: La interfaz de usuario real donde los editores interactúan con el contenido. Se construye utilizando React y las herramientas de frontend.
*   **Servidor Django/Wagtail**: El backend que aloja la lógica del CMS, las APIs y los modelos de datos.
*   **`django_react_ui_editor`**: Un marco que permite montar SPAs React dentro de una aplicación Django/Wagtail, proporcionando una interfaz para configurar y gestionar las SPAs. (Ver [Django_React_UI_Editor_Framework.md](Django_React_UI_Editor_Framework.md) para más detalles).
*   **`Shopify_Content_API`**: La API que expone el contenido de Wagtail a la SPA del CMS para su edición. (Ver [Shopify_Content_API.md](Shopify_Content_API.md) para más detalles).

## Sub-módulos

El módulo `CMS_UI_Integration` se organiza en los siguientes sub-módulos para gestionar sus distintas responsabilidades:

*   **[Gestión y Configuración del Modelo CmsSpaMount](CMS_UI_Integration/CMS_UI_Integration_CmsSpaMount.md)**: Se encarga de la definición del modelo `CmsSpaMount`, su integración con el panel de administración de Django/Wagtail y la configuración inicial.
*   **[Gestión de Activos Frontend](CMS_UI_Integration/CMS_UI_Integration_Frontend.md)**: Contiene los scripts y configuraciones para la construcción y el desarrollo del frontend de la SPA.
*   **[Comandos de Gestión y Middleware](CMS_UI_Integration/CMS_UI_Integration_CMS_UI_Integration_Management.md)**: Incluye comandos de Django para inicializar la SPA y un middleware para restringir el acceso al panel de administración de Wagtail.
