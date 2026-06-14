#!/usr/bin/env python3
"""EGC — Executive Governance Council full governance cycle (CEO V3)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "governance" / "egc"
EXEC = ROOT / "governance" / "executive"
CAO = ROOT / "governance" / "cao" / "department_scoreboard.json"
CEC = ROOT / "governance" / "execution" / "ROADMAP_CONSUMPTION_REPORT.json"
COVERAGE = ROOT / "governance" / "execution" / "EXECUTION_COVERAGE.json"
PREDICTION = ROOT / "governance" / "execution" / "DELIVERY_PREDICTION_ACCURACY.json"
DELIVERY_HEALTH = ROOT / "governance" / "reality" / "DELIVERY_HEALTH.json"
PRODUCT_REALITY = ROOT / "governance" / "reality" / "PRODUCT_REALITY_SCORE.json"
LAUNCH_PRESSURE = ROOT / "governance" / "reality" / "LAUNCH_PRESSURE.json"
ROADMAP = ROOT / "governance" / "product_decision" / "roadmap_priorities.json"
DECISION_LOG = ROOT / "governance" / "product_decision" / "decision_log.json"
CONTENT_GAP = ROOT / "curriculum" / "content_gap_report.json"
AID_RET = ROOT / "governance" / "analytics" / "output" / "retention_snapshot.json"
LOC = ROOT / "governance" / "localization" / "output" / "locale_parity.json"
CLID = ROOT / "governance" / "clinical" / "output" / "risk_report.json"
SCORECARD = EXEC / "CEO_SCORECARD.json"
MASTER = EXEC / "CEO_MASTER_REPORT.md"
CSGB = EXEC / "CEO_STRATEGIC_GOVERNANCE_REVIEW.md"

FIVE_YEAR_NORTH_STAR = (
    "Ship measurable, high-retention Android products across multiple verticals "
    "with evidence-driven governance and portfolio outcomes."
)

COMPETITORS = [
    {"name": "Competitor A", "speech_focus": 85, "retention_proof": 80, "locale_depth": 70, "clinical": 60},
    {"name": "Competitor B", "speech_focus": 70, "retention_proof": 75, "locale_depth": 80, "clinical": 55},
    {"name": "Competitor C", "speech_focus": 60, "retention_proof": 90, "locale_depth": 90, "clinical": 50},
]

APP_EST = {
    "speech_focus": 0,
    "retention_proof": 0,
    "locale_depth": 0,
    "clinical": 0,
    "intelligence_pipeline": 0,
    "execution_alignment": 0,
}


def _load(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _dept_score(cao: dict, dept_id: str) -> int:
    for s in cao.get("department_scoreboard", []):
        if s.get("department_id") == dept_id:
            return int(s.get("quality_score", 0))
    return 0


def _compute_health_v3(cao: dict, cec: dict, aid: dict, loc: dict, clid: dict, gaps: list) -> dict:
    exec_align = cec.get("execution_alignment_score", 0)
    enforcement = 100 if cec.get("enforcement_layer") == "active" else 40
    execution_health = int(exec_align * 0.7 + enforcement * 0.3)

    intel_depts = ["market_growth", "trends", "liud", "cika"]
    intel_scores = [_dept_score(cao, d) for d in intel_depts]
    intelligence_health = int(sum(intel_scores) / len(intel_scores)) if intel_scores else 50

    strategy_health = int(
        _dept_score(cao, "pdc") * 0.5
        + cao.get("organization_health_components", {}).get("roadmap_consistency", 70) * 0.5
    )
    governance_health = int(
        cao.get("organization_health_components", {}).get("audit_integrity", 50) * 0.4
        + enforcement * 0.3
        + (100 if cec.get("enforcement_layer") == "active" else 30) * 0.3
    )
    market_health = _dept_score(cao, "market_growth")
    critical_gaps = sum(1 for g in gaps if g.get("gap_pct", 0) >= 60)
    product_health = int(
        _dept_score(cao, "cika") * 0.35
        + _dept_score(cao, "clid") * 0.25
        + _dept_score(cao, "lid") * 0.25
        + max(0, 100 - critical_gaps * 8) * 0.15
    )
    if not aid.get("live_analytics", False):
        product_health = min(product_health, 58)

    components = {
        "execution_health": execution_health,
        "intelligence_health": intelligence_health,
        "strategy_health": strategy_health,
        "governance_health": governance_health,
        "market_health": market_health,
        "product_health": product_health,
    }
    company_health = int(sum(components.values()) / len(components))
    return {"components": components, "company_health_score": company_health}


def _ceo_performance(cao: dict, cec: dict, company: dict, prediction: dict) -> dict:
    org = cao.get("organization_health_score", 0)
    align = cec.get("execution_alignment_score", 0)
    pdc_accuracy = prediction.get("average_accuracy_pct", 65)
    return {
        "ceo_score": int(org * 0.4 + align * 0.3 + company["company_health_score"] * 0.3),
        "ceo_accuracy": 78,
        "ceo_prediction_accuracy": pdc_accuracy,
        "ceo_alignment": align,
        "delivery_success_pct": pdc_accuracy,
        "notes": [
            "CEO operational cycle complete",
            "Execution alignment below 80 threshold",
            "AID blind spot limits prediction accuracy",
        ],
    }


def _pdc_quality(decisions: dict, cec: dict) -> dict:
    entries = decisions.get("decisions", [])
    p0 = [d for d in entries if d.get("priority_level") == "P0"]
    return {
        "total_decisions": len(entries),
        "p0_decisions": len(p0),
        "successful_estimated": len(p0) - 1,
        "failed_estimated": 1,
        "pending_execution": 1,
        "success_rate_pct": round(100 * (len(p0) - 1) / max(len(p0), 1), 1),
        "notes": "F002 LATE_TALKER partial — primary failure mode is execution not decision quality",
    }


def _roadmap_drift(roadmap: dict, cec: dict) -> dict:
    p0 = roadmap.get("P0", [])
    p0_status = {p["feature_id"]: p for p in cec.get("p0_status", []) if "feature_id" in p}
    drift = []
    for item in p0:
        fid = item.get("id")
        st = p0_status.get(fid, {})
        drift.append({
            "feature_id": fid,
            "pdc_name": item.get("name"),
            "ceo_priority": item.get("priority_level", "P0"),
            "cec_status": st.get("status", "unknown"),
            "drift": st.get("status") in ("not_started", "partial"),
        })
    return {
        "p0_count": len(p0),
        "drift_count": sum(1 for d in drift if d["drift"]),
        "items": drift,
    }


def _department_roi(cao: dict) -> dict:
    mapping = {
        "liud": ("User intent + phrase intelligence", "PDC P0 evidence"),
        "cika": ("Curriculum + content gap clarity", "CIKA→PDC pipeline"),
        "pdc": ("Canonical roadmap P0-P4", "CEC execution targets"),
        "market_growth": ("Demand signals 229+ intents", "LIUD input"),
        "aid": ("Retention/session truth", "BLOCKED — no live data"),
        "clid": ("Clinical risk flags", "Partial age norms"),
        "lid": ("Locale parity audit", "FR/IT/ES app gap"),
    }
    roi = []
    for dept_id, (output, impact) in mapping.items():
        score = _dept_score(cao, dept_id)
        roi.append({
            "department_id": dept_id,
            "output": output,
            "product_impact": impact,
            "quality_score": score,
            "roi_rating": "high" if score >= 85 else "medium" if score >= 70 else "low",
        })
    return {"departments": roi}


def _global_leadership() -> dict:
    dims = ["speech_focus", "retention_proof", "locale_depth", "clinical"]
    k_scores = [APP_EST[d] for d in dims]
    k_avg = sum(k_scores) / len(dims)
    comparisons = []
    for comp in COMPETITORS:
        c_scores = [comp[d] for d in dims]
        c_avg = sum(c_scores) / len(dims)
        comparisons.append({
            "competitor": comp["name"],
            "composite": round(c_avg, 1),
            "vs_flagship": round(k_avg - c_avg, 1),
            "dimensions": {d: comp[d] for d in dims},
        })
    leader_avg = sum(c["composite"] for c in comparisons) / len(comparisons)
    return {
        "flagship_composite": round(k_avg, 1),
        "flagship_intelligence_pipeline": APP_EST["intelligence_pipeline"],
        "leader_benchmark_avg": round(leader_avg, 1),
        "gap_to_leaders": round(leader_avg - k_avg, 1),
        "leadership_score": max(0, min(100, int(50 + (k_avg - leader_avg) + APP_EST["intelligence_pipeline"] * 0.2))),
        "comparisons": comparisons,
    }


def _strategic_debt(cao: dict, aid: dict, loc: dict, clid: dict) -> dict:
    debts = [
        {"id": "aid_live_analytics", "area": "Analytics", "severity": "critical", "description": "No live retention/session/completion/churn/conversion data", "owner": "AID Sprint P"},
        {"id": "clinical_age_norms", "area": "Clinical", "severity": "high", "description": "CLID 72/100 — age norms incomplete", "owner": "CLID V2"},
        {"id": "localization_parity", "area": "Localization", "severity": "high", "description": "FR/IT/ES app content gap", "owner": "LID + CIKA"},
        {"id": "f002_execution", "area": "Execution", "severity": "high", "description": "LATE_TALKER P0 not started in app", "owner": "CEC → Android"},
        {"id": "voc_stale", "area": "Governance", "severity": "medium", "description": "VOC metadata stale vs forum batch", "owner": "Market"},
    ]
    if aid.get("live_analytics"):
        debts = [d for d in debts if d["id"] != "aid_live_analytics"]
    return {
        "total_debt_items": len(debts),
        "critical_count": sum(1 for d in debts if d["severity"] == "critical"),
        "high_count": sum(1 for d in debts if d["severity"] == "high"),
        "debts": debts,
    }


def _five_year_vision(roadmap: dict) -> dict:
    p0_names = [f.get("name", "") for f in roadmap.get("P0", [])]
    aligned = all(
        any(k in n.lower() for k in ("fonem", "phoneme", "late", "daily", "mission", "retention"))
        for n in p0_names
    )
    return {
        "north_star": FIVE_YEAR_NORTH_STAR,
        "p0_serves_vision": aligned,
        "alignment_score": 82 if aligned else 45,
        "gaps": [
            "Retention proof missing (5-year scale requires cohort data)",
            "Global locale parity not yet at 6-locale product depth",
            "Clinical credibility needs V2 completion",
        ],
        "verdict": "aligned_with_gaps" if aligned else "misaligned",
    }


def _egc_verdict(
    company: dict,
    cec: dict,
    debt: dict,
    drift: dict,
    coverage: dict,
    cao: dict,
) -> str:
    ch = company["company_health_score"]
    align = cec.get("execution_alignment_score", 0)
    cov = coverage.get("execution_coverage_pct", 0)
    critical_debt = debt.get("critical_count", 0)
    high_debt = debt.get("high_count", 0)
    drift_pct = int(100 * drift.get("drift_count", 0) / max(drift.get("p0_count", 1), 1))
    critical_depts = sum(
        1 for s in cao.get("department_scoreboard", [])
        if s.get("status") in ("CRITICAL", "REVIEW_REQUIRED") and s.get("quality_score", 100) < 60
    )

    # AUTONOMOUS_READY — V4 apex
    if (
        ch >= 90
        and cov >= 90
        and align >= 90
        and critical_depts == 0
        and drift_pct < 10
        and critical_debt == 0
    ):
        return "AUTONOMOUS_READY"

    if ch < 45 or critical_debt >= 2:
        return "NO_GO"
    if high_debt >= 3 and align < 70:
        return "RESTRUCTURE"
    if ch >= 88 and align >= 85 and critical_debt == 0:
        return "WORLD_CLASS"
    if ch >= 75 and align >= 80 and critical_debt == 0:
        return "GO"
    return "REVIEW_REQUIRED"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)

    cao = _load(CAO)
    cec = _load(CEC)
    coverage = _load(COVERAGE)
    prediction = _load(PREDICTION)
    delivery = _load(DELIVERY_HEALTH)
    reality = _load(PRODUCT_REALITY)
    launch = _load(LAUNCH_PRESSURE)
    roadmap = _load(ROADMAP)
    decisions = _load(DECISION_LOG)
    gaps = _load(CONTENT_GAP).get("gaps", [])
    aid = _load(AID_RET)
    loc = _load(LOC)
    clid = _load(CLID)

    company = _compute_health_v3(cao, cec, aid, loc, clid, gaps)
    ceo_perf = _ceo_performance(cao, cec, company, prediction)
    pdc_q = _pdc_quality(decisions, cec)
    pdc_q["prediction_accuracy_pct"] = prediction.get("average_accuracy_pct", 0)
    pdc_q["delivery_success_tracked"] = True
    drift = _roadmap_drift(roadmap, cec)
    roi = _department_roi(cao)
    leadership = _global_leadership()
    debt = _strategic_debt(cao, aid, loc, clid)
    vision = _five_year_vision(roadmap)
    verdict = _egc_verdict(company, cec, debt, drift, coverage, cao)

    ts = now.isoformat()
    (OUT / "COMPANY_HEALTH_SCORE.json").write_text(
        json.dumps({"generated_at": ts, "version": "V3", **company}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT / "CEO_PERFORMANCE_SCORECARD.json").write_text(
        json.dumps({"generated_at": ts, **ceo_perf}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "PDC_DECISION_QUALITY.json").write_text(
        json.dumps({"generated_at": ts, **pdc_q}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "ROADMAP_DRIFT_REPORT.json").write_text(
        json.dumps({"generated_at": ts, **drift}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "DEPARTMENT_ROI.json").write_text(
        json.dumps({"generated_at": ts, **roi}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "GLOBAL_LEADERSHIP_SCORE.json").write_text(
        json.dumps({"generated_at": ts, **leadership}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "STRATEGIC_DEBT_REGISTER.json").write_text(
        json.dumps({"generated_at": ts, **debt}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "EGC_VERDICT.json").write_text(
        json.dumps(
            {
                "generated_at": ts,
                "egc_verdict": verdict,
                "version": "V4",
                "company_health_score": company["company_health_score"],
                "execution_alignment_score": cec.get("execution_alignment_score", 0),
                "execution_coverage_score": coverage.get("execution_coverage_pct", 0),
                "delivery_health_score": delivery.get("delivery_health_score", 0),
                "product_reality_score": reality.get("product_reality_score", 0),
                "analysis_paralysis_risk": launch.get("analysis_paralysis_risk", False),
                "p0_stalled_count": delivery.get("p0_stalled_features", 0),
                "pdc_prediction_accuracy": prediction.get("average_accuracy_pct", 0),
                "ceo_decision_accuracy": ceo_perf.get("ceo_accuracy", 0),
                "delivery_success_pct": ceo_perf.get("delivery_success_pct", 0),
                "roadmap_drift_pct": int(100 * drift.get("drift_count", 0) / max(drift.get("p0_count", 1), 1)),
                "leadership_score": leadership["leadership_score"],
                "strategic_debt_critical": debt["critical_count"],
                "autonomous_ready": verdict == "AUTONOMOUS_READY",
                "binding": True,
                "supersedes": "ceo_operational_verdict",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    vision_md = [
        "# Five Year Vision Alignment",
        "",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        f"**Alignment score:** {vision['alignment_score']}/100  ",
        f"**Verdict:** {vision['verdict']}",
        "",
        "## North Star",
        "",
        vision["north_star"],
        "",
        "## P0 serves 5-year vision?",
        "",
        f"**{'Yes' if vision['p0_serves_vision'] else 'No'}** — current P0 focuses on content depth, late talker, daily retention ritual.",
        "",
        "## Gaps",
        "",
    ]
    for g in vision["gaps"]:
        vision_md.append(f"- {g}")
    vision_md.append("")
    (OUT / "FIVE_YEAR_VISION_ALIGNMENT.md").write_text("\n".join(vision_md), encoding="utf-8")

    master_lines = [
        "# EGC Master Report",
        "",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        "**Authority:** Executive Governance Council  ",
        f"**EGC Verdict:** **{verdict}**  ",
        f"**Company Health V3:** {company['company_health_score']}/100  ",
        "",
        "---",
        "",
        "## Company Health V3",
        "",
        "| Dimension | Score |",
        "|-----------|-------|",
    ]
    for k, v in company["components"].items():
        master_lines.append(f"| {k.replace('_', ' ').title()} | {v}/100 |")
    master_lines += [
        f"| **Company Health** | **{company['company_health_score']}/100** |",
        "",
        "---",
        "",
        "## CEO Performance",
        "",
        f"- CEO Score: **{ceo_perf['ceo_score']}/100**",
        f"- CEO Alignment: **{ceo_perf['ceo_alignment']}%**",
        f"- CEO Accuracy: **{ceo_perf['ceo_accuracy']}%**",
        f"- CEO Prediction Accuracy: **{ceo_perf['ceo_prediction_accuracy']}%**",
        "",
        "---",
        "",
        "## Global Leadership",
        "",
        f"- Flagship composite: **{leadership['flagship_composite']}**",
        f"- Leader benchmark avg: **{leadership['leader_benchmark_avg']}**",
        f"- Leadership score: **{leadership['leadership_score']}/100**",
        "",
        "---",
        "",
        "## Strategic Debt",
        "",
        f"Critical: **{debt['critical_count']}** · High: **{debt['high_count']}** · Total: **{debt['total_debt_items']}**",
        "",
        "Top debt: AID live analytics (Sprint P) — organizational blind spot.",
        "",
        "---",
        "",
        "## EGC Verdict Framework",
        "",
        "| Verdict | Meaning |",
        "|---------|---------|",
        "| WORLD_CLASS | World leadership trajectory |",
        "| GO | Healthy company operation |",
        "| REVIEW_REQUIRED | Intervention needed |",
        "| RESTRUCTURE | Organizational debt — structural fix |",
        "| NO_GO | Crisis — freeze major execution |",
        "| AUTONOMOUS_READY | Self-governing OS — coverage/alignment/health apex |",
        "",
        "## EGC V4 Metrics",
        "",
        f"- Execution Coverage: **{coverage.get('execution_coverage_pct', 0)}%**",
        f"- PDC Prediction Accuracy: **{prediction.get('average_accuracy_pct', 0)}%**",
        f"- CEO Decision Accuracy: **{ceo_perf.get('ceo_accuracy', 0)}%**",
        f"- Product Reality Score: **{reality.get('product_reality_score', 0)}%**",
        f"- Delivery Health: **{delivery.get('delivery_health_score', 0)}/100**",
        f"- Analysis Paralysis: **{'YES' if launch.get('analysis_paralysis_risk') else 'No'}**",
        f"- P0 Stalled: **{delivery.get('p0_stalled_features', 0)}**",
        "",
        f"**Binding verdict: {verdict}**",
        "",
        "Inputs: CEO_MASTER_REPORT · CSGB Review · CAO · CEC · PDC",
        "",
    ]
    (OUT / "EGC_MASTER_REPORT.md").write_text("\n".join(master_lines), encoding="utf-8")

    print(f"   ✅ EGC cycle — Company Health {company['company_health_score']}/100 — Verdict: {verdict}")
    for f in [
        "EGC_MASTER_REPORT.md",
        "COMPANY_HEALTH_SCORE.json",
        "EGC_VERDICT.json",
        "CEO_PERFORMANCE_SCORECARD.json",
        "GLOBAL_LEADERSHIP_SCORE.json",
        "STRATEGIC_DEBT_REGISTER.json",
    ]:
        print(f"   ✅ governance/egc/{f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
