"""Shopify Metaobjects: modular client for definitions and instances."""

from .client import MetaobjectClient
from .definition import MetaobjectDefinitionSpec, MetaobjectFieldSpec
from .exceptions import DefinitionError, MetaobjectError, UpsertError
from .metaobject import Metaobject

__all__ = [
    "DefinitionError",
    "Metaobject",
    "MetaobjectClient",
    "MetaobjectDefinitionSpec",
    "MetaobjectFieldSpec",
    "MetaobjectError",
    "UpsertError",
]
