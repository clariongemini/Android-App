#!/usr/bin/env python3
"""Write generic governance state seeds — no Konuşma live data."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOV = ROOT / "governance"
NOW = datetime.now(timezone.utc).isoformat()


def write(rel: str, data: dict | list) -> None:
    path = GOV / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    app = sys.argv[1] if len(sys.argv) > 1 else "{{APP_NAME}}"
    pkg = sys.argv[2] if len(sys.argv) > 2 else "{{PACKAGE_NAME}}"
    slug = sys.argv[3] if len(sys.argv) > 3 else "{{SLUG}}"

    write("memory/ORGANIZATIONAL_MEMORY.json", {"version": "1.0", "events": []})
    write("memory/DELIVERY_HISTORY.json", {"entries": []})
    write("memory/DECISION_HISTORY.json", {"entries": []})
    write("memory/SUCCESS_HISTORY.json", {"entries": []})
    write("memory/FAILURE_HISTORY.json", {"entries": []})

    write("reality/PRODUCT_REALITY_SCORE.json", {
        "generated_at": NOW, "product_reality_score": 0,
        "implemented_reaches_user": 0, "approved_features": 0, "features": [],
    })
    for name in (
        "FEATURE_AGING", "FEATURE_PROGRESS_REGISTRY", "FEATURE_BIRTH_REGISTRY",
        "LAUNCH_PRESSURE", "DELIVERY_HEALTH",
    ):
        write(f"reality/{name}.json", {"generated_at": NOW, "items": []})
    write("reality/NO_NEW_P0_RULE.json", {"active": True, "note": "P0 sprint lock enforced by CEO"})

    write("execution/EXECUTION_COVERAGE.json", {"generated_at": NOW, "execution_coverage_percent": 0})
    write("execution/EXECUTION_BLOCKERS.json", {"generated_at": NOW, "blockers": []})
    write("execution/UNOWNED_GAPS.json", {"generated_at": NOW, "gaps": []})
    write("execution/FEATURE_DELIVERY_SCOREBOARD.json", {"generated_at": NOW, "features": []})
    write("execution/ROADMAP_CONSUMPTION_MANIFEST.json", {"generated_at": NOW, "manifest": []})
    write("execution/ROADMAP_CONSUMPTION_REPORT.json", {"generated_at": NOW, "violations": []})
    write("execution/DELIVERY_PREDICTION_ACCURACY.json", {"generated_at": NOW, "accuracy_pct": 0})

    write("product_decision/rejected_features.json", {"version": "1.0", "rejected": []})
    write("product_decision/decision_log.json", {"entries": []})
    write("product_decision/evidence_links.json", {"links": []})
    write("product_decision/feature_ranking.json", {"ranked": []})
    write("product_decision/priority_matrix.json", {"matrix": []})
    write("product_decision/quarterly_decisions.json", {"quarters": []})

    write("cao/department_scoreboard.json", {"generated_at": NOW, "departments": []})
    write("cao/audit_report.json", {"generated_at": NOW, "findings": []})
    write("cao/governance_report.json", {"generated_at": NOW, "summary": "pending first CAO cycle"})
    write("cao/integrity_report.json", {"generated_at": NOW, "integrity_score": 0})
    write("cao/consistency_report.json", {"generated_at": NOW, "issues": []})

    write("egc/EGC_VERDICT.json", {
        "generated_at": NOW, "egc_verdict": "BOOTSTRAP",
        "version": "V4", "company_health_score": 0, "binding": False,
    })
    for name in (
        "CEO_PERFORMANCE_SCORECARD", "STRATEGIC_DEBT_REGISTER", "DEPARTMENT_ROI",
        "ROADMAP_DRIFT_REPORT", "PDC_DECISION_QUALITY", "GLOBAL_LEADERSHIP_SCORE",
        "COMPANY_HEALTH_SCORE",
    ):
        write(f"egc/{name}.json", {"generated_at": NOW, "status": "bootstrap"})

    write("cdid/GENERATED_WORK_PACKAGES.json", {"generated_at": NOW, "packages": []})

    write("blue_ocean/project_index.json", {
        "version": "1.0",
        "flagship": {"slug": slug, "package": pkg, "name": app, "portfolio_rank": 1},
        "candidates": [],
        "note": "Fill via Mavi Okyanus discovery — not live Konuşma data",
    })

    write("market/USER_INTENT_SIGNALS.json", {"signals": []})
    write("market/competitor_catalog.json", {"competitors": []})
    write("market/PLAY_STORE_BENCHMARKS.json", {"benchmarks": []})
    write("market/demand_intelligence_catalog.json", {"items": []})
    write("market/forum_query_catalog.json", {"queries": []})

    write("trends/discovery_data.json", {"items": []})
    write("trends/discovery_candidates.json", {"candidates": []})
    write("trends/trends_data.json", {"trends": []})
    write("trends/queries.json", {"queries": []})
    write("trends/ceo_validation.json", {"generated_at": NOW, "validated": []})

    write("linguistic/LOCALE_MARKET_REGISTRY.json", {"locales": []})
    write("linguistic/exercise_scope_targets.json", {"targets": []})
    write("linguistic/output_catalog.json", {"outputs": []})

    print(f"   ✅ Governance state seeded for {app} ({len(list(GOV.rglob('*.json')))} json files under governance/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
