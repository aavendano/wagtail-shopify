# Bloques Wagtail StreamField

## Introducción y Propósito

El módulo `Wagtail_StreamField_Blocks` es fundamental para la gestión de contenido flexible y estructurado dentro del sistema de administración de contenido Wagtail, específicamente adaptado para la integración con Shopify. Proporciona una colección de bloques reutilizables que permiten a los editores construir páginas dinámicas (Artículos, Colecciones, Productos y Páginas de Inicio) utilizando una interfaz intuitiva de arrastrar y soltar de StreamField. Estos bloques están diseñados para generar HTML compatible con Shopify, facilitando la sincronización de contenido entre Wagtail y las tiendas Shopify.

El propósito principal de este módulo es:

*   **Flexibilidad editorial:** Permitir a los editores crear diseños de página complejos y variados sin necesidad de conocimientos técnicos.
*   **Consistencia de marca:** Asegurar que el contenido generado siga las directrices de diseño y estilo de Shopify.
*   **Integración con Shopify:** Facilitar la representación de contenido en el escaparate de Shopify a través de la generación de HTML o referencias a metaobjetos y medios.

## Arquitectura General

El módulo `Wagtail_StreamField_Blocks` organiza los bloques de contenido en categorías lógicas, cada una con su propio archivo para mejorar la modularidad y mantenibilidad. El archivo `__init__.py` actúa como el punto central, agregando los bloques definidos en los sub-módulos y definiendo los `StreamBlock` principales que se utilizan en los modelos de página de Wagtail, como `ProductBodyStreamBlock`, `CollectionBodyStreamBlock`, `ArticleBodyStreamBlock` y `HomeBodyStreamBlock`.

La arquitectura se puede visualizar de la siguiente manera:

```mermaid
graph TD
    subgraph Wagtail_StreamField_Blocks
        init_py[shopify_content/blocks/__init__.py]
        content_py[shopify_content/blocks/content.py]
        home_py[shopify_content/blocks/home.py]
        media_py[shopify_content/blocks/media.py]
        metafield_py[shopify_content/blocks/metafield.py]
        product_py[shopify_content/blocks/product.py]

        init_py -- Define StreamBlocks para páginas --> ProductBodyStreamBlock((ProductBodyStreamBlock))
        init_py -- Define StreamBlocks para páginas --> CollectionBodyStreamBlock((CollectionBodyStreamBlock))
        init_py -- Define StreamBlocks para páginas --> ArticleBodyStreamBlock((ArticleBodyStreamBlock))
        init_py -- Define StreamBlocks para páginas --> HomeBodyStreamBlock((HomeBodyStreamBlock))

        ProductBodyStreamBlock --> content_py
        ProductBodyStreamBlock --> media_py
        ProductBodyStreamBlock --> product_py
        ProductBodyStreamBlock --> metafield_py

        CollectionBodyStreamBlock --> content_py
        CollectionBodyStreamBlock --> media_py

        ArticleBodyStreamBlock --> content_py
        ArticleBodyStreamBlock --> media_py

        HomeBodyStreamBlock --> home_py

        content_py -- Define bloques de contenido general --> HeadingBlock
        content_py -- Define bloques de contenido general --> ParagraphBlock
        content_py -- Define bloques de contenido general --> HtmlBlock
        content_py -- Define bloques de contenido general --> CalloutBlock
        content_py -- Define bloques de contenido general --> ProductBannerBlock

        home_py -- Define bloques específicos de página de inicio --> TrustBarBlock
        home_py -- Define bloques específicos de página de inicio --> FeaturedCollectionsBlock
        home_py -- Define bloques específicos de página de inicio --> NavCollectionPillsBlock
        home_py -- Define bloques específicos de página de inicio --> EditorialIntroBlock
        home_py -- Define bloques específicos de página de inicio --> BestSellersBlock
        home_py -- Define bloques específicos de página de inicio --> ShopByNeedBlock
        home_py -- Define bloques específicos de página de inicio --> EducationalHubBlock
        home_py -- Define bloques específicos de página de inicio --> BrandValuesBlock
        home_py -- Define bloques específicos de página de inicio --> MarketBlock
        home_py -- Define bloques específicos de página de inicio --> FAQBlock
        home_py -- Define bloques específicos de página de inicio --> InternalLinksBlock
        home_py -- Define bloques específicos de página de inicio --> PromoGatewayBlock
        home_py -- Define bloques específicos de página de inicio --> SEOSchemaBlock

        media_py -- Define bloques de medios --> ImageBlock
        media_py -- Define bloques de medios --> VideoEmbedBlock

        metafield_py -- Define bloque de metafield --> MetafieldBlock

        product_py -- Define bloque de característica de producto --> ProductFeatureBlock
    end

    ProductBodyStreamBlock --- Utilizado por ---> [Páginas de Producto]
    CollectionBodyStreamBlock --- Utilizado por ---> [Páginas de Colección]
    ArticleBodyStreamBlock --- Utilizado por ---> [Páginas de Artículo]
    HomeBodyStreamBlock --- Utilizado por ---> [Páginas de Inicio]
```

## Funcionalidad de los Sub-módulos

Este módulo se divide en varios sub-módulos, cada uno encargado de definir un conjunto específico de bloques de `StreamField`:

*   **[Bloques de Contenido General](Wagtail_StreamField_Blocks/Wagtail_StreamField_Blocks_BloquesContenidoGeneral.md):** Define bloques básicos para texto, encabezados, HTML incrustado y elementos de llamada a la acción.
*   **[Bloques de Página de Inicio](Wagtail_StreamField_Blocks/Wagtail_StreamField_Blocks_BloquesPaginaInicio.md):** Contiene bloques diseñados específicamente para estructurar la página de inicio, como barras de confianza, colecciones destacadas, secciones editoriales y de SEO.
*   **[Bloques de Medios](Wagtail_StreamField_Blocks/Wagtail_StreamField_Blocks_BloquesMedios.md):** Gestiona la incrustación de imágenes y videos en el contenido.
*   **[Bloques de Metafield](Wagtail_StreamField_Blocks/Wagtail_StreamField_Blocks_BloquesMetafield.md):** Permite la inclusión directa de Shopify Metafields dentro del flujo de contenido.
*   **[Bloques de Características de Producto](Wagtail_StreamField_Blocks/Wagtail_StreamField_Blocks_BloquesCaracteristicasProducto.md):** Proporciona un bloque específico para resaltar características clave de un producto.

La siguiente sección detalla cada uno de estos sub-módulos.