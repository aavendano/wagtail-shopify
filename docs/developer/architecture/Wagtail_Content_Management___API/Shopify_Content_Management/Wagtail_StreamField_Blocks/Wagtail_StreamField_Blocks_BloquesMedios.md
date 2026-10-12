# Bloques de Medios de Wagtail StreamField

Este módulo, `Wagtail_StreamField_Blocks_BloquesMedios`, define bloques de contenido para la gestión de medios enriquecidos dentro de Wagtail StreamField, específicamente para imágenes y vídeos. Estos bloques están diseñados para facilitar la inclusión de elementos multimedia en el contenido gestionado por Wagtail, con consideraciones para la sincronización y visualización en plataformas como Shopify.

## Componentes Principales

### `ImageBlock`

El `ImageBlock` permite a los editores incrustar imágenes en el contenido. Está enriquecido con funcionalidad de inteligencia artificial para la generación automática de texto alternativo (`alt_text`).

#### Propiedades:

*   `image`: Un `ImageChooserBlock` requerido que permite seleccionar una imagen de la biblioteca de Wagtail.
*   `alt_text`: Un `CharBlock` opcional para el texto alternativo de la imagen. Este campo puede ser autogenerado por la funcionalidad de IA de Wagtail AI y anula el título de la imagen para mejorar la accesibilidad.
*   `caption`: Un `CharBlock` opcional para una descripción o pie de foto de la imagen.

#### Metadatos (`ImageBlock.Meta`):

*   `icon`: Representado por el icono 'image'.
*   `label`: 'Image'.
*   `template`: `shopify_content/blocks/image_block.html` para la renderización.

#### Relación con Shopify

Cuando el contenido se sincroniza con Shopify, la URL de la imagen de Wagtail se transfiere a Shopify, ya sea como una referencia de medios o incrustada directamente en el HTML del contenido. Esto asegura que las imágenes sean accesibles y se muestren correctamente en la tienda Shopify.

### `VideoEmbedBlock`

El `VideoEmbedBlock` proporciona una forma sencilla de incrustar vídeos de plataformas como YouTube o Vimeo en el contenido.

#### Propiedades:

*   `url`: Un `URLBlock` requerido para la URL del vídeo de YouTube o Vimeo.
*   `caption`: Un `CharBlock` opcional para un pie de foto o descripción del vídeo.

#### Metadatos (`VideoEmbedBlock.Meta`):

*   `icon`: Representado por el icono 'media'.
*   `label`: 'Video Embed'.
*   `template`: `shopify_content/blocks/video_embed_block.html` para la renderización.

#### Relación con Shopify

Los vídeos incrustados se renderizan como elementos `<iframe>` en el HTML que se envía a Shopify, permitiendo la reproducción directa del vídeo dentro del contenido de la tienda.

## Arquitectura y Relaciones de Componentes

Los bloques `ImageBlock` y `VideoEmbedBlock` son componentes clave dentro del sistema de gestión de contenido de Wagtail, específicamente en el contexto de `StreamField`. Permiten a los editores construir contenido dinámico y rico en medios.

```mermaid
classDiagram
    direction LR
    AbstractBlock <|-- StructBlock
    StructBlock <|-- ImageBlock
    StructBlock <|-- VideoEmbedBlock

    ImageBlock : +ImageChooserBlock image
    ImageBlock : +CharBlock alt_text
    ImageBlock : +CharBlock caption
    ImageBlock : +Meta class (icon, label, template)

    VideoEmbedBlock : +URLBlock url
    VideoEmbedBlock : +CharBlock caption
    VideoEmbedBlock : +Meta class (icon, label, template)

    note for ImageBlock
        @ai_image_block decorator for alt_text generation.
    end note
```

## Flujo de Datos y Integración con Shopify

El siguiente diagrama ilustra cómo los bloques de medios se integran con Wagtail y cómo su contenido se transfiere a Shopify.

```mermaid
graph TD
    A[Editor de Wagtail] --> B{StreamField de Contenido}
    B --> C[ImageBlock]
    B --> D[VideoEmbedBlock]

    C --> E[Sistema de Imágenes de Wagtail]
    C --> F[Metadatos de Imagen (alt_text, caption)]

    D --> G[URL de Vídeo (YouTube/Vimeo)]
    D --> H[Metadatos de Vídeo (caption)]

    E --> I[URL de Imagen]

    F --> J[Generación de Texto Alternativo (AI)]

    I --> K[Sincronización a Shopify]
    J --> K

    G --> K
    H --> K

    K --> L[Shopify: Media Reference / HTML Embed (Imágenes)]
    K --> M[Shopify: iFrame Embed (Vídeos)]

    subgraph Wagtail CMS
        A
        B
        C
        D
        E
        F
        G
        H
        I
        J
    end

    subgraph Shopify
        L
        M
    end

    classDef default fill:#ECECFF,stroke:#333,stroke-width:2px;
    classDef wagtail fill:#CCFFCC,stroke:#3C3,stroke-width:2px;
    classDef shopify fill:#FFCCEE,stroke:#E33,stroke-width:2px;

    class A,B,C,D,E,F,G,H,I,J wagtail;
    class K default;
    class L,M shopify;
```

En el diagrama:

*   El **Editor de Wagtail** utiliza el **StreamField de Contenido** para añadir `ImageBlock` y `VideoEmbedBlock`.
*   Para `ImageBlock`, el sistema de imágenes de Wagtail proporciona las imágenes y los metadatos. La generación de texto alternativo por IA es una característica adicional.
*   Para `VideoEmbedBlock`, se proporciona una URL de vídeo y opcionalmente un pie de foto.
*   Todo este contenido se somete a un proceso de **Sincronización a Shopify**.
*   En Shopify, las imágenes se gestionan como referencias de medios o se incrustan en HTML, mientras que los vídeos se insertan como elementos `<iframe>`.