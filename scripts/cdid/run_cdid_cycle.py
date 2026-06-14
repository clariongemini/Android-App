#!/usr/bin/env python3
"""CDID — Autonomous Work Package Engine + Coverage + Memory + Escalation."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CDID_OUT = ROOT / "governance" / "cdid"
EXEC_OUT = ROOT / "governance" / "execution"
MEM_OUT = ROOT / "governance" / "memory"
ROADMAP = ROOT / "governance" / "product_decision" / "roadmap_priorities.json"
DECISION_LOG = ROOT / "governance" / "product_decision" / "decision_log.json"
QUEUE = ROOT / "governance" / "executive" / "APPROVAL_QUEUE.md"
CEC_REPORT = EXEC_OUT / "ROADMAP_CONSUMPTION_REPORT.json"
FEATURE_BOARD = EXEC_OUT / "FEATURE_DELIVERY_SCOREBOARD.json"
GENERATED = CDID_OUT / "GENERATED_WORK_PACKAGES.json"

CHAIN = [
    ("research", "Research", "CIKA"),
    ("content", "Content Build", "CIKA"),
    ("android", "Android Integration", "Android"),
    ("qa", "QA Validation", "Denetçi"),
    ("release", "Release Gate", "CPO"),
]

FEATURE_SHORT = {
    "F001": "TR Phoneme Expansion",
    "F002": "Late Talker Phrase Bank",
    "F003": "Daily Missions 365",
}


def _load(path: Path) -> dict | list:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _save(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _max_wp_num() -> int:
    if not QUEUE.exists():
        return 17
    nums = [int(m.group(1)) for m in re.finditer(r"WP-(\d+)", QUEUE.read_text(encoding="utf-8"))]
    return max(nums) if nums else 17


def _queue_wp_status() -> dict[str, str]:
    status: dict[str, str] = {}
    if not QUEUE.exists():
        return status
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| WP-"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 8:
            continue
        wp = parts[1]
        st = parts[7].strip("` ")
        status[wp] = st
    return status


def _approved_features(roadmap: dict) -> list[dict]:
    items = []
    for level in ("P0", "P1"):
        for f in roadmap.get(level, []):
            items.append({**f, "priority_level": level})
    return items


def _generate_wps(features: list[dict], existing: dict) -> list[dict]:
    new_wps: list[dict] = list(existing.get("work_packages", []))
    existing_auto = {w.get("auto_id") for w in new_wps}
    existing_codes = {w["wp_id"] for w in new_wps}
    wp_num = _max_wp_num()
    for feat in features:
        fid = feat.get("id", "")
        for step_key, step_label, agent in CHAIN:
            auto_id = f"WP-AUTO-{fid}-{step_key}"
            if auto_id in existing_auto:
                continue
            wp_num += 1
            wp_code = f"WP-{wp_num:02d}"
            while wp_code in existing_codes:
                wp_num += 1
                wp_code = f"WP-{wp_num:02d}"
            short = FEATURE_SHORT.get(fid, (feat.get("name") or fid)[:30])
            new_wps.append({
                "wp_id": wp_code,
                "auto_id": auto_id,
                "feature_id": fid,
                "feature_name": feat.get("name"),
                "priority_level": feat.get("priority_level"),
                "chain_step": step_key,
                "title": f"{fid} {short} — {step_label}",
                "agent": agent,
                "status": "pending",
                "owner": feat.get("owner", ""),
                "generated_by": "CDID",
            })
            existing_auto.add(auto_id)
            existing_codes.add(wp_code)
    return new_wps


def _feature_implementation(fid: str, board: dict) -> dict:
    for f in board.get("features", []):
        if f.get("feature_id") == fid:
            return f
    return {}


def _execution_coverage(features: list[dict], wps: list[dict], board: dict, queue: dict) -> dict:
    approved = len(features)
    implemented = 0
    partial = 0
    detail = []
    for feat in features:
        fid = feat.get("id")
        feat_wps = [w for w in wps if w.get("feature_id") == fid]
        completed = sum(1 for w in feat_wps if queue.get(w["wp_id"], w.get("status", "")) == "completed")
        impl_info = _feature_implementation(fid, board)
        signal_ratio = impl_info.get("signal_ratio", 0)
        chain_complete = completed >= 3
        code_ready = signal_ratio >= 0.66
        if chain_complete and code_ready:
            implemented += 1
            state = "implemented"
        elif completed >= 1 or signal_ratio >= 0.33:
            partial += 1
            state = "partial"
        else:
            state = "not_started"
        detail.append({
            "feature_id": fid,
            "name": feat.get("name"),
            "priority_level": feat.get("priority_level"),
            "state": state,
            "wps_total": len(feat_wps),
            "wps_completed": completed,
            "signal_ratio": signal_ratio,
        })
    coverage_pct = int(100 * implemented / approved) if approved else 0
    return {
        "approved_features": approved,
        "implemented_features": implemented,
        "partial_features": partial,
        "execution_coverage_pct": coverage_pct,
        "target_pct": 90,
        "coverage_pass": coverage_pct >= 90,
        "features": detail,
    }


def _unowned_gaps(features: list[dict], wps: list[dict]) -> dict:
    gaps = []
    for feat in features:
        fid = feat.get("id")
        owner = (feat.get("owner") or "").strip()
        feat_wps = [w for w in wps if w.get("feature_id") == fid]
        red_flags = []
        if not owner:
            red_flags.append("missing_owner")
        if len(feat_wps) < len(CHAIN):
            red_flags.append("incomplete_wp_chain")
        if red_flags:
            gaps.append({
                "feature_id": fid,
                "name": feat.get("name"),
                "priority_level": feat.get("priority_level"),
                "owner": owner or None,
                "wp_count": len(feat_wps),
                "red_flags": red_flags,
                "severity": "critical" if "incomplete_wp_chain" in red_flags else "high",
            })
    return {
        "count": len(gaps),
        "red_flag_count": len(gaps),
        "gaps": gaps,
        "rule": "Owner olmayan veya WP zinciri eksik feature otomatik RED FLAG",
    }


def _update_memory(features: list[dict], coverage: dict, decisions: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    dec_hist = _load(MEM_OUT / "DECISION_HISTORY.json") or {"entries": []}
    if not dec_hist.get("entries"):
        for d in decisions.get("decisions", [])[:20]:
            dec_hist.setdefault("entries", []).append({
                "decision_id": d.get("decision_id"),
                "feature_id": d.get("feature_id"),
                "feature_name": d.get("feature_name"),
                "priority_level": d.get("priority_level"),
                "recorded_at": now,
            })
    dec_hist["updated_at"] = now
    _save(MEM_OUT / "DECISION_HISTORY.json", dec_hist)

    delivery = _load(MEM_OUT / "DELIVERY_HISTORY.json") or {"entries": []}
    for f in coverage.get("features", []):
        entry = {
            "feature_id": f["feature_id"],
            "state": f["state"],
            "wps_completed": f["wps_completed"],
            "recorded_at": now,
        }
        recent = delivery.get("entries", [])
        if not recent or recent[-1].get("feature_id") != f["feature_id"] or recent[-1].get("state") != f["state"]:
            recent.append(entry)
        delivery["entries"] = recent[-100:]
        delivery["updated_at"] = now
    _save(MEM_OUT / "DELIVERY_HISTORY.json", delivery)

    failures = _load(MEM_OUT / "FAILURE_HISTORY.json") or {"entries": []}
    for f in coverage.get("features", []):
        if f["state"] == "not_started":
            failures.setdefault("entries", []).append({
                "feature_id": f["feature_id"],
                "reason": "no_execution_progress",
                "recorded_at": now,
            })
    failures["entries"] = failures.get("entries", [])[-50:]
    failures["updated_at"] = now
    _save(MEM_OUT / "FAILURE_HISTORY.json", failures)

    successes = _load(MEM_OUT / "SUCCESS_HISTORY.json") or {"entries": []}
    for f in coverage.get("features", []):
        if f["state"] == "implemented":
            successes.setdefault("entries", []).append({
                "feature_id": f["feature_id"],
                "recorded_at": now,
            })
    successes["entries"] = successes.get("entries", [])[-50:]
    successes["updated_at"] = now
    _save(MEM_OUT / "SUCCESS_HISTORY.json", successes)

    org_mem = {
        "generated_at": now,
        "version": "V4",
        "decision_entries": len(dec_hist.get("entries", [])),
        "delivery_entries": len(delivery.get("entries", [])),
        "failure_entries": len(failures.get("entries", [])),
        "success_entries": len(successes.get("entries", [])),
        "learning_loop_active": True,
    }
    _save(MEM_OUT / "ORGANIZATIONAL_MEMORY.json", org_mem)
    return org_mem


def _prediction_accuracy(features: list[dict]) -> dict:
    records = []
    for feat in features:
        fid = feat.get("id")
        scores = feat.get("scores", {})
        expected_ret = scores.get("retention", 0) / 10
        actual_map = {"F001": 3.0, "F002": 0.0, "F003": 2.0}
        actual_ret = actual_map.get(fid, 0.0)
        accuracy = int(100 * actual_ret / expected_ret) if expected_ret else 0
        records.append({
            "feature_id": fid,
            "name": feat.get("name"),
            "expected_retention_impact_pct": expected_ret,
            "actual_retention_impact_pct": actual_ret,
            "prediction_accuracy_pct": min(accuracy, 100),
            "note": "Pre-Sprint P stub — AID live data pending",
        })
    avg = int(sum(r["prediction_accuracy_pct"] for r in records) / len(records)) if records else 0
    return {"average_accuracy_pct": avg, "records": records, "feeds": ["PDC", "CEO", "EGC"]}


def _sync_auto_queue(wps: list[dict]) -> None:
    auto_wps = [w for w in wps if w.get("generated_by") == "CDID"]
    lines = [
        "",
        "---",
        "",
        "## CDID Auto-Generated WPs (V4)",
        "",
        f"**Son üretim:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC  ",
        "**Owner:** CDID — otomatik; onay: CPO L1",
        "",
        "| WP | Feature | Başlık | Ajan | Durum |",
        "|----|---------|--------|------|-------|",
    ]
    for w in sorted(auto_wps, key=lambda x: x["wp_id"]):
        lines.append(
            f"| {w['wp_id']} | {w['feature_id']} | {w['title']} | {w['agent']} | `{w.get('status', 'pending')}` |"
        )
    lines.append("")
    section = "\n".join(lines)
    if QUEUE.exists():
        text = QUEUE.read_text(encoding="utf-8")
        marker = "## CDID Auto-Generated WPs"
        if marker in text:
            text = text[: text.index(marker)] + section.lstrip("\n")
        else:
            text = text.rstrip() + section
        QUEUE.write_text(text, encoding="utf-8")


def _run_wp_phase() -> int:
    CDID_OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    roadmap = _load(ROADMAP)
    decisions = _load(DECISION_LOG)
    board = _load(FEATURE_BOARD)
    existing = _load(GENERATED) if GENERATED.exists() else {"work_packages": []}

    features = _approved_features(roadmap)
    wps = _generate_wps(features, existing)
    queue_status = _queue_wp_status()
    for w in wps:
        st = queue_status.get(w["wp_id"])
        if st:
            w["status"] = st

    _save(GENERATED, {
        "generated_at": now.isoformat(),
        "department": "CDID",
        "version": "V4",
        "principle": "No critical finding without action",
        "work_packages": wps,
        "chain_template": [c[0] for c in CHAIN],
    })

    coverage = _execution_coverage(features, wps, board, queue_status)
    coverage["generated_at"] = now.isoformat()
    _save(EXEC_OUT / "EXECUTION_COVERAGE.json", coverage)

    unowned = _unowned_gaps(features, wps)
    unowned["generated_at"] = now.isoformat()
    _save(EXEC_OUT / "UNOWNED_GAPS.json", unowned)

    _update_memory(features, coverage, decisions)

    prediction = _prediction_accuracy(features)
    prediction["generated_at"] = now.isoformat()
    _save(EXEC_OUT / "DELIVERY_PREDICTION_ACCURACY.json", prediction)

    _sync_auto_queue(wps)

    print(f"   ✅ CDID — {len(wps)} WPs · Coverage {coverage['execution_coverage_pct']}% · Unowned {unowned['count']}")
    print("   ✅ governance/cdid/GENERATED_WORK_PACKAGES.json")
    print("   ✅ governance/execution/EXECUTION_COVERAGE.json")
    print("   ✅ governance/memory/ORGANIZATIONAL_MEMORY.json")
    return 0


def _run_escalation_phase() -> int:
    now = datetime.now(timezone.utc)
    cec = _load(CEC_REPORT)
    coverage = _load(EXEC_OUT / "EXECUTION_COVERAGE.json")
    unowned = _load(EXEC_OUT / "UNOWNED_GAPS.json")
    align = cec.get("execution_alignment_score", 0)
    escalations = []

    if align < 70:
        escalations.append({
            "id": "alignment_below_70",
            "severity": "high",
            "from": "CEO",
            "to": "CEC",
            "message": f"Execution alignment {align}% < 70",
        })

    for f in coverage.get("features", []):
        if f.get("state") == "not_started" and f.get("priority_level") == "P0":
            escalations.append({
                "id": f"p0_stalled_{f['feature_id']}",
                "severity": "critical",
                "from": "CEO",
                "to": "CEC",
                "message": f"P0 {f['feature_id']} no progress — 14-day escalation rule",
            })

    for g in unowned.get("gaps", []):
        escalations.append({
            "id": f"unowned_{g['feature_id']}",
            "severity": g.get("severity", "high"),
            "from": "CDID",
            "to": "CEO",
            "message": f"RED FLAG {g['feature_id']}: {', '.join(g['red_flags'])}",
        })

    lines = [
        "# Escalation Report",
        "",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        f"**Active escalations:** {len(escalations)}  ",
        "",
        "---",
        "",
    ]
    for e in escalations:
        lines.append(f"## [{e['severity'].upper()}] {e['id']}")
        lines.append(f"- Route: {e['from']} → {e['to']}")
        lines.append(f"- {e['message']}")
        lines.append("")

    if not escalations:
        lines.append("No active escalations.")
        lines.append("")

    (EXEC_OUT / "ESCALATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"   ✅ CDID escalation — {len(escalations)} → ESCALATION_REPORT.md")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post-cec", action="store_true")
    args = parser.parse_args()
    return _run_escalation_phase() if args.post_cec else _run_wp_phase()


if __name__ == "__main__":
    raise SystemExit(main())
