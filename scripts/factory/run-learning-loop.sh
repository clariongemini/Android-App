#!/usr/bin/env bash
# V3.1 Learning loop — WP → Proof → Reality → Revenue → Decision → Benchmark
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
EXIT=0

echo "==> Factory Learning Loop (V3.1 operational)"
echo "    WP → Proof → Reality → Revenue → Decision Accuracy → Benchmark"

"$ROOT/scripts/runtime/init-runtime.sh"

# 1. CDID work packages + proof gate sync
if [[ -f "$ROOT/scripts/cdid/run_cdid_cycle.py" ]]; then
  python3 "$ROOT/scripts/cdid/run_cdid_cycle.py" 2>/dev/null || true
fi
python3 "$ROOT/scripts/factory/wp-proof-gate.py" --sync-cdid || EXIT=1

# 2. Product reality (if project initialized)
if [[ -f "$ROOT/scripts/reality/run_product_reality_layer.py" ]]; then
  python3 "$ROOT/scripts/reality/run_product_reality_layer.py" 2>/dev/null || true
fi

# 3. Revenue (application-scoped)
python3 "$ROOT/scripts/factory/build-revenue-snapshot.py"

# 4. Decision accuracy + 90-day enforcement
python3 "$ROOT/scripts/factory/compute-decision-accuracy.py"
python3 "$ROOT/scripts/factory/enforce-decision-reviews.py" || EXIT=1

# 5. Benchmark (factory + product + market + velocity)
python3 "$ROOT/scripts/factory/build-benchmark.py"

python3 "$ROOT/scripts/factory/append_telemetry.py" \
  --cycle learning-loop \
  --script run-learning-loop.sh \
  --started "$START" \
  --motors "proof,reality,revenue,decision_accuracy,benchmark" \
  --exit-code "$EXIT"

if [[ $EXIT -ne 0 ]]; then
  echo "==> Learning loop completed with blockers (proof or decision review)"
  exit "$EXIT"
fi
echo "==> Learning loop closed successfully"
