# Páginas de Inicio (Home Pages)


Este documento detalla el módulo `Content_Page_Models_Home_Pages`, que se centra en la definición del modelo `HomePage` utilizado para gestionar el contenido de las páginas de inicio dentro del sistema. `HomePage` es una página de Wagtail que se sincroniza con un metaobjeto de Shopify, permitiendo la gestión de contenido multilingüe para las fachadas de las tiendas.

## Propósito y Funcionalidad Principal

El módulo `Content_Page_Models_Home_Pages` define el modelo `HomePage`, que es fundamental para la gestión de las páginas de inicio de las tiendas Shopify. Cada instancia de `HomePage` representa el contenido de una página de inicio para una localización específica y se encarga de:

*   **Almacenar contenido editorial**: Incluye campos para el héroe (hero_eyebrow, hero_heading, hero_subheading, hero_body, hero_image) y una estructura flexible para secciones del cuerpo (`StreamField`).
*   **Sincronización con Shopify**: Se vincula a un metaobjeto de Shopify (`home_page`) para mantener el contenido sincronizado con la plataforma de comercio electrónico.
*   **Soporte multilingüe**: Permite especificar una localización de Shopify (`shopify_locale`) para el contenido de la página de inicio.
*   **Gestión de URL**: Utiliza un slug derivado del handle y una URL de Shopify.

### Componentes Principales

A continuación, se describen los componentes clave de este módulo:

*   `shopify_content/models/home_page.py::HomePage`
*   `shopify_content/models/home_page.py::HomePage.Meta`

#### `HomePage`

La clase `HomePage` es un modelo de página de Wagtail que extiende `wagtail.models.Page`. Está diseñada para ser la representación en el CMS del contenido de la página de inicio de Shopify.

**Campos Clave**:

*   `shopify_id`: GID del metaobjeto de Shopify, se rellena después de la primera sincronización.
*   `handle`: Handle del metaobjeto de Shopify, se deriva automáticamente como `home-<locale>`.
*   `sync_enabled`: Booleano para habilitar o deshabilitar la sincronización con Shopify.
*   `last_synced_at`: Fecha y hora de la última sincronización.
*   `shopify_locale`: Código de localización (e.g., `en-US`) que se envía a Shopify. Utiliza las opciones definidas en `config.settings.ALLOWED_LOCALE_CODES`.
*   **Campos del Héroe**: `hero_eyebrow`, `hero_heading`, `hero_subheading`, `hero_body` (RichTextField), `hero_primary_cta_label`, `hero_primary_cta_url`, `hero_secondary_cta_label`, `hero_secondary_cta_url`, `hero_image` (ForeignKey a `wagtailimages.Image`), `hero_image_url`.
*   `body`: Un `StreamField` que utiliza los bloques definidos en `HOME_BODY_BLOCKS` (ver [Wagtail_StreamField_Blocks.md](../Wagtail_StreamField_Blocks.md)).
*   `sections_json`: Un campo JSON que almacena el contenido del `StreamField` `body` en un formato normalizado (versión 1, 13 tipos canónicos).

**Métodos Importantes**:

*   `sync_body_and_sections_json()`: Sincroniza el contenido entre `body` (StreamField) y `sections_json`. Garantiza que `sections_json` se derive de `body` si este tiene bloques, o que `body` se reconstruya a partir de `sections_json` normalizado.
*   `clean()`: Realiza la validación del modelo antes de guardar. Deriva el slug y el handle, invoca `sync_body_and_sections_json`, y valida la localización de `sections_json`. También asegura que solo exista una `HomePage` por localización bajo la raíz `ShopifyRootPage`.
*   `get_seo_title()`: Devuelve el título SEO de la página o el `hero_heading` si el título SEO está vacío.
*   `get_seo_description()`: Devuelve la descripción SEO o el `hero_subheading` si la descripción SEO está vacía.

#### `HomePage.Meta`

Define metadatos para el modelo `HomePage`, incluyendo `verbose_name` y `verbose_name_plural`, que se utilizan en la interfaz de administración de Django y Wagtail para una mejor presentación.

## Arquitectura y Relaciones de Componentes

El modelo `HomePage` se integra en la arquitectura general de gestión de contenido de Shopify de la siguiente manera:

```mermaid
graph TD
    subgraph CMS [Sistema de Gestión de Contenido Wagtail]
        HP[HomePage] --- extiende --> Page("wagtail.models.Page")
        HP --- utiliza --> HOME_BODY_BLOCKS["StreamField Blocks"]
        HP --- paneles de admin --> ContentPanels("content_panels")
        HP --- paneles de admin --> PromotePanels("promote_panels")
        HP --- paneles de admin --> SettingsPanels("settings_panels")
        HP --- validación de localización --> validate_sections_json_locale
        HP --- normalización de secciones --> normalize_sections_json
        HP --- serialización --> sections_json_to_stream_data
        HP --- serialización --> streamfield_to_sections_json
        HP --- gestión de handle --> home_page_handle
    end

    subgraph Shopify [Plataforma Shopify]
        Metaobject("Metaobject (tipo: home_page)")
    end

    Shopify_Root_Page("ShopifyRootPage") --- es padre de --> HP

    HOME_BODY_BLOCKS --- definidos en --> Shopify_Content_Management/Wagtail_StreamField_Blocks.md
    ContentPanels --- incluye --> HeroFields("Campos de Héroe")
    ContentPanels --- incluye --> BodyStreamField("body StreamField")
    PromotePanels --- incluye --> SHOPIFY_SEO_PANELS["Paneles SEO"]
    PromotePanels --- incluye --> LocaleField("shopify_locale")
    SettingsPanels --- incluye --> ShopifySyncFields("Campos de Sincronización de Shopify")
    SettingsPanels --- incluye --> StorefrontUrlsPanel("Panel de URLs de Fachada")

    HP --- contiene ID y handle --> Metaobject
    Metaobject --- sincroniza contenido con --> HP
    SHOPIFY_SEO_PANELS --- definidos en --> mixins.py
    StorefrontUrlsPanel --- definido en --> admin_panels.py
```

**Relaciones Clave**:

*   **Wagtail Page**: `HomePage` hereda de `wagtail.models.Page`, lo que le proporciona todas las funcionalidades de una página de Wagtail, incluyendo la jerarquía, la publicación y la interfaz de edición.
*   **StreamField Blocks**: El campo `body` de `HomePage` utiliza `HOME_BODY_BLOCKS`, que son bloques de `StreamField` definidos en el módulo [Wagtail_StreamField_Blocks.md](../Wagtail_StreamField_Blocks.md), permitiendo la creación de contenido flexible y estructurado.
*   **Shopify Metaobjects**: `HomePage` está diseñado para sincronizar su contenido con un metaobjeto de Shopify de tipo `home_page`. Esto se gestiona a través de los campos `shopify_id`, `handle` y la lógica de sincronización. La definición de estos metaobjetos se bootstrap con el comando `python manage.py ensure_metaobject_definitions`.
*   **ShopifyRootPage**: `HomePage` solo puede ser una subpágina de `ShopifyRootPage` (ver [Content_Page_Models_Root_Pages.md](Content_Page_Models_Root_Pages.md)), asegurando una estructura de contenido organizada. Además, se aplica una restricción para que solo exista una `HomePage` por localización bajo una `ShopifyRootPage` con slug `cms-home`.
*   **Paneles de Administración**: La interfaz de edición de `HomePage` se organiza mediante `TabbedInterface` y `ObjectList`, utilizando `content_panels`, `promote_panels` (que incluye `SHOPIFY_SEO_PANELS` de `mixins.py`) y `settings_panels` (que incluye `StorefrontUrlsPanel` de `admin_panels.py`).

## Cómo Encaja el Módulo en el Sistema General

El módulo `Content_Page_Models_Home_Pages` es una parte integral del sistema de gestión de contenido de Shopify, específicamente dentro de las [Páginas de Modelos de Contenido](Content_Page_Models.md).

*   **Gestión de Contenido Centralizada**: Proporciona la estructura de datos fundamental para las páginas de inicio, permitiendo a los editores de contenido crear y gestionar el contenido de la página de inicio directamente desde el CMS de Wagtail.
*   **Integración con Shopify**: Actúa como el puente entre el contenido editorial en Wagtail y los metaobjetos de Shopify, asegurando que el contenido de la página de inicio esté disponible en la fachada de la tienda Shopify.
*   **Localización**: Su soporte para `shopify_locale` es crucial para aplicaciones multilingües, permitiendo que diferentes versiones de la página de inicio existan para diferentes mercados.
*   **Extensibilidad**: El uso de `StreamField` para el cuerpo de la página de inicio permite a los desarrolladores añadir nuevos tipos de bloques de contenido sin modificar la estructura fundamental de la página, proporcionando flexibilidad para futuras expansiones.
*   **Flujo de Sincronización**: Los mecanismos de `sync_body_and_sections_json` y la validación en `clean` son vitales para mantener la integridad de los datos entre el `StreamField` de Wagtail y el JSON normalizado que se sincroniza con Shopify.

En resumen, `HomePage` es la piedra angular para la gestión de contenido de la página de inicio dentro del entorno de Shopify, facilitando la creación, edición y sincronización de contenido rico y localizado.