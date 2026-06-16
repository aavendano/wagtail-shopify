class MetaobjectError(Exception):
    """Base error for metaobject operations."""


class DefinitionError(MetaobjectError):
    """Raised when a metaobject definition operation fails."""

    def __init__(self, message, *, error_code=None, user_errors=None):
        super().__init__(message)
        self.error_code = error_code
        self.user_errors = user_errors or []


class UpsertError(MetaobjectError):
    """Raised when a metaobject upsert operation fails."""

    def __init__(self, message, *, error_code=None, user_errors=None):
        super().__init__(message)
        self.error_code = error_code
        self.user_errors = user_errors or []
