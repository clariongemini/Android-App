#!/usr/bin/env bash
# Sprint P device validation — install APK, enable Firebase DebugView, print checklist.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
APK="$ROOT/app/build/outputs/apk/debug/app-debug.apk"
PACKAGE="com.konusma"
JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home}"
export JAVA_HOME
ADB="${ANDROID_HOME:-$HOME/Library/Android/sdk}/platform-tools/adb"
EMULATOR="${ANDROID_HOME:-$HOME/Library/Android/sdk}/emulator/emulator"

wait_for_device() {
  "$ADB" wait-for-device
  for _ in $(seq 1 60); do
    boot=$("$ADB" shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
    [[ "$boot" == "1" ]] && return 0
    sleep 2
  done
  echo "❌ Device boot timeout"
  exit 1
}

if [[ ! -f "$APK" ]]; then
  echo "Building debug APK..."
  (cd "$ROOT" && ./gradlew :app:assembleDebug --quiet)
fi

if ! "$ADB" devices | grep -qE 'device$'; then
  AVD=$("$EMULATOR" -list-avds 2>/dev/null | head -1)
  if [[ -z "$AVD" ]]; then
    echo "❌ No device and no AVD. Connect a phone via USB or create an emulator."
    exit 1
  fi
  echo "Starting emulator: $AVD"
  "$EMULATOR" -avd "$AVD" -no-snapshot-load >/dev/null 2>&1 &
  wait_for_device
fi

echo "=== Sprint P Device Test ==="
"$ADB" install -r "$APK" | tail -1
"$ADB" shell setprop debug.firebase.analytics.app "$PACKAGE" || true

if [[ -f "$ROOT/app/google-services.json" ]]; then
  echo "   ✅ google-services.json present — Firebase remote events enabled"
else
  echo "   ⚠️  google-services.json missing — local Room events only"
  echo "   Run: ./scripts/analytics/connect_firebase.sh /path/to/google-services.json"
fi

echo ""
echo "Manual test flow (10 min):"
echo "  1. Open app → complete onboarding if needed"
echo "  2. Oyna → start daily exercise (3x for daily_mission + streak)"
echo "  3. Keşfet → Late Talker → 3 complete, 1 repeat, 1 skip"
echo "  4. Open Premium paywall once (Settings or Gelişimim)"
echo "  5. Background app → session_end"
echo ""
echo "Firebase DebugView: Console → Analytics → DebugView (real-time)"
echo "Local check: ./scripts/analytics/pull_device_events.sh"
echo ""
echo "Required 13 events:"
python3 - <<PY
import json
from pathlib import Path
cat = json.loads(Path("$ROOT/governance/analytics/SPRINT_P_EVENT_CATALOG.json").read_text())
for i, e in enumerate(cat["minimum_events"], 1):
    print(f"  {i:2}. {e['name']}")
PY
