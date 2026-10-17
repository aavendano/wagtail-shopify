#!/usr/bin/env bash
# Per-boot reconciliation for Cloud Agent / deploy environments.
# Idempotent: applies migrations, ensures Wagtail locales, CMS SPA mount,
# and provisions the admin user from ADMIN_* (or DJANGO_SUPERUSER_*) env vars.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PY=.venv/bin/python

# Optional local secrets (never committed). PLT default admin credentials.
if [[ -f "${HOME}/.secrets/plt/default-user.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${HOME}/.secrets/plt/default-user.env"
  set +a
fi

# Migrations are gitignored in this repo (see .gitignore: */migrations/*), so a
# fresh checkout may lack migrations for the latest models. Regenerate them
# (idempotent: "No changes detected" once up to date) before applying.
echo "[start] generating any missing migrations"
"$PY" manage.py makemigrations --noinput

echo "[start] applying migrations"
"$PY" manage.py migrate --noinput

echo "[start] ensuring Wagtail locales"
"$PY" manage.py setup_locales

echo "[start] ensuring CMS SPA mount"
"$PY" manage.py ensure_cms_spa

echo "[start] ensuring admin superuser from env"
"$PY" manage.py ensure_superuser --update-password

echo "[start] done"
