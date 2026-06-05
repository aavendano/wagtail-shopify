
import pandas as pd
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from datetime import datetime
import json
from pathlib import Path
from .metaobject import Metaobject
from .utils import (
    ShopifyAPIError, ShopifyRateLimitError, ShopifyUserError,
    MetaobjectFieldDefinition, MetaobjectDefinition
)
from .api import make_graphql_request

class ShopifyMetaobjectLoader:
    """
    A class to handle loading data from CSV files into Shopify metaobjects.
    This class manages the entire process of reading CSV data and upserting it into
    Shopify metaobjects using the GraphQL API. It handles both creation and updates
    of metaobjects based on a unique handle field.
    Attributes:
        shop_domain (str): The Shopify store domain
        access_token (str): The Shopify Admin API access token
        api_version (str): The Shopify API version to use
        headers (Dict[str, str]): Headers for API requests
        base_url (str): Base URL for Shopify GraphQL API
        cache_dir (Path): Directory for caching API responses
    """
    def __init__(
        self,
        shop_domain: str,
        access_token: str,
        api_version: str = "2025-04",
        cache_dir: str = None
    ) -> None:
        self.shop_domain = shop_domain
        self.access_token = access_token
        self.api_version = api_version
        self.headers = {
            'X-Shopify-Access-Token': self.access_token,
            'Content-Type': 'application/json',
        }
        self.base_url = f"https://{self.shop_domain}/admin/api/{self.api_version}/graphql.json"
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

