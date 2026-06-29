METAOBJECT_BY_HANDLE = """
query getMetaobject($handle: String!, $type: String!) {
    metaobjectByHandle(handle: {type: $type, handle: $handle}) {
        id
        handle
        type
        fields {
            key
            value
        }
    }
}
"""

METAOBJECT_DEFINITION_BY_TYPE = """
query getMetaobjectDefinitionByType($type: String!) {
    metaobjectDefinitionByType(type: $type) {
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
}
"""
