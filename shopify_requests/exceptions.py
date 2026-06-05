class ShopifyIntegrationError(Exception):
    """Base error for Shopify Admin integration (GraphQL, tokens)."""


class ReauthorizationRequired(ShopifyIntegrationError):
    """Raised when the merchant must reauthorize or reinstall the app."""
