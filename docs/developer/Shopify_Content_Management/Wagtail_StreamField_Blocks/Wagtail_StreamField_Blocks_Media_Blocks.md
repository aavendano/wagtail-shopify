# Bloques de Medios de StreamField de Wagtail

Este módulo (`shopify_content/blocks/media.py`) contiene bloques de StreamField de Wagtail diseñados para la incrustación de medios, específicamente imágenes y videos, dentro del contenido editable. Estos bloques son fundamentales para crear contenido rico en medios a través de la interfaz de administración de Wagtail y para preparar dicho contenido para su sincronización con Shopify.

## Componentes del Módulo

Los componentes principales definidos en este módulo son `ImageBlock` y `VideoEmbedBlock`, junto con sus respectivas clases `Meta` que configuran su comportamiento y presentación en Wagtail.

### `ImageBlock`

El `ImageBlock` permite a los editores incrustar imágenes en sus StreamFields de Wagtail. Se potencia con funcionalidades de inteligencia artificial a través de `@ai_image_block` de `wagtail_ai` para la generación automática y asistida de texto alternativo.

#### Propósito

Su propósito es proporcionar una forma estructurada y accesible de añadir imágenes a las páginas de Wagtail. Durante el proceso de sincronización saliente, la URL de la imagen gestionada por Wagtail se transforma y se envía a Shopify, ya sea como una referencia de medios o directamente incrustada en el HTML del contenido.

#### Campos

*   `image` (ImageChooserBlock, requerido): Campo principal para seleccionar una imagen de la biblioteca de medios de Wagtail.
*   `alt_text` (CharBlock, opcional): Texto alternativo para mejorar la accesibilidad de la imagen y el SEO. Si se proporciona, anula el título de la imagen. Este campo se beneficia de la integración con IA para la generación asistida de texto.
*   `caption` (CharBlock, opcional): Un subtítulo descriptivo para la imagen.

#### Clase `Meta`

*   `icon`: 'image'
*   `label`: 'Image'
*   `template`: 'shopify_content/blocks/image_block.html'

### `VideoEmbedBlock`

El `VideoEmbedBlock` facilita la incrustación de videos de plataformas populares como YouTube o Vimeo.

#### Propósito

Este bloque está diseñado para permitir a los editores integrar fácilmente contenido de video en sus páginas. Se renderiza como un elemento `<iframe>` en el HTML de Shopify, asegurando la compatibilidad y visualización correcta en el storefront de la tienda.

#### Campos

*   `url` (URLBlock, requerido): La URL completa del video de YouTube o Vimeo.
*   `caption` (CharBlock, opcional): Un subtítulo opcional para el video incrustado.

#### Clase `Meta`

*   `icon`: 'media'
*   `label`: 'Video Embed'
*   `template`: 'shopify_content/blocks/video_embed_block.html'

## Arquitectura y Relaciones de Componentes

Los bloques `ImageBlock` y `VideoEmbedBlock` heredan de `wagtail.blocks.StructBlock`, lo que les permite encapsular múltiples campos relacionados. La interacción y herencia se visualizan a continuación:

```mermaid
graph TD
    A[StructBlock] --> B(ImageBlock)
    A --> C(VideoEmbedBlock)
    B --> D[ImageChooserBlock]
    B --> E[CharBlock (alt_text)]
    B --> F[CharBlock (caption)]
    C --> G[URLBlock]
    C --> H[CharBlock (caption)]
    D -- "Selecciona imagen de Wagtail" --> I[Biblioteca de Medios de Wagtail]
    G -- "Proporciona URL de video" --> J[YouTube/Vimeo]
    I -- "Generación asistida por IA (wagtail_ai)" --> E
```

## Integración en el Sistema General

Estos bloques son componentes esenciales dentro del ecosistema de [Bloques de StreamField de Wagtail](../Wagtail_StreamField_Blocks.md) en la aplicación de gestión de contenido para Shopify. Se emplean en los `StreamField` de diversas páginas de contenido, como artículos, colecciones y páginas de inicio, que se definen en [Modelos de Página de Contenido](../../Content_Page_Models.md).

Durante el proceso de sincronización con Shopify, el contenido de estos bloques se adapta para asegurar su compatibilidad con el tema y la estructura de Shopify:

*   **Imágenes (`ImageBlock`):** Las imágenes pueden ser referenciadas directamente o incrustadas en el HTML. El `alt_text` generado (potencialmente con IA) es crucial para la accesibilidad y la optimización para motores de búsqueda (SEO).
*   **Videos (`VideoEmbedBlock`):** Los videos se renderizan como elementos `<iframe>`, lo que permite su incrustación directa y funcional en el HTML del storefront de Shopify.

La definición y el uso de estos bloques contribuyen a la riqueza visual y la capacidad de edición del contenido editorial gestionado a través de Wagtail, facilitando una experiencia de usuario final dinámica en la tienda Shopify.