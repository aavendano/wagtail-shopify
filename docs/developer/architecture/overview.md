# Visión General de wagtail-shopify

El repositorio `wagtail-shopify` proporciona una sólida plataforma para integrar el sistema de gestión de contenido (CMS) Wagtail con las tiendas Shopify. Su propósito principal es permitir a los equipos editoriales gestionar contenido rico y estructurado dentro de Wagtail y luego sincronizarlo o exponerlo a Shopify. Esto facilita la creación de experiencias de compra y contenido altamente personalizadas en Shopify, ya sea a través de escaparates personalizados (como Hydrogen) que consumen una API de contenido, o mediante la sincronización directa con Metaobjetos de Shopify para ampliar la funcionalidad de la tienda nativa.

La aplicación funciona como una aplicación Shopify incrustada, manejando la autenticación OAuth, las interacciones con la API de Shopify (REST y GraphQL) y el procesamiento de webhooks para mantener la coherencia y la sincronización del contenido entre ambas plataformas.

## Arquitectura de wagtail-shopify

La arquitectura de `wagtail-shopify` se centra en la aplicación como un centro de gestión e integración de contenido, actuando como intermediario entre el potente CMS de Wagtail y el ecosistema de Shopify.

La aplicación se incrusta en el panel de administración de Shopify, permitiendo una experiencia de usuario fluida. Utiliza un cliente API dedicado para comunicarse con Shopify, tanto para obtener datos (productos, colecciones) como para enviar contenido (Metaobjetos). A su vez, el módulo de manejo de webhooks de Shopify garantiza que cualquier cambio relevante en la tienda Shopify active actualizaciones en Wagtail.

Dentro de Wagtail, se definen modelos de contenido específicos para Shopify (productos, colecciones, blogs, etc.), que luego pueden ser gestionados por los editores. Este contenido se expone a través de una API de contenido de Wagtail para que los escaparates personalizados puedan consumirlo. Además, la integración de Metaobjetos permite que el contenido editorial de Wagtail se materialice directamente en Shopify como datos estructurados.

```mermaid
graph TD
    subgraph Ecosistema Shopify
        SHOPIFY_STORE[Tienda Shopify]
        SHOPIFY_ADMIN[Panel de Administración de Shopify]
        SHOPIFY_FRONTEND[Frontend de Shopify (ej. Hydrogen)]
    end

    subgraph Aplicación wagtail-shopify
        direction LR
        CORE_APP[core/: Aplicación Embebida de Shopify]
        SHOPIFY_API_CLIENT[shopify_requests/: Cliente API Shopify]
        WEBHOOKS[webhooks/: Manejo de Webhooks]
        SHOPIFY_METAOBJECTS[metaobjects/shopify_metaobjects/: Integración de Metaobjetos Shopify]
        WAGTAIL_CMS_UI[cms_ui/: Integración de UI del CMS]
        WAGTAIL_CONTENT[shopify_content/: Gestión de Contenido Wagtail]
        WAGTAIL_API[api/: API de Contenido Wagtail]
        DB[Base de Datos (Wagtail/Django)]
    end

    SHOPIFY_ADMIN -- Accede a la interfaz de administración --> CORE_APP
    SHOPIFY_STORE -- Envía eventos (ej. Pedidos, Productos) --> WEBHOOKS
    WEBHOOKS -- Activa lógica de sincronización --> WAGTAIL_CONTENT

    WAGTAIL_CONTENT -- Sincroniza/Obtiene datos --> SHOPIFY_API_CLIENT
    SHOPIFY_API_CLIENT -- Realiza llamadas GraphQL/REST --> SHOPIFY_STORE

    WAGTAIL_CONTENT -- Define y almacena contenido --> DB
    WAGTAIL_CONTENT -- Expone contenido editorial --> WAGTAIL_API

    SHOPIFY_METAOBJECTS -- Crea/Actualiza Metaobjetos --> SHOPIFY_STORE
    SHOPIFY_STORE -- Utiliza Metaobjetos de --> SHOPIFY_METAOBJECTS

    WAGTAIL_API -- Es consumida por --> SHOPIFY_FRONTEND

    WAGTAIL_CMS_UI -- Proporciona interfaz de usuario para --> WAGTAIL_CONTENT
    CORE_APP -- Autentica y gestiona sesiones con --> SHOPIFY_ADMIN
    CORE_APP -- Coordina el uso de --> SHOPIFY_API_CLIENT
    WAGTAIL_CONTENT -- Utiliza los servicios de --> SHOPIFY_METAOBJECTS
```
<p class="mermaid-caption">Diagrama de Arquitectura de Alto Nivel de wagtail-shopify</p>

## Módulos Principales

El repositorio `wagtail-shopify` se organiza en varios módulos clave que gestionan distintas facetas de la integración y el funcionamiento:

*   **[Configuración, CI y Construcción](Build,_CI___Configuration.md)**: Este módulo abarca todas las configuraciones y herramientas relacionadas con la construcción, las pruebas, la gestión de dependencias y la integración continua/despliegue continuo (CI/CD) del proyecto.
*   **[Núcleo de la Aplicación y Plataforma de Integración con Shopify](Application_Core___Shopify_Integration_Platform.md)**: Contiene la lógica central de la aplicación, incluida la aplicación embebida de Shopify, el cliente de la API para interactuar con Shopify, el manejo de webhooks y la integración de metaobjetos de Shopify.
*   **[Gestión de Contenido y API de Wagtail](Wagtail_Content_Management___API.md)**: Este es el módulo principal para la gestión de contenido editorial. Define los modelos de contenido de Wagtail relacionados con Shopify, los servicios de sincronización, los comandos de importación/exportación y la API RESTful que expone el contenido de Wagtail.
*   **[Personalización](Customization.md)**: Este módulo proporciona un punto de extensión para adaptar la aplicación a requisitos específicos del proyecto, permitiendo la sobrescritura de plantillas, la adición de nuevos modelos y la modificación de la lógica de sincronización.

## Construcción y Ejecución

El proyecto `wagtail-shopify` está diseñado para ser construido, probado y desplegado utilizando un conjunto estándar de herramientas de desarrollo Python y JavaScript.

1.  **Gestión de Dependencias**: Las dependencias de Python se gestionan a través de `requirements.txt`. Para instalarlas, se utiliza `pip install -r requirements.txt`. Las dependencias de frontend se gestionan con `package.json` y Vite (`cms_ui/frontend/vite.config.js`).
2.  **Construcción y Desarrollo**: El `Makefile` proporciona objetivos convenientes para tareas como `install-test-deps`, `test`, y `test-glossary`. Los scripts `.cursor/install.sh` y `.cursor/start.sh` facilitan la inicialización del entorno de desarrollo.
3.  **Pruebas**: Las pruebas se ejecutan utilizando Pytest, con configuraciones definidas en `pytest.ini` y `conftest.py`. El `Makefile` incluye un objetivo `test` para ejecutar todas las pruebas unitarias y de integración.
4.  **Integración Continua**: El repositorio utiliza GitHub Actions para la integración continua. El flujo de trabajo `.github/workflows/content-validate.yml` asegura que las validaciones de contenido y las pruebas automatizadas se ejecuten en cada cambio propuesto.
5.  **Configuración de la Aplicación**: La configuración de la aplicación Shopify se gestiona con `shopify.web.toml`. La configuración general del proyecto, incluyendo variables de entorno y ajustes de Django, se define en los archivos `settings.py`.
6.  **Empaquetado**: El archivo `setup.py` se utiliza para empaquetar el proyecto como una librería de Python.

Para una documentación más detallada sobre la configuración del proyecto, la gestión de dependencias, las herramientas de construcción y la integración CI/CD, consulte el módulo [Configuración, CI y Construcción](Build,_CI___Configuration.md).