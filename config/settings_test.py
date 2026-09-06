"""Pytest only: SQLite in-memory. For local Daphne use config.settings_dev."""

import os

from config.settings import *  # noqa: F403

SECRET_KEY = os.environ.get('DJANGO_SECRET') or 'test-secret-not-for-production'
DEBUG = True
WAGTAIL_AI_PGVECTOR = False
SEMANTIC_LINKS_ENABLED = False
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

# Isolate from ambient .env.dev / shell exports (CONTENT_STORE_*).
CONTENT_STORE_ENABLED = False
CONTENT_STORE_MODE = ''
CONTENT_STORE_GIT_FALLBACK_TO_DB = False

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

CSRF_TRUSTED_ORIGINS = [
    *CSRF_TRUSTED_ORIGINS,
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
