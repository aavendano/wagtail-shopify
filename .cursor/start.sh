#!/usr/bin/env bash
# Per-boot reconciliation for Cloud Agent environments.
# Idempotent: applies migrations, ensures Wagtail locales, and provisions a dev
# superuser (admin / admin) so the Wagtail admin and /cms/ SPA are usable.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PY=.venv/bin/python

# Migrations are gitignored in this repo (see .gitignore: */migrations/*), so a
# fresh checkout may lack migrations for the latest models. Regenerate them
# (idempotent: "No changes detected" once up to date) before applying.
echo "[start] generating any missing migrations"
"$PY" manage.py makemigrations --noinput

echo "[start] applying migrations"
"$PY" manage.py migrate --noinput

echo "[start] ensuring Wagtail locales"
"$PY" manage.py setup_locales

echo "[start] ensuring dev superuser (admin/admin)"
DJANGO_SUPERUSER_PASSWORD=admin "$PY" manage.py createsuperuser \
  --noinput --username admin --email admin@example.com 2>/dev/null \
  || echo "[start] superuser already exists"

echo "[start] done"
