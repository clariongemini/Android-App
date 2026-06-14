#!/usr/bin/env bash
# Wrapper — canonical DX path for Executive OS bootstrap
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/governance/init-governance.sh" "$@"
