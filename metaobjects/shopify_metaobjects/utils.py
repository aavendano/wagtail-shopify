from typing import TypedDict, Optional, List, Dict, Any

# General utilities: caching, logging, etc.
# To be populated with utility functions

class ShopifyAPIError(Exception):
    pass

class ShopifyRateLimitError(ShopifyAPIError):
    pass

class ShopifyUserError(ShopifyAPIError):
    pass

class MetaobjectFieldDefinition(TypedDict):
    key: str
    name: str
    type: str
    description: Optional[str]
    required: bool
    validations: List[Dict[str, Any]]

class MetaobjectDefinition(TypedDict):
    type: str
    name: str
    description: Optional[str]
    fields: List[MetaobjectFieldDefinition]
