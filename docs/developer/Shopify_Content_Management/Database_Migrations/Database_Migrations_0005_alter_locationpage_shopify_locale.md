# Migración de Base de Datos 0005: Alterar shopify_locale de LocationPage

Esta documentación describe la migración de base de datos `0005_alter_locationpage_shopify_locale.py`, que forma parte del módulo `Shopify_Content_Management/Database_Migrations`.

## Propósito y Funcionalidad del Módulo

El propósito principal de esta migración es modificar el campo `shopify_locale` del modelo `LocationPage`. Esta modificación ajusta las opciones (`choices`) disponibles para este campo, así como su texto de ayuda (`help_text`), `max_length`, `blank` y `verbose_name`, para reflejar un conjunto específico de configuraciones regionales de Shopify.

### Cambios Específicos

La migración realiza la siguiente operación:

```python
migrations.AlterField(
    model_name='locationpage',
    name='shopify_locale',
    field=models.CharField(blank=True, choices=[
        ('en-US', 'English (United States)'),
        ('es-US', 'Spanish (United States)'),
        ('en-CA', 'English (Canada)'),
        ('fr-CA', 'French (Canada)')
    ], help_text='Shopify locale code pushed to the locale field (e.g. "es", "en-CA").', max_length=20, verbose_name='Shopify Locale'),
)
```

Esto asegura que el campo `shopify_locale` de la página de ubicación solo pueda contener uno de los códigos de configuración regional predefinidos, lo que es crucial para la gestión de contenido localizado dentro del sistema Shopify.

## Arquitectura y Relaciones entre Componentes

Esta migración es un paso secuencial en la evolución del esquema de la base de datos para el módulo de gestión de contenido de Shopify. Su dependencia directa es la migración `0004_add_location_page`, que es donde se introdujo inicialmente el modelo `LocationPage`.

### Relación con el Modelo `LocationPage`

El componente principal afectado por esta migración es el modelo `LocationPage`, definido en [Content_Page_Models_Location_Pages.md](../../Content_Page_Models/Content_Page_Models_Location_Pages.md). Esta migración refina la definición de uno de sus campos críticos para la localización.

### Diagrama de la Modificación del Esquema

El siguiente diagrama ilustra la modificación del campo `shopify_locale` en la tabla `locationpage`:

```mermaid
erDiagram
    LocationPage {
        ...
        CharField shopify_locale "Shopify Locale (en-US, es-US, en-CA, fr-CA)"
        ...
    }
```

## Encaje en el Sistema General

Esta migración juega un papel fundamental en el subsistema de gestión de contenido localizado. Al estandarizar los códigos de `shopify_locale` para las páginas de ubicación, garantiza la coherencia de los datos y facilita la integración con las capacidades de localización de la plataforma Shopify. Es esencial para cualquier funcionalidad que dependa de la visualización o gestión de contenido específico de una región o idioma para las ubicaciones.