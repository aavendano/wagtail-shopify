# Bloques de Contenido Wagtail

El módulo `Wagtail_Content_Blocks` define una colección de bloques de contenido reusables para Wagtail StreamFields, diseñados específicamente para la gestión de contenido en Shopify. Estos bloques permiten a los editores construir páginas ricas y estructuradas como artículos, colecciones, páginas de productos y la página de inicio, utilizando una interfaz de arrastrar y soltar en el CMS de Wagtail.

## Propósito y Funcionalidad Principal

Este módulo tiene como objetivo principal proporcionar un conjunto flexible y potente de componentes de contenido que se pueden utilizar para construir diversos diseños de página dentro del ecosistema de Shopify. Facilita la creación de contenido dinámico y adaptable a través de StreamFields de Wagtail, asegurando la compatibilidad y la renderización adecuada en la tienda Shopify.

Los bloques se dividen en categorías funcionales, incluyendo:

*   **Bloques de Contenido General:** Elementos básicos de texto, títulos, llamadas de atención y HTML sin formato.
*   **Bloques Específicos de la Página de Inicio:** Componentes complejos para construir la página principal, como barras de confianza, colecciones destacadas, secciones de editorial, productos más vendidos, y enlaces internos.
*   **Bloques de Medios:** Gestión de imágenes y videos incrustados.
*   **Bloques de Metafields:** Permiten la inserción de metafields de Shopify directamente en el flujo de contenido.
*   **Bloques de Productos:** Componentes para destacar características de productos o banners de productos.

## Arquitectura General

La arquitectura de `Wagtail_Content_Blocks` se basa en la extensibilidad de Wagtail StreamFields. Cada tipo de bloque es una clase Python que hereda de `wagtail.blocks.StructBlock` o `wagtail.blocks.StreamBlock`, definiendo su estructura, campos y opciones de renderizado. Los bloques se organizan en diferentes archivos Python dentro del directorio `shopify_content/blocks/` según su propósito.

```mermaid
graph TD
    A[shopify_content/blocks/__init__.py] --> B(StreamBlock base para tipos de página)
    B --> C(ProductBodyStreamBlock)
    B --> D(CollectionBodyStreamBlock)
    B --> E(ArticleBodyStreamBlock)
    B --> F(HomeBodyStreamBlock)

    subgraph Bloques de Contenido Generales
        G[shopify_content/blocks/content.py] --> H(HeadingBlock)
        G --> I(ParagraphBlock)
        G --> J(HtmlBlock)
        G --> K(CalloutBlock)
        G --> L(ProductBannerBlock)
    end

    subgraph Bloques de Contenido de la Página de Inicio
        M[shopify_content/blocks/home.py] --> N(TrustBarBlock)
        M --> O(FeaturedCollectionsBlock)
        M --> P(NavCollectionPillsBlock)
        M --> Q(EditorialIntroBlock)
        M --> R(BestSellersBlock)
        M --> S(ShopByNeedBlock)
        M --> T(EducationalHubBlock)
        M --> U(BrandValuesBlock)
        M --> V(MarketBlock)
        M --> W(FAQBlock)
        M --> X(InternalLinksBlock)
        M --> Y(PromoGatewayBlock)
        M --> Z(SEOSchemaBlock)
        M --> ZL(LocaleAwarePageChooserBlock)
    end

    subgraph Bloques de Medios
        AA[shopify_content/blocks/media.py] --> BB(ImageBlock)
        AA --> CC(VideoEmbedBlock)
    end

    subgraph Bloques de Metafield
        DD[shopify_content/blocks/metafield.py] --> EE(MetafieldBlock)
    end

    subgraph Bloques de Producto
        FF[shopify_content/blocks/product.py] --> GG(ProductFeatureBlock)
    end

    C --> H
    C --> I
    C --> BB
    C --> CC
    C --> GG
    C --> K
    C --> J
    C --> EE

    D --> H
    D --> I
    D --> BB
    D --> K
    D --> J

    E --> H
    E --> I
    E --> BB
    E --> CC
    E --> K
    E --> J
    E --> L

    F --> N
    F --> O
    F --> P
    F --> Q
    F --> R
    F --> S
    F --> T
    F --> U
    F --> V
    F --> W
    F --> X
    F --> Y
    F --> Z

    H, I, J, K, L -- usa --> G
    N, O, P, Q, R, S, T, U, V, W, X, Y, Z, ZL -- usa --> M
    BB, CC -- usa --> AA
    EE -- usa --> DD
    GG -- usa --> FF
```

## Relación con el Sistema General

Los bloques de contenido definidos en este módulo son el corazón de la edición de contenido en el CMS de Wagtail para las páginas de Shopify. Se integran con el módulo [`Shopify_Content_Models`](Shopify_Content_Models.md) para definir los `StreamField` de los modelos de página (e.g., `ArticlePage`, `CollectionPage`, `HomePage`, `ProductPage`).

La salida de estos bloques se serializa y se sincroniza con Shopify, lo que permite que el contenido creado en Wagtail se muestre correctamente en la tienda en línea. Algunos bloques, como `MetafieldBlock`, interactúan directamente con la funcionalidad de metafields de Shopify. Además, los bloques de medios pueden depender de la infraestructura de medios de Wagtail (`ImageChooserBlock`).

## Sub-módulos

A continuación, se describen los sub-módulos que componen `Wagtail_Content_Blocks`, con enlaces a su documentación detallada:

*   **[`Bloques de Contenido General`](Wagtail_Content_Blocks/Wagtail_Content_Blocks_Content_Genericos.md)**: Proporciona bloques básicos para texto, encabezados, llamadas de atención y HTML.
*   **[`Bloques de Contenido de la Página de Inicio`](Wagtail_Content_Blocks/Wagtail_Content_Blocks_Home_Page.md)**: Contiene bloques especializados para la construcción de la página de inicio, como barras de confianza, colecciones destacadas y secciones editoriales.
*   **[`Bloques de Medios`](Wagtail_Content_Blocks/Wagtail_Content_Blocks_Medios.md)**: Incluye bloques para la inserción de imágenes y videos.
*   **[`Bloques de Metafields`](Wagtail_Content_Blocks/Wagtail_Content_Blocks_Metafield.md)**: Permite añadir metafields de Shopify directamente en el contenido.
*   **[`Bloques de Producto`](Wagtail_Content_Blocks/Wagtail_Content_Blocks_Producto.md)**: Ofrece bloques para mostrar características de productos.
