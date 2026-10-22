class ShopifyLocalProxyMiddleware:
    """Set X-Forwarded-Proto when Shopify CLI local proxy omits it."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.META.get("HTTP_X_FORWARDED_PROTO"):
            host = request.META.get("HTTP_HOST", "")
            if host.startswith(("localhost:", "127.0.0.1:", "[::1]:")):
                request.META["HTTP_X_FORWARDED_PROTO"] = "https"
        return self.get_response(request)
