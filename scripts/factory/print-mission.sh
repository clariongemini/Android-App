#!/usr/bin/env bash
# Print factory mission — read at every quality gate / audit.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MISSION="$ROOT/FACTORY_MISSION.md"

if [[ ! -f "$MISSION" ]]; then
  echo "HATA: FACTORY_MISSION.md eksik — fabrika amacı tanımsız." >&2
  exit 1
fi

echo "── Factory Mission ──"
grep -m1 "Factory'nin amacı" "$MISSION" | sed 's/^> //;s/\*\*//g'
echo ""
