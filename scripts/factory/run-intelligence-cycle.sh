#!/usr/bin/env bash
# Run all V3 intelligence motors and log telemetry.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "==> Factory Intelligence Cycle (V3)"

"$ROOT/scripts/factory/init-intelligence.sh"

python3 "$ROOT/scripts/factory/build-revenue-snapshot.py"
python3 "$ROOT/scripts/factory/compute-decision-accuracy.py"
python3 "$ROOT/scripts/factory/build-benchmark.py"
python3 "$ROOT/scripts/factory/record-proof.py" --status 2>/dev/null || true

"$ROOT/scripts/factory/validate-intelligence.sh"

python3 "$ROOT/scripts/factory/append_telemetry.py" \
  --cycle intelligence \
  --script run-intelligence-cycle.sh \
  --started "$START" \
  --motors proof,revenue,decision_accuracy,benchmark,memory

echo "==> Intelligence cycle complete"
