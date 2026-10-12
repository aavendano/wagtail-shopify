# Bloques de Metafields de Wagtail StreamField

Este módulo, `Wagtail_StreamField_Blocks_Metafield_Blocks`, define el bloque `MetafieldBlock` para su uso en los campos StreamField de Wagtail. Su propósito principal es permitir la incrustación directa de metafields de Shopify dentro del contenido estructurado de las páginas de Wagtail, ofreciendo flexibilidad para gestionar datos personalizados directamente en el editor.

## Propósito y Funcionalidad Principal

El `MetafieldBlock` facilita la creación y edición de metafields de Shopify de forma individual dentro de un StreamField. Si bien proporciona una manera rápida de añadir datos personalizados, la documentación enfatiza que para una gestión más estructurada y en grandes volúmenes de metafields, es preferible utilizar los paneles `InlinePanel` asociados a modelos de página específicos (como `ProductPageMetafield` o `ArticlePageMetafield`). Esto asegura una experiencia de usuario más limpia y un ordenamiento fiable de los metafields.

### Componentes Clave

#### `shopify_content/blocks/metafield.py::MetafieldBlock`

`MetafieldBlock` es un `StructBlock` de Wagtail que encapsula la información necesaria para definir un metafield de Shopify. Sus campos son:

*   `namespace` (CharBlock): El espacio de nombres del metafield en Shopify (por defecto es "custom"). Campo requerido con una longitud máxima de 255 caracteres.
*   `key` (CharBlock): La clave única del metafield. Campo requerido con una longitud máxima de 64 caracteres.
*   `type` (ChoiceBlock): El tipo de dato del metafield, seleccionado de una lista predefinida de `SHOPIFY_METAFIELD_TYPES`. El valor por defecto es 'single_line_text_field'.
*   `value` (TextBlock): El valor real del metafield. Campo requerido.

```python
class MetafieldBlock(StructBlock):
    namespace = CharBlock(default='custom', required=True, max_length=255)
    key = CharBlock(required=True, max_length=64)
    type = ChoiceBlock(
        choices=SHOPIFY_METAFIELD_TYPES,
        default='single_line_text_field',
    )
    value = TextBlock(required=True)
```

#### `shopify_content/blocks/metafield.py::MetafieldBlock.Meta`

La clase `Meta` dentro de `MetafieldBlock` define metadatos para la interfaz de usuario de Wagtail:

*   `icon`: 'tag' - Icono que representa el bloque en la interfaz de Wagtail.
*   `label`: 'Metafield' - Etiqueta visible del bloque.
*   `help_text`: 'Prefer the Metafields panel below the editor for bulk metafield management.' - Texto de ayuda para guiar a los editores sobre el uso preferente de los paneles de metafields.

```python
    class Meta:
        icon = 'tag'
        label = 'Metafield'
        help_text = 'Prefer the Metafields panel below the editor for bulk metafield management.'
```

#### `SHOPIFY_METAFIELD_TYPES`

Esta lista global de tuplas define los tipos de metafields que se pueden seleccionar en el `ChoiceBlock` del campo `type`.

```python
SHOPIFY_METAFIELD_TYPES = [
    ('single_line_text_field', 'Single Line Text'),
    ('rich_text_field', 'Multi Line Text'),
    ('json', 'JSON'),
    ('number_integer', 'Integer'),
    ('number_decimal', 'Decimal'),
    ('boolean', 'Boolean'),
    ('color', 'Color'),
    ('date', 'Date'),
    ('date_time', 'Date & Time'),
    ('url', 'URL'),
    ('rich_text_field', 'Rich Text (HTML)'),
    ('file_reference', 'File Reference'),
    ('page_reference', 'Page Reference'),
    ('product_reference', 'Product Reference'),
    ('collection_reference', 'Collection Reference'),
    ('variant_reference', 'Variant Reference'),
    ('metaobject_reference', 'Metaobject Reference'),
]
```

## Arquitectura y Relaciones entre Componentes

El `MetafieldBlock` es un componente de la arquitectura de bloques de StreamField de Wagtail. Se relaciona con otros bloques definidos en el módulo [Wagtail_StreamField_Blocks](../Wagtail_StreamField_Blocks.md) y se consume dentro de los StreamFields de varias páginas de contenido. Su diseño como `StructBlock` le permite agrupar múltiples campos relacionados para una entrada de datos cohesiva.

Aunque se puede usar directamente en StreamFields, su relación con la gestión estructurada de metafields se extiende a los modelos de página que utilizan `InlinePanel` para `ShopifyMetafield` u otras subclases. Para más detalles sobre cómo se manejan los metafields de manera más estructurada, consulte la documentación de [Content_Page_Models/Content_Page_Models_Reusable_Mixins.md](Shopify_Content_Management/Content_Page_Models/Content_Page_Models_Reusable_Mixins.md).

```mermaid
graph TD
    subgraph BloquesDeStreamFieldDeWagtail
        MetafieldBlockNode[MetafieldBlock]
        MetafieldTypesNode(SHOPIFY_METAFIELD_TYPES)
    end

    subgraph CoreDeWagtail
        StructBlockNode[StructBlock]
        CharBlockNode[CharBlock]
        TextBlockNode[TextBlock]
        ChoiceBlockNode[ChoiceBlock]
    end

    MetafieldBlockNode ---|> StructBlockNode
    MetafieldBlockNode -- uses --> CharBlockNode
    MetafieldBlockNode -- uses --> TextBlockNode
    MetafieldBlockNode -- uses --> ChoiceBlockNode
    ChoiceBlockNode -- references --> MetafieldTypesNode

    subgraph GestionDeContenidoDeShopify
        ContentPageModelsNode[ContentPageModels]
        ShopifyMetafieldMixinNode[ShopifyMetafieldMixin]
        InlinePanelNode[InlinePanel]
    end

    ContentPageModelsNode -- includes --> ShopifyMetafieldMixinNode
    ContentPageModelsNode -- uses for structured metafields --> InlinePanelNode

    MetafieldBlockNode -- alternativa a la gestión estructurada --> InlinePanelNode
    MetafieldBlockNode -- relación conceptual --> ShopifyMetafieldMixinNode
```

## Cómo se Integra en el Sistema General

El `MetafieldBlock` es una herramienta flexible para los editores de contenido que necesitan añadir rápidamente campos de metadatos personalizados a sus páginas de Shopify a través de la interfaz de Wagtail. Complementa la gestión más robusta de metafields proporcionada por los `InlinePanel` y los modelos específicos de metafields de página. Esto permite una experiencia de edición híbrida donde los metafields pueden ser parte del flujo de contenido (`StreamField`) o gestionados como datos estructurados separados (`InlinePanel`), dependiendo de la complejidad y la necesidad de ordenación. La información definida en estos bloques se utiliza en la sincronización de contenido con Shopify, donde se mapea a los metafields correspondientes en la plataforma de e-commerce.