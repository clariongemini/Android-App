#!/usr/bin/env python3
"""CEC — Chief Execution Council audit. Generates governance/execution/* reports."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "governance" / "execution"
ROADMAP = ROOT / "governance" / "product_decision" / "roadmap_priorities.json"
REJECTED = ROOT / "governance" / "product_decision" / "rejected_features.json"
QUEUE = ROOT / "governance" / "executive" / "APPROVAL_QUEUE.md"
MANIFEST = OUT / "ROADMAP_CONSUMPTION_MANIFEST.json"
YAPILACAKLAR = ROOT / "YAPILACAKLAR.md"


def _p0_spec(feature: dict) -> dict:
    """Generic P0 signals from roadmap — project adds REALITY_CHECKS for deep proof."""
    fid = feature.get("id", "F000")
    name = feature.get("name") or feature.get("title") or fid
    return {
        "name": name,
        "checks": [
            ("grep", "app/src/main", fid),
            ("grep", "docs", fid),
        ],
    }


def _load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _grep_dir(rel: str, pattern: str) -> bool:
    base = ROOT / rel
    if not base.exists():
        return False
    rx = re.compile(pattern, re.IGNORECASE)
    files = list(base.rglob("*")) if base.is_dir() else [base]
    for f in files:
        if not f.is_file():
            continue
        try:
            if rx.search(f.read_text(encoding="utf-8", errors="ignore")):
                return True
        except Exception:
            pass
    return False


def _eval_check(check: tuple) -> bool:
    kind = check[0]
    if kind == "path_exists":
        return (ROOT / check[1]).exists()
    if kind == "file_contains":
        p = ROOT / check[1]
        return p.exists() and check[2] in p.read_text(encoding="utf-8", errors="ignore")
    if kind == "file_contains_all":
        p = ROOT / check[1]
        if not p.exists():
            return False
        text = p.read_text(encoding="utf-8", errors="ignore")
        return all(s in text for s in check[2])
    if kind == "grep":
        return _grep_dir(check[1], check[2])
    return False


def _score_p0(feature_id: str, spec: dict) -> dict:
    checks = spec["checks"]
    passed = sum(1 for c in checks if _eval_check(c))
    total = len(checks)
    ratio = passed / total if total else 0
    if ratio >= 0.66:
        status = "working_on"
    elif ratio >= 0.33:
        status = "partial"
    else:
        status = "not_started"
    return {
        "feature_id": feature_id,
        "name": spec["name"],
        "signals_passed": passed,
        "signals_total": total,
        "signal_ratio": round(ratio, 2),
        "status": status,
        "active_execution": status == "working_on",
    }


def _wp_feature_links() -> list[dict]:
    links = []
    if not QUEUE.exists():
        return links
    text = QUEUE.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.startswith("| WP-"):
            continue
        m = re.search(r"(F\d{3})", line)
        if m:
            wp = line.split("|")[1].strip()
            links.append({"wp": wp, "feature_id": m.group(1), "linked": True})
    return links


def _scan_blockers(enforcement_active: bool, p0_board: list[dict], wp_links: list[dict]) -> list[dict]:
    blockers = []
    if not enforcement_active:
        blockers.append({
            "id": "enforcement_incomplete",
            "severity": "critical",
            "message": "PDC → Execution mandatory consumption layer incomplete",
            "owner": "CEC",
        })
    p0_ids = {p["feature_id"] for p in p0_board}
    linked_ids = {w["feature_id"] for w in wp_links}
    for p in p0_board:
        if p["status"] == "not_started":
            blockers.append({
                "id": f"p0_not_started_{p['feature_id']}",
                "severity": "high",
                "message": f"P0 {p['feature_id']} ({p['name']}) — no execution signals",
                "owner": "CEC → Android/CPO",
            })
    if not wp_links:
        blockers.append({
            "id": "wp_no_pdc_feature_id",
            "severity": "medium",
            "message": "APPROVAL_QUEUE has no WP entries linked to PDC feature_id (F001…)",
            "owner": "CPO",
        })
    elif not linked_ids.intersection(p0_ids):
        blockers.append({
            "id": "wp_p0_unlinked",
            "severity": "high",
            "message": "Active WPs not linked to current P0 items",
            "owner": "CPO",
        })
    return blockers


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)

    # Refresh enforcement validation
    subprocess.run([sys.executable, str(ROOT / "scripts/execution/validate_roadmap_consumption.py")], check=False)

    manifest = _load_json(MANIFEST)
    enforcement_active = manifest.get("enforcement_layer") == "active"
    enforcement_pct = manifest.get("enforcement_pct", 0)

    roadmap = _load_json(ROADMAP)
    p0_items = roadmap.get("P0", [])
    p0_board = [_score_p0(f["id"], _p0_spec(f)) for f in p0_items if f.get("id")]
    working_on = sum(1 for p in p0_board if p["active_execution"])
    p0_total = len(p0_board) or 1
    delivery_alignment = int(100 * working_on / p0_total)

    if enforcement_active:
        execution_alignment = delivery_alignment
    else:
        execution_alignment = min(delivery_alignment, int(enforcement_pct * 0.5))

    wp_links = _wp_feature_links()
    blockers = _scan_blockers(enforcement_active, p0_board, wp_links)

    consumption_report = {
        "generated_at": now.isoformat(),
        "department": "CEC",
        "enforcement_layer": manifest.get("enforcement_layer", "unknown"),
        "enforcement_pct": enforcement_pct,
        "agents_enforced": manifest.get("agents_enforced", 0),
        "agents_total": manifest.get("agents_total", 5),
        "mandatory_sources_read_required": manifest.get("mandatory_sources", []),
        "pdc_p0_count": len(p0_items),
        "execution_working_on": working_on,
        "execution_alignment_score": execution_alignment,
        "delivery_alignment_score": delivery_alignment,
        "alignment_threshold_pct": 80,
        "alignment_pass": execution_alignment >= 80,
        "p0_status": p0_board,
        "wp_feature_links": wp_links,
        "validation_results": manifest.get("validation_results", []),
    }
    (OUT / "ROADMAP_CONSUMPTION_REPORT.json").write_text(
        json.dumps(consumption_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    scoreboard = {
        "generated_at": now.isoformat(),
        "p0_total": len(p0_items),
        "features": p0_board,
        "summary": {
            "working_on": working_on,
            "partial": sum(1 for p in p0_board if p["status"] == "partial"),
            "not_started": sum(1 for p in p0_board if p["status"] == "not_started"),
        },
    }
    (OUT / "FEATURE_DELIVERY_SCOREBOARD.json").write_text(
        json.dumps(scoreboard, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    blockers_doc = {
        "generated_at": now.isoformat(),
        "count": len(blockers),
        "blockers": blockers,
    }
    (OUT / "EXECUTION_BLOCKERS.json").write_text(
        json.dumps(blockers_doc, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    yap_status = "unknown"
    if YAPILACAKLAR.exists():
        text = YAPILACAKLAR.read_text(encoding="utf-8", errors="ignore")
        yap_status = "references PDC" if "roadmap_priorities" in text or "F001" in text else "no PDC linkage"

    velocity_lines = [
        "# Delivery Velocity Report",
        "",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        "**Owner:** CEC",
        "",
        "---",
        "",
        "## Queue Status",
        "",
        f"- WP entries with PDC feature_id: **{len(wp_links)}**",
        f"- YAPILACAKLAR PDC linkage: **{yap_status}**",
        "",
        "## P0 Delivery",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| PDC P0 items | {len(p0_items)} |",
        f"| Execution working on | {working_on} |",
        f"| Delivery alignment | {delivery_alignment}% |",
        f"| Execution alignment (with enforcement) | {execution_alignment}% |",
        "",
        "## Per-Feature",
        "",
    ]
    for p in p0_board:
        velocity_lines.append(
            f"- **{p['feature_id']}** {p['name']} — {p['status']} ({p['signals_passed']}/{p['signals_total']} signals)"
        )
    velocity_lines += [
        "",
        "## Blockers",
        "",
    ]
    for b in blockers:
        velocity_lines.append(f"- [{b['severity'].upper()}] {b['message']}")
    if not blockers:
        velocity_lines.append("- None")
    velocity_lines.append("")
    (OUT / "DELIVERY_VELOCITY_REPORT.md").write_text("\n".join(velocity_lines), encoding="utf-8")

    align_lines = [
        "# Execution Alignment Report",
        "",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        "**Owner:** Chief Execution Council (CEC)  ",
        f"**Execution Alignment Score:** **{execution_alignment}%**  ",
        f"**Threshold:** 80% (CEO V3: below → Verdict ≤ REVIEW_REQUIRED)  ",
        f"**Status:** {'✅ PASS' if execution_alignment >= 80 else '⚠ BELOW THRESHOLD'}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"- PDC P0 items: **{len(p0_items)}**",
        f"- Execution working on: **{working_on}**",
        f"- Alignment: **{working_on}/{len(p0_items)} = {delivery_alignment}%** (delivery)",
        f"- Rule enforcement: **{manifest.get('enforcement_layer', '?')}** ({enforcement_pct}%)",
        "",
        "---",
        "",
        "## P0 Scoreboard",
        "",
        "| ID | Feature | Status | Signals |",
        "|----|---------|--------|---------|",
    ]
    for p in p0_board:
        align_lines.append(
            f"| {p['feature_id']} | {p['name']} | {p['status']} | {p['signals_passed']}/{p['signals_total']} |"
        )
    align_lines += [
        "",
        "---",
        "",
        "## Enforcement Layer",
        "",
        "Contract: `governance/execution/PDC_CONSUMPTION_CONTRACT.md`",
        "",
    ]
    for r in manifest.get("validation_results", []):
        icon = "✅" if r.get("enforced") else "❌"
        align_lines.append(f"- {icon} **{r.get('agent_id')}** — `{r.get('rule_file')}`")
    align_lines += [
        "",
        "---",
        "",
        "## CEO Action",
        "",
    ]
    if execution_alignment < 80:
        align_lines.append(
            "- **REVIEW_REQUIRED cap active** — link WPs to P0 feature IDs; start F002 execution"
        )
    else:
        align_lines.append("- Execution alignment acceptable — continue P0 delivery")
    align_lines.append("")
    (OUT / "EXECUTION_ALIGNMENT_REPORT.md").write_text("\n".join(align_lines), encoding="utf-8")

    print(f"   ✅ CEC audit — Execution Alignment {execution_alignment}% ({working_on}/{len(p0_items)} P0)")
    for name in [
        "EXECUTION_ALIGNMENT_REPORT.md",
        "ROADMAP_CONSUMPTION_REPORT.json",
        "FEATURE_DELIVERY_SCOREBOARD.json",
        "EXECUTION_BLOCKERS.json",
        "DELIVERY_VELOCITY_REPORT.md",
    ]:
        print(f"   ✅ governance/execution/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
