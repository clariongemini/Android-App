#!/usr/bin/env python3
"""AID V2 — Analytics Intelligence with Sprint P live metrics framework."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "governance" / "analytics" / "output"
SCHEMA = ROOT / "governance" / "analytics" / "SPRINT_P_SCHEMA.json"


def _metric_block(status: str = "unverified") -> dict:
    return {"status": status, "live": False, "sprint_p": "0/10"}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    schema = {}
    if SCHEMA.exists():
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    meta = {
        "generated_at": now,
        "version": "V2",
        "source": "SPRINT_P_SCHEMA + activation pipeline",
        "live_analytics": False,
        "event_pipeline": True,
        "organizational_blind_spot": True,
        "quality_note": "PIPELINE_READY — add google-services.json + Sprint P field proof for ACTIVE",
    }

    live_metrics = {
        **meta,
        "retention": {
            **_metric_block(),
            "d1": None,
            "d3": None,
            "d7": None,
            "d30": None,
            "targets": schema.get("metrics", {}).get("retention", {}),
        },
        "session": {
            **_metric_block(),
            "daily_practice_rate": None,
            "avg_session_minutes": None,
            "sessions_per_week": None,
        },
        "completion": {
            **_metric_block(),
            "exercise_completion_rate": None,
            "learning_path_progress": None,
            "daily_mission_completion": None,
        },
        "churn": {
            **_metric_block(),
            "d7_churn_rate": None,
            "content_exhaustion_signal": True,
            "stt_frustration_rate": None,
        },
        "conversion": {
            **_metric_block(),
            "trial_start_rate": None,
            "trial_to_paid": None,
            "premium_conversion_p50": 70,
        },
        "activation_gate": schema.get("activation_gate", "Sprint P"),
        "f002_events": {
            "status": "pipeline_wired",
            "events": [
                "phrase_started",
                "phrase_completed",
                "phrase_repeated",
                "phrase_skipped",
                "session_duration",
                "parent_retention",
            ],
            "spec": "curriculum/late_talker/analytics/f002_analytics_hooks.json",
        },
    }
    (OUT / "live_metrics.json").write_text(
        json.dumps(live_metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("   ✅ governance/analytics/output/live_metrics.json")

    files = {
        "retention_snapshot.json": {
            **meta,
            "d1": "unverified",
            "d7": "unverified",
            "d30": "unverified",
            "sprint_p": "0/10 testers",
            "live_metrics_ref": "live_metrics.json",
        },
        "churn_signals.json": {
            **meta,
            "signals": ["content_exhaustion_risk", "stt_frustration", "no_sprint_p_proof"],
        },
        "session_analysis.json": {
            **meta,
            "daily_practice_rate": "unknown",
            "session_length": "unknown",
            "target_minutes": "5-10",
        },
        "feature_adoption.json": {
            **meta,
            "journey": "code_ready",
            "courage": "code_ready",
            "in_app_review": "wp04_done",
        },
        "completion_metrics.json": {
            **meta,
            "learning_completion": "unknown",
            "content_repeat_ratio_estimated": 0.35,
        },
    }
    for name, data in files.items():
        (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"   ✅ governance/analytics/output/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
