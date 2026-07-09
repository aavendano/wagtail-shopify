#!/usr/bin/env python3
"""Import bigframes before daphne/twisted starts (zope.interface conflict)."""
from __future__ import annotations

import sys


def main() -> None:
    import bigframes.pandas as bpd  # noqa: F401

    from daphne.cli import CommandLineInterface

    args = sys.argv[1:] if len(sys.argv) > 1 else []
    CommandLineInterface().run(args)


if __name__ == "__main__":
    main()
