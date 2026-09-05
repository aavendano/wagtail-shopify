"""Aislado de producción: SQLite, sin pgvector, Celery eager."""

import os

from config.settings import *  # noqa: F403

SECRET_KEY = os.environ.get('DJANGO_SECRET') or 'test-secret-not-for-production'
DEBUG = True
# Solo SQLite de archivo (launch.json). :memory: de pytest no crea superuser.
ENSURE_TEST_SUPERUSER = os.environ.get('TEST_SQLITE_NAME', ':memory:') not in (
    ':memory:',
    '',
)
# Daphne local (launch.json :8083; README :8082) habla HTTP directo, no el proxy TLS de Shopify CLI.
CSRF_TRUSTED_ORIGINS = [
    *CSRF_TRUSTED_ORIGINS,
    'http://127.0.0.1:8082',
    'http://localhost:8082',
    'http://127.0.0.1:8083',
    'http://localhost:8083',
]
SECURE_PROXY_SSL_HEADER = None
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('TEST_SQLITE_NAME', ':memory:'),
    }
}
