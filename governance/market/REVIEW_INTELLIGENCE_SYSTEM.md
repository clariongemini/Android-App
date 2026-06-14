# Play Store Yorum Zekâsı Sistemi

**Amaç:** Rakip yorumlarından **beğeni / şikâyet / istek** + **«insanlar ne istiyor?»** katmanı.

---

## Katmanlar (ikisi de zorunlu)

| Katman | Soru | Modül |
|--------|------|-------|
| **Pazar sinyali** | Ne kadar insan? Rakip zayıf mı? | `THEME_PATTERNS` |
| **Kullanıcı niyeti** | Tam olarak ne istiyor? | `USER_INTENT_PATTERNS` |

Çıktılar:
- `docs/COMPETITOR_ANALYSIS.md` — rakip + **6 locale**
- `governance/market/USER_INTENT_SIGNALS.md` — özellik talebi
- `governance/market/FORUM_INTELLIGENCE_PLAN.md` — Reddit/TR forum (planlı)

---

## Bileşenler

| Dosya | Rol |
|-------|-----|
| `competitor_catalog.json` | 13 rakip + **6 locale** |
| `play_store_analyzer.py` | Metadata + yorum |
| `review_intelligence.py` | Tema + **USER_INTENT** |
| `analyze_user_intent.py` | Niyet raporu üretici |
| `generate_market_report.py` | Rakip MD + benchmark JSON |
| `forum_intelligence.py` | Forum iskelet (planlı) |

---

## Growth ajanı — kalıcı kurallar

1. **620 abone yasak** — P50 = **50–150** ücretli (hedef 100).
2. **ASO tek motor değil** — Klinik %40 · ASO %40 · SEO %20.
3. **6 locale eşit** — tr, en, de, fr, it, es.
4. Forum verisi olmadan «tam anlayış» iddiası yasak.
5. Klinik kanalı **birincil** — destekleyici değil.

Detay: `.cursor/rules/17-marketing-growth.mdc`

---

## Çalıştırma

```bash
source .venv-scraper/bin/activate
python scripts/scrapers/play_store_analyzer.py --locale tr,en,de,fr,it,es --search
python scripts/scrapers/generate_market_report.py
python scripts/scrapers/analyze_user_intent.py
```

**Revizyon:** Ayda 1 + forum batch (planlı).
