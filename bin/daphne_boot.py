#!/usr/bin/env python3
"""Thin launcher for Daphne ASGI (no eager bigframes import)."""
from __future__ import annotations

import sys


def main() -> None:
    from daphne.cli import CommandLineInterface

    args = sys.argv[1:] if len(sys.argv) > 1 else []
    CommandLineInterface().run(args)


if __name__ == "__main__":
    main()
