#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if [[ -d .venv-scraper/bin ]]; then
  # shellcheck disable=SC1091
  source .venv-scraper/bin/activate
fi

echo "▶ PDC — Product Decision Council"
python scripts/product_decision/build_pdc_outputs.py
echo "✅ PDC → governance/product_decision/"
