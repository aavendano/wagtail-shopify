# Visión General del Repositorio wagtail-shopify

## Propósito

El repositorio `wagtail-shopify` es una solución integral diseñada para integrar el sistema de gestión de contenido (CMS) Wagtail con la plataforma de comercio electrónico Shopify. Su objetivo principal es permitir a los usuarios gestionar el contenido de su tienda Shopify (productos, colecciones, artículos, blogs y metaobjetos) directamente desde la interfaz de Wagtail, proporcionando una experiencia editorial rica y flexible. La aplicación facilita la sincronización bidireccional de datos, la creación de experiencias de usuario personalizadas y la extensibilidad para satisfacer diversas necesidades de comercio electrónico.

## Arquitectura de Extremo a Extremo

La arquitectura del repositorio `wagtail-shopify` se basa en la interacción entre la aplicación Django/Wagtail, la API de Shopify y una interfaz de usuario React. A continuación, se visualiza el flujo de información y la interconexión de los componentes principales:

```mermaid
graph TD
    A[Usuario/Editor Wagtail] --> B{CMS UI / Frontend<br>(cms_ui/)}
    B --> C[Aplicación Django Wagtail<br>(core/)]

    C -- Gestiona Contenido --> D[Gestión de Contenido Shopify<br>(shopify_content/)]
    C -- Gestiona Metaobjetos --> E[Metaobjetos Shopify<br>(metaobjects/shopify_metaobjects/)]
    D -- Utiliza Modelos de Datos --> F[Esquemas API Shopify<br>(api/)]
    E -- Utiliza Modelos de Datos --> F

    C -- Realiza Solicitudes --> G[Cliente API Shopify<br>(shopify_requests/)]
    G --> H[Shopify (API de Admin/Storefront)]

    H -- Envía Notificaciones --> I[Webhooks Shopify<br>(webhooks/)]
    I --> C

    C -- Habilita Edición Rica --> J[Framework Editor UI Django React<br>(django_react_ui_editor/)]
    J --> B

    subgraph Plataforma Wagtail
        C
        D
        E
        F
        I
        J
    end
    subgraph Experiencia de Usuario
        A
        B
    end
    subgraph Integración Shopify
        G
        H
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#bbf,stroke:#333,stroke-width:2px
```

**Descripción de Componentes Clave:**

*   **Usuario/Editor Wagtail:** Interactúa con el CMS para gestionar el contenido.
*   **CMS UI / Frontend (`cms_ui/`):** La interfaz de usuario construida con React que se ejecuta dentro del administrador de Wagtail, proporcionando herramientas de edición y visualización.
*   **Aplicación Django Wagtail (`core/`):** La aplicación central de Django que aloja el CMS Wagtail y coordina todas las interacciones.
*   **Gestión de Contenido Shopify (`shopify_content/`):** Módulo responsable de modelar, sincronizar y editar los tipos de contenido de Shopify (productos, colecciones, blogs, artículos) dentro de Wagtail. Incluye la lógica para bloques de contenido, la interfaz de usuario de administración y la gestión de URLs.
*   **Metaobjetos Shopify (`metaobjects/shopify_metaobjects/`):** Módulo dedicado a la gestión de metaobjetos de Shopify, incluyendo su definición, modelado de datos y serialización.
*   **Esquemas API Shopify (`api/`):** Define los modelos de datos (Pydantic) para las entidades de Shopify, asegurando la consistencia y validación de los datos.
*   **Cliente API Shopify (`shopify_requests/`):** Gestiona la comunicación con las APIs de Shopify (principalmente GraphQL) para recuperar y enviar datos.
*   **Shopify:** La plataforma de comercio electrónico real, a la que el sistema se conecta a través de sus APIs de administración y storefront.
*   **Webhooks Shopify (`webhooks/`):** Recibe notificaciones de Shopify sobre eventos (por ejemplo, actualizaciones de productos), lo que permite mantener el CMS actualizado.
*   **Framework Editor UI Django React (`django_react_ui_editor/`):** Un framework que permite integrar componentes de React directamente en el panel de administración de Django, mejorando la experiencia de edición.

## Módulos Principales

El repositorio se organiza en varios módulos clave, cada uno con una responsabilidad específica:

*   **[Core Shopify App](Core_Shopify_App.md):** Contiene la lógica central de la aplicación Django que integra Wagtail con Shopify. Maneja la configuración global, la autenticación y las rutas principales.
*   **[Shopify API Schemas](Shopify_API___Schemas.md):** Define los esquemas de datos utilizados para interactuar con la API de Shopify, asegurando la validación y tipificación de los datos.
*   **[Shopify API Client](Shopify_API_Client.md):** Proporciona el cliente para realizar solicitudes a la API GraphQL de Shopify, gestionando la comunicación y el manejo de errores.
*   **[Shopify Content Management](Shopify_Content_Management.md):** El módulo más grande, encargado de la gestión de contenido de Shopify dentro de Wagtail. Incluye modelos de contenido, bloques de Wagtail, UI de administración, sincronización y lógica de enlaces semánticos.
*   **[Shopify Metaobjects](Shopify_Metaobjects.md):** Gestiona la interacción con los metaobjetos de Shopify, incluyendo sus definiciones, modelos de datos y serialización.
*   **[Webhooks](Webhooks.md):** Configura y procesa los webhooks enviados por Shopify, permitiendo que la aplicación responda a eventos en la tienda.
*   **[CMS UI / Frontend](CMS_UI___Frontend.md):** Desarrolla la interfaz de usuario de React para el administrador de Wagtail, incluyendo la aplicación frontend, las páginas de administración y el middleware.
*   **[Django React UI Editor Framework](Django_React_UI_Editor_Framework.md):** Proporciona las herramientas y el marco para integrar componentes de React en el panel de administración de Django, facilitando la creación de interfaces de usuario personalizadas.
*   **[Custom App Placeholder](Custom_App_Placeholder.md):** Un módulo de marcador de posición para la lógica de aplicación personalizada, que permite la extensibilidad sin modificar el código fuente principal.

## Compilación, Ejecución y Configuración

El proyecto `wagtail-shopify` se configura y ejecuta utilizando una combinación de herramientas de desarrollo estándar para Python y JavaScript.

**Compilación y Desarrollo:**

*   **Frontend:** La interfaz de usuario de React (ubicada en `cms_ui/frontend/`) se compila utilizando Vite. El archivo `cms_ui/frontend/vite.config.js` define la configuración de construcción. Las dependencias de JavaScript se gestionan a través de `cms_ui/frontend/package.json`, que también incluye scripts para `build`, `dev` y `preview`.
*   **Backend:** Las dependencias de Python se gestionan con `requirements.txt`.

**Pruebas:**

*   Las pruebas unitarias y de integración para el backend se ejecutan utilizando `pytest`. La configuración de Pytest se encuentra en `pytest.ini` y `conftest.py` para configuraciones compartidas.
*   El `Makefile` incluye objetivos como `test` y `test-glossary` para ejecutar los conjuntos de pruebas.
*   `install-test-deps` en el `Makefile` asegura que todas las dependencias necesarias para las pruebas estén instaladas.

**Empaquetado y Despliegue:**

*   El proyecto utiliza `setup.py` para su empaquetado como un paquete de Python, lo que facilita su distribución e instalación.
*   Para el despliegue de la aplicación de Shopify, `shopify.web.toml` contiene la configuración específica de Shopify, incluyendo la información de la aplicación y los webhooks.
*   El repositorio también incluye scripts `.cursor/install.sh` y `.cursor/start.sh` que son útiles para configurar y ejecutar el proyecto en un entorno de desarrollo.

**Integración Continua:**

*   La validación de contenido y otras verificaciones automatizadas se gestionan a través de GitHub Actions, como se define en `.github/workflows/content-validate.yml`.

Para obtener detalles específicos sobre la configuración de webhooks, consulte la documentación del módulo [Webhooks](Webhooks.md). La configuración de la aplicación principal y los pasos de autenticación se encuentran en la documentación de [Core Shopify App](Core_Shopify_App.md).