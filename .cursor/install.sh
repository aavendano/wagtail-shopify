#!/usr/bin/env bash
# Idempotent repository bootstrap for Cloud Agent environments.
# Durable, source-derived setup only: virtualenv + Python dependencies + dev .env.
# Per-boot reconciliation (migrations, locales) lives in .cursor/start.sh.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -x .venv/bin/python ]]; then
  echo "[install] creating virtualenv"
  python3 -m venv .venv
fi

echo "[install] installing Python dependencies"
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

if [[ ! -f .env ]]; then
  echo "[install] seeding dev .env from .cursor/dev.env.example"
  cp .cursor/dev.env.example .env
fi

echo "[install] done"
