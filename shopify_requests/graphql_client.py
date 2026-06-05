from core.utils import log_shopify_result


def raw_admin_graphql(
    shopify_app,
    query,
    *,
    shop,
    access_token,
    api_version,
    variables=None,
    headers=None,
    max_retries=None,
    invalid_token_response=None,
):
    """
    Low-level Admin GraphQL call. This module is the only place that invokes
    ShopifyApp.admin_graphql_request.
    """
    kwargs = {
        "shop": shop,
        "access_token": access_token,
        "api_version": api_version,
        "invalid_token_response": invalid_token_response,
    }
    if variables is not None:
        kwargs["variables"] = variables
    if headers is not None:
        kwargs["headers"] = headers
    if max_retries is not None:
        kwargs["max_retries"] = max_retries

    result = shopify_app.admin_graphql_request(query, **kwargs)
    log_shopify_result(result)
    return result
