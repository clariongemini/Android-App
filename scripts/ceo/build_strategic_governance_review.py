#!/usr/bin/env python3
"""CEO V2 Step 20 — Strategic Governance Review for CSGB."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXEC = ROOT / "governance" / "executive"
CAO = ROOT / "governance" / "cao" / "department_scoreboard.json"
SCORECARD = ROOT / "governance" / "executive" / "CEO_SCORECARD.json"
MASTER = ROOT / "governance" / "executive" / "CEO_MASTER_REPORT.md"
PDC_ROADMAP = ROOT / "governance" / "product_decision" / "roadmap_priorities.json"
PDC_REJECT = ROOT / "governance" / "product_decision" / "rejected_features.json"
USER_INTENT = ROOT / "governance" / "market" / "USER_INTENT_SIGNALS.json"
CONTENT_GAP = ROOT / "curriculum" / "content_gap_report.json"
CONSISTENCY = ROOT / "governance" / "cao" / "consistency_report.json"

STALE_PATHS = [
    ("VOC_JTBD_DEMAND_RESEARCH.md", ROOT / "governance" / "market" / "VOC_JTBD_DEMAND_RESEARCH.md", 30),
    ("ROADMAP_AUDIT.md", ROOT / "governance" / "audits" / "ROADMAP_AUDIT.md", 60),
    ("COMPETITOR_ANALYSIS.md", ROOT / "docs" / "COMPETITOR_ANALYSIS.md", 45),
    ("LIUD roadmap_priorities.json", ROOT / "governance" / "linguistic" / "output" / "roadmap_priorities.json", 14),
]

ASSUMPTION_GAPS = [
    "Retention impact of daily missions — no live cohort data (AID stub)",
    "TR fonem expansion clinical efficacy — partial age norms",
    "Y1 revenue P50 ~70 subs — model not field-validated",
    "FR/IT/ES locale demand — intelligence exists, app content absent",
    "Gamification intent (229 signals) — educational value unverified",
]


def _load(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _top_intents(data: dict, n: int = 5) -> list[str]:
    combined = data.get("combined_intent_counts") or data.get("play", {}).get("global", {}).get("intent_counts", {})
    items = sorted(combined.items(), key=lambda x: -x[1]) if isinstance(combined, dict) else []
    return [f"{k} ({v})" for k, v in items[:n]]


def _stale_reports() -> list[str]:
    stale = []
    now = datetime.now(timezone.utc)
    for name, path, threshold in STALE_PATHS:
        if not path.exists():
            stale.append(f"**{name}** — file missing")
            continue
        age = (now - datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)).days
        if age > threshold:
            stale.append(f"**{name}** — {age} days old (threshold {threshold}d)")
    return stale or ["None above threshold this cycle"]


def _largest_gap(gaps: list[dict]) -> str:
    if not gaps:
        return "Unknown — content_gap_report empty"
    top = max(gaps, key=lambda g: g.get("gap_pct", 0))
    topic = top.get("user_demand_topic", top.get("user_demand", "?"))
    return f"**{topic}** — gap ~{top.get('gap_pct', '?')}%"


def main() -> int:
    now = datetime.now(timezone.utc)
    cao = _load(CAO)
    scorecard = _load(SCORECARD)
    roadmap = _load(PDC_ROADMAP)
    rejected = _load(PDC_REJECT).get("rejected", [])
    intent = _load(USER_INTENT)
    gaps = _load(CONTENT_GAP).get("gaps", [])
    critical_gaps = [g for g in gaps if g.get("gap_pct", 0) >= 60]
    scoreboard = cao.get("department_scoreboard", [])
    conflicts = _load(CONSISTENCY).get("conflicts", [])

    p0 = roadmap.get("P0", [])
    p1 = roadmap.get("P1", [])
    p2 = roadmap.get("P2", [])
    verdict = scorecard.get("ceo_verdict", "CONDITIONAL_GO")
    org_health = scorecard.get("organization_health", 0)

    underperformers = sorted(
        [s for s in scoreboard if s.get("quality_score", 100) < 75],
        key=lambda x: x["quality_score"],
    )

    remove_candidates = [r.get("name") for r in rejected]
    for f in p2:
        if "copy" in f.get("name", "").lower() or f.get("priority_score", 100) < 40:
            remove_candidates.append(f.get("name"))

    accelerate = [f.get("name") for f in p0]
    if any(g.get("gap_pct", 0) >= 80 for g in critical_gaps):
        accelerate.append("Content gap themes %80+ — executive priority")

    leverage_action = (
        "Wire PDC → CPO mandatory roadmap consumption + launch Sprint P analytics"
        if any(c.get("id") == "pdc_cpo_unwired" for c in conflicts)
        else "Execute P0 TR fonem + LATE_TALKER with CIKA content pipeline"
    )

    lines = [
        "# CEO Strategic Governance Review",
        "",
        f"**Üretim:** {now.strftime('%Y-%m-%d %H:%M')} UTC  ",
        "**Audience:** CSGB (under EGC)  ",
        "**Agent:** CSGB — Step 17  ",
        "**Escalates to:** EGC Step 18  ",
        f"**Organization Health:** {org_health}/100  ",
        f"**CEO Verdict:** **{verdict}**  ",
        f"**Master Report:** [CEO_MASTER_REPORT.md](CEO_MASTER_REPORT.md)",
        "",
        "---",
        "",
        "## 15 Strategic Questions",
        "",
        "### 1. What do users want most?",
        "",
    ]
    for item in _top_intents(intent) or [
        "gamification (229)",
        "video/mirror (100)",
        "phoneme (64)",
        "stuttering (64)",
        "speech delay (45)",
    ]:
        lines.append(f"- {item}")

    lines += [
        "",
        "### 2. What do users actually do?",
        "",
        "- **Canlı analytics yok** — Sprint P 0/10; retention doğrulanmadı (AID REVIEW_REQUIRED)",
        "- Kod hazır: journey, courage, streak — saha kanıtı bekliyor",
        "- Rule 6: retention signals outweigh acquisition until AID live",
        "",
        "### 3. What is the largest content gap?",
        "",
        _largest_gap(gaps),
        "",
    ]
    for g in critical_gaps[:3]:
        topic = g.get("user_demand_topic", g.get("user_demand", "?"))
        lines.append(f"- {topic} — ~{g.get('gap_pct', '?')}%")

    lines += [
        "",
        "### 4. What is the largest retention opportunity?",
        "",
        "- **365 daily missions + 5–10 dk ritüel** (forum + LIUD daily_routine 27)",
        "- TR fonem derinliği — «içerik bitti» churn önleme",
        "",
        "### 5. What is the largest revenue opportunity?",
        "",
        "- Store/SEO kullanıcı dili (acquisition) — retention sonrası ölçek",
        "- TR PPP fiyat vs Speech Blubs fiyat şikâyeti",
        "- Y1 organic only — B2B blocked per Rule 8",
        "",
        "### 6. What should be built immediately?",
        "",
    ]
    for f in p0:
        lines.append(f"- **{f.get('name', f)}**")

    lines += [
        "",
        "### 7. What should not be built?",
        "",
    ]
    for r in rejected:
        reason = r.get("anti_bias_rule") or (r.get("reason", [""])[0] if r.get("reason") else "P4")
        lines.append(f"- **{r.get('name')}** — {reason}")

    lines += [
        "",
        "### 8. What is the largest strategic risk?",
        "",
        "- İçerik envanteri hedefin ~%12'si → erken churn",
        "- PDC → CPO/Architect otomatik bağ yok → roadmap drift",
        "- FR/IT/ES app içeriği yok → locale parity failure",
        "",
        "### 9. How far are we from global leadership?",
        "",
        "- **Uzak** (pre-launch): 0 install, 0 paid proof, analytics stub",
        "- Güçlü: 6-locale intelligence pipeline, PDC kanıt modeli, content gap clarity",
        "- North Star gap: execution + content depth + retention proof",
        "",
        "### 10. Which department is underperforming?",
        "",
    ]
    if underperformers:
        for s in underperformers:
            lines.append(f"- **{s['department_name']}** — {s['quality_score']}/100 ({s['status']})")
    else:
        lines.append("- None below 75 threshold")

    lines += [
        "",
        "### 11. Which reports are stale?",
        "",
    ]
    for s in _stale_reports():
        lines.append(f"- {s}")

    lines += [
        "",
        "### 12. Which assumptions lack evidence?",
        "",
    ]
    for a in ASSUMPTION_GAPS:
        lines.append(f"- {a}")

    lines += [
        "",
        "### 13. Which roadmap items should be removed?",
        "",
    ]
    for name in remove_candidates or ["None — PDC reject list current"]:
        lines.append(f"- {name}")

    lines += [
        "",
        "### 14. Which roadmap items should be accelerated?",
        "",
    ]
    for name in accelerate:
        lines.append(f"- **{name}**")

    lines += [
        "",
        "### 15. What single action creates the highest organizational leverage?",
        "",
        f"**{leverage_action}**",
        "",
        "Rationale: unblocks execution alignment (Rule 3–5) and closes analytics blind spot (AID).",
        "",
        "---",
        "",
        "## CSGB Evaluation Inputs",
        "",
        "| Input | Value |",
        "|-------|-------|",
        f"| Organization Health | {org_health}/100 |",
        f"| CEO Verdict | {verdict} |",
        f"| P0 count | {len(p0)} |",
        f"| Critical content gaps (%60+) | {len(critical_gaps)} |",
        f"| Underperforming departments | {len(underperformers)} |",
        f"| Stale reports | {len(_stale_reports())} |",
        f"| Assumption gaps | {len(ASSUMPTION_GAPS)} |",
        "",
        "---",
        "",
        "## North Star Alignment",
        "",
        "Mission: Build the most effective, scalable, evidence-driven speech development ecosystem.",
        "",
        "This cycle optimizes: **User Outcomes · Learning Outcomes · Retention · Trust · Global Scalability**",
        "",
        "Not optimizing: vanity downloads · competitor copy · unverified gamification demand",
        "",
        "---",
        "",
        "**Next cycle:** `./scripts/ceo/run_ceo_cycle.sh`",
        "",
    ]

    out = EXEC / "CEO_STRATEGIC_GOVERNANCE_REVIEW.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("   ✅ governance/executive/CEO_STRATEGIC_GOVERNANCE_REVIEW.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
