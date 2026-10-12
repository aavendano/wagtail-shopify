# Migración de Base de Datos 0002_blog_description_and_seo

Esta documentación detalla la migración de base de datos `0002_blog_description_and_seo`, parte del módulo `shopify_content` dentro del sistema de gestión de contenido Wagtail y la integración con Shopify.

## 1. Propósito y Funcionalidad Principal

La migración `0002_blog_description_and_seo` tiene como objetivo principal extender el modelo `BlogPage` de Wagtail, añadiendo un campo `description` para permitir la inclusión de descripciones detalladas y contenido optimizado para SEO en las páginas de blog.

El campo `description` se define como un `models.TextField`, lo que permite almacenar texto largo, incluyendo HTML. Este campo está diseñado para sincronizarse con `metafield descriptors.description` en Shopify, facilitando la gestión de metadatos de SEO directamente desde Wagtail.

## 2. Arquitectura y Relaciones entre Componentes

Esta migración es una migración estándar de Django que modifica el esquema de la base de datos.

### Dependencias

La migración `0002_blog_description_and_seo` depende de la migración `0001_initial` del módulo `shopify_content`, lo que asegura que las tablas iniciales y el modelo `BlogPage` existan antes de intentar añadir el nuevo campo.

```python
class Migration(migrations.Migration):
    dependencies = [
        ("shopify_content", "0001_initial"),
    ]
    # ...
```

### Componentes Modificados

El componente principal afectado por esta migración es el modelo `BlogPage`. Aunque el código del modelo `BlogPage` no se encuentra directamente en este archivo de migración, la migración lo modifica añadiendo el campo `description`. El modelo `BlogPage` reside en `shopify_content/models/blog.py`. Para más detalles sobre el modelo `BlogPage`, consulte la documentación del módulo [Modelos de Contenido de Blog](../Blog_Content_Models.md).

### Diagrama de Relaciones de la Migración

```mermaid
graph TD
    subgraph shopify_content/migrations
        A[0001_initial.py] --> B(0002_blog_description_and_seo.py)
    end

    subgraph shopify_content/models
        C[BlogPage (shopify_content/models/blog.py)]
    end

    B -- Añade campo 'description' a --> C
```

## 3. Posición en el Sistema General

Esta migración es un paso fundamental en la evolución del módulo de gestión de contenido de Shopify, permitiendo a los editores de contenido enriquecer las páginas de blog con descripciones detalladas que pueden ser utilizadas para SEO y para la presentación en el frontend de Shopify.

Al añadir el campo `description` al `BlogPage`, se habilita una característica clave para la optimización de motores de búsqueda y la mejora de la visibilidad del contenido del blog. La integración con los metafields de Shopify (`metafield descriptors.description`) asegura que esta información sea coherente y esté disponible en la plataforma Shopify, uniendo la gestión de contenido de Wagtail con las capacidades de e-commerce de Shopify.

Esta migración forma parte de las [Migraciones de Base de Datos](../Database_Migrations.md) del módulo [Gestión de Contenido de Shopify](../../Shopify_Content_Management.md).
