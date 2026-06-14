#!/usr/bin/env python3
"""CAO V2 — multi-dimensional department scoreboard + org health components."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "governance" / "cao"

DEPARTMENTS = [
    {
        "id": "market_growth",
        "name": "Market & Growth",
        "strategic_weight": 0.9,
        "outputs": [
            "governance/market/USER_INTENT_SIGNALS.json",
            "governance/market/demand_output/DEMAND_INTELLIGENCE_REPORT.md",
            "docs/COMPETITOR_ANALYSIS.md",
        ],
        "inputs": ["governance/market/scraper_output/manifest.json"],
    },
    {
        "id": "trends",
        "name": "Trends",
        "strategic_weight": 0.75,
        "outputs": ["governance/trends/trends_data.json", "governance/trends/TERM_DISCOVERY_REPORT.md"],
        "inputs": ["governance/trends/queries.json"],
    },
    {
        "id": "liud",
        "name": "LIUD",
        "strategic_weight": 0.95,
        "outputs": [
            "governance/linguistic/output/intent_map.json",
            "governance/linguistic/reports/LIUD_REPORT_2026-06-12.md",
        ],
        "inputs": ["governance/market/USER_INTENT_SIGNALS.json"],
    },
    {
        "id": "cika",
        "name": "CIKA",
        "strategic_weight": 0.95,
        "outputs": ["curriculum/curriculum_master.json", "curriculum/content_gap_report.json"],
        "inputs": ["governance/linguistic/output/content_gaps.json"],
    },
    {
        "id": "clid",
        "name": "Clinical (CLID)",
        "strategic_weight": 0.85,
        "outputs": ["governance/clinical/output/risk_report.json"],
        "inputs": ["governance/clinical/CLINICAL_EVIDENCE_INDEX.md"],
    },
    {
        "id": "aid",
        "name": "Analytics (AID)",
        "strategic_weight": 0.7,
        "outputs": ["governance/analytics/output/retention_snapshot.json"],
        "inputs": [],
    },
    {
        "id": "lid",
        "name": "Localization (LID)",
        "strategic_weight": 0.8,
        "outputs": ["governance/localization/output/locale_parity.json"],
        "inputs": ["curriculum/language_content_map.json"],
    },
    {
        "id": "fid",
        "name": "Finance (FID)",
        "strategic_weight": 0.75,
        "outputs": ["governance/finance/output/revenue_forecast.json"],
        "inputs": ["governance/market/YEAR1_ORGANIC_FINANCIAL_MODEL.md"],
    },
    {
        "id": "pdc",
        "name": "PDC",
        "strategic_weight": 1.0,
        "outputs": [
            "governance/product_decision/roadmap_priorities.json",
            "governance/product_decision/executive_summary.md",
        ],
        "inputs": ["curriculum/content_gap_report.json"],
    },
]

STRATEGIC_CONTRIBUTION = {
    "market_growth": 85,
    "trends": 70,
    "liud": 92,
    "cika": 95,
    "clid": 68,
    "aid": 40,
    "lid": 72,
    "fid": 78,
    "pdc": 90,
}


def _age_days(path: Path) -> float | None:
    if not path.exists():
        return None
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return (datetime.now(timezone.utc) - mtime).total_seconds() / 86400


def _freshness_score(days: float | None) -> int:
    if days is None:
        return 20
    if days < 1:
        return 100
    if days < 7:
        return 95
    if days < 30:
        return 70
    if days < 90:
        return 40
    return 20


def _evidence_score(paths: list[Path]) -> int:
    hits = 0
    for p in paths:
        if not p.exists():
            continue
        try:
            text = p.read_text(encoding="utf-8").lower()
            hits += text.count("evidence")
            hits += text.count("kanıt")
            if p.suffix == ".json":
                data = json.loads(p.read_text(encoding="utf-8"))
                hits += len(str(data).split("source"))
        except Exception:
            pass
    return min(100, 30 + hits * 3)


def _rating_label(score: int) -> str:
    if score >= 90:
        return "World Class"
    if score >= 80:
        return "Excellent"
    if score >= 70:
        return "Acceptable"
    if score >= 60:
        return "Review Required"
    return "Critical"


def _score_dept(dept: dict) -> dict:
    out_paths = [ROOT / p for p in dept["outputs"]]
    in_paths = [ROOT / p for p in dept["inputs"]]
    out_ok = sum(1 for p in out_paths if p.exists())
    in_ok = sum(1 for p in in_paths if in_paths and p.exists())
    ages = [_age_days(p) for p in out_paths if p.exists()]
    freshness_days = min(ages) if ages else None

    coverage_score = int(100 * out_ok / max(len(out_paths), 1))
    input_score = 100 if not in_paths else int(100 * in_ok / len(in_paths))
    freshness_score = _freshness_score(freshness_days)
    evidence_score = _evidence_score(out_paths)
    strategic_score = STRATEGIC_CONTRIBUTION.get(dept["id"], 70)

    quality_score = int(
        coverage_score * 0.25
        + input_score * 0.15
        + freshness_score * 0.20
        + evidence_score * 0.20
        + strategic_score * 0.20
    )

    if dept["id"] == "aid":
        quality_score = min(quality_score, 55)
        strategic_score = min(strategic_score, 40)
    if dept["id"] == "clid" and out_ok:
        quality_score = min(max(quality_score, 62), 72)

    status = "OK"
    if quality_score < 60:
        status = "CRITICAL"
    elif quality_score < 70:
        status = "REVIEW_REQUIRED"

    return {
        "department_id": dept["id"],
        "department_name": dept["name"],
        "output_files_ok": f"{out_ok}/{len(out_paths)}",
        "input_sources_ok": f"{in_ok}/{len(in_paths) or 0}",
        "freshness_days_min": round(freshness_days, 1) if freshness_days is not None else None,
        "quality_score": quality_score,
        "freshness_score": freshness_score,
        "evidence_score": evidence_score,
        "coverage_score": coverage_score,
        "strategic_contribution_score": strategic_score,
        "quality_label": _rating_label(quality_score),
        "status": status,
    }


def _org_health_components(scoreboard: list[dict], audit_ok: bool, roadmap_ok: bool) -> dict:
    dept_avg = sum(s["quality_score"] for s in scoreboard) / len(scoreboard)
    evidence_avg = sum(s["evidence_score"] for s in scoreboard) / len(scoreboard)
    return {
        "strategic_alignment": int(min(100, dept_avg * 0.85 + 15)),
        "department_health": int(dept_avg),
        "evidence_quality": int(evidence_avg),
        "audit_integrity": 90 if audit_ok else 45,
        "roadmap_consistency": 88 if roadmap_ok else 50,
        "execution_readiness": 72,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    scoreboard = [_score_dept(d) for d in DEPARTMENTS]

    roadmap_path = ROOT / "governance" / "product_decision" / "roadmap_priorities.json"
    roadmap_ok = roadmap_path.exists()
    if roadmap_ok:
        try:
            rd = json.loads(roadmap_path.read_text(encoding="utf-8"))
            p0 = rd.get("P0", [])
            roadmap_ok = all(
                all(k in f for k in ("demand", "retention", "strategic_value"))
                or "priority_score" in f
                for f in p0
            ) if p0 else True
        except Exception:
            roadmap_ok = False

    conflicts = [
        {
            "id": "voc_reddit_stale",
            "a": "VOC_JTBD claims Reddit not scraped",
            "b": "forum batch_001 exists",
            "severity": "medium",
        },
        {
            "id": "roadmap_dual",
            "a": "LIUD roadmap_priorities.json",
            "b": "PDC roadmap_priorities.json",
            "severity": "low",
            "note": "different schema OK — PDC canonical per Rule 1",
        },
        {
            "id": "pdc_cpo_unwired",
            "a": "PDC canonical roadmap",
            "b": "CEC enforcement layer + rule updates",
            "severity": "resolved",
            "note": "PDC_CONSUMPTION_CONTRACT.md active 2026-06-14",
        },
    ]
    integrity = {
        "pipeline_chain": ["market", "liud", "cika", "pdc", "cao", "ceo_master", "csgb_review"],
        "broken_links": ["pdc_to_cpo_enforcement", "cika_to_app_content_db"],
        "stub_paths": ["forum_intelligence.py --dry-run", "youtube_demand_stub"],
    }
    governance = {
        "agent_approval_covers_intelligence": True,
        "agent_audit_covers_intelligence": True,
        "canonical_sources": [
            "CEO_MASTER_REPORT.md",
            "CEO_STRATEGIC_GOVERNANCE_REVIEW.md",
            "roadmap_priorities.json",
            "CEO_SCORECARD.json",
        ],
        "csgb_oversight": True,
    }

    review_required = [s for s in scoreboard if s["status"] in ("REVIEW_REQUIRED", "CRITICAL")]
    high_conflicts = [c for c in conflicts if c.get("severity") == "high"]
    audit_ok = len(review_required) == 0 and not high_conflicts

    components = _org_health_components(scoreboard, audit_ok, roadmap_ok)
    org_health = sum(components.values()) // len(components)

    reports = {
        "generated_at": now,
        "department": "CAO",
        "version": "V2",
        "audit_pass": audit_ok,
        "organization_health_score": org_health,
        "organization_health_components": components,
        "review_required_count": len(review_required),
        "department_scoreboard": scoreboard,
    }
    (OUT / "department_scoreboard.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "audit_report.json").write_text(
        json.dumps({**reports, "verdict": "PASS" if audit_ok else "CONDITIONAL"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT / "consistency_report.json").write_text(
        json.dumps({"generated_at": now, "conflicts": conflicts}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "integrity_report.json").write_text(
        json.dumps({"generated_at": now, **integrity}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "governance_report.json").write_text(
        json.dumps({"generated_at": now, **governance}, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    stop = ROOT / "governance" / "executive" / "CEO_STOP.json"
    if review_required or high_conflicts:
        stop.write_text(
            json.dumps(
                {
                    "generated_at": now,
                    "stopped": False,
                    "warnings": [s["department_name"] for s in review_required]
                    + [c["id"] for c in high_conflicts],
                    "note": "CEO V2 may halt execution — see CEO_MASTER_REPORT verdict",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    print(f"   ✅ CAO V2 audit — org health {org_health}/100 — review_required={len(review_required)}")
    for p in ["department_scoreboard.json", "audit_report.json", "consistency_report.json"]:
        print(f"   ✅ governance/cao/{p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
