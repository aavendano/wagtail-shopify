"""
Shared Shopify Admin GraphQL integration.

Public entry points for the rest of the project. Do not call
``ShopifyApp.admin_graphql_request`` outside ``shopify_requests.graphql_client``.
"""

from .domains.shop import fetch_shop_admin_graphql
from .graphql_service import AdminGraphqlResult, execute_admin_graphql

__all__ = [
    "AdminGraphqlResult",
    "execute_admin_graphql",
    "fetch_shop_admin_graphql",
]
