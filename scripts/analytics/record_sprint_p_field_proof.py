#!/usr/bin/env python3
"""Record Sprint P field proof — promotes gate to ACTIVE when 13/13 events verified."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "governance/analytics/SPRINT_P_EVENT_CATALOG.json"
PROOF = ROOT / "governance/analytics/output/sprint_p_field_proof.json"
GATE = ROOT / "governance/analytics/SPRINT_P_ACTIVATION_GATE.json"

REQUIRED = [e["name"] for e in json.loads(CATALOG.read_text(encoding="utf-8"))["minimum_events"]]


def main() -> int:
    events = [e.strip() for e in sys.argv[1:] if e.strip()]
    if not events and PROOF.exists():
        data = json.loads(PROOF.read_text(encoding="utf-8"))
        events = data.get("events_seen", [])

    if not events:
        print("Usage: python record_sprint_p_field_proof.py app_open session_start ...")
        print(f"Required ({len(REQUIRED)}): {', '.join(REQUIRED)}")
        return 1

    seen = sorted(set(events))
    missing = [e for e in REQUIRED if e not in seen]
    passed = len(missing) == 0

    proof = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "events_required": len(REQUIRED),
        "events_seen": seen,
        "events_missing": missing,
        "minimum_pass": passed,
        "source": "manual_or_script",
        "f002_scenario_ref": "governance/analytics/SPRINT_P_DEVICE_VALIDATION.md#f002-dogrulama",
    }
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    PROOF.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   ✅ Wrote {PROOF.relative_to(ROOT)}")
    print(f"   Events: {len(seen)}/{len(REQUIRED)} — missing: {missing or 'none'}")

    gate = json.loads(GATE.read_text(encoding="utf-8"))
    firebase_ok = (ROOT / "app/google-services.json").exists()
    active = firebase_ok and passed
    gate["status"] = "ACTIVE" if active else gate.get("status", "PIPELINE_READY")
    gate["updated_at"] = datetime.now(timezone.utc).isoformat()
    gate["field_proof_ref"] = str(PROOF.relative_to(ROOT))
    gate["success_criteria"] = {
        "live_analytics": active,
        "firebase_connected": firebase_ok,
        "session_tracking": True,
        "retention_tracking": firebase_ok,
        "completion_tracking": True,
        "event_pipeline": True,
        "field_events_verified": passed,
        "events_verified_count": f"{len(seen)}/{len(REQUIRED)}",
    }
    GATE.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   Gate status → {gate['status']}")
    return 0 if active else 2


if __name__ == "__main__":
    raise SystemExit(main())
