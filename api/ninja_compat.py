"""
Compatibility shim for django-ninja fork on Django 6+.

The fork registers a custom ``uuid`` URL converter, but Django 6 already
registers ``uuid``. Patch register_converter to ignore duplicate registration.
"""

from django.urls import register_converter as _register_converter


def _safe_register_converter(converter, type_name):
    try:
        _register_converter(converter, type_name)
    except ValueError as exc:
        if "already registered" not in str(exc):
            raise


import django.urls

django.urls.register_converter = _safe_register_converter
