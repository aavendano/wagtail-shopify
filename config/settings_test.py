"""Test settings: inherit production settings but use SQLite for pytest/manage.py test."""

from config.settings import *  # noqa: F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
