#!/usr/bin/env bash
# Idempotent Root 1 for wagtail-runner-01 (reuses github-runner user if present).
set -euo pipefail

RUNNER_USER="github-runner"
RUNNER_NAME="wagtail-runner-01"
RUNNER_ROOT="/opt/github-runners/${RUNNER_NAME}"
RUNNER_VERSION="2.338.0"
TARBALL="actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"
DOWNLOAD_URL="https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/${TARBALL}"
EXPECTED_SHA256="af4b794c1bc41d73d40535e3fe092a39f9679cd8d965954c2aca25a05ca41d32"

if [[ "${EUID}" -ne 0 ]]; then
  echo "ERROR: run as root (sudo bash $0)" >&2
  exit 1
fi

echo "==> [1/5] Ensure system user ${RUNNER_USER}"
if id -u "${RUNNER_USER}" >/dev/null 2>&1; then
  echo "    user exists"
else
  useradd --system --create-home --home-dir "/home/${RUNNER_USER}" \
    --shell /usr/sbin/nologin "${RUNNER_USER}"
  echo "    user created"
fi
if getent group sudo >/dev/null 2>&1 && id -nG "${RUNNER_USER}" | grep -qw sudo; then
  echo "ERROR: ${RUNNER_USER} is in sudo group" >&2; exit 1
fi
if getent group docker >/dev/null 2>&1 && id -nG "${RUNNER_USER}" | grep -qw docker; then
  echo "ERROR: ${RUNNER_USER} is in docker group" >&2; exit 1
fi

echo "==> [2/5] Apt deps (no Docker)"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
ICU_PKG="$(apt-cache search --names-only '^libicu[0-9]+$' 2>/dev/null | awk '{print $1}' | sort -V | tail -1 || true)"
APT_PKGS=(curl ca-certificates tar gzip libicu-dev libssl-dev zlib1g build-essential git jq python3-venv python3-dev libpq-dev)
[[ -n "${ICU_PKG}" ]] && APT_PKGS+=("${ICU_PKG}")
apt-get install -y --no-install-recommends "${APT_PKGS[@]}"

echo "==> [3/5] Create ${RUNNER_ROOT}"
mkdir -p "${RUNNER_ROOT}" "${RUNNER_ROOT}/_work" "${RUNNER_ROOT}/_diag"
chown -R "${RUNNER_USER}:${RUNNER_USER}" "${RUNNER_ROOT}"
chmod 750 "${RUNNER_ROOT}" "${RUNNER_ROOT}/_work" "${RUNNER_ROOT}/_diag"

echo "==> [4/5] Download and verify runner ${RUNNER_VERSION}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT
cd "${TMP_DIR}"
curl -fsSL -o "${TARBALL}" "${DOWNLOAD_URL}"
echo "${EXPECTED_SHA256}  ${TARBALL}" | sha256sum -c -
if [[ -x "${RUNNER_ROOT}/config.sh" && -f "${RUNNER_ROOT}/bin/Runner.Listener" ]]; then
  echo "    binaries present; skip extract"
else
  tar xzf "${TARBALL}" -C "${RUNNER_ROOT}"
  chown -R "${RUNNER_USER}:${RUNNER_USER}" "${RUNNER_ROOT}"
  chmod 750 "${RUNNER_ROOT}"
fi

echo "==> [5/5] Verify"
id "${RUNNER_USER}"
ls -la "${RUNNER_ROOT}" | head -20
test -x "${RUNNER_ROOT}/config.sh"
cat <<EOF

Root 1 (wagtail) complete.
Next: ask the agent to prepare /tmp/wagtail-runner-configure-and-svc.sh
EOF
