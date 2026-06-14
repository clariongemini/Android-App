#!/usr/bin/env bash
# Wrapper — delegates to canonical gate at scripts/agent-approval-gate.sh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/../agent-approval-gate.sh" "$@"
