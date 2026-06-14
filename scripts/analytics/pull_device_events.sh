#!/usr/bin/env bash
# Pull distinct analytics event names from debug build via Room (local pipeline proof).
set -euo pipefail

PACKAGE="com.konusma"
DB="databases/speech_therapy_db"

if ! adb devices | grep -qE 'device$'; then
  echo "❌ No adb device. Connect phone or start emulator."
  exit 1
fi

if ! adb shell pm path "$PACKAGE" >/dev/null 2>&1; then
  echo "❌ $PACKAGE not installed"
  exit 1
fi

echo "=== Local analytics events (Room) ==="
adb shell run-as "$PACKAGE" sqlite3 "$DB" \
  "SELECT eventName, COUNT(*) AS n FROM analytics_events GROUP BY eventName ORDER BY eventName;" 2>/dev/null \
  || {
    echo "❌ Could not read database (debug build required)"
    exit 1
  }

echo ""
echo "=== Recent events (last 20) ==="
adb shell run-as "$PACKAGE" sqlite3 "$DB" \
  "SELECT datetime(createdAt/1000, 'unixepoch', 'localtime'), eventName FROM analytics_events ORDER BY createdAt DESC LIMIT 20;" 2>/dev/null
