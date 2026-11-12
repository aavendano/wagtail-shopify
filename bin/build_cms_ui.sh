#!/usr/bin/env bash
# Build Polaris embedded CMS bundles into cms_ui/static/cms_ui/ (then collectstatic).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/cms_ui/frontend"
if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required. Install Node 20+ on the production host." >&2
  exit 1
fi
npm ci --legacy-peer-deps
npm run build
echo "Built: $ROOT/cms_ui/static/cms_ui/cms-embedded.js"
