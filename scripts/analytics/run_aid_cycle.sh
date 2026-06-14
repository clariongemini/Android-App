#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
echo "=== AID Cycle ==="
python3 scripts/analytics/validate_sprint_p_activation.py
python3 scripts/analytics/build_aid_output.py
if [[ -f governance/analytics/output/sprint_p_field_proof.json ]]; then
  echo "   ℹ️  Field proof present — see sprint_p_field_proof.json"
fi
echo "=== AID Cycle complete ==="
