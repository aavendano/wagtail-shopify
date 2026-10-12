# Bloques de Contenido de la Página de Inicio de Wagtail

Este módulo define una serie de bloques de contenido personalizados de Wagtail, diseñados específicamente para estructurar y gestionar el contenido de las páginas de inicio de Shopify. Estos bloques permiten a los editores construir páginas de inicio ricas y dinámicas con una variedad de componentes, como barras de confianza, colecciones destacadas, secciones editoriales, enlaces internos, y más.

## Funcionalidad y Componentes Principales

El módulo `shopify_content/blocks/home.py` contiene varias definiciones de `StructBlock` que representan diferentes secciones de contenido para una página de inicio. A continuación, se detallan los componentes clave:

### LocaleAwarePageChooserBlock

Este bloque (`shopify_content/blocks/home.py::LocaleAwarePageChooserBlock`) extiende `PageChooserBlock` de Wagtail. Su propósito principal es filtrar las `GlossaryTermPage` por la configuración regional de la página actual, asegurando la consistencia del idioma en las secciones de la página de inicio. Esto es crucial para sitios multilingües que necesitan mostrar contenido relevante para la configuración regional seleccionada.

### Bloques de Contenido Específicos para la Página de Inicio

Aquí se describen los principales bloques de contenido disponibles para las páginas de inicio:

*   **`TrustBarItemBlock`** (`shopify_content/blocks/home.py::TrustBarItemBlock`): Representa un elemento individual dentro de una barra de confianza, incluyendo un icono, título y descripción. Es un `StructBlock` con opciones predefinidas para iconos.
*   **`TrustBarBlock`** (`shopify_content/blocks/home.py::TrustBarBlock`): Un `StructBlock` que contiene una lista de `TrustBarItemBlock`, permitiendo la creación de barras de confianza con múltiples elementos.
*   **`FeaturedCollectionItemBlock`** (`shopify_content/blocks/home.py::FeaturedCollectionItemBlock`): Define un elemento de colección destacado, con un selector de página para `CollectionPage` y campos opcionales para sobrescribir el título y la etiqueta.
*   **`FeaturedCollectionsBlock`** (`shopify_content/blocks/home.py::FeaturedCollectionsBlock`): Un `StructBlock` que agrupa múltiples `FeaturedCollectionItemBlock`, junto con un distintivo, título e introducción.
*   **`NavCollectionPillItemBlock`** (`shopify_content/blocks/home.py::NavCollectionPillItemBlock`): Representa un elemento de "píldora" de colección para la navegación rápida, con un selector de página para `CollectionPage` y una etiqueta opcional.
*   **`NavCollectionPillsBlock`** (`shopify_content/blocks/home.py::NavCollectionPillsBlock`): Un `StructBlock` que gestiona una lista de `NavCollectionPillItemBlock`. Permite sembrar las píldoras a partir de las colecciones relacionadas de una colección de origen si la lista de ítems está vacía.
*   **`EditorialIntroBlock`** (`shopify_content/blocks/home.py::EditorialIntroBlock`): Un bloque para la introducción editorial con un encabezado, cuerpo de texto enriquecido y opciones de alineación.
*   **`BestSellersBlock`** (`shopify_content/blocks/home.py::BestSellersBlock`): Muestra una sección de los productos más vendidos, permitiendo especificar un título, una colección de origen, un límite de productos, un distintivo y un fondo.
*   **`ShopByNeedCardBlock`** (`shopify_content/blocks/home.py::ShopByNeedCardBlock`): Una tarjeta individual dentro de una sección "Shop by need", con título, descripción, página de destino (colección o producto), etiqueta y URL de CTA, URL de imagen y etiqueta de intención.
*   **`ShopByNeedBlock`** (`shopify_content/blocks/home.py::ShopByNeedBlock`): Un `StructBlock` que contiene una lista de `ShopByNeedCardBlock`, para crear una sección de compra por necesidad.
*   **`EducationalHubLinkBlock`** (`shopify_content/blocks/home.py::EducationalHubLinkBlock`): Define un enlace dentro de un centro educativo, apuntando a una página vinculable (`LINKABLE_PAGE_TYPES`) y con una etiqueta y descripción opcionales. Utiliza `LocaleAwarePageChooserBlock`.
*   **`EducationalHubBlock`** (`shopify_content/blocks/home.py::EducationalHubBlock`): Un `StructBlock` para un centro educativo, con título, introducción y una lista de `EducationalHubLinkBlock`.
*   **`BrandValueItemBlock`** (`shopify_content/blocks/home.py::BrandValueItemBlock`): Un elemento individual de valor de marca, con icono, título y descripción.
*   **`BrandValuesBlock`** (`shopify_content/blocks/home.py::BrandValuesBlock`): Agrupa los `BrandValueItemBlock` junto con una ceja, encabezado, cuerpo de texto, imagen, URL de imagen, posición de los medios, etiqueta y URL de CTA.
*   **`MarketBlock`** (`shopify_content/blocks/home.py::MarketBlock`): Un bloque que permite mostrar contenido específico del mercado con un encabezado, cuerpo, destacados, etiqueta y URL de CTA, y un código de mercado (ej. US, CA).
*   **`FAQItemBlock`** (`shopify_content/blocks/home.py::FAQItemBlock`): Representa una pregunta frecuente individual con su pregunta y respuesta de texto enriquecido.
*   **`FAQBlock`** (`shopify_content/blocks/home.py::FAQBlock`): Un `StructBlock` que contiene una lista de `FAQItemBlock` para crear una sección de preguntas frecuentes.
*   **`InternalLinkItemBlock`** (`shopify_content/blocks/home.py::InternalLinkItemBlock`): Un elemento de enlace interno, apuntando a una página vinculable (`LINKABLE_PAGE_TYPES`) y con una etiqueta opcional. Utiliza `LocaleAwarePageChooserBlock`.
*   **`InternalLinkGroupBlock`** (`shopify_content/blocks/home.py::InternalLinkGroupBlock`): Un grupo de enlaces internos con un título y una lista de `InternalLinkItemBlock`.
*   **`InternalLinksBlock`** (`shopify_content/blocks/home.py::InternalLinksBlock`): Agrupa múltiples `InternalLinkGroupBlock` con un encabezado.
*   **`PromoGatewayCardBlock`** (`shopify_content/blocks/home.py::PromoGatewayCardBlock`): Una tarjeta individual para el "promo gateway", con título, distintivo, fuente de medios (productos de colección o lista de colecciones), colección principal, colecciones de categoría, etiqueta y URL de CTA, y extensión de columna.
*   **`PromoGatewayBlock`** (`shopify_content/blocks/home.py::PromoGatewayBlock`): Un `StructBlock` que contiene una lista de `PromoGatewayCardBlock`.
*   **`SEOSchemaBlock`** (`shopify_content/blocks/home.py::SEOSchemaBlock`): Un bloque para gestionar las banderas de esquema SEO, permitiendo incluir o excluir el esquema de FAQ y de organización.

## Arquitectura y Relaciones entre Componentes

Este módulo es una colección de bloques de contenido de Wagtail. Cada `XBlock` es un `StructBlock` o un `ListBlock` que encapsula campos y, a menudo, otros `StructBlock` más pequeños para construir estructuras de contenido complejas y reutilizables. Estos bloques están diseñados para ser utilizados dentro de un `StreamField` del modelo `HomePage` (definido en `shopify_content/models/home_page.py`), permitiendo a los editores arrastrar y soltar diferentes secciones en sus páginas de inicio.

La clase `LocaleAwarePageChooserBlock` es un componente clave que asegura que los enlaces internos a páginas como `GlossaryTermPage` respeten la configuración regional de la página de inicio en la que se están utilizando. Esto se logra mediante la lógica de `get_queryset` que filtra las opciones de página disponibles para el editor basándose en la configuración regional de la página actual o de la sesión.

Los `LINKABLE_PAGE_TYPES` definen qué tipos de páginas pueden ser referenciadas por los bloques de enlace, como `ProductPage`, `CollectionPage`, `ArticlePage`, `GlossaryTermPage` y `BlogPage`.

```mermaid
classDiagram
    direction LR

    class Wagtail.blocks.StructBlock {
        + value
    }
    class Wagtail.blocks.ListBlock {
        + items
    }
    class Wagtail.blocks.PageChooserBlock {
        + page_type
    }
    class Wagtail.images.blocks.ImageChooserBlock {
        + image
    }

    class LocaleAwarePageChooserBlock {
        + get_queryset(request, model_admin)
    }
    LocaleAwarePageChooserBlock --|> Wagtail.blocks.PageChooserBlock

    class TrustBarItemBlock {
        + icon: CharBlock
        + title: CharBlock
        + description: CharBlock
    }
    TrustBarItemBlock --|> Wagtail.blocks.StructBlock

    class TrustBarBlock {
        + items: ListBlock~TrustBarItemBlock~
    }
    TrustBarBlock --|> Wagtail.blocks.StructBlock
    TrustBarBlock --> TrustBarItemBlock : contiene

    class FeaturedCollectionItemBlock {
        + collection: PageChooserBlock
        + override_title: CharBlock
        + override_label: CharBlock
    }
    FeaturedCollectionItemBlock --|> Wagtail.blocks.StructBlock

    class FeaturedCollectionsBlock {
        + badge: CharBlock
        + title: CharBlock
        + intro: CharBlock
        + items: ListBlock~FeaturedCollectionItemBlock~
    }
    FeaturedCollectionsBlock --|> Wagtail.blocks.StructBlock
    FeaturedCollectionsBlock --> FeaturedCollectionItemBlock : contiene

    class NavCollectionPillItemBlock {
        + collection: PageChooserBlock
        + override_label: CharBlock
    }
    NavCollectionPillItemBlock --|> Wagtail.blocks.StructBlock

    class NavCollectionPillsBlock {
        + source_collection: PageChooserBlock
        + items: ListBlock~NavCollectionPillItemBlock~
    }
    NavCollectionPillsBlock --|> Wagtail.blocks.StructBlock
    NavCollectionPillsBlock --> NavCollectionPillItemBlock : contiene

    class EditorialIntroBlock {
        + heading: CharBlock
        + body: RichTextBlock
        + alignment: ChoiceBlock
    }
    EditorialIntroBlock --|> Wagtail.blocks.StructBlock

    class BestSellersBlock {
        + title: CharBlock
        + collection: PageChooserBlock
        + product_limit: IntegerBlock
        + badge: CharBlock
        + background: ChoiceBlock
    }
    BestSellersBlock --|> Wagtail.blocks.StructBlock

    class ShopByNeedCardBlock {
        + title: CharBlock
        + description: CharBlock
        + target_page: PageChooserBlock
        + cta_label: CharBlock
        + cta_url: CharBlock
        + image_url: URLBlock
        + intent_tag: CharBlock
    }
    ShopByNeedCardBlock --|> Wagtail.blocks.StructBlock

    class ShopByNeedBlock {
        + title: CharBlock
        + cards: ListBlock~ShopByNeedCardBlock~
    }
    ShopByNeedBlock --|> Wagtail.blocks.StructBlock
    ShopByNeedBlock --> ShopByNeedCardBlock : contiene

    class EducationalHubLinkBlock {
        + page: LocaleAwarePageChooserBlock
        + label: CharBlock
        + description: CharBlock
    }
    EducationalHubLinkBlock --|> Wagtail.blocks.StructBlock
    EducationalHubLinkBlock --> LocaleAwarePageChooserBlock : usa

    class EducationalHubBlock {
        + title: CharBlock
        + intro: CharBlock
        + links: ListBlock~EducationalHubLinkBlock~
    }
    EducationalHubBlock --|> Wagtail.blocks.StructBlock
    EducationalHubBlock --> EducationalHubLinkBlock : contiene

    class BrandValueItemBlock {
        + icon: CharBlock
        + title: CharBlock
        + description: CharBlock
    }
    BrandValueItemBlock --|> Wagtail.blocks.StructBlock

    class BrandValuesBlock {
        + eyebrow: CharBlock
        + heading: CharBlock
        + body: RichTextBlock
        + image: ImageChooserBlock
        + image_url: URLBlock
        + media_position: ChoiceBlock
        + values: ListBlock~BrandValueItemBlock~
        + cta_label: CharBlock
        + cta_url: CharBlock
    }
    BrandValuesBlock --|> Wagtail.blocks.StructBlock
    BrandValuesBlock --> BrandValueItemBlock : contiene

    class MarketBlock {
        + heading: CharBlock
        + body: RichTextBlock
        + highlights: ListBlock~CharBlock~
        + cta_label: CharBlock
        + cta_url: CharBlock
        + market_code: ChoiceBlock
    }
    MarketBlock --|> Wagtail.blocks.StructBlock

    class FAQItemBlock {
        + question: CharBlock
        + answer: RichTextBlock
    }
    FAQItemBlock --|> Wagtail.blocks.StructBlock

    class FAQBlock {
        + heading: CharBlock
        + items: ListBlock~FAQItemBlock~
    }
    FAQBlock --|> Wagtail.blocks.StructBlock
    FAQBlock --> FAQItemBlock : contiene

    class InternalLinkItemBlock {
        + page: LocaleAwarePageChooserBlock
        + label: CharBlock
    }
    InternalLinkItemBlock --|> Wagtail.blocks.StructBlock
    InternalLinkItemBlock --> LocaleAwarePageChooserBlock : usa

    class InternalLinkGroupBlock {
        + title: CharBlock
        + links: ListBlock~InternalLinkItemBlock~
    }
    InternalLinkGroupBlock --|> Wagtail.blocks.StructBlock
    InternalLinkGroupBlock --> InternalLinkItemBlock : contiene

    class InternalLinksBlock {
        + heading: CharBlock
        + groups: ListBlock~InternalLinkGroupBlock~
    }
    InternalLinksBlock --|> Wagtail.blocks.StructBlock
    InternalLinksBlock --> InternalLinkGroupBlock : contiene

    class PromoGatewayCardBlock {
        + title: CharBlock
        + badge: CharBlock
        + media_source: ChoiceBlock
        + primary_collection: PageChooserBlock
        + category_collections: ListBlock~PageChooserBlock~
        + cta_label: CharBlock
        + cta_url: CharBlock
        + column_span: ChoiceBlock
    }
    PromoGatewayCardBlock --|> Wagtail.blocks.StructBlock

    class PromoGatewayBlock {
        + cards: ListBlock~PromoGatewayCardBlock~
    }
    PromoGatewayBlock --|> Wagtail.blocks.StructBlock
    PromoGatewayBlock --> PromoGatewayCardBlock : contiene

    class SEOSchemaBlock {
        + include_faq_schema: BooleanBlock
        + include_organization: BooleanBlock
    }
    SEOSchemaBlock --|> Wagtail.blocks.StructBlock

    class HomePage {
      + body: StreamField
    }
    HomePage --o TrustBarBlock
    HomePage --o FeaturedCollectionsBlock
    HomePage --o NavCollectionPillsBlock
    HomePage --o EditorialIntroBlock
    HomePage --o BestSellersBlock
    HomePage --o ShopByNeedBlock
    HomePage --o EducationalHubBlock
    HomePage --o BrandValuesBlock
    HomePage --o MarketBlock
    HomePage --o FAQBlock
    HomePage --o InternalLinksBlock
    HomePage --o PromoGatewayBlock
    HomePage --o SEOSchemaBlock


    link HomePage [./Shopify_Content_Management/Shopify_Content_Models.md#homepage]
```

## Cómo encaja el Módulo en el Sistema General

Los bloques de contenido definidos en este módulo son fundamentales para la gestión del contenido de las páginas de inicio dentro del sistema de gestión de contenido de Shopify. Integrados con Wagtail, proporcionan una interfaz de usuario flexible y potente para que los editores creen y gestionen las páginas de inicio sin necesidad de escribir código.

*   **Flexibilidad para Editores**: Los editores pueden seleccionar, ordenar y configurar una amplia gama de secciones predefinidas para construir sus páginas de inicio, lo que permite una gran flexibilidad en el diseño y la presentación del contenido.
*   **Consistencia de Datos**: El `LocaleAwarePageChooserBlock` garantiza la consistencia del idioma en los enlaces de las páginas de inicio, lo que es esencial para experiencias de usuario multilingües coherentes.
*   **Estructura de Contenido**: Al utilizar `StructBlock` y `ListBlock`, el módulo impone una estructura clara al contenido, lo que facilita el mantenimiento, la reutilización y la integración con el frontend de Shopify.
*   **Integración con Shopify_Content_Models**: Estos bloques se utilizan en el `StreamField` de la `HomePage` (véase [Modelos de Contenido de Shopify](../Shopify_Content_Models.md#homepage)), que es el modelo central para las páginas de inicio. Esto permite que el contenido creado con estos bloques se almacene y se sirva a la tienda Shopify.
*   **Soporte SEO**: El `SEOSchemaBlock` permite a los editores controlar aspectos del esquema SEO directamente desde el CMS, contribuyendo a la optimización para motores de búsqueda de las páginas de inicio.

En resumen, este módulo actúa como la base para la construcción visual y estructurada de las páginas de inicio, conectando la capacidad de edición de Wagtail con los requisitos de contenido de Shopify.