#!/usr/bin/env python3
"""Thin launcher for Daphne ASGI (no eager bigframes import)."""
from __future__ import annotations

import os
import sys

_TEST_SETTINGS = "config.settings_test"


def main() -> None:
    settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "")
    if settings_module == _TEST_SETTINGS:
        sys.stderr.write(
            "Refusing to start Daphne with DJANGO_SETTINGS_MODULE="
            f"{_TEST_SETTINGS}. That module is for pytest only; unset it "
            "or use config.settings / config.settings_dev.\n"
        )
        raise SystemExit(2)

    from daphne.cli import CommandLineInterface

    args = sys.argv[1:] if len(sys.argv) > 1 else []
    CommandLineInterface().run(args)


if __name__ == "__main__":
    main()
