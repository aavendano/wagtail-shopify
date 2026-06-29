import os


def pytest_configure():
    os.environ.setdefault('NINJA_SKIP_REGISTRY', 'true')
