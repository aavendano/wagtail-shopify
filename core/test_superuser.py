import os

from django.conf import settings
from django.contrib.auth import get_user_model


def ensure_test_superuser():
    """Crea un superuser local si settings_test usa SQLite de archivo vacía."""
    if not getattr(settings, "ENSURE_TEST_SUPERUSER", False):
        return False
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@localhost")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        return False
    User.objects.create_superuser(username, email, password)
    return True
