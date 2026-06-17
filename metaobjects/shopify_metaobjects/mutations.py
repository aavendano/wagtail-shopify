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
            metafields(first: 250) {
                edges {
                    node {
                        id
                        key
                        value
                        type
                        namespace
                    }
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
            displayNameField
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
