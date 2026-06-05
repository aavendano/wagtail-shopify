"""
Shopify Metaobject Loader Module

This module provides functionality to load data from CSV files into Shopify metaobjects
using the Shopify Admin GraphQL API. It handles both creation and updates of metaobjects
based on a unique handle field.

Dependencies:
    - pandas: For CSV parsing
    - requests: For HTTP requests to Shopify API
    - python-dotenv: For environment variable management
    - typing: For type hints
    - logging: For logging functionality
    - tenacity: For retry logic
"""

import os
import logging
from typing import Dict, List, Optional, Any, TypedDict, Union, Iterator
import pandas as pd
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from datetime import datetime
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ShopifyAPIError(Exception):
    """Base exception for Shopify API errors."""
    pass

class ShopifyRateLimitError(ShopifyAPIError):
    """Exception raised when Shopify API rate limit is exceeded."""
    pass

class ShopifyUserError(ShopifyAPIError):
    """Exception raised when Shopify API returns user errors."""
    pass

class MetaobjectFieldDefinition(TypedDict):
    """Type definition for metaobject field definitions."""
    key: str
    name: str
    type: str
    description: Optional[str]
    required: bool
    validations: List[Dict[str, Any]]

class MetaobjectDefinition(TypedDict):
    """Type definition for metaobject definitions."""
    type: str
    name: str
    description: Optional[str]
    fields: List[MetaobjectFieldDefinition]

class Metaobject:
    """
    A class representing a Shopify metaobject.
    
    This class provides a convenient interface for working with Shopify metaobjects,
    including accessing fields, adding/modifying metafields, and managing the metaobject's
    lifecycle.
    
    Attributes:
        id (str): The unique identifier of the metaobject
        handle (str): The handle of the metaobject
        type (str): The type of the metaobject
        fields (Dict[str, Any]): Dictionary of field key-value pairs
        metafields (Dict[str, Dict[str, Any]]): Dictionary of metafields by key
    """
    
    def __init__(
        self,
        type: str,
        handle: str,
        id: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None,
        metafields: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        """
        Initialize a Metaobject instance.
        
        Args:
            type: The type of the metaobject
            handle: The handle of the metaobject
            id: Optional ID of the metaobject
            fields: Optional dictionary of field key-value pairs
            metafields: Optional dictionary of metafields by key
        """
        self.type = type
        self.handle = handle
        self.id = id
        self.fields = fields or {}
        self.metafields = metafields or {}
        
    @classmethod
    def from_shopify_data(cls, data: Dict[str, Any]) -> 'Metaobject':
        """
        Create a Metaobject instance from Shopify API response data.
        
        Args:
            data: Dictionary containing metaobject data from Shopify API
            
        Returns:
            Metaobject: A new Metaobject instance
        """
        fields = {
            field["key"]: field["value"]
            for field in data.get("fields", [])
        }
        
        metafields = {
            metafield["key"]: metafield
            for metafield in data.get("metafields", {}).get("edges", [])
        }
        
        return cls(
            type=data.get("type"),
            handle=data.get("handle"),
            id=data.get("id"),
            fields=fields,
            metafields=metafields
        )
        
    def to_shopify_fields(self) -> List[Dict[str, str]]:
        """
        Convert the metaobject's fields to Shopify API format.
        
        Returns:
            List[Dict[str, str]]: List of field objects in Shopify format
        """
        return [
            {"key": key, "value": str(value)}
            for key, value in self.fields.items()
        ]
        
    def get_field(self, key: str) -> Optional[Any]:
        """
        Get the value of a field by key.
        
        Args:
            key: The key of the field to get
            
        Returns:
            Optional[Any]: The value of the field, or None if not found
        """
        return self.fields.get(key)
        
    def set_field(self, key: str, value: Any) -> None:
        """
        Set the value of a field.
        
        Args:
            key: The key of the field to set
            value: The value to set
        """
        self.fields[key] = value
        
    def get_metafield(self, key: str, namespace: str = "custom") -> Optional[Dict[str, Any]]:
        """
        Get a metafield by key and namespace.
        
        Args:
            key: The key of the metafield
            namespace: The namespace of the metafield (default: "custom")
            
        Returns:
            Optional[Dict[str, Any]]: The metafield data, or None if not found
        """
        return self.metafields.get(f"{namespace}.{key}")
        
    def set_metafield(
        self,
        key: str,
        value: str,
        type: str = "single_line_text_field",
        namespace: str = "custom"
    ) -> None:
        """
        Set a metafield value.
        
        Args:
            key: The key of the metafield
            value: The value to set
            type: The type of the metafield (default: "single_line_text_field")
            namespace: The namespace of the metafield (default: "custom")
        """
        self.metafields[f"{namespace}.{key}"] = {
            "key": key,
            "value": value,
            "type": type,
            "namespace": namespace
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the metaobject to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the metaobject
        """
        return {
            "id": self.id,
            "handle": self.handle,
            "type": self.type,
            "fields": self.fields,
            "metafields": self.metafields
        }
        
    def __str__(self) -> str:
        """Return a string representation of the metaobject."""
        return f"Metaobject(type={self.type}, handle={self.handle}, id={self.id})"
        
    def __repr__(self) -> str:
        """Return a detailed string representation of the metaobject."""
        return (
            f"Metaobject(\n"
            f"    type='{self.type}',\n"
            f"    handle='{self.handle}',\n"
            f"    id='{self.id}',\n"
            f"    fields={self.fields},\n"
            f"    metafields={self.metafields}\n"
            f")"
        )

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
        cache_dir: Optional[str] = None
    ) -> None:
        """
        Initialize the ShopifyMetaobjectLoader.
        
        Args:
            shop_domain: The Shopify store domain (e.g., 'your-store.myshopify.com')
            access_token: The Shopify Admin API access token
            api_version: The Shopify API version to use (default: "2025-04")
            cache_dir: Optional directory for caching API responses
        """
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
            
    def _get_cache_path(self, key: str) -> Path:
        """Get the cache file path for a given key."""
        if not self.cache_dir:
            raise ValueError("Cache directory not set")
        return self.cache_dir / f"{key}.json"
        
    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Get data from cache if available and not expired."""
        if not self.cache_dir:
            return None
            
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None
            
        try:
            with cache_path.open() as f:
                data = json.load(f)
                if datetime.fromisoformat(data["timestamp"]) < datetime.now():
                    return data["data"]
        except Exception as e:
            logger.warning(f"Error reading cache: {e}")
            
        return None
        
    def _save_to_cache(self, key: str, data: Dict[str, Any], ttl_seconds: int = 3600) -> None:
        """Save data to cache with expiration."""
        if not self.cache_dir:
            return
            
        cache_path = self._get_cache_path(key)
        try:
            with cache_path.open("w") as f:
                json.dump({
                    "timestamp": (datetime.now() + pd.Timedelta(seconds=ttl_seconds)).isoformat(),
                    "data": data
                }, f)
        except Exception as e:
            logger.warning(f"Error writing to cache: {e}")
            
    def batch_upsert_metaobjects(
        self,
        metaobjects: List[Metaobject],
        batch_size: int = 50
    ) -> Dict[str, int]:
        """
        Upsert multiple metaobjects in batches.
        
        Args:
            metaobjects: List of Metaobject instances to upsert
            batch_size: Number of metaobjects to process in each batch
            
        Returns:
            Dict[str, int]: Statistics about the operation
        """
        stats = {"upserted": 0, "failed": 0}
        
        for i in range(0, len(metaobjects), batch_size):
            batch = metaobjects[i:i + batch_size]
            for metaobject in batch:
                try:
                    result = self._upsert_metaobject(metaobject)
                    if result:
                        stats["upserted"] += 1
                        logger.info(f"Upserted metaobject: {metaobject.handle}")
                    else:
                        stats["failed"] += 1
                        logger.error(f"Failed to upsert metaobject: {metaobject.handle}")
                except ShopifyAPIError as e:
                    stats["failed"] += 1
                    logger.error(f"Error processing metaobject {metaobject.handle}: {str(e)}")
                    
        return stats
        
    def export_metaobjects_to_csv(
        self,
        metaobject_type: str,
        output_file: str,
        include_metafields: bool = False
    ) -> None:
        """
        Export metaobjects of a specific type to a CSV file.
        
        Args:
            metaobject_type: The type of metaobjects to export
            output_file: Path to the output CSV file
            include_metafields: Whether to include metafields in the export
        """
        metaobjects = self.fetch_all_metaobjects(metaobject_type)
        if not metaobjects:
            logger.warning(f"No metaobjects found of type: {metaobject_type}")
            return
            
        # Convert metaobjects to DataFrame
        rows = []
        for metaobject in metaobjects:
            row = {
                "handle": metaobject.handle,
                "id": metaobject.id,
                **metaobject.fields
            }
            
            if include_metafields:
                for key, metafield in metaobject.metafields.items():
                    row[f"metafield_{key}"] = metafield["value"]
                    
            rows.append(row)
            
        df = pd.DataFrame(rows)
        df.to_csv(output_file, index=False)
        logger.info(f"Exported {len(rows)} metaobjects to {output_file}")
        
    def validate_metaobject_definition(
        self,
        metaobject: Metaobject,
        definition: MetaobjectDefinition
    ) -> List[str]:
        """
        Validate a metaobject against its definition.
        
        Args:
            metaobject: The Metaobject instance to validate
            definition: The MetaobjectDefinition to validate against
            
        Returns:
            List[str]: List of validation errors, empty if valid
        """
        errors = []
        
        # Check required fields
        for field in definition["fields"]:
            if field["required"] and field["key"] not in metaobject.fields:
                errors.append(f"Missing required field: {field['key']}")
                
        # Check field types
        for field in definition["fields"]:
            if field["key"] in metaobject.fields:
                value = metaobject.fields[field["key"]]
                if not self._validate_field_type(value, field["type"]):
                    errors.append(
                        f"Invalid type for field {field['key']}: "
                        f"expected {field['type']}, got {type(value).__name__}"
                    )
                    
        # Check validations
        for field in definition["fields"]:
            if field["key"] in metaobject.fields:
                value = metaobject.fields[field["key"]]
                for validation in field["validations"]:
                    if not self._validate_field_value(value, validation):
                        errors.append(
                            f"Validation failed for field {field['key']}: "
                            f"{validation['name']} = {validation['value']}"
                        )
                        
        return errors
        
    def _validate_field_type(self, value: Any, expected_type: str) -> bool:
        """Validate a field value against its expected type."""
        type_map = {
            "single_line_text_field": str,
            "multi_line_text_field": str,
            "number_integer": int,
            "number_decimal": (int, float),
            "boolean": bool,
            "date": str,
            "date_time": str,
            "json": (dict, list),
            "color": str,
            "rating": (int, float),
            "dimension": (int, float),
            "volume": (int, float),
            "weight": (int, float)
        }
        
        expected = type_map.get(expected_type)
        if not expected:
            return True  # Unknown type, skip validation
            
        return isinstance(value, expected)
        
    def _validate_field_value(self, value: Any, validation: Dict[str, Any]) -> bool:
        """Validate a field value against a validation rule."""
        name = validation["name"]
        rule_value = validation["value"]
        
        if name == "min":
            return float(value) >= float(rule_value)
        elif name == "max":
            return float(value) <= float(rule_value)
        elif name == "pattern":
            import re
            return bool(re.match(rule_value, str(value)))
        elif name == "in":
            return value in rule_value.split(",")
            
        return True  # Unknown validation, skip
        
    def get_metaobject_stats(self, metaobject_type: str) -> Dict[str, Any]:
        """
        Get statistics about metaobjects of a specific type.
        
        Args:
            metaobject_type: The type of metaobjects to analyze
            
        Returns:
            Dict[str, Any]: Statistics about the metaobjects
        """
        metaobjects = self.fetch_all_metaobjects(metaobject_type)
        if not metaobjects:
            return {
                "total": 0,
                "fields": {},
                "metafields": {}
            }
            
        # Analyze fields
        field_stats = {}
        for metaobject in metaobjects:
            for key, value in metaobject.fields.items():
                if key not in field_stats:
                    field_stats[key] = {
                        "count": 0,
                        "types": set(),
                        "values": set()
                    }
                field_stats[key]["count"] += 1
                field_stats[key]["types"].add(type(value).__name__)
                field_stats[key]["values"].add(str(value))
                
        # Convert sets to lists for JSON serialization
        for stats in field_stats.values():
            stats["types"] = list(stats["types"])
            stats["values"] = list(stats["values"])
            
        return {
            "total": len(metaobjects),
            "fields": field_stats,
            "metafields": {
                "total": sum(len(m.metafields) for m in metaobjects),
                "per_object": {
                    "min": min(len(m.metafields) for m in metaobjects),
                    "max": max(len(m.metafields) for m in metaobjects),
                    "avg": sum(len(m.metafields) for m in metaobjects) / len(metaobjects)
                }
            }
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ShopifyRateLimitError, requests.RequestException))
    )
    def _make_request(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a GraphQL request to the Shopify API with retry logic.
        
        Args:
            query: The GraphQL query or mutation
            variables: The variables for the query
            
        Returns:
            Dict[str, Any]: The API response data
            
        Raises:
            ShopifyRateLimitError: If the API rate limit is exceeded
            ShopifyUserError: If the API returns user errors
            requests.RequestException: If the request fails
        """
        try:
            response = requests.post(
                self.base_url,
                json={"query": query, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            # Check for rate limiting
            if response.status_code == 429:
                raise ShopifyRateLimitError("Shopify API rate limit exceeded")
                
            # Check for GraphQL errors
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                raise ShopifyAPIError(f"GraphQL errors: {data['errors']}")
                
            # Check for user errors in mutations
            if "userErrors" in data.get("data", {}).get("metaobjectUpsert", {}):
                user_errors = data["data"]["metaobjectUpsert"]["userErrors"]
                if user_errors:
                    raise ShopifyUserError(f"User errors: {user_errors}")
                    
            return data.get("data", {})
            
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
            
    def _fetch_metaobject_by_handle(
        self,
        handle: str,
        metaobject_type: str
    ) -> Optional[Metaobject]:
        """
        Fetch an existing metaobject by its handle.
        
        Args:
            handle: The handle of the metaobject to fetch
            metaobject_type: The type of metaobject to fetch
            
        Returns:
            Optional[Metaobject]: The metaobject if found, None otherwise
            
        Raises:
            ShopifyAPIError: If the API request fails
        """
        query = """
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
        
        variables = {
            "handle": handle,
            "type": metaobject_type
        }
        
        try:
            data = self._make_request(query, variables)
            metaobject_data = data.get("metaobject")
            if metaobject_data:
                return Metaobject.from_shopify_data(metaobject_data)
            return None
            
        except ShopifyAPIError as e:
            logger.error(f"Failed to fetch metaobject: {str(e)}")
            raise
            
    def _upsert_metaobject(
        self,
        metaobject: Metaobject
    ) -> Optional[Metaobject]:
        """
        Create or update a metaobject in Shopify using the metaobjectUpsert mutation.
        
        Args:
            metaobject: The Metaobject instance to upsert
            
        Returns:
            Optional[Metaobject]: The upserted metaobject if successful
            
        Raises:
            ShopifyAPIError: If the API request fails
        """
        mutation = """
        mutation UpsertMetaobject($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
            metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
                metaobject {
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
                userErrors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        variables = {
            "handle": {
                "type": metaobject.type,
                "handle": metaobject.handle
            },
            "metaobject": {
                "fields": metaobject.to_shopify_fields()
            }
        }
        
        try:
            data = self._make_request(mutation, variables)
            result = data.get("metaobjectUpsert", {})
            metaobject_data = result.get("metaobject")
            if metaobject_data:
                return Metaobject.from_shopify_data(metaobject_data)
            return None
            
        except ShopifyAPIError as e:
            logger.error(f"Failed to upsert metaobject: {str(e)}")
            raise
            
    def process_csv(
        self,
        file_path: str,
        metaobject_type: str
    ) -> Dict[str, int]:
        """
        Process a CSV file and upsert its contents into Shopify metaobjects.
        
        Args:
            file_path: Path to the CSV file
            metaobject_type: The type of metaobject to create/update
            
        Returns:
            Dict[str, int]: Statistics about the operation (upserted, failed)
            
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            pd.errors.EmptyDataError: If the CSV file is empty
            ShopifyAPIError: If API requests fail
        """
        stats = {"upserted": 0, "failed": 0}
        
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            logger.error(f"CSV file not found: {file_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error(f"CSV file is empty: {file_path}")
            raise
            
        for _, row in df.iterrows():
            handle = row["handle"]
            fields = {
                column: str(row[column])
                for column in row.index
                if column != "handle"
            }
            
            metaobject = Metaobject(
                type=metaobject_type,
                handle=handle,
                fields=fields
            )
            
            try:
                result = self._upsert_metaobject(metaobject)
                if result:
                    stats["upserted"] += 1
                    logger.info(f"Upserted metaobject: {handle}")
                else:
                    stats["failed"] += 1
                    logger.error(f"Failed to upsert metaobject: {handle}")
                    
            except ShopifyAPIError as e:
                stats["failed"] += 1
                logger.error(f"Error processing row for handle {handle}: {str(e)}")
                continue
                
        return stats

    def fetch_metaobjects(
        self,
        metaobject_type: str,
        first: int = 250,
        after: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch metaobjects of a specific type from Shopify.
        
        Args:
            metaobject_type: The type of metaobjects to fetch
            first: Number of metaobjects to fetch per page (default: 250, max: 250)
            after: Cursor for pagination (default: None)
            
        Returns:
            Dict[str, Any]: Dictionary containing metaobjects and pagination info
            
        Raises:
            requests.RequestException: If the API request fails
        """
        query = """
        query getMetaobjects($type: String!, $first: Int!, $after: String) {
            metaobjects(type: $type, first: $first, after: $after) {
                edges {
                    node {
                        id
                        handle
                        fields {
                            key
                            value
                        }
                    }
                    cursor
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        """
        
        variables = {
            "type": metaobject_type,
            "first": min(first, 250),  # Ensure we don't exceed Shopify's limit
            "after": after
        }
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": query, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return {"metaobjects": [], "pageInfo": {"hasNextPage": False}}
                
            return data.get("data", {}).get("metaobjects", {})
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch metaobjects: {str(e)}")
            raise

    def fetch_all_metaobjects(
        self,
        metaobject_type: str,
        batch_size: int = 250
    ) -> List[Dict[str, Any]]:
        """
        Fetch all metaobjects of a specific type from Shopify using pagination.
        
        Args:
            metaobject_type: The type of metaobjects to fetch
            batch_size: Number of metaobjects to fetch per page (default: 250, max: 250)
            
        Returns:
            List[Dict[str, Any]]: List of all metaobjects
            
        Raises:
            requests.RequestException: If the API request fails
        """
        all_metaobjects = []
        has_next_page = True
        cursor = None
        
        while has_next_page:
            result = self.fetch_metaobjects(
                metaobject_type=metaobject_type,
                first=batch_size,
                after=cursor
            )
            
            # Extract metaobjects from edges
            metaobjects = [
                edge["node"] for edge in result.get("edges", [])
            ]
            all_metaobjects.extend(metaobjects)
            
            # Update pagination info
            page_info = result.get("pageInfo", {})
            has_next_page = page_info.get("hasNextPage", False)
            cursor = page_info.get("endCursor")
            
            if has_next_page and not cursor:
                logger.warning("Pagination cursor is missing but hasNextPage is true")
                break
                
        return all_metaobjects

    def fetch_metaobjects_as_dict(
        self,
        metaobject_type: str,
        key_field: str = "handle"
    ) -> Dict[str, Dict[str, Any]]:
        """
        Fetch all metaobjects of a specific type and return them as a dictionary
        indexed by the specified key field.
        
        Args:
            metaobject_type: The type of metaobjects to fetch
            key_field: The field to use as the dictionary key (default: "handle")
            
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of metaobjects indexed by key_field
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If key_field is not found in metaobject fields
        """
        metaobjects = self.fetch_all_metaobjects(metaobject_type)
        result = {}
        
        for metaobject in metaobjects:
            # Convert fields list to dictionary for easier access
            fields_dict = {
                field["key"]: field["value"]
                for field in metaobject.get("fields", [])
            }
            
            # Add handle and id to fields_dict for convenience
            fields_dict["handle"] = metaobject["handle"]
            fields_dict["id"] = metaobject["id"]
            
            # Get the key value
            key_value = fields_dict.get(key_field)
            if not key_value:
                raise ValueError(f"Key field '{key_field}' not found in metaobject fields")
                
            result[key_value] = fields_dict
            
        return result

    def fetch_metaobjects_to_csv(
        self,
        metaobject_type: str,
        output_file: str,
        include_id: bool = False,
        include_handle: bool = True,
        field_order: Optional[List[str]] = None
    ) -> None:
        """
        Fetch metaobjects of a specific type and save them to a CSV file.
        
        Args:
            metaobject_type: The type of metaobjects to fetch
            output_file: Path to the output CSV file
            include_id: Whether to include the metaobject ID in the CSV (default: False)
            include_handle: Whether to include the handle field in the CSV (default: True)
            field_order: Optional list of field names to specify the order of columns
            
        Raises:
            requests.RequestException: If the API request fails
            IOError: If there's an error writing the CSV file
        """
        try:
            # Fetch all metaobjects
            metaobjects = self.fetch_all_metaobjects(metaobject_type)
            
            if not metaobjects:
                logger.warning(f"No metaobjects found of type: {metaobject_type}")
                return
                
            # Convert metaobjects to a list of dictionaries
            rows = []
            all_fields = set()
            
            for metaobject in metaobjects:
                # Convert fields list to dictionary
                fields_dict = {
                    field["key"]: field["value"]
                    for field in metaobject.get("fields", [])
                }
                
                # Add handle and id if requested
                if include_handle:
                    fields_dict["handle"] = metaobject["handle"]
                if include_id:
                    fields_dict["id"] = metaobject["id"]
                    
                rows.append(fields_dict)
                all_fields.update(fields_dict.keys())
                
            # Convert to DataFrame
            df = pd.DataFrame(rows)
            
            # Reorder columns if field_order is specified
            if field_order:
                # Ensure all specified fields exist
                valid_fields = [f for f in field_order if f in df.columns]
                if len(valid_fields) != len(field_order):
                    missing_fields = set(field_order) - set(valid_fields)
                    logger.warning(f"Some specified fields were not found: {missing_fields}")
                
                # Add any missing columns from the data
                remaining_fields = [f for f in df.columns if f not in valid_fields]
                ordered_fields = valid_fields + remaining_fields
                
                df = df[ordered_fields]
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            logger.info(f"Successfully saved {len(rows)} metaobjects to {output_file}")
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch metaobjects: {str(e)}")
            raise
        except IOError as e:
            logger.error(f"Failed to write CSV file: {str(e)}")
            raise

    def fetch_metaobject_definition(
        self,
        metaobject_type: str
    ) -> Optional[MetaobjectDefinition]:
        """
        Fetch the definition of a metaobject type from Shopify.

        Args:
            metaobject_type: The type of the metaobject to fetch the definition for

        Returns:
            Optional[MetaobjectDefinition]: The metaobject definition if found

        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the metaobject type is not found
        """
        definition_query = """
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

        variables = {
            "type": metaobject_type
        }

        try:
            response = requests.post(
                self.base_url,
                json={"query": definition_query, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return None

            definition = data.get("data", {}).get("metaobjectDefinition")
            if not definition:
                logger.warning(f"Metaobject definition for type '{metaobject_type}' not found.")
                return None

            # Normalize the 'type' field inside fieldDefinitions
            for field in definition.get("fieldDefinitions", []):
                if 'type' in field and isinstance(field['type'], dict):
                    field['type'] = field['type']['name']

            return definition

        except requests.RequestException as e:
            logger.error(f"Failed to fetch metaobject definition: {str(e)}")
            raise

    def describe_metaobject_type(
        self,
        metaobject_type: str
    ) -> Dict[str, Any]:
        """
        Get a detailed description of a metaobject type, including its fields and validations.
        
        Args:
            metaobject_type: The type of metaobject to describe
            
        Returns:
            Dict[str, Any]: A dictionary containing the metaobject type description
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the metaobject type is not found
        """
        definition = self.fetch_metaobject_definition(metaobject_type)
        
        if not definition:
            raise ValueError(f"Metaobject type '{metaobject_type}' not found")
            
        # Count fields by type
        field_types = {}
        required_fields = []
        optional_fields = []
        
        for field in definition["fields"]:
            field_type = field["type"]
            field_types[field_type] = field_types.get(field_type, 0) + 1
            
            field_info = {
                "key": field["key"],
                "name": field["name"],
                "type": field["type"],
                "description": field.get("description", ""),
                "validations": field["validations"]
            }
            
            if field["required"]:
                required_fields.append(field_info)
            else:
                optional_fields.append(field_info)
               
        # Build the description
        description = {
            "type": definition["type"],
            "name": definition["name"],
            "description": definition.get("description", ""),
            "field_summary": {
                "total_fields": len(definition["fields"]),
                "field_types": field_types,
                "required_fields": len(required_fields),
                "optional_fields": len(optional_fields)
            },
            "fields": {
                "required": required_fields,
                "optional": optional_fields
            }
        }
        
        return description

    def print_metaobject_type_description(
        self,
        metaobject_type: str
    ) -> None:
        """
        Print a human-readable description of a metaobject type.
        
        Args:
            metaobject_type: The type of metaobject to describe
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the metaobject type is not found
        """
        try:
            description = self.describe_metaobject_type(metaobject_type)
            
            print(f"\nMetaobject Type: {description['name']} ({description['type']})")
            if description['description']:
                print(f"Description: {description['description']}")
                
            print("\nField Summary:")
            print(f"Total Fields: {description['field_summary']['total_fields']}")
            print(f"Required Fields: {description['field_summary']['required_fields']}")
            print(f"Optional Fields: {description['field_summary']['optional_fields']}")
            
            print("\nField Types:")
            for field_type, count in description['field_summary']['field_types'].items():
                print(f"- {field_type}: {count}")
                
            print("\nRequired Fields:")
            for field in description['fields']['required']:
                print(f"\n- {field['name']} ({field['key']})")
                print(f"  Type: {field['type']}")
                if field['description']:
                    print(f"  Description: {field['description']}")
                if field['validations']:
                    print("  Validations:")
                    for validation in field['validations']:
                        print(f"    - {validation['name']}: {validation['value']}")
                        
            print("\nOptional Fields:")
            for field in description['fields']['optional']:
                print(f"\n- {field['name']} ({field['key']})")
                print(f"  Type: {field['type']}")
                if field['description']:
                    print(f"  Description: {field['description']}")
                if field['validations']:
                    print("  Validations:")
                    for validation in field['validations']:
                        print(f"    - {validation['name']}: {validation['value']}")
                        
        except Exception as e:
            logger.error(f"Error describing metaobject type: {str(e)}")
            raise

    def create_metaobject_definition(
        self,
        type_name: str,
        display_name: str,
        description: str,
        fields: List[Dict[str, Any]]
    ) -> Optional[MetaobjectDefinition]:
        """
        Create a new metaobject definition in Shopify.
        
        Args:
            type_name: The type name for the new metaobject definition
            display_name: The display name for the new metaobject definition
            description: The description for the new metaobject definition
            fields: List of field definitions for the new metaobject
            
        Returns:
            Optional[MetaobjectDefinition]: The created metaobject definition if successful
            
        Raises:
            requests.RequestException: If the API request fails
        """
        mutation = """
        mutation createMetaobjectDefinition($definition: MetaobjectDefinitionCreateInput!) {
            metaobjectDefinitionCreate(definition: $definition) {
                metaobjectDefinition {
                    type
                    name
                    description
                    fields {
                        key
                        name
                        type
                        description
                        required
                        validations {
                            name
                            value
                        }
                    }
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        variables = {
            "definition": {
                "type": type_name,
                "name": display_name,
                "description": description,
                "fields": fields
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": mutation, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return None
                
            result = data.get("data", {}).get("metaobjectDefinitionCreate", {})
            if result.get("userErrors"):
                logger.error(f"User errors: {result['userErrors']}")
                return None
                
            return result.get("metaobjectDefinition")
            
        except requests.RequestException as e:
            logger.error(f"Failed to create metaobject definition: {str(e)}")
            raise

    def add_metafield(
        self,
        metaobject_id: str,
        key: str,
        value: str,
        type: str = "single_line_text_field",
        namespace: str = "custom"
    ) -> Optional[Dict[str, Any]]:
        """
        Add a new metafield to a metaobject.
        
        Args:
            metaobject_id: The ID of the metaobject to add the metafield to
            key: The key for the metafield
            value: The value for the metafield
            type: The type of the metafield (default: "single_line_text_field")
            namespace: The namespace for the metafield (default: "custom")
            
        Returns:
            Optional[Dict[str, Any]]: The created metafield data if successful
            
        Raises:
            requests.RequestException: If the API request fails
        """
        mutation = """
        mutation CreateMetaobjectMetafield($metafield: MetaobjectMetafieldCreateInput!) {
            metaobjectMetafieldCreate(metafield: $metafield) {
                metafield {
                    id
                    key
                    value
                    type
                    namespace
                }
                userErrors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        variables = {
            "metafield": {
                "metaobjectId": metaobject_id,
                "key": key,
                "value": value,
                "type": type,
                "namespace": namespace
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": mutation, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return None
                
            result = data.get("data", {}).get("metaobjectMetafieldCreate", {})
            if result.get("userErrors"):
                logger.error(f"User errors: {result['userErrors']}")
                return None
                
            return result.get("metafield")
            
        except requests.RequestException as e:
            logger.error(f"Failed to add metafield: {str(e)}")
            raise

    def modify_metafield(
        self,
        metafield_id: str,
        value: str,
        type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Modify an existing metafield of a metaobject.
        
        Args:
            metafield_id: The ID of the metafield to modify
            value: The new value for the metafield
            type: Optional new type for the metafield
            
        Returns:
            Optional[Dict[str, Any]]: The updated metafield data if successful
            
        Raises:
            requests.RequestException: If the API request fails
        """
        mutation = """
        mutation UpdateMetaobjectMetafield($metafield: MetaobjectMetafieldUpdateInput!) {
            metaobjectMetafieldUpdate(metafield: $metafield) {
                metafield {
                    id
                    key
                    value
                    type
                    namespace
                }
                userErrors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        metafield_input = {
            "id": metafield_id,
            "value": value
        }
        if type:
            metafield_input["type"] = type
            
        variables = {
            "metafield": metafield_input
        }
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": mutation, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return None
                
            result = data.get("data", {}).get("metaobjectMetafieldUpdate", {})
            if result.get("userErrors"):
                logger.error(f"User errors: {result['userErrors']}")
                return None
                
            return result.get("metafield")
            
        except requests.RequestException as e:
            logger.error(f"Failed to modify metafield: {str(e)}")
            raise

    def delete_metafield(
        self,
        metafield_id: str
    ) -> bool:
        """
        Delete a metafield from a metaobject.
        
        Args:
            metafield_id: The ID of the metafield to delete
            
        Returns:
            bool: True if the deletion was successful, False otherwise
            
        Raises:
            requests.RequestException: If the API request fails
        """
        mutation = """
        mutation DeleteMetaobjectMetafield($id: ID!) {
            metaobjectMetafieldDelete(id: $id) {
                deletedId
                userErrors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        variables = {
            "id": metafield_id
        }
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": mutation, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return False
                
            result = data.get("data", {}).get("metaobjectMetafieldDelete", {})
            if result.get("userErrors"):
                logger.error(f"User errors: {result['userErrors']}")
                return False
                
            return bool(result.get("deletedId"))
            
        except requests.RequestException as e:
            logger.error(f"Failed to delete metafield: {str(e)}")
            raise

def main():
    """Example usage of the ShopifyMetaobjectLoader class."""
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    shop_domain = os.getenv("SHOPIFY_SHOP_DOMAIN")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    if not shop_domain or not access_token:
        logger.error("Missing required environment variables")
        return
        
    # Initialize the loader with caching
    loader = ShopifyMetaobjectLoader(
        shop_domain=shop_domain,
        access_token=access_token,
        cache_dir=".cache"
    )
    
    try:
        # Example: Create and upsert multiple metaobjects
        metaobjects = [
            Metaobject(
                type="product_spec",
                handle=f"example-spec-{i}",
                fields={
                    "spec_name": f"Spec {i}",
                    "spec_value": str(i * 100),
                    "unit": "g"
                }
            )
            for i in range(3)
        ]
        
        # Batch upsert
        stats = loader.batch_upsert_metaobjects(metaobjects, batch_size=2)
        print(f"Batch upsert stats: {stats}")
        
        # Export to CSV
        loader.export_metaobjects_to_csv(
            metaobject_type="product_spec",
            output_file="exported_specs.csv",
            include_metafields=True
        )
        
        # Get statistics
        stats = loader.get_metaobject_stats("product_spec")
        print(f"Metaobject stats: {json.dumps(stats, indent=2)}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
    main()