#!/usr/bin/env bash
# Wrapper — canonical DX path for CEO cycle
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$ROOT/ceo/run_ceo_cycle.sh" "$@"
