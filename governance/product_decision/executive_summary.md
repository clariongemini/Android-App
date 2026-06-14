# PDC Executive Summary

**Üretim:** 2026-06-14T02:18:15 UTC  
**Konsey:** Product Decision Council  
**Soru:** «Ekip sırada ne inşa etmeli?»

---

## Karar özeti

- **P0 (hemen):** 3 özellik
- **P1 (bu çeyrek):** 3 özellik
- **P4 (red):** 2 özellik

### P0 — Kritik

1. **TR Fonem Expansion (R/Ş/L)** — skor **87.1** · Product & Education + CIKA
   - Gerekçe: LIUD content_gaps urgent, CIKA gap 86%, USER_INTENT phoneme 64
1. **LATE_TALKER Parent Phrase Bank** — skor **80.85** · Product & Education
   - Gerekçe: forum batch KK, CIKA content_gap 72%, LIUD speech_delay
1. **365 Daily Missions CHILD_4_7 (non-repeating)** — skor **79.6** · CIKA + Product
   - Gerekçe: CIKA minimum standard, forum content_repetitive 33, daily_practice_engine

### P1 — Yüksek

- **STT Phoneme Calibration** (78.15)
- **5–10 dk Speech Time Ritual (UX + content)** (76.15)
- **Stuttering Exposure Hierarchy (500 scenarios)** (71.0)

### P4 — Reddedildi

- **B2B Clinical / Therapist Portal Year 1** — Rejected — Year 2+ gate
- **Copy Speech Blubs Feature Parity** — Rejected

---

## Koruma kuralları uygulandı

- Content Coverage kritik: **True** → içerik P0 otomatik inceleme
- Retention First: eşit değerde retention kazanan seçildi
- Yıl 1 B2B: **P4** (`B2B_GATE_CRITERIA.md`)
- 6 locale: karar analizinde TR/EN/DE/FR/IT/ES temsil edildi

---

## Product Health (pre-launch tahmin)

| Metrik | Değer |
|--------|-------|
| content_coverage_estimated_pct | 28-42 (child/articulation) |
| content_inventory_critical | True |
| curriculum_risk | high |
| retention_priority | active |
| localization_coverage_DE_FR_IT_ES | ~35% |
| clinical_coverage | partial — index only |
| daily_practice_rate | doğrulanacak — Product Analytics |
| premium_conversion_Y1_P50 | 70 subs — Finance model |
| year1_b2b | forbidden |

---

## Çelişki çözümü örneği

**Growth** Store dili (F006) vs **CIKA** TR fonem (F001):
- F001 retention 90, content gap 86% → **P0**
- F006 revenue 85, retention 35 → **P1** (acquisition, retention second)
- **Kazanan sıra:** F001 → F002 → F003 → F004 → F005 → F006

**Yenileme:** `./scripts/product_decision/run_product_decision_council.sh`
