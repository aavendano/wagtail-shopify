"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.asgi import get_asgi_application

django_application = get_asgi_application()

import api.main  # noqa: F401 — initialize MCP server before middleware handles requests

from api.mcp_asgi import MCPStreamableHTTPMiddleware  # noqa: E402

application = MCPStreamableHTTPMiddleware(django_application)
