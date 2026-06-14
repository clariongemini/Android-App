#!/usr/bin/env bash
# Search factory memory — failures, successes, lessons, ADR index.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
exec python3 "$ROOT/scripts/factory/query_memory.py" "$@"
