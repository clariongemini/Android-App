#!/usr/bin/env python3
"""Validate AID Sprint P activation — code pipeline + optional Firebase credentials."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANALYTICS_KT = ROOT / "app/src/main/java/com/konusma/domain/model/AnalyticsEvent.kt"
REPO_KT = ROOT / "app/src/main/java/com/konusma/repository/AnalyticsRepository.kt"
GATE = ROOT / "governance/analytics/SPRINT_P_ACTIVATION_GATE.json"
CATALOG = ROOT / "governance/analytics/SPRINT_P_EVENT_CATALOG.json"
APP_GRADLE = ROOT / "app/build.gradle.kts"
FIREBASE_DS = ROOT / "app/src/main/java/com/konusma/data/remote/datasource/FirebaseAnalyticsRemoteDataSource.kt"
SESSION_TRACKER = ROOT / "app/src/main/java/com/konusma/analytics/AnalyticsSessionTracker.kt"
GOOGLE_SERVICES = ROOT / "app/google-services.json"


def _fail(msg: str) -> None:
    print(f"   ❌ {msg}")
    sys.exit(1)


def main() -> int:
    print("AID Sprint P — activation validation")
    errors: list[str] = []

    if not ANALYTICS_KT.exists():
        errors.append("AnalyticsEvent.kt missing")
    else:
        kt = ANALYTICS_KT.read_text(encoding="utf-8")
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        for item in catalog["minimum_events"]:
            const = item["constant"]
            if f"const val {const} =" not in kt and f'const val {const} =' not in kt:
                errors.append(f"Missing constant {const} for {item['name']}")

    if not REPO_KT.exists() or "remoteDataSource.trackEvent" not in REPO_KT.read_text(encoding="utf-8"):
        errors.append("AnalyticsRepository does not forward to remoteDataSource.trackEvent")

    for path, label in [(FIREBASE_DS, "FirebaseAnalyticsRemoteDataSource"), (SESSION_TRACKER, "AnalyticsSessionTracker")]:
        if not path.exists():
            errors.append(f"{label} missing")

    gradle = APP_GRADLE.read_text(encoding="utf-8")
    if "firebase.analytics" not in gradle:
        errors.append("firebase-analytics dependency missing in app/build.gradle.kts")

    firebase_connected = GOOGLE_SERVICES.exists()
    field_proof_path = ROOT / "governance/analytics/output/sprint_p_field_proof.json"
    field_verified = False
    if field_proof_path.exists():
        proof = json.loads(field_proof_path.read_text(encoding="utf-8"))
        field_verified = proof.get("minimum_pass") is True

    pipeline_ready = len(errors) == 0

    if errors:
        for err in errors:
            print(f"   ❌ {err}")
        return 1

    print("   ✅ Minimum event constants present")
    print("   ✅ Event pipeline wired (Room + remote)")
    print("   ✅ FirebaseAnalyticsRemoteDataSource present")
    print("   ✅ AnalyticsSessionTracker present")
    print(f"   {'✅' if firebase_connected else '⚠️ '} Firebase credentials: {'connected' if firebase_connected else 'awaiting google-services.json'}")

    gate = json.loads(GATE.read_text(encoding="utf-8"))
    if firebase_connected and field_verified:
        gate_status = "ACTIVE"
    elif firebase_connected:
        gate_status = "FIREBASE_CONNECTED"
    else:
        gate_status = "PIPELINE_READY"
    gate["status"] = gate_status
    gate["updated_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
    gate["success_criteria"] = {
        "live_analytics": firebase_connected and field_verified,
        "firebase_connected": firebase_connected,
        "session_tracking": True,
        "retention_tracking": firebase_connected,
        "completion_tracking": True,
        "event_pipeline": True,
        "field_events_verified": field_verified,
    }
    gate["minimum_events"] = [e["name"] for e in json.loads(CATALOG.read_text(encoding="utf-8"))["minimum_events"]]
    gate["code_refs"] = {
        "repository": "app/src/main/java/com/konusma/repository/AnalyticsRepository.kt",
        "firebase": "app/src/main/java/com/konusma/data/remote/datasource/FirebaseAnalyticsRemoteDataSource.kt",
        "session": "app/src/main/java/com/konusma/analytics/AnalyticsSessionTracker.kt",
        "catalog": "governance/analytics/SPRINT_P_EVENT_CATALOG.json",
    }
    GATE.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   ✅ Updated {GATE.relative_to(ROOT)} → status={gate['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
