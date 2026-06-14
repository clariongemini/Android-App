#!/usr/bin/env bash
# Sprint P device smoke — requires debug app + adb.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PACKAGE="$(python3 -c "import sys; sys.path.insert(0,'$ROOT/scripts/governance'); from project_meta import load_project_meta; print(load_project_meta()['package_name'])")"

echo "==> Sprint P device test ($PACKAGE)"
adb shell am force-stop "$PACKAGE" 2>/dev/null || true
adb shell monkey -p "$PACKAGE" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1 || {
  echo "❌ Could not launch $PACKAGE"
  exit 1
}
sleep 3
"$ROOT/scripts/analytics/pull_device_events.sh"
