#!/usr/bin/env bash
# Validate V3 Factory Intelligence Layer canonical structure.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ERR=0

echo "==> Factory Intelligence validation (V3)"

REQUIRED=(
  "factory/README.md"
  "factory/proof/README.md"
  "factory/memory/README.md"
  "factory/decision_accuracy/README.md"
  "factory/revenue/README.md"
  "factory/benchmark/README.md"
  "factory/telemetry/README.md"
  "FACTORY_MISSION.md"
  "docs/FACTORY_V3.md"
  "templates/factory/proof_registry.template.json"
  "scripts/factory/init-intelligence.sh"
  "scripts/factory/seed-intelligence.py"
  "scripts/factory/record-proof.py"
  "scripts/factory/query-memory.sh"
  "scripts/factory/compute-decision-accuracy.py"
  "scripts/factory/build-benchmark.py"
  "scripts/factory/run-intelligence-cycle.sh"
  "scripts/factory/append_telemetry.py"
  "scripts/factory/build-revenue-snapshot.py"
  "scripts/factory/record-decision.py"
  "scripts/factory/wp-proof-gate.py"
  "scripts/factory/enforce-decision-reviews.py"
  "scripts/factory/run-learning-loop.sh"
  "scripts/factory/print-mission.sh"
  "scripts/runtime/init-runtime.sh"
  "factory/portfolio/README.md"
  "factory/outcomes/README.md"
  "docs/FACTORY_V4_PRODUCTIZATION.md"
  "scripts/factory/register-app.py"
  "scripts/factory/record-outcome.py"
  "scripts/factory/build-portfolio-outcomes.py"
  "scripts/factory/seed-outcomes.py"
  "scripts/factory/build-factory-kpi.py"
  "scripts/factory/seed-portfolio.py"
)

for f in "${REQUIRED[@]}"; do
  if [[ ! -e "$ROOT/$f" ]]; then
    echo "  ❌ missing: $f"
    ERR=$((ERR + 1))
  fi
done

if [[ $ERR -eq 0 ]]; then
  echo "  ✅ V3 canonical structure OK"
fi

exit "$ERR"
