"""
Import bigframes before Django setup.

Django (via daphne/twisted) loads zope.interface; bigframes' vendored ibis then
fails on lazy import with AttributeError: __provides__.
"""
from __future__ import annotations

import sys


def ensure_bigframes_pre_django() -> None:
    if "bigframes.pandas" in sys.modules:
        return
    import bigframes.pandas as bpd  # noqa: F401
