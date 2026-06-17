METAOBJECT_BY_HANDLE = """
query getMetaobject($handle: String!, $type: String!) {
    metaobject(handle: $handle, type: $type) {
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
}
"""

METAOBJECT_DEFINITION_BY_TYPE = """
query getMetaobjectDefinitionByType($type: String!) {
    metaobjectDefinition(type: $type) {
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
}
"""
