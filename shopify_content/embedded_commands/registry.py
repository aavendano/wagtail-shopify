"""
Allowlist of management commands exposed from the Shopify embedded app home.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EmbeddedCommandSpec:
    id: str
    command: str
    label: str
    description: str
    group: str
    when_to_use: str = ''
    kwargs: dict[str, Any] = field(default_factory=dict)
    dangerous: bool = False


COMMAND_GROUPS: dict[str, str] = {
    'setup': 'Configuración inicial',
    'indexes': 'Índices y búsqueda',
    'semantic': 'Enlaces semánticos',
    'migrations': 'Migraciones y reparación',
}

EMBEDDED_COMMANDS: tuple[EmbeddedCommandSpec, ...] = (
    EmbeddedCommandSpec(
        id='setup_locales',
        command='setup_locales',
        label='Configurar locales',
        description='Crea los objetos Wagtail Locale (en-US, es-US, en-CA, fr-CA) necesarios para el contenido multi-idioma y las etiquetas hreflang.',
        group='setup',
        when_to_use='Una sola vez, justo después de instalar la app en una tienda nueva y correr las migraciones. Si Wagtail no muestra los idiomas esperados al crear páginas.',
    ),
    EmbeddedCommandSpec(
        id='setup_celery_beat_schedules',
        command='setup_celery_beat_schedules',
        label='Programar tareas Celery Beat',
        description='Crea o actualiza las tareas periódicas de sincronización (importación automática, índices). Quedan deshabilitadas por defecto; se activan desde Django Admin.',
        group='setup',
        when_to_use='Al preparar la sincronización automática por primera vez, o tras añadir nuevas tareas programadas que aún no aparecen en Django Admin → Periodic tasks.',
    ),
    EmbeddedCommandSpec(
        id='ensure_metaobject_definitions',
        command='ensure_metaobject_definitions',
        label='Verificar metaobjetos',
        description='Crea o verifica las definiciones de metaobjetos propias del merchant en Shopify (local_page, root_page, glossary_term).',
        group='setup',
        when_to_use='Tras instalar la app en una tienda nueva, o si una definición de metaobjeto se borró en Shopify Admin y el sync de páginas empieza a fallar.',
    ),
    EmbeddedCommandSpec(
        id='bootstrap_index_pages',
        command='bootstrap_index_pages',
        label='Crear páginas índice',
        description='Crea las Shopify Pages de glossary, locations y blog, y muestra el JSON de export_config resultante (sin escribir nada en Wagtail).',
        group='setup',
        when_to_use='Para previsualizar los GIDs antes de aplicarlos. Úsalo primero si quieres revisar el export_config antes de guardarlo con la variante "Aplicar".',
    ),
    EmbeddedCommandSpec(
        id='bootstrap_index_pages_apply',
        command='bootstrap_index_pages',
        label='Aplicar export_config de índices',
        description='Crea las páginas índice y guarda los GIDs generados en export_config de los ShopifyRootPage de Wagtail.',
        group='setup',
        when_to_use='Al configurar los índices por primera vez, cuando ya validaste la salida de "Crear páginas índice" y quieres persistir la configuración.',
        kwargs={'apply_export_config': True},
    ),
    EmbeddedCommandSpec(
        id='ensure_page_metafield_definitions',
        command='ensure_page_metafield_definitions',
        label='Metafields de página',
        description='Crea o verifica las metafield definitions de tipo PAGE que usa el sync de índices.',
        group='setup',
        when_to_use='Durante el setup inicial, o si el push de índices falla con errores de metafield definition inexistente en recursos PAGE.',
    ),
    EmbeddedCommandSpec(
        id='ensure_index_metafield_definitions',
        command='ensure_index_metafield_definitions',
        label='Metafields de índices',
        description='Asegura la definición custom.index_listings (PAGE) y available_locales en los recursos BLOG y ARTICLE.',
        group='setup',
        when_to_use='Antes del primer rebuild de índices, o si el storefront no recibe el listado custom.index_listings de glossary/locations.',
    ),
    EmbeddedCommandSpec(
        id='ensure_blog_metafield_definitions',
        command='ensure_blog_metafield_definitions',
        label='Metafields de blog',
        description='Crea las metafield definitions para listados de blog (PAGE) y available_locales en BLOG y ARTICLE.',
        group='setup',
        when_to_use='Al configurar el índice de blog por primera vez, o si "Reconstruir índice blog" falla por definiciones ausentes.',
    ),
    EmbeddedCommandSpec(
        id='rebuild_glossary_index',
        command='rebuild_glossary_index',
        label='Reconstruir índice glossary',
        description='Reconstruye y empuja custom.index_listings a la Shopify Page índice de glossary.',
        group='indexes',
        when_to_use='Tras crear, editar o despublicar términos del glosario cuando el listado del storefront quedó desactualizado.',
    ),
    EmbeddedCommandSpec(
        id='rebuild_location_index',
        command='rebuild_location_index',
        label='Reconstruir índice locations',
        description='Reconstruye y empuja custom.index_listings a la Shopify Page índice de locations.',
        group='indexes',
        when_to_use='Después de añadir o modificar ubicaciones cuando el listado de locations del storefront no refleja los cambios.',
    ),
    EmbeddedCommandSpec(
        id='rebuild_blog_index',
        command='rebuild_blog_index',
        label='Reconstruir índice blog',
        description='Reconstruye y empuja custom.index_listings a la Shopify Page con handle "blogs".',
        group='indexes',
        when_to_use='Tras publicar o editar artículos cuando el índice de blog del storefront quedó obsoleto.',
    ),
    EmbeddedCommandSpec(
        id='index_pages_batch',
        command='index_pages_batch',
        label='Indexar páginas (lotes)',
        description='Actualiza el PageIndex vectorial por lotes (memory-safe) y encola el backfill de enlaces semánticos al terminar.',
        group='indexes',
        when_to_use='Para (re)construir la búsqueda vectorial tras una importación masiva, o cuando los enlaces semánticos automáticos no encuentran páginas relacionadas. Puede tardar en catálogos grandes.',
        kwargs={'model': 'all'},
    ),
    EmbeddedCommandSpec(
        id='refresh_semantic_links_batch',
        command='refresh_semantic_links_batch',
        label='Generar enlaces semánticos',
        description='Genera enlaces internos automáticos entre páginas publicadas (solo las que aún no tienen enlaces).',
        group='semantic',
        when_to_use='Tras indexar contenido nuevo, para poblar enlaces internos en páginas que todavía no los tienen. No sobrescribe enlaces existentes.',
        kwargs={'model': 'all', 'only_missing': True},
    ),
    EmbeddedCommandSpec(
        id='sync_semantic_links_revisions',
        command='sync_semantic_links_revisions',
        label='Sincronizar revisiones de enlaces',
        description='Publica revisiones Wagtail para páginas que ya tienen filas de enlaces tipados en la BD pero no se ven en el admin.',
        group='semantic',
        when_to_use='Después de "Generar enlaces semánticos" si los enlaces existen en la base de datos pero no aparecen en el editor de Wagtail.',
        kwargs={'model': 'all'},
    ),
    EmbeddedCommandSpec(
        id='backfill_shopify_native_references',
        command='backfill_shopify_native_references',
        label='Empujar referencias nativas',
        description='Encola sync outbound de las páginas con enlaces tipados para empujar los metafields list.*_reference nativos a Shopify.',
        group='semantic',
        when_to_use='Cuando ya generaste enlaces semánticos y quieres que Shopify reciba las referencias nativas (metaobjetos/productos relacionados) en sus metafields.',
        kwargs={'model': 'all'},
    ),
    EmbeddedCommandSpec(
        id='migrate_glossary_locales',
        command='migrate_glossary_locales',
        label='Migrar locales glossary',
        description='Asigna el Locale de Wagtail a los GlossaryTermPage a partir de su locale_code (en→en-US, etc.).',
        group='migrations',
        when_to_use='Migración puntual, solo si tienes términos de glosario antiguos con locale_code pero sin Locale de Wagtail asignado.',
        dangerous=True,
    ),
    EmbeddedCommandSpec(
        id='migrate_glossary_links_to_fk',
        command='migrate_glossary_links_to_fk',
        label='Migrar enlaces glossary a FK',
        description='Migra las entradas JSON de related_links de los términos del glosario a filas FK tipadas.',
        group='migrations',
        when_to_use='Migración de una sola vez al adoptar el modelo de enlaces tipados, si tienes datos legacy de related_links en formato JSON.',
        dangerous=True,
    ),
    EmbeddedCommandSpec(
        id='migrate_index_export_config',
        command='migrate_index_export_config',
        label='Migrar export_config índices',
        description='Migra el export_config de glossary/locations del formato multi-página pages{} al nuevo page_gid único.',
        group='migrations',
        when_to_use='Migración puntual al pasar a la arquitectura de página índice única. No es necesario en instalaciones nuevas.',
        kwargs={'apply': True},
        dangerous=True,
    ),
    EmbeddedCommandSpec(
        id='fix_location_richtext',
        command='fix_location_richtext',
        label='Reparar RichText locations',
        description='Repara HTML malformado en los RichTextField de LocationPage que provoca errores de renderizado o sync.',
        group='migrations',
        when_to_use='Solo cuando una LocationPage falla al guardarse o sincronizarse por HTML corrupto en su contenido enriquecido.',
        dangerous=True,
    ),
)

# Import commands are exposed via EmbeddedShopifySyncView (products/collections/blogs/all).
IMPORT_COMMAND_NAMES = frozenset({
    'import_shopify_products',
    'import_shopify_collections',
    'import_shopify_blogs',
    'import_shopify_glossary',
})

ALL_MANAGEMENT_COMMAND_NAMES = frozenset(
    {spec.command for spec in EMBEDDED_COMMANDS} | IMPORT_COMMAND_NAMES
)

_COMMAND_BY_ID = {spec.id: spec for spec in EMBEDDED_COMMANDS}


def get_command_by_id(command_id: str) -> EmbeddedCommandSpec | None:
    return _COMMAND_BY_ID.get(command_id)


def get_commands_by_group() -> list[tuple[str, str, list[EmbeddedCommandSpec]]]:
    grouped: dict[str, list[EmbeddedCommandSpec]] = {key: [] for key in COMMAND_GROUPS}
    for spec in EMBEDDED_COMMANDS:
        grouped[spec.group].append(spec)
    return [
        (group_key, COMMAND_GROUPS[group_key], grouped[group_key])
        for group_key in COMMAND_GROUPS
        if grouped[group_key]
    ]
