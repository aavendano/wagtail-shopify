# Shopify API request/response utilities
# To be populated with API call logic

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .utils import ShopifyRateLimitError, ShopifyAPIError, ShopifyUserError

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((ShopifyRateLimitError, requests.RequestException))
)
def make_graphql_request(base_url, headers, query, variables):
    """
    Make a GraphQL request to the Shopify API with retry logic.
    """
    try:
        response = requests.post(
            base_url,
            json={"query": query, "variables": variables},
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        if response.status_code == 429:
            raise ShopifyRateLimitError("Shopify API rate limit exceeded")
        if "errors" in data:
            raise ShopifyAPIError(f"GraphQL errors: {data['errors']}")
        return data.get("data", {})
    except requests.RequestException as e:
        raise
