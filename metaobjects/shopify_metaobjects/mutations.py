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
