#!/usr/bin/env bash
# Connect Firebase — copy google-services.json, validate package, rebuild debug APK.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TARGET="$ROOT/app/google-services.json"
SOURCE="${1:-${GOOGLE_SERVICES_JSON:-}}"
PACKAGE="$(python3 -c "import sys; sys.path.insert(0,'$ROOT/scripts/governance'); from project_meta import load_project_meta; print(load_project_meta()['package_name'])")"

if [[ -z "$SOURCE" ]]; then
  echo "Usage: GOOGLE_SERVICES_JSON=/path/to/google-services.json $0"
  echo "   or: $0 /path/to/google-services.json"
  echo ""
  echo "Firebase Console → Project settings → Your apps → Android ($PACKAGE) → Download google-services.json"
  exit 1
fi

if [[ ! -f "$SOURCE" ]]; then
  echo "❌ File not found: $SOURCE"
  exit 1
fi

python3 - "$SOURCE" "$PACKAGE" <<'PY'
import json, sys
path, expected = sys.argv[1], sys.argv[2]
data = json.load(open(path, encoding="utf-8"))
packages = [
    c.get("client_info", {}).get("android_client_info", {}).get("package_name")
    for c in (data.get("client") or [])
]
if expected not in packages:
    print(f"❌ Expected package {expected}, found: {packages}")
    sys.exit(1)
print(f"   ✅ Valid Firebase config — project_id={data.get('project_info', {}).get('project_id')}")
PY

cp "$SOURCE" "$TARGET"
echo "   ✅ Copied → app/google-services.json"

if [[ -x "$ROOT/gradlew" ]]; then
  export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home}"
  cd "$ROOT"
  ./gradlew :app:assembleDebug --quiet
  echo "   ✅ Debug APK rebuilt with Firebase plugin"
fi

python3 scripts/analytics/validate_sprint_p_activation.py
echo ""
echo "Next:"
echo "  1. ./scripts/analytics/run_sprint_p_device_test.sh"
echo "  2. Firebase Console → Analytics → DebugView"
echo "  3. Confirm events → record field proof"
