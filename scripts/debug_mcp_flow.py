#!/usr/bin/env python
"""Reproduce MCP tools/list over SSE and emit debug logs in api/mcp.py."""

import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ["MCP_DEBUG_RUN_ID"] = "repro-script"

import api.ninja_compat  # noqa: E402, F401

from mcp import ClientSession  # noqa: E402
from mcp.client.sse import sse_client  # noqa: E402


async def main() -> int:
    base_url = os.environ.get("MCP_SSE_URL", "http://127.0.0.1:8000/api/v1/mcp")
    api_key = os.environ.get("MCP_API_KEY", "")
    if not api_key:
        print("Set MCP_API_KEY to a valid Django API key.", file=sys.stderr)
        return 1

    headers = {"Authorization": f"Bearer {api_key}"}
    print(f"Connecting to {base_url}")
    try:
        async with sse_client(base_url, headers=headers, timeout=15, sse_read_timeout=30) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                print(f"SUCCESS: {len(tools.tools)} tools")
                return 0
    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
