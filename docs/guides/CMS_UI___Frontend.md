# Módulo CMS_UI___Frontend

## Introducción y Propósito

El módulo `CMS_UI___Frontend` gestiona la interfaz de usuario del sistema de gestión de contenido (CMS) para comerciantes. Proporciona una aplicación de página única (SPA) construida con React y Vite, integrada con el entorno Django. Este módulo permite a los usuarios editar y gestionar contenido de manera eficiente a través de una experiencia de usuario moderna y dinámica, desacoplada de la interfaz de administración tradicional de Django/Wagtail.

Su propósito principal es:
*   Ofrecer una interfaz de usuario rica y reactiva para la edición de contenido.
*   Integrar un editor visual de contenido (Puck) en el flujo de trabajo del CMS.
*   Proporcionar un mecanismo para montar y gestionar aplicaciones SPA dentro de la estructura de Django.
*   Restringir el acceso al panel de administración de Wagtail a usuarios autorizados cuando sea necesario, dirigiendo a los editores de contenido a la interfaz del CMS SPA.

## Arquitectura General

La arquitectura del módulo `CMS_UI___Frontend` se centra en la integración de una aplicación React de frontend con el backend de Django. Utiliza el módulo `django_react_ui_editor` como base para montar la SPA y gestiona sus propios modelos, vistas y configuraciones.

```mermaid
graph TD
    A[Usuario Final/Editor] -->|Accede| B(Navegador Web)
    B -->|Solicitud| C[Servidor Django]
    C -->|Middleware| D{Restringir Wagtail?}
    D -- No --> E[Vistas SPA (cms_ui)]
    D --> E
    D --> F[Acceso Denegado]
    E -->|Carga Frontend| B
    B -->|SPA React Puck| G[API Backend (Django Rest Framework)]
    G -->|Modelos CMS| H[Base de Datos]
    C -->|Admin Django| I[CmsSpaMountAdmin]
    I --> H

    subgraph Frontend
        B
    end

    subgraph Backend Django
        C
        D
        E
        F
        G
        H
        I
    end

    subgraph Integración con django_react_ui_editor
        E -- Utiliza --> J[SpaMount, SpaRegistration]
        I -- Utiliza --> K[VisualEditorAdminMixin]
    end

    J:::hidden
    K:::hidden

    classDef hidden display:none

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#fbb,stroke:#333,stroke-width:2px
    style D fill:#fcb,stroke:#333,stroke-width:2px
    style E fill:#bfb,stroke:#333,stroke-width:2px
    style F fill:#f77,stroke:#333,stroke-width:2px
    style G fill:#ffb,stroke:#333,stroke-width:2px
    style H fill:#dfd,stroke:#333,stroke-width:2px
    style I fill:#ccf,stroke:#333,stroke-width:2px
```

## Sub-módulos y Funcionalidades

Este módulo se organiza en varias secciones lógicas que cubren la administración, la aplicación de frontend y la gestión de middleware. A continuación, se detalla la funcionalidad de cada sub-módulo con enlaces a su documentación específica:

*   **[Administración del CMS SPA](CMS_UI___Frontend/CMS_UI___Frontend_Administracion.md)**: Gestiona la configuración y el registro de la aplicación SPA del CMS, incluyendo el modelo de montaje y la integración con el panel de administración de Django.
*   **[Aplicación Frontend del CMS](CMS_UI___Frontend/CMS_UI___Frontend_Aplicacion_Frontend.md)**: Contiene los archivos de configuración y scripts para el desarrollo, construcción y previsualización de la aplicación React SPA.
*   **[Middleware del CMS](CMS_UI___Frontend/CMS_UI___Frontend_Middleware.md)**: Implementa la lógica para restringir el acceso al panel de administración de Wagtail, asegurando que solo los usuarios autorizados puedan acceder a él.
