#!/usr/bin/env python3
"""CEO V4 — CEO_AUTONOMOUS_REPORT.md (autonomous operating system summary)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXEC = ROOT / "governance" / "executive"
EGC_VERDICT = ROOT / "governance" / "egc" / "EGC_VERDICT.json"
COMPANY = ROOT / "governance" / "egc" / "COMPANY_HEALTH_SCORE.json"
COVERAGE = ROOT / "governance" / "execution" / "EXECUTION_COVERAGE.json"
UNOWNED = ROOT / "governance" / "execution" / "UNOWNED_GAPS.json"
ESCALATION = ROOT / "governance" / "execution" / "ESCALATION_REPORT.md"
PREDICTION = ROOT / "governance" / "execution" / "DELIVERY_PREDICTION_ACCURACY.json"
MEMORY = ROOT / "governance" / "memory" / "ORGANIZATIONAL_MEMORY.json"
GENERATED = ROOT / "governance" / "cdid" / "GENERATED_WORK_PACKAGES.json"
CEC = ROOT / "governance" / "execution" / "ROADMAP_CONSUMPTION_REPORT.json"
SCORECARD = EXEC / "CEO_SCORECARD.json"


def _load(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    now = datetime.now(timezone.utc)
    coverage = _load(COVERAGE)
    unowned = _load(UNOWNED)
    prediction = _load(PREDICTION)
    memory = _load(MEMORY)
    generated = _load(GENERATED)
    cec = _load(CEC)
    scorecard = _load(SCORECARD)
    company = _load(COMPANY)
    egc = _load(EGC_VERDICT)

    wps = generated.get("work_packages", [])
    auto_wps = [w for w in wps if w.get("generated_by") == "CDID"]
    pending_wps = [w for w in auto_wps if w.get("status") == "pending"]

    lines = [
        "# CEO Autonomous Report",
        "",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        "**Agent:** CEO V4 — Autonomous Product Company OS  ",
        "**Principle:** Hiçbir kritik bulgu aksiyonsuz kalamaz  ",
        "",
        "---",
        "",
        "## Autonomous Loop Status",
        "",
        "| Layer | Status |",
        "|-------|--------|",
        f"| CDID Work Packages | **{len(auto_wps)}** auto-generated ({len(pending_wps)} pending) |",
        f"| Execution Coverage | **{coverage.get('execution_coverage_pct', 0)}%** (target ≥ 90%) |",
        f"| Execution Alignment | **{cec.get('execution_alignment_score', 0)}%** |",
        f"| Unowned RED FLAGS | **{unowned.get('red_flag_count', 0)}** |",
        f"| PDC Prediction Accuracy | **{prediction.get('average_accuracy_pct', 0)}%** avg |",
        f"| Organizational Memory | **{memory.get('decision_entries', 0)}** decisions tracked |",
        "",
        "---",
        "",
        "## CDID Auto Work Packages",
        "",
        "Her P0/P1 → Research · Content · Android · QA · Release zinciri.",
        "",
        "| WP | Feature | Title | Agent | Status |",
        "|----|---------|-------|-------|--------|",
    ]
    for w in sorted(auto_wps, key=lambda x: x["wp_id"])[:15]:
        lines.append(
            f"| {w['wp_id']} | {w['feature_id']} | {w['title'][:40]} | {w['agent']} | {w.get('status')} |"
        )
    if len(auto_wps) > 15:
        lines.append(f"| … | | +{len(auto_wps) - 15} more | | |")

    lines += [
        "",
        "Full list: `governance/cdid/GENERATED_WORK_PACKAGES.json`",
        "",
        "---",
        "",
        "## Learning Loop",
        "",
    ]
    for r in prediction.get("records", []):
        lines.append(
            f"- **{r['feature_id']}** expected retention +{r['expected_retention_impact_pct']}% "
            f"→ actual +{r['actual_retention_impact_pct']}% · accuracy {r['prediction_accuracy_pct']}%"
        )

    esc_snip = ""
    if ESCALATION.exists():
        esc_snip = ESCALATION.read_text(encoding="utf-8")
        active = esc_snip.count("## [")
    else:
        active = 0

    lines += [
        "",
        "---",
        "",
        "## Escalations",
        "",
        f"Active: **{active}** — see `governance/execution/ESCALATION_REPORT.md`",
        "",
        "---",
        "",
        "## Company Health & Verdict",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Company Health V3 | {company.get('company_health_score', scorecard.get('organization_health', '?'))}/100 |",
        f"| CEO Operational | {scorecard.get('ceo_verdict', scorecard.get('operational_verdict', '?'))} |",
        f"| EGC Binding | {egc.get('egc_verdict', 'pending Step 20')} |",
        "",
        "---",
        "",
        "## V4 Verdict Model",
        "",
        "WORLD_CLASS · GO · REVIEW_REQUIRED · RESTRUCTURE · NO_GO · **AUTONOMOUS_READY**",
        "",
        "**AUTONOMOUS_READY** when: Company Health ≥ 90 · Coverage ≥ 90 · Alignment ≥ 90 · Critical Depts = 0 · Drift < 10%",
        "",
        "---",
        "",
        "## Next Autonomous Actions",
        "",
        "1. Execute pending CDID WPs (F002 chain priority)",
        "2. Activate AID Sprint P — close analytics blind spot",
        "3. Raise Execution Coverage from "
        f"{coverage.get('execution_coverage_pct', 0)}% → 90%",
        "",
        "**Cycle:** `./scripts/ceo/run_ceo_cycle.sh`",
        "",
    ]

    (EXEC / "CEO_AUTONOMOUS_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print("   ✅ governance/executive/CEO_AUTONOMOUS_REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
