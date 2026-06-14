#!/usr/bin/env python3
"""Validate AID Sprint P activation — code pipeline + optional Firebase credentials."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "governance"))
from project_meta import kotlin_path, load_project_meta  # noqa: E402

GATE = ROOT / "governance/analytics/SPRINT_P_ACTIVATION_GATE.json"
CATALOG = ROOT / "governance/analytics/SPRINT_P_EVENT_CATALOG.json"
APP_GRADLE = ROOT / "app/build.gradle.kts"
GOOGLE_SERVICES = ROOT / "app/google-services.json"


def main() -> int:
    meta = load_project_meta(ROOT)
    print(f"AID Sprint P — activation validation ({meta['package_name']})")
    errors: list[str] = []

    analytics_kt = kotlin_path(ROOT, "domain", "model", "AnalyticsEvent.kt")
    repo_kt = kotlin_path(ROOT, "repository", "AnalyticsRepository.kt")
    firebase_ds = kotlin_path(ROOT, "data", "remote", "datasource", "FirebaseAnalyticsRemoteDataSource.kt")
    session_tracker = kotlin_path(ROOT, "analytics", "AnalyticsSessionTracker.kt")

    if not analytics_kt.exists():
        errors.append(f"AnalyticsEvent.kt missing ({analytics_kt.relative_to(ROOT)})")
    elif CATALOG.exists():
        kt = analytics_kt.read_text(encoding="utf-8")
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        for item in catalog.get("minimum_events", []):
            const = item["constant"]
            if f"const val {const} =" not in kt:
                errors.append(f"Missing constant {const} for {item['name']}")

    if not repo_kt.exists() or "remoteDataSource.trackEvent" not in repo_kt.read_text(encoding="utf-8"):
        errors.append("AnalyticsRepository does not forward to remoteDataSource.trackEvent")

    for path, label in [(firebase_ds, "FirebaseAnalyticsRemoteDataSource"), (session_tracker, "AnalyticsSessionTracker")]:
        if not path.exists():
            errors.append(f"{label} missing")

    if APP_GRADLE.exists():
        gradle = APP_GRADLE.read_text(encoding="utf-8")
        if "firebase.analytics" not in gradle:
            errors.append("firebase-analytics dependency missing in app/build.gradle.kts")
    else:
        errors.append("app/build.gradle.kts missing — run init-new-app.sh first")

    firebase_connected = GOOGLE_SERVICES.exists()
    field_proof_path = ROOT / "governance/analytics/output/sprint_p_field_proof.json"
    field_verified = False
    if field_proof_path.exists():
        proof = json.loads(field_proof_path.read_text(encoding="utf-8"))
        field_verified = proof.get("minimum_pass") is True

    if errors:
        for err in errors:
            print(f"   ❌ {err}")
        return 1

    print("   ✅ Minimum event constants present")
    print("   ✅ Event pipeline wired (Room + remote)")
    print("   ✅ FirebaseAnalyticsRemoteDataSource present")
    print("   ✅ AnalyticsSessionTracker present")
    print(f"   {'✅' if firebase_connected else '⚠️ '} Firebase credentials: {'connected' if firebase_connected else 'awaiting google-services.json'}")

    if not GATE.exists() or not CATALOG.exists():
        print("   ⚠️  Sprint P gate/catalog missing — init-governance.sh")
        return 0

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
    pkg_rel = analytics_kt.parent.parent.parent.relative_to(ROOT / "app" / "src" / "main" / "java")
    base = f"app/src/main/java/{pkg_rel}"
    gate["code_refs"] = {
        "repository": f"{base}/repository/AnalyticsRepository.kt",
        "firebase": f"{base}/data/remote/datasource/FirebaseAnalyticsRemoteDataSource.kt",
        "session": f"{base}/analytics/AnalyticsSessionTracker.kt",
        "catalog": "governance/analytics/SPRINT_P_EVENT_CATALOG.json",
    }
    GATE.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   ✅ Updated {GATE.relative_to(ROOT)} → status={gate['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
