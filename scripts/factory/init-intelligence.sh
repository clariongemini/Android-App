#!/usr/bin/env bash
# Bootstrap factory intelligence — delegates to runtime consolidation (V3.1).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
exec "$ROOT/scripts/runtime/init-runtime.sh"
