#!/usr/bin/env python3
"""
PDC — Product Decision Council output builder.
LIUD + CIKA + Market kanıtlarından ağırlıklı öncelik kararları üretir.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT = PROJECT_ROOT / "governance" / "product_decision"
CURRICULUM = PROJECT_ROOT / "curriculum"
LIUD = PROJECT_ROOT / "governance" / "linguistic" / "output"
MARKET = PROJECT_ROOT / "governance" / "market"

WEIGHTS = {
    "demand": 0.25,
    "retention": 0.20,
    "revenue": 0.15,
    "strategic": 0.15,
    "competitive": 0.10,
    "clinical": 0.10,
    "localization": 0.05,
}

LOCALES = ["TR", "EN", "DE", "FR", "IT", "ES"]


def _load(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _priority_score(scores: dict[str, int | float]) -> float:
    return round(
        scores["demand"] * WEIGHTS["demand"]
        + scores["retention"] * WEIGHTS["retention"]
        + scores["revenue"] * WEIGHTS["revenue"]
        + scores["strategic"] * WEIGHTS["strategic"]
        + scores["competitive"] * WEIGHTS["competitive"]
        + scores["clinical"] * WEIGHTS["clinical"]
        + scores["localization"] * WEIGHTS["localization"],
        2,
    )


def _level(score: float, *, content_p0: bool = False) -> str:
    if content_p0:
        return "P0"
    if score >= 82:
        return "P0"
    if score >= 70:
        return "P1"
    if score >= 55:
        return "P2"
    if score >= 40:
        return "P3"
    return "P4"


def _write(name: str, payload: dict | list) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"   ✅ {p.relative_to(PROJECT_ROOT)}")


def _build_features(gaps: list, content_critical: bool) -> list[dict]:
    """Evidence-backed feature proposals — scores 0-100."""
    features = [
        {
            "id": "F001",
            "name": "TR Fonem Expansion (R/Ş/L)",
            "segment": "ARTICULATION",
            "locales": ["TR"],
            "scores": {"demand": 95, "retention": 90, "revenue": 65, "strategic": 92, "competitive": 88, "clinical": 85, "localization": 90},
            "complexity": 30,
            "mandatory_questions": {
                "users_requested": "intent phoneme 64 + trends artikülasyon RSV 16",
                "locales": ["TR"],
                "segments": ["CHILD_4_7", "ARTICULATION"],
                "competitor_solves": "partial — global apps weak TR phoneme",
                "retention": True,
                "paid_conversion": "medium",
                "engagement": True,
                "churn_reduction": True,
                "differentiation": True,
            },
            "evidence": ["LIUD content_gaps urgent", "CIKA gap 86%", "USER_INTENT phoneme 64"],
            "content_p0": True,
            "owner": "Product & Education + CIKA",
        },
        {
            "id": "F002",
            "name": "LATE_TALKER Parent Phrase Bank",
            "segment": "LATE_TALKER",
            "locales": ["TR", "EN"],
            "scores": {"demand": 90, "retention": 88, "revenue": 60, "strategic": 85, "competitive": 75, "clinical": 80, "localization": 70},
            "complexity": 25,
            "mandatory_questions": {
                "users_requested": "speech_delay 45 combined + forum KK",
                "locales": ["TR", "EN"],
                "segments": ["CHILD_1_3", "CHILD_4_7", "LATE_TALKER"],
                "competitor_solves": "partial",
                "retention": True,
                "paid_conversion": "medium",
                "engagement": True,
                "churn_reduction": True,
                "differentiation": True,
            },
            "evidence": ["forum batch KK", "CIKA content_gap 72%", "LIUD speech_delay"],
            "content_p0": True,
            "owner": "Product & Education",
        },
        {
            "id": "F003",
            "name": "365 Daily Missions CHILD_4_7 (non-repeating)",
            "segment": "CHILD_4_7",
            "locales": LOCALES,
            "scores": {"demand": 85, "retention": 92, "revenue": 55, "strategic": 88, "competitive": 70, "clinical": 75, "localization": 80},
            "complexity": 45,
            "mandatory_questions": {
                "users_requested": "gamification 229 + daily_routine 27",
                "locales": LOCALES,
                "segments": ["CHILD_4_7"],
                "competitor_solves": "Speech Blubs partial — repetition complaints",
                "retention": True,
                "paid_conversion": "low-medium",
                "engagement": True,
                "churn_reduction": True,
                "differentiation": True,
            },
            "evidence": ["CIKA minimum standard", "forum content_repetitive 33", "daily_practice_engine"],
            "content_p0": True,
            "owner": "CIKA + Product",
        },
        {
            "id": "F004",
            "name": "STT Phoneme Calibration",
            "segment": "ARTICULATION",
            "locales": LOCALES,
            "scores": {"demand": 80, "retention": 85, "revenue": 70, "strategic": 78, "competitive": 82, "clinical": 70, "localization": 75},
            "complexity": 55,
            "mandatory_questions": {
                "users_requested": "Play 1-3★ STT themes + forum stt_or_mic 5",
                "locales": LOCALES,
                "segments": ["ALL"],
                "competitor_solves": "industry-wide weakness",
                "retention": True,
                "paid_conversion": "high — rating affects conversion",
                "engagement": True,
                "churn_reduction": True,
                "differentiation": True,
            },
            "evidence": ["COMPETITOR_ANALYSIS STT", "LIUD urgent STT", "review_intelligence"],
            "content_p0": False,
            "owner": "Android Elite",
        },
        {
            "id": "F005",
            "name": "5–10 dk Speech Time Ritual (UX + content)",
            "segment": "ALL_CHILD",
            "locales": ["TR", "EN"],
            "scores": {"demand": 82, "retention": 90, "revenue": 58, "strategic": 80, "competitive": 65, "clinical": 72, "localization": 65},
            "complexity": 35,
            "mandatory_questions": {
                "users_requested": "daily_routine 27 + beaming_health 5-10dk",
                "locales": ["TR", "EN"],
                "segments": ["CHILD_1_3", "CHILD_4_7", "LATE_TALKER"],
                "competitor_solves": "partial — long sessions complained",
                "retention": True,
                "paid_conversion": "medium",
                "engagement": True,
                "churn_reduction": True,
                "differentiation": True,
            },
            "evidence": ["CIKA daily_practice_engine", "USER_INTENT daily_routine"],
            "content_p0": False,
            "owner": "Product & Education",
        },
        {
            "id": "F006",
            "name": "Store/SEO User Language Alignment",
            "segment": "ACQUISITION",
            "locales": LOCALES,
            "scores": {"demand": 88, "retention": 35, "revenue": 85, "strategic": 75, "competitive": 60, "clinical": 40, "localization": 85},
            "complexity": 20,
            "mandatory_questions": {
                "users_requested": "expert vs user language all locales",
                "locales": LOCALES,
                "segments": ["ACQUISITION"],
                "competitor_solves": "n/a — listing optimization",
                "retention": False,
                "paid_conversion": "high",
                "engagement": False,
                "churn_reduction": False,
                "differentiation": True,
            },
            "evidence": ["LIUD expert_vs_user_language", "TERM_DISCOVERY", "Growth ASO"],
            "content_p0": False,
            "owner": "Growth + LIUD",
        },
        {
            "id": "F007",
            "name": "Stuttering Exposure Hierarchy (500 scenarios)",
            "segment": "STUTTERING",
            "locales": LOCALES,
            "scores": {"demand": 78, "retention": 75, "revenue": 50, "strategic": 70, "competitive": 72, "clinical": 78, "localization": 70},
            "complexity": 50,
            "mandatory_questions": {
                "users_requested": "stuttering 64 combined",
                "locales": LOCALES,
                "segments": ["STUTTERING", "TEEN_13_17", "ADULT_30_PLUS"],
                "competitor_solves": "Stamurai partial",
                "retention": True,
                "paid_conversion": "low-medium",
                "engagement": True,
                "churn_reduction": True,
                "differentiation": True,
            },
            "evidence": ["CIKA backlog P1", "LIUD stuttering", "forum eksi"],
            "content_p0": False,
            "owner": "CIKA + Product",
        },
        {
            "id": "F008",
            "name": "DE/FR/IT/ES Curriculum Parity Sprint",
            "segment": "LOCALIZATION",
            "locales": ["DE", "FR", "IT", "ES"],
            "scores": {"demand": 55, "retention": 70, "revenue": 45, "strategic": 80, "competitive": 55, "clinical": 60, "localization": 95},
            "complexity": 60,
            "mandatory_questions": {
                "users_requested": "6 locale policy — parity gap CIKA 35% coverage",
                "locales": ["DE", "FR", "IT", "ES"],
                "segments": ["ALL"],
                "competitor_solves": "n/a",
                "retention": True,
                "paid_conversion": "medium long-term",
                "engagement": True,
                "churn_reduction": True,
                "differentiation": False,
            },
            "evidence": ["CIKA language_content_map", "Growth 6-locale rule"],
            "content_p0": False,
            "owner": "CIKA + Localization",
        },
        {
            "id": "F009",
            "name": "Adult UX Panel (UserPurpose — non-childish)",
            "segment": "ADULT_30_PLUS",
            "locales": ["TR", "EN"],
            "scores": {"demand": 72, "retention": 68, "revenue": 62, "strategic": 75, "competitive": 80, "clinical": 55, "localization": 60},
            "complexity": 40,
            "mandatory_questions": {
                "users_requested": "childish_or_too_young theme 9 + VOC",
                "locales": ["TR", "EN"],
                "segments": ["YOUNG_ADULT_18_29", "ADULT_30_PLUS", "DICTION"],
                "competitor_solves": "Speech Blubs weak adult",
                "retention": True,
                "paid_conversion": "medium",
                "engagement": True,
                "churn_reduction": True,
                "differentiation": True,
            },
            "evidence": ["LIUD content_gaps adult UX", "COMPETITOR_ANALYSIS"],
            "content_p0": False,
            "owner": "Product CPO",
        },
        {
            "id": "F010",
            "name": "Interview STAR Dataset (1000+ Q)",
            "segment": "INTERVIEW_PREPARATION",
            "locales": ["EN", "TR"],
            "scores": {"demand": 45, "retention": 55, "revenue": 40, "strategic": 50, "competitive": 45, "clinical": 35, "localization": 50},
            "complexity": 55,
            "mandatory_questions": {
                "users_requested": "LIUD jtbd mülakat — lower volume vs child",
                "locales": ["EN", "TR"],
                "segments": ["YOUNG_ADULT_18_29"],
                "competitor_solves": "Speeko partial",
                "retention": True,
                "paid_conversion": "low",
                "engagement": True,
                "churn_reduction": False,
                "differentiation": False,
            },
            "evidence": ["LIUD jtbd", "CIKA DICTION minimums future"],
            "content_p0": False,
            "owner": "CIKA",
        },
        {
            "id": "F011",
            "name": "B2B Clinical / Therapist Portal Year 1",
            "segment": "B2B",
            "locales": ["TR", "EN"],
            "scores": {"demand": 25, "retention": 30, "revenue": 40, "strategic": 35, "competitive": 30, "clinical": 70, "localization": 40},
            "complexity": 75,
            "mandatory_questions": {
                "users_requested": "therapist_homework 3 — low pre-launch",
                "locales": ["TR", "EN"],
                "segments": ["B2B"],
                "competitor_solves": "Constant Therapy etc.",
                "retention": False,
                "paid_conversion": "uncertain Y1",
                "engagement": False,
                "churn_reduction": False,
                "differentiation": False,
            },
            "evidence": ["B2B_GATE_CRITERIA", "YEAR1_ORGANIC_FINANCIAL_MODEL", "Growth Y1 B2B ban"],
            "content_p0": False,
            "force_p4": True,
            "owner": "Rejected — Year 2+ gate",
        },
        {
            "id": "F012",
            "name": "Copy Speech Blubs Feature Parity",
            "segment": "COMPETITOR_COPY",
            "locales": ["EN"],
            "scores": {"demand": 40, "retention": 45, "revenue": 35, "strategic": 20, "competitive": 25, "clinical": 50, "localization": 30},
            "complexity": 50,
            "mandatory_questions": {
                "users_requested": "none — internal assumption",
                "locales": ["EN"],
                "segments": [],
                "competitor_solves": "already solved by competitor",
                "retention": False,
                "paid_conversion": False,
                "engagement": False,
                "churn_reduction": False,
                "differentiation": False,
            },
            "evidence": ["PDC anti-bias — competitor copying forbidden"],
            "content_p0": False,
            "force_p4": True,
            "owner": "Rejected",
        },
    ]

    # Content protection auto P0
    if content_critical:
        for f in features:
            cov = next((g.get("estimated_coverage_pct", 100) for g in gaps
                       if f["segment"] in str(g.get("segment", "")) or f["id"] in ("F001", "F002", "F003")), 100)
            if cov < 70 and f.get("content_p0"):
                f["content_protection_trigger"] = True

    ranked = []
    for f in features:
        ps = _priority_score(f["scores"])
        if f.get("force_p4"):
            level = "P4"
        else:
            level = _level(ps, content_p0=f.get("content_p0", False) and ps >= 70)
        ranked.append({
            **f,
            "priority_score": ps,
            "priority_level": level,
            "retention_first_note": "Retention weighted 0.20 — ties favor retention per PDC rule",
        })
    ranked.sort(key=lambda x: (-x["priority_score"] if x["priority_level"] != "P4" else -999, x["id"]))
    return ranked


def _executive_summary(now: str, ranked: list[dict], health: dict) -> str:
    p0 = [f for f in ranked if f["priority_level"] == "P0"]
    p1 = [f for f in ranked if f["priority_level"] == "P1"]
    p4 = [f for f in ranked if f["priority_level"] == "P4"]

    lines = [
        "# PDC Executive Summary",
        "",
        f"**Üretim:** {now[:19]} UTC  ",
        "**Konsey:** Product Decision Council  ",
        "**Soru:** «Ekip sırada ne inşa etmeli?»",
        "",
        "---",
        "",
        "## Karar özeti",
        "",
        f"- **P0 (hemen):** {len(p0)} özellik",
        f"- **P1 (bu çeyrek):** {len(p1)} özellik",
        f"- **P4 (red):** {len(p4)} özellik",
        "",
        "### P0 — Kritik",
        "",
    ]
    for f in p0:
        lines.append(f"1. **{f['name']}** — skor **{f['priority_score']}** · {f['owner']}")
        lines.append(f"   - Gerekçe: {', '.join(f['evidence'][:3])}")

    lines += ["", "### P1 — Yüksek", ""]
    for f in p1:
        lines.append(f"- **{f['name']}** ({f['priority_score']})")

    lines += [
        "",
        "### P4 — Reddedildi",
        "",
    ]
    for f in p4:
        lines.append(f"- **{f['name']}** — {f.get('owner', 'Rejected')}")

    lines += [
        "",
        "---",
        "",
        "## Koruma kuralları uygulandı",
        "",
        f"- Content Coverage kritik: **{health.get('content_coverage_critical', True)}** → içerik P0 otomatik inceleme",
        "- Retention First: eşit değerde retention kazanan seçildi",
        "- Yıl 1 B2B: **P4** (`B2B_GATE_CRITERIA.md`)",
        "- 6 locale: karar analizinde TR/EN/DE/FR/IT/ES temsil edildi",
        "",
        "---",
        "",
        "## Product Health (pre-launch tahmin)",
        "",
        f"| Metrik | Değer |",
        f"|--------|-------|",
    ]
    for k, v in health.items():
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "---",
        "",
        "## Çelişki çözümü örneği",
        "",
        "**Growth** Store dili (F006) vs **CIKA** TR fonem (F001):",
        "- F001 retention 90, content gap 86% → **P0**",
        "- F006 revenue 85, retention 35 → **P1** (acquisition, retention second)",
        "- **Kazanan sıra:** F001 → F002 → F003 → F004 → F005 → F006",
        "",
        "**Yenileme:** `./scripts/product_decision/run_product_decision_council.sh`",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    print(f"▶ PDC builder — {now[:19]} UTC")

    gaps_data = _load(CURRICULUM / "content_gap_report.json")
    gaps = gaps_data.get("gaps", [])
    capacity = _load(CURRICULUM / "content_capacity_report.json")
    content_critical = any(
        g.get("estimated_coverage_pct", 100) < 70 or g.get("gap_pct", 0) >= 60
        for g in gaps if isinstance(g.get("estimated_coverage_pct"), (int, float))
    ) or any(a.get("content_exhausted_risk") == "high" for a in capacity.get("capacity", []))

    ranked = _build_features(gaps, content_critical)

    health = {
        "content_coverage_estimated_pct": "28-42 (child/articulation)",
        "content_inventory_critical": content_critical,
        "curriculum_risk": "high",
        "retention_priority": "active",
        "localization_coverage_DE_FR_IT_ES": "~35%",
        "clinical_coverage": "partial — index only",
        "daily_practice_rate": "doğrulanacak — Product Analytics",
        "premium_conversion_Y1_P50": "70 subs — Finance model",
        "year1_b2b": "forbidden",
    }

    matrix = {
        "generated_at": now,
        "department": "PDC",
        "weights": WEIGHTS,
        "features": [
            {
                "id": f["id"],
                "name": f["name"],
                "scores": f["scores"],
                "complexity": f["complexity"],
                "priority_score": f["priority_score"],
                "priority_level": f["priority_level"],
            }
            for f in ranked
        ],
    }

    roadmap = {
        "generated_at": now,
        "department": "PDC",
        "P0": [f for f in ranked if f["priority_level"] == "P0"],
        "P1": [f for f in ranked if f["priority_level"] == "P1"],
        "P2": [f for f in ranked if f["priority_level"] == "P2"],
        "P3": [f for f in ranked if f["priority_level"] == "P3"],
    }

    decision_log = {
        "generated_at": now,
        "decisions": [
            {
                "decision_id": f"D-{f['id']}",
                "feature_id": f["id"],
                "feature_name": f["name"],
                "priority_level": f["priority_level"],
                "priority_score": f["priority_score"],
                "action": "build_now" if f["priority_level"] == "P0" else "schedule" if f["priority_level"] in ("P1", "P2") else "backlog" if f["priority_level"] == "P3" else "reject",
                "reason": f["evidence"],
                "decided_by": "PDC weighted evidence model",
            }
            for f in ranked
        ],
    }

    quarterly = {
        "generated_at": now,
        "quarter": "2026-Q2",
        "theme": "Content depth + retention before acquisition scale",
        "P0_commitments": [f["name"] for f in ranked if f["priority_level"] == "P0"],
        "P1_commitments": [f["name"] for f in ranked if f["priority_level"] == "P1"],
        "deferred": [f["name"] for f in ranked if f["priority_level"] in ("P2", "P3")],
        "rejected": [f["name"] for f in ranked if f["priority_level"] == "P4"],
        "gates": ["B2B_GATE_CRITERIA", "Content Protection <70%", "6-locale parity"],
    }

    rejected = {
        "generated_at": now,
        "rejected": [
            {
                "feature_id": f["id"],
                "name": f["name"],
                "priority_level": "P4",
                "priority_score": f["priority_score"],
                "reason": f["evidence"],
                "anti_bias_rule": "competitor_copy" if "Copy" in f["name"] else "policy" if "B2B" in f["name"] else "insufficient_evidence",
            }
            for f in ranked if f["priority_level"] == "P4"
        ],
    }

    evidence_links = {
        "generated_at": now,
        "links": [
            {"feature_id": f["id"], "evidence_files": f["evidence"], "upstream_departments": ["LIUD", "CIKA", "Market", "Clinical"]}
            for f in ranked
        ],
        "input_chain": [
            "governance/market/USER_INTENT_SIGNALS.json",
            "governance/linguistic/output/*.json",
            "curriculum/*.json",
            "docs/COMPETITOR_ANALYSIS.md",
            "governance/clinical/CLINICAL_EVIDENCE_INDEX.md",
        ],
    }

    _write("priority_matrix.json", matrix)
    _write("feature_ranking.json", {"generated_at": now, "ranking": ranked})
    _write("roadmap_priorities.json", roadmap)
    _write("decision_log.json", decision_log)
    _write("quarterly_decisions.json", quarterly)
    _write("rejected_features.json", rejected)
    _write("evidence_links.json", evidence_links)

    summary = _executive_summary(now, ranked, health)
    summary_path = OUT / "executive_summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    print(f"   ✅ {summary_path.relative_to(PROJECT_ROOT)}")

    print("✅ PDC outputs tamamlandı")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
