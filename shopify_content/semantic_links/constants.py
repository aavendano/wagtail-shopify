"""Constants for typed semantic internal links."""

SEMANTIC_LINK_RELATION_NAMES = (
    'related_products',
    'related_collections',
    'related_articles',
    'related_glossary_terms',
)

TYPE_TO_RELATION = {
    'product': 'related_products',
    'collection': 'related_collections',
    'article': 'related_articles',
    'glossary': 'related_glossary_terms',
}

RELATION_TO_TYPE = {value: key for key, value in TYPE_TO_RELATION.items()}

RELATION_CONFIG = {
    'related_products': {
        'type_key': 'product',
        'target_model_label': 'shopify_content.ProductPage',
        'heading': 'Related products',
        'label': 'Product',
        'type_suffix': 'Product',
    },
    'related_collections': {
        'type_key': 'collection',
        'target_model_label': 'shopify_content.CollectionPage',
        'heading': 'Related collections',
        'label': 'Collection',
        'type_suffix': 'Collection',
    },
    'related_articles': {
        'type_key': 'article',
        'target_model_label': 'shopify_content.ArticlePage',
        'heading': 'Related articles',
        'label': 'Article',
        'type_suffix': 'Article',
    },
    'related_glossary_terms': {
        'type_key': 'glossary',
        'target_model_label': 'shopify_content.GlossaryTermPage',
        'heading': 'Related glossary terms',
        'label': 'Glossary term',
        'type_suffix': 'GlossaryTerm',
    },
}

PARENT_PAGE_CONFIG = (
    ('ArticlePage', 'shopify_content.ArticlePage', 'Article'),
    ('ProductPage', 'shopify_content.ProductPage', 'Product'),
    ('CollectionPage', 'shopify_content.CollectionPage', 'Collection'),
    ('GlossaryTermPage', 'shopify_content.GlossaryTermPage', 'GlossaryTerm'),
)

LEGACY_SEMANTIC_LINK_MODEL_NAMES = (
    'ArticleSemanticLink',
    'ProductSemanticLink',
    'CollectionSemanticLink',
    'GlossarySemanticLink',
)

NATIVE_REFERENCE_RELATION_NAMES = (
    'related_products',
    'related_collections',
    'related_glossary_terms',
)

NATIVE_REFERENCE_CONFIG = {
    'related_products': {
        'shopify_type': 'list.product_reference',
        'metafield_key': 'related_products',
        'metaobject_field_key': 'related_products',
    },
    'related_collections': {
        'shopify_type': 'list.collection_reference',
        'metafield_key': 'related_collections',
        'metaobject_field_key': 'related_collections',
    },
    'related_glossary_terms': {
        'shopify_type': 'list.metaobject_reference',
        'metafield_key': 'related_glossary_terms',
        'metaobject_field_key': 'related_glossary_terms',
        'metaobject_definition_type': 'glossary_term',
    },
}
