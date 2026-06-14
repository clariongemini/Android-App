#!/usr/bin/env python3
"""CEO V5 — Product Reality Enforcement Layer (no new department)."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "governance" / "reality"
EXEC = ROOT / "governance" / "executive"
ROADMAP = ROOT / "governance" / "product_decision" / "roadmap_priorities.json"
GENERATED = ROOT / "governance" / "cdid" / "GENERATED_WORK_PACKAGES.json"
COVERAGE = ROOT / "governance" / "execution" / "EXECUTION_COVERAGE.json"
CAO = ROOT / "governance" / "cao" / "department_scoreboard.json"
PROGRESS_REG = OUT / "FEATURE_PROGRESS_REGISTRY.json"
BIRTH_REG = OUT / "FEATURE_BIRTH_REGISTRY.json"

CHAIN = ["research", "content", "android", "qa", "release"]

# User-facing reality — did it reach the user?
REALITY_CHECKS: dict[str, list[tuple[str, str, str | None]]] = {
    "F001": [
        ("file", "app/src/main/assets/content/tr/age_4_7.json", '"id": "r"'),
        ("file", "app/src/main/assets/content/tr/age_4_7.json", '"id": "sh"'),
        ("file", "app/src/main/assets/content/tr/age_4_7.json", '"id": "l"'),
        ("code", "app/src/main/java/com/konusma/data/local/dao/PhonemeProgressDao.kt", None),
    ],
    "F002": [
        ("file", "app/src/main/assets/content/tr/late_talker/phrase_bank_v1.json", '"featureId": "F002"'),
        ("file", "app/src/main/java/com/konusma/repository/LateTalkerPhraseRepository.kt", None),
        ("grep", "app/src/main/java/com/konusma/domain/model/AnalyticsEvent.kt", r"F002_PHRASE_COMPLETED"),
        ("grep", "curriculum/late_talker/inventory/phrase_inventory_tr_v1.json", r'"current_count": 1000'),
        ("grep", "curriculum/late_talker/inventory/phrase_inventory_en_v1.json", r'"current_count": 1000'),
        ("grep", "app/src/main/java/com/konusma/ui", r"LateTalkerPhrase|PhraseSession|late_talker"),
        ("grep", "governance/reality/F002_RELEASE_GATE.json", r'"f002_release_status": "RELEASED"'),
    ],
    "F003": [
        ("file", "app/src/main/java/com/konusma/domain/usecase/GetDailyTaskUseCase.kt", None),
        ("grep", "app/src/main/java/com/konusma/ui/screens/DashboardScreen.kt", r"dailyTask|DailyTask"),
        ("file", "curriculum/daily_practice_engine.json", None),
    ],
    "F004": [
        ("grep", "app/src/main/java", r"SpeechRecognizer|stt|clarityScore"),
    ],
    "F005": [
        ("grep", "app/src/main/java", r"session.*minute|practice.*time|5.*10"),
    ],
    "F006": [
        ("grep", "governance/market", r"store.*language|aso"),
    ],
}


def _load(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _save(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _grep(path: Path, pattern: str) -> bool:
    if not path.exists():
        return False
    rx = re.compile(pattern, re.IGNORECASE)
    if path.is_dir():
        for f in path.rglob("*"):
            if f.is_file():
                try:
                    if rx.search(f.read_text(encoding="utf-8", errors="ignore")):
                        return True
                except Exception:
                    pass
        return False
    try:
        return bool(rx.search(path.read_text(encoding="utf-8", errors="ignore")))
    except Exception:
        return False


def _check_reality(check: tuple) -> bool:
    kind, rel, needle = check
    path = ROOT / rel
    if kind == "file":
        return path.exists() and (needle is None or needle in path.read_text(encoding="utf-8", errors="ignore"))
    if kind == "grep":
        return _grep(path, needle or "")
    return False


def _feature_age_days(fid: str, birth_reg: dict, now: datetime) -> int:
    features = birth_reg.get("features", {})
    if fid in features:
        born = datetime.fromisoformat(features[fid]["first_approved_at"]).replace(tzinfo=timezone.utc)
        return (now - born).days
    return 0


def _aging_level(days: int) -> str:
    if days > 60:
        return "executive_escalation"
    if days > 30:
        return "critical"
    if days > 14:
        return "warning"
    return "ok"


def _chain_status(wps: list[dict], fid: str, queue_done: set[str]) -> dict:
    feat_wps = {w["chain_step"]: w for w in wps if w.get("feature_id") == fid}
    steps = {}
    for step in CHAIN:
        wp = feat_wps.get(step)
        if not wp:
            steps[step] = "missing"
        elif wp["wp_id"] in queue_done or wp.get("status") == "completed":
            steps[step] = "done"
        elif wp.get("status") in ("in_progress", "review", "approved_l1", "approved_l2"):
            steps[step] = "in_progress"
        else:
            steps[step] = "pending"
    return steps


def _reality_state(fid: str) -> dict:
    checks = REALITY_CHECKS.get(fid, [])
    passed = sum(1 for c in checks if _check_reality(c))
    total = len(checks) or 1
    ratio = passed / total
    if ratio >= 0.85:
        state = "shipped_to_user"
    elif ratio >= 0.5:
        state = "partial_in_app"
    elif ratio > 0:
        state = "started"
    else:
        state = "not_in_product"
    return {
        "checks_passed": passed,
        "checks_total": total,
        "ratio": round(ratio, 2),
        "state": state,
        "reaches_user": state in ("shipped_to_user", "partial_in_app"),
    }


def _update_progress_registry(features: list[dict], chain_map: dict[str, dict]) -> dict:
    reg = _load(PROGRESS_REG) or {"features": {}}
    now = datetime.now(timezone.utc).isoformat()
    for feat in features:
        fid = feat["id"]
        chain = chain_map.get(fid, {})
        any_done = any(v == "done" for v in chain.values())
        any_progress = any(v in ("done", "in_progress") for v in chain.values())
        entry = reg["features"].get(fid, {})
        if any_progress and entry.get("last_progress_at") is None:
            entry["last_progress_at"] = now
        elif any_done:
            entry["last_progress_at"] = now
        entry["chain_snapshot"] = chain
        reg["features"][fid] = entry
    reg["updated_at"] = now
    _save(PROGRESS_REG, reg)
    return reg


def _is_stalled(fid: str, age_days: int, chain: dict, reality: dict, progress_reg: dict) -> bool:
    if reality["state"] == "shipped_to_user":
        return False
    if all(v == "done" for v in chain.values() if v != "missing"):
        return False
    last = progress_reg.get("features", {}).get(fid, {}).get("last_progress_at")
    if last:
        last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
        stall_days = (datetime.now(timezone.utc) - last_dt).days
        return stall_days >= 14
    return age_days >= 14 and reality["state"] == "not_in_product"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    ts = now.isoformat()

    roadmap = _load(ROADMAP)
    generated = _load(GENERATED)
    coverage_doc = _load(COVERAGE)
    cao = _load(CAO)
    birth_reg = _load(BIRTH_REG)

    wps = generated.get("work_packages", [])
    queue_done = set()
    queue_path = EXEC / "APPROVAL_QUEUE.md"
    if queue_path.exists():
        for line in queue_path.read_text(encoding="utf-8").splitlines():
            if "`completed`" in line:
                m = re.search(r"WP-\d+", line)
                if m:
                    queue_done.add(m.group(0))

    p0 = roadmap.get("P0", [])
    p1 = roadmap.get("P1", [])
    approved_p0_p1 = p0 + p1

    chain_map = {f["id"]: _chain_status(wps, f["id"], queue_done) for f in approved_p0_p1}
    progress_reg = _update_progress_registry(approved_p0_p1, chain_map)

    aging_entries = []
    stalled_features = []
    blocked_features = []
    p0_completed = 0
    p0_active = len(p0)
    reality_shipped = 0
    reality_detail = []

    for feat in approved_p0_p1:
        fid = feat["id"]
        age = _feature_age_days(fid, birth_reg, now)
        level = _aging_level(age)
        chain = chain_map.get(fid, {})
        reality = _reality_state(fid)
        stalled = _is_stalled(fid, age, chain, reality, progress_reg)
        blocked = any(v == "missing" for v in chain.values())

        if feat.get("priority_level") == "P0" or fid in {f["id"] for f in p0}:
            if reality["state"] == "shipped_to_user":
                p0_completed += 1
            if stalled:
                stalled_features.append(fid)
            if blocked:
                blocked_features.append(fid)

        if reality["reaches_user"]:
            reality_shipped += 1

        aging_entries.append({
            "feature_id": fid,
            "name": feat.get("name"),
            "priority_level": feat.get("priority_level", "P0" if feat in p0 else "P1"),
            "feature_age_days": age,
            "aging_level": level,
            "chain": chain,
            "stalled": stalled,
            "reality": reality,
        })
        reality_detail.append({
            "feature_id": fid,
            "name": feat.get("name"),
            **reality,
            "stalled": stalled,
        })

    approved_count = len(approved_p0_p1)
    reality_score = int(100 * reality_shipped / approved_count) if approved_count else 0

    org_health = cao.get("organization_health_score", 0)
    exec_coverage = coverage_doc.get("execution_coverage_pct", 0)
    scoreboard = cao.get("department_scoreboard", [])
    intel_scores = [
        s["quality_score"] for s in scoreboard
        if s.get("department_id") in ("market_growth", "liud", "cika", "pdc")
    ]
    intel_avg = int(sum(intel_scores) / len(intel_scores)) if intel_scores else 0
    analysis_paralysis = exec_coverage < 25 and (org_health > 80 or intel_avg > 85)

    avg_age = int(sum(e["feature_age_days"] for e in aging_entries if e["priority_level"] == "P0") / max(p0_active, 1))

    delivery_health_score = max(0, min(100, int(
        (p0_completed / max(p0_active, 1)) * 40
        + reality_score * 0.35
        + max(0, 25 - len(stalled_features) * 8)
        + max(0, 15 - len(blocked_features) * 5)
    )))

    delivery_health = {
        "generated_at": ts,
        "version": "V5",
        "delivery_health_score": delivery_health_score,
        "p0_active_features": p0_active,
        "p0_completed_features": p0_completed,
        "p0_stalled_features": len([e for e in aging_entries if e["stalled"] and e["priority_level"] == "P0"]),
        "p0_blocked_features": len(blocked_features),
        "average_delivery_age_days_p0": avg_age,
        "stalled_feature_ids": stalled_features,
        "blocked_feature_ids": blocked_features,
        "rule": "No Feature Left Behind — 14d no progress = STALLED",
    }
    _save(OUT / "DELIVERY_HEALTH.json", delivery_health)

    feature_aging = {
        "generated_at": ts,
        "thresholds": {">14": "warning", ">30": "critical", ">60": "executive_escalation"},
        "features": aging_entries,
    }
    _save(OUT / "FEATURE_AGING.json", feature_aging)

    product_reality = {
        "generated_at": ts,
        "product_reality_score": reality_score,
        "implemented_reaches_user": reality_shipped,
        "approved_features": approved_count,
        "formula": "features_reaching_user / approved_p0_p1",
        "note": "Unlike coverage (WP exists), reality asks: did user get it?",
        "features": reality_detail,
    }
    _save(OUT / "PRODUCT_REALITY_SCORE.json", product_reality)

    launch_pressure = {
        "generated_at": ts,
        "execution_coverage_pct": exec_coverage,
        "organization_health": org_health,
        "intelligence_avg": intel_avg,
        "analysis_paralysis_risk": analysis_paralysis,
        "delivery_bottleneck": "intelligence strong · product weak · delivery at 0%",
        "mandate": "Product delivery — not new decisions",
        "execution_stack": [
            "P0 AID Sprint P — live data",
            "P1 F002 WP-24 — 1000 TR + 1000 EN",
            "P2 F002 WP-25 — UI flow integration",
            "P3 F002 WP-26 — real usage analytics",
            "P4 F002 WP-27 — RELEASED gate",
        ],
        "no_new_p0_rule": "Execution Coverage < 80 OR Reality Score < 80 → PDC blocked",
        "f002_release_gate": "LOCKED — WP-27 criteria not met",
    }
    _save(OUT / "LAUNCH_PRESSURE.json", launch_pressure)

    no_new_p0 = {
        "generated_at": ts,
        "rule_id": "NO_NEW_P0",
        "authority": "CEO V5 Product Reality Layer",
        "status": "ACTIVE",
        "rule": "PDC yeni P0 üretemez when Execution Coverage < 80 OR Product Reality Score < 80",
        "current_state": {
            "execution_coverage_pct": exec_coverage,
            "product_reality_score": reality_score,
            "pdc_p0_generation_blocked": exec_coverage < 80 or reality_score < 80,
            "reason": "Teslimat eksikliği — karar eksikliği değil",
        },
        "trigger_thresholds": {"execution_coverage_pct": 80, "product_reality_score": 80},
        "companion_gate": "governance/reality/F002_RELEASE_GATE.json",
    }
    _save(OUT / "NO_NEW_P0_RULE.json", no_new_p0)

    lines = [
        "# CEO Product Reality Report",
        "",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        "**Layer:** CEO V5 — Product Reality Enforcement  ",
        "**Rule:** No Feature Left Behind  ",
        "",
        "---",
        "",
        "## The Signal",
        "",
        f"| Dimension | Score |",
        f"|-----------|-------|",
        f"| Intelligence Health | ~91 |",
        f"| Market Health | ~94 |",
        f"| Strategy Health | ~89 |",
        f"| Product Health | ~58 |",
        f"| Execution Coverage | {exec_coverage}% |",
        f"| **Delivery Health** | **{delivery_health_score}/100** |",
        f"| **Product Reality Score** | **{reality_score}%** |",
        "",
        "Sistem ne yapacağını biliyor — henüz kullanıcıya ulaştırmıyor.",
        "",
        "---",
        "",
        "## Analysis Paralysis",
        "",
        f"**{'⚠ ACTIVE' if analysis_paralysis else 'No'}** — Coverage {exec_coverage}% · Intel avg {intel_avg} · Org {org_health}",
        "",
        "Organizasyon karmaşıklığı ürün hızını geçmemeli. **Agent freeze aktif.**",
        "",
        "---",
        "",
        "## P0 Feature Reality",
        "",
        "| ID | Age (d) | Aging | Chain | Reality | Stalled |",
        "|----|---------|-------|-------|---------|---------|",
    ]
    for e in aging_entries:
        if e["priority_level"] != "P0":
            continue
        chain_s = " → ".join(f"{k[0].upper()}:{v[0].upper()}" for k, v in e["chain"].items())
        lines.append(
            f"| {e['feature_id']} | {e['feature_age_days']} | {e['aging_level']} "
            f"| {chain_s} | {e['reality']['state']} | {'YES' if e['stalled'] else 'no'} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Delivery Health",
        "",
        f"- P0 Active: **{p0_active}**",
        f"- P0 Completed (user-facing): **{p0_completed}**",
        f"- P0 Stalled: **{delivery_health['p0_stalled_features']}**",
        f"- P0 Blocked: **{delivery_health['p0_blocked_features']}**",
        f"- Avg P0 Age: **{avg_age} days**",
        "",
        "---",
        "",
        "## CEO V5 Execution Stack",
        "",
        "1. **P0 — AID Sprint P** — live_analytics · retention · completion · session",
        "2. **P1 — F002 WP-24** — 1000 TR + 1000 EN (CIKA standard)",
        "3. **P2 — F002 WP-25** — Parent Mode → Late Talker → Phrase Session (no UI redesign)",
        "4. **P3 — F002 WP-26** — phrase_* real usage data",
        "5. **P4 — F002 WP-27** — RELEASED gate (≥100 sessions)",
        "",
        "**No New P0:** Coverage < 80% OR Reality < 80% → PDC blocked.",
        "",
        "Program: `governance/features/F002/F002_DELIVERY_VALIDATION_PROGRAM.md`",
        "",
        "---",
        "",
        "## Mandate",
        "",
        "Yeni departman yok. Yeni rapor araştırması yok.",
        "**F001 · F002 · F003 uygulamaya girmeli.**",
        "",
        "Detay: `governance/reality/`",
        "",
    ]
    (EXEC / "CEO_PRODUCT_REALITY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"   ✅ Product Reality — Delivery Health {delivery_health_score}/100 · Reality {reality_score}%")
    if analysis_paralysis:
        print("   ⚠ ANALYSIS PARALYSIS RISK — intelligence >> delivery")
    if stalled_features:
        print(f"   ⚠ STALLED: {', '.join(stalled_features)}")
    for f in [
        "DELIVERY_HEALTH.json",
        "FEATURE_AGING.json",
        "PRODUCT_REALITY_SCORE.json",
        "LAUNCH_PRESSURE.json",
        "NO_NEW_P0_RULE.json",
    ]:
        print(f"   ✅ governance/reality/{f}")
    print("   ✅ governance/executive/CEO_PRODUCT_REALITY_REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
