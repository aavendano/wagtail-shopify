METAOBJECT_UPDATE = """
mutation UpdateMetaobject($id: ID!, $metaobject: MetaobjectUpdateInput!) {
    metaobjectUpdate(id: $id, metaobject: $metaobject) {
        metaobject {
            id
            handle
            type
            fields {
                key
                value
            }
        }
        userErrors {
            field
            message
            code
        }
    }
}
"""

METAOBJECT_UPSERT = """
mutation UpsertMetaobject($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
    metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
        metaobject {
            id
            handle
            type
            fields {
                key
                value
            }
        }
        userErrors {
            field
            message
            code
        }
    }
}
"""

METAOBJECT_DEFINITION_UPDATE = """
mutation updateMetaobjectDefinition($id: ID!, $definition: MetaobjectDefinitionUpdateInput!) {
    metaobjectDefinitionUpdate(id: $id, definition: $definition) {
        metaobjectDefinition {
            id
            type
            name
            description
            fieldDefinitions {
                key
                name
                required
                type {
                    name
                }
                validations {
                    name
                    value
                }
            }
        }
        userErrors {
            field
            message
            code
        }
    }
}
"""

METAOBJECT_DEFINITION_CREATE = """
mutation createMetaobjectDefinition($definition: MetaobjectDefinitionCreateInput!) {
    metaobjectDefinitionCreate(definition: $definition) {
        metaobjectDefinition {
            type
            name
            description
            fieldDefinitions {
                key
                name
                required
                type {
                    name
                }
                validations {
                    name
                    value
                }
            }
        }
        userErrors {
            field
            message
            code
        }
    }
}
"""
