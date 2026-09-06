"""Desarrollo local (Daphne :8083): SQLite en archivo, content store, sin Postgres."""

import os
from pathlib import Path

from dotenv import load_dotenv

from config.settings import *  # noqa: F403

# .env.dev overrides .env so CONTENT_STORE_* / DEV_SQLITE_NAME apply to Daphne :8083.
load_dotenv(Path(BASE_DIR) / '.env.dev', override=True)  # noqa: F405

SECRET_KEY = os.environ.get('DJANGO_SECRET') or 'dev-secret-not-for-production'
DEBUG = True
WAGTAIL_AI_PGVECTOR = False
SEMANTIC_LINKS_ENABLED = False
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

INSTALLED_APPS = [
    app
    for app in INSTALLED_APPS
    if app != 'django_ai_core.contrib.index.storage.pgvector'
]

# launch.json / .env.dev → archivo; default dedicado a dev (no mezclar con pytest)
_dev_sqlite = os.environ.get('DEV_SQLITE_NAME') or os.environ.get(
    'TEST_SQLITE_NAME', '/tmp/cms-shop-dev.sqlite3'
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _dev_sqlite,
    }
}

# Content store (re-read after .env.dev): default mirror; flip via CONTENT_STORE_MODE
CONTENT_STORE_ENABLED = (
    os.environ.get('CONTENT_STORE_ENABLED', 'true').lower() == 'true'
)
CONTENT_STORE_MODE = (os.environ.get('CONTENT_STORE_MODE') or 'mirror').strip().lower()
CONTENT_STORE_ROOT = os.environ.get(
    'CONTENT_STORE_ROOT',
    str(Path(BASE_DIR) / 'content'),  # noqa: F405
)
CONTENT_STORE_GIT_FALLBACK_TO_DB = (
    os.environ.get('CONTENT_STORE_GIT_FALLBACK_TO_DB', 'false').lower() == 'true'
)

# Daphne local habla HTTP directo (sin proxy TLS de Shopify CLI).
CSRF_TRUSTED_ORIGINS = [
    *CSRF_TRUSTED_ORIGINS,  # noqa: F405
    'http://127.0.0.1:8082',
    'http://localhost:8082',
    'https://127.0.0.1:8082',
    'https://localhost:8082',
    'http://127.0.0.1:8083',
    'http://localhost:8083',
    'https://127.0.0.1:8083',
    'https://localhost:8083',
]
SECURE_PROXY_SSL_HEADER = None
