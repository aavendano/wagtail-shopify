# Bloque de Metafields de Wagtail

El módulo `Wagtail_Content_Blocks_Metafield` define el bloque `MetafieldBlock`, que permite la inclusión de metafields de Shopify directamente dentro de StreamFields de Wagtail. Este componente es esencial para proporcionar a los editores de contenido la flexibilidad de incrustar información estructurada de Shopify en el flujo de contenido de las páginas, complementando la gestión de metafields más estructurada a través de paneles dedicados.

## Funcionalidad Principal

El `MetafieldBlock` permite a los usuarios definir un metafield con un `namespace`, `key`, `type` y `value`. Esto es particularmente útil para metafields únicos o contextuales que necesitan aparecer en puntos específicos dentro del cuerpo del contenido, en lugar de ser gestionados de forma global para toda la página.

### `MetafieldBlock`

El `MetafieldBlock` es un `StructBlock` de Wagtail que encapsula la información de un metafield de Shopify.

**Campos:**
*   `namespace` (CharBlock): El namespace del metafield en Shopify. Por defecto es 'custom'.
*   `key` (CharBlock): La clave única del metafield.
*   `type` (ChoiceBlock): El tipo de dato del metafield, seleccionable de una lista predefinida (`SHOPIFY_METAFIELD_TYPES`).
*   `value` (TextBlock): El valor del metafield.

#### Tipos de Metafields Soportados (`SHOPIFY_METAFIELD_TYPES`)

La constante `SHOPIFY_METAFIELD_TYPES` define los tipos de metafields de Shopify que pueden ser seleccionados para un `MetafieldBlock`. Esta lista incluye una variedad de tipos de datos, desde texto simple hasta referencias a otros recursos de Shopify.

*   `single_line_text_field`: Texto de una sola línea.
*   `rich_text_field`: Texto multilínea (HTML o texto enriquecido).
*   `json`: Datos en formato JSON.
*   `number_integer`: Número entero.
*   `number_decimal`: Número decimal.
*   `boolean`: Valor booleano.
*   `color`: Valor de color.
*   `date`: Fecha.
*   `date_time`: Fecha y hora.
*   `url`: URL.
*   `file_reference`: Referencia a un archivo.
*   `page_reference`: Referencia a una página de Shopify.
*   `product_reference`: Referencia a un producto de Shopify.
*   `collection_reference`: Referencia a una colección de Shopify.
*   `variant_reference`: Referencia a una variante de producto.
*   `metaobject_reference`: Referencia a un metaobjeto de Shopify.

### `MetafieldBlock.Meta`

La clase `Meta` anidada dentro de `MetafieldBlock` proporciona metadatos para la configuración del bloque en la interfaz de usuario de Wagtail.

*   `icon`: 'tag' - El icono que representa el bloque en el editor de Wagtail.
*   `label`: 'Metafield' - La etiqueta visible para el bloque.
*   `help_text`: 'Prefer the Metafields panel below the editor for bulk metafield management.' - Texto de ayuda que sugiere el uso de paneles de metafields dedicados para una gestión masiva.

## Arquitectura y Relaciones

El `MetafieldBlock` es un componente de [Wagtail_Content_Blocks](../Wagtail_Content_Blocks.md), el cual forma parte del módulo más grande [Shopify_Content_Management](../../Shopify_Content_Management.md). Su diseño como `StructBlock` lo integra directamente en el sistema de StreamField de Wagtail, permitiendo a los editores insertarlo en cualquier `StreamField` definido en los modelos de página.

### Diagrama de Relaciones de Componentes

```mermaid
graph TD
    A[shopify_content/blocks/metafield.py::MetafieldBlock] --> B{StreamField de Wagtail};
    A --> C[shopify_content/blocks/metafield.py::MetafieldBlock.Meta];
    A -- Utiliza --> D[SHOPIFY_METAFIELD_TYPES];
    B -- Contiene --> A;
    E[Páginas de Wagtail (e.g., ArticlePage, ProductPage)] -- Pueden contener --> B;
    F[ShopifyMetafield (en Shopify_Content_Management/Shopify_Content_Models.md)] -- Gestión estructurada de metafields --> G{Base de datos / API de Shopify};
    A -- Gestión inline de metafields --> G;

    subgraph Shopify_Content_Management/Wagtail_Content_Blocks
        A
        C
        D
    end

    subgraph Shopify_Content_Management/Shopify_Content_Models
        F
    end
```
**Leyenda:**
*   **A:** `MetafieldBlock` - Bloque de Wagtail para metafields.
*   **B:** `StreamField` de Wagtail - Contenedor principal de bloques de contenido.
*   **C:** `MetafieldBlock.Meta` - Metadatos de configuración del bloque.
*   **D:** `SHOPIFY_METAFIELD_TYPES` - Lista de tipos de metafields soportados.
*   **E:** Páginas de Wagtail - Modelos de páginas que utilizan `StreamField`.
*   **F:** `ShopifyMetafield` - Modelo para una gestión más estructurada de metafields (ver [Shopify_Content_Management/Shopify_Content_Models.md](../Shopify_Content_Models.md)).
*   **G:** Base de datos / API de Shopify - Donde se almacenan los metafields.

## Integración con el Sistema General

El `MetafieldBlock` se integra en el sistema de gestión de contenido de Shopify a través de Wagtail. Permite a los equipos de contenido una granularidad fina sobre dónde y cómo se presentan los metafields en el cuerpo del contenido.

Aunque proporciona flexibilidad, la `help_text` del bloque enfatiza que para la gestión masiva o estructurada de metafields, se prefiere el uso de `InlinePanel` en las páginas (como `ProductPageMetafield` o `ArticlePageMetafield`), que se encuentran en [Shopify_Content_Management/Shopify_Content_Models.md](../Shopify_Content_Models.md). Estos paneles ofrecen una experiencia de usuario más limpia y garantizan un orden fiable para metafields con una estructura predefinida.

En resumen, el `MetafieldBlock` actúa como un complemento para la gestión de contenido, ofreciendo una solución para casos de uso específicos donde los metafields deben ser insertados directamente en el flujo de contenido de una página, mientras que los modelos de metafields dedicados manejan la información estructurada a nivel de página o de recurso de Shopify.
