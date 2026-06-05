from ..graphql_service import AdminGraphqlResult, execute_admin_graphql

_SHOP_ID_QUERY = """
{
  shop {
    id
  }
}
"""


def fetch_shop_admin_graphql(
    shop,
    *,
    verification_result=None,
    invalid_token_response=None,
    shopify_app=None,
) -> AdminGraphqlResult:
    return execute_admin_graphql(
        _SHOP_ID_QUERY,
        shop=shop,
        verification_result=verification_result,
        invalid_token_response=invalid_token_response,
        shopify_app=shopify_app,
    )
