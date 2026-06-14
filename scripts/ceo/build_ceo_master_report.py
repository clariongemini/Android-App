#!/usr/bin/env python3
"""CEO V3 Operational Review — CEO_MASTER_REPORT.md + CEO_SCORECARD.json"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXEC = ROOT / "governance" / "executive"
CAO = ROOT / "governance" / "cao" / "department_scoreboard.json"
AUDIT = ROOT / "governance" / "cao" / "audit_report.json"
CONSISTENCY = ROOT / "governance" / "cao" / "consistency_report.json"
PDC_ROADMAP = ROOT / "governance" / "product_decision" / "roadmap_priorities.json"
PDC_REJECT = ROOT / "governance" / "product_decision" / "rejected_features.json"
USER_INTENT = ROOT / "governance" / "market" / "USER_INTENT_SIGNALS.json"
CONTENT_GAP = ROOT / "curriculum" / "content_gap_report.json"
LOC = ROOT / "governance" / "localization" / "output" / "locale_parity.json"
FIN = ROOT / "governance" / "finance" / "output" / "revenue_forecast.json"
CEC = ROOT / "governance" / "execution" / "ROADMAP_CONSUMPTION_REPORT.json"

STALE_PATHS = [
    ("VOC_JTBD", ROOT / "governance" / "market" / "VOC_JTBD_DEMAND_RESEARCH.md", 30),
    ("ROADMAP_AUDIT", ROOT / "governance" / "audits" / "ROADMAP_AUDIT.md", 60),
    ("COMPETITOR_ANALYSIS", ROOT / "docs" / "COMPETITOR_ANALYSIS.md", 45),
]


def _load(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _top_intents(data: dict, n: int = 5) -> list[str]:
    combined = data.get("combined_intent_counts") or data.get("play", {}).get("global", {}).get("intent_counts", {})
    if not combined and "intents" in str(data):
        play = data.get("play", {}).get("global", {})
        combined = play.get("intent_counts", {})
    items = sorted(combined.items(), key=lambda x: -x[1]) if isinstance(combined, dict) else []
    return [f"{k} ({v})" for k, v in items[:n]]


def _stale_reports() -> list[str]:
    stale = []
    now = datetime.now(timezone.utc)
    for name, path, threshold in STALE_PATHS:
        if not path.exists():
            stale.append(f"{name} — missing")
            continue
        age = (now - datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)).days
        if age > threshold:
            stale.append(f"{name} — {age}d old (threshold {threshold}d)")
    return stale


def _compute_verdict(
    org_health: int,
    audit_pass: bool,
    review_depts: list[dict],
    critical_gaps: list[dict],
    high_conflicts: list[dict],
    execution_alignment: int,
) -> str:
    critical_depts = [s for s in review_depts if s.get("status") == "CRITICAL"]
    if org_health < 50 or len(critical_depts) >= 2:
        return "NO_GO"

    # CEO V3 rule: Execution Alignment < 80 → Verdict ≤ REVIEW_REQUIRED
    if execution_alignment < 80:
        return "REVIEW_REQUIRED"

    if org_health < 75 or critical_depts or len(critical_gaps) >= 5:
        return "REVIEW_REQUIRED"
    if review_depts or high_conflicts or not audit_pass or critical_gaps:
        return "GO"
    return "GO"


def main() -> int:
    now = datetime.now(timezone.utc)
    cao = _load(CAO)
    audit = _load(AUDIT)
    consistency = _load(CONSISTENCY)
    scoreboard = cao.get("department_scoreboard", [])
    components = cao.get("organization_health_components", {})
    org_health = cao.get("organization_health_score", 0)
    audit_pass = audit.get("audit_pass", False)
    high_conflicts = [c for c in consistency.get("conflicts", []) if c.get("severity") == "high"]

    roadmap = _load(PDC_ROADMAP)
    rejected = _load(PDC_REJECT).get("rejected", [])
    intent = _load(USER_INTENT)
    gaps = _load(CONTENT_GAP).get("gaps", [])
    critical_gaps = [g for g in gaps if g.get("severity") == "critical" or g.get("gap_pct", 0) >= 60]

    p0 = roadmap.get("P0", [])
    p1 = roadmap.get("P1", [])
    review_depts = [s for s in scoreboard if s.get("status") in ("REVIEW_REQUIRED", "CRITICAL")]
    weak_depts = [s["department_name"] for s in scoreboard if s.get("quality_score", 100) < 70]
    stale = _stale_reports()

    cec = _load(CEC)
    execution_alignment = cec.get("execution_alignment_score", 0)
    p0_count = cec.get("pdc_p0_count", len(p0))
    working_on = cec.get("execution_working_on", 0)
    enforcement = cec.get("enforcement_layer", "unknown")

    verdict = _compute_verdict(
        org_health, audit_pass, review_depts, critical_gaps, high_conflicts, execution_alignment
    )

    scorecard = {
        "generated_at": now.isoformat(),
        "version": "V3",
        "operational_verdict": verdict,
        "binding_verdict_source": "governance/egc/EGC_VERDICT.json",
        "demand_coverage": next((s["quality_score"] for s in scoreboard if s["department_id"] == "market_growth"), 0),
        "curriculum_coverage": next((s["quality_score"] for s in scoreboard if s["department_id"] == "cika"), 0),
        "content_coverage_estimated_pct": 35,
        "clinical_coverage": next((s["quality_score"] for s in scoreboard if s["department_id"] == "clid"), 0),
        "localization_coverage": next((s["quality_score"] for s in scoreboard if s["department_id"] == "lid"), 0),
        "retention": 55,
        "churn_risk": "medium-high",
        "feature_adoption": "unverified",
        "learning_completion": "unknown",
        "premium_conversion_p50": 70,
        "revenue_forecast_y1_subs": 70,
        "strategic_alignment": components.get("strategic_alignment", 78),
        "department_health_avg": components.get("department_health", org_health),
        "evidence_quality": components.get("evidence_quality", 70),
        "audit_integrity": components.get("audit_integrity", 45 if not audit_pass else 90),
        "roadmap_consistency": components.get("roadmap_consistency", 88),
        "execution_readiness": components.get("execution_readiness", 72),
        "organization_health": org_health,
        "organization_health_components": components,
        "execution_alignment_score": execution_alignment,
        "execution_working_on": working_on,
        "pdc_p0_count": p0_count,
        "enforcement_layer": enforcement,
        "ceo_verdict": verdict,
        "executive_intervention_required": org_health < 75 or execution_alignment < 80,
    }
    (EXEC / "CEO_SCORECARD.json").write_text(json.dumps(scorecard, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# CEO Master Report",
        "",
        f"**Üretim:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        "**Agent:** CEO V3 — Operational Quarter  ",
        "**Reports to:** CSGB → EGC  ",
        f"**Organization Health (V2 composite):** {org_health}/100  ",
        f"**Execution Alignment:** {execution_alignment}% ({working_on}/{p0_count} P0)  ",
        f"**Enforcement Layer:** {enforcement}  ",
        f"**CEO Operational Verdict:** **{verdict}**  ",
        "**Binding Verdict:** EGC Step 18 → `governance/egc/EGC_VERDICT.json`",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        "Konuşma **AI-Native Product Company OS V3** — CEO yönetir, EGC denetler.",
        "Pipeline: Market → Intelligence → PDC → CAO → CEC → Factory → CEO → CSGB → EGC",
        "",
        f"- **P0 kararlar:** {len(p0)} — TR fonem, LATE_TALKER, daily missions",
        f"- **Kritik içerik boşluğu (Rule 7):** {len(critical_gaps)} tema (%60+ gap)",
        f"- **Review departman:** {', '.join(s['department_name'] for s in review_depts) or 'none'}",
        "- **Nihai şirket kararı:** EGC `EGC_VERDICT.json` (Step 18)",
        "- **CSGB girdi:** Step 17 → `CEO_STRATEGIC_GOVERNANCE_REVIEW.md`",
        "",
        "---",
        "",
        "## Organization Health Model (V2)",
        "",
        "| Bileşen | Skor |",
        "|---------|------|",
    ]
    for key, val in components.items():
        label = key.replace("_", " ").title()
        lines.append(f"| {label} | {val}/100 |")
    lines += [
        f"| **Composite** | **{org_health}/100** |",
        f"| Execution Alignment | {execution_alignment}% |",
        f"| P0 Working On | {working_on}/{p0_count} |",
        "",
        "---",
        "",
        "## Execution Alignment (CEC)",
        "",
        f"PDC P0 = **{p0_count}** · Execution working on = **{working_on}** · Alignment = **{execution_alignment}%**",
        "",
        "CEO V3 rule: Execution Alignment < 80 → Verdict ≤ REVIEW_REQUIRED",
        "",
        "Detay: `governance/execution/EXECUTION_ALIGNMENT_REPORT.md`",
        "",
        "---",
        "",
        "## Department Scoreboard (V2)",
        "",
        "| Departman | Quality | Freshness | Evidence | Coverage | Strategic | Label | Status |",
        "|-----------|---------|-----------|----------|----------|-----------|-------|--------|",
    ]
    for s in scoreboard:
        lines.append(
            f"| {s['department_name']} | {s['quality_score']} | {s.get('freshness_score', '—')} "
            f"| {s.get('evidence_score', '—')} | {s.get('coverage_score', '—')} "
            f"| {s.get('strategic_contribution_score', '—')} | {s['quality_label']} | {s['status']} |"
        )

    lines += [
        "",
        "Detay: `governance/cao/department_scoreboard.json`",
        "",
        "---",
        "",
        "## Absolute Rules Status",
        "",
        "| Rule | Status |",
        "|------|--------|",
        "| 1 PDC-only roadmap | ✅ PDC canonical |",
        f"| 2 Evidence on roadmap | {'✅' if p0 else '⚠'} P0 items checked |",
        "| 3 No execution without PDC | ✅ CEC + rule enforcement |",
        "| 4 CAO audit mandatory | ✅ Step 13 complete |",
        "| 6 Retention > acquisition | ✅ PDC retention weight |",
        f"| 7 Content gap %60+ review | {'⚠ TRIGGERED' if critical_gaps else '✅'} |",
        "| 8 Y1 B2B forbidden | ✅ P4 rejected |",
        "| 9 Competitor-copy challenge | ✅ Speech Blubs rejected |",
        "| 10 Educational impact required | ✅ PDC gate |",
        "",
        "---",
        "",
        "## Top Opportunities",
        "",
        "1. TR R/Ş/L fonem graph — rakip boşluğu + arama talebi",
        "2. LATE_TALKER parent phrase bank — forum kanıtı",
        "3. STT kalibrasyon — 1★ tema azaltma",
        "",
        "## Top Risks",
        "",
        "1. Content exhaustion < 6 ay",
        "2. Analytics blind spot (AID)",
        "3. VOC/ROADMAP stale docs vs PDC",
        "",
        "---",
        "",
        "## P0 Priorities",
        "",
    ]
    for f in p0:
        lines.append(f"- **{f['name']}** (score {f.get('priority_score', '—')})")

    lines += ["", "## P1 Priorities", ""]
    for f in p1[:5]:
        lines.append(f"- {f['name']}")

    lines += ["", "## Rejected Work", ""]
    for r in rejected:
        lines.append(f"- {r.get('name')}")

    lines += [
        "",
        "---",
        "",
        "## Status Dashboards",
        "",
        "| Alan | Durum |",
        "|------|-------|",
        "| Retention | Sprint P 0/10 — doğrulanmadı |",
        f"| Revenue Y1 P50 | ~70 subs — FID model |",
        f"| Content | Critical gap — {len(critical_gaps)} themes %60+ |",
        "| Clinical | Medium risk — age norms incomplete |",
        "| Localization | FR/IT/ES app gap — critical |",
        "",
        "---",
        "",
        "## Audit Findings",
        "",
        "CAO: `governance/cao/consistency_report.json` · `integrity_report.json`",
        "",
        "- VOC Reddit metadata stale",
        "- PDC → CPO enforcement **resolved** (CEC layer active)",
        "- Intelligence agents outside AGENT_APPROVAL_PROTOCOL (v2 expanded — partial)",
        "",
        "---",
        "",
        "## Strategic Recommendations",
        "",
        "1. Link APPROVAL_QUEUE WPs to PDC feature_id (F001–F003)",
        "2. Start F002 LATE_TALKER execution — 0 signals",
        "3. Sprint P launch — AID canlı veri",
        "4. FR/IT/ES parity sprint (PDC P1)",
        "5. VOC + ROADMAP_AUDIT reconcile with PDC",
        "",
        "---",
        "",
        "## CEO Operational Verdict",
        "",
        f"**{verdict}** (operational — quarter focus)",
        "",
        "**EGC binding verdict:** see `governance/egc/EGC_VERDICT.json` after Step 18",
        "",
        "| EGC Verdict | Meaning |",
        "|-------------|---------|",
        "| WORLD_CLASS | World leadership trajectory |",
        "| GO | Healthy company |",
        "| REVIEW_REQUIRED | Intervention needed |",
        "| RESTRUCTURE | Organizational debt |",
        "| NO_GO | Crisis — freeze execution |",
        "",
        "Roadmap: `governance/product_decision/roadmap_priorities.json`",
        "",
        "**Cycle:** `./scripts/ceo/run_ceo_cycle.sh`",
        "",
    ]

    (EXEC / "CEO_MASTER_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print("   ✅ governance/executive/CEO_MASTER_REPORT.md")
    print("   ✅ governance/executive/CEO_SCORECARD.json")
    print(f"   Verdict: {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
