# Market Intelligence Department

**Soru:** Pazar ne istiyor, rakipler ne yapıyor, organik büyüme mümkün mü?  
**Durum:** v1 — demand intelligence + VOC/JTBD + finans modelleri  
**Agent rule:** `.cursor/rules/17-marketing-growth.mdc`

---

## Üretir

| Dosya | Açıklama |
|-------|----------|
| `MARKET_DEMAND_RESEARCH.md` | Pazar talebi, epidemiyoloji, arama sinyalleri |
| `VOC_JTBD_DEMAND_RESEARCH.md` | Voice of Customer + Jobs-to-be-Done |
| `DEMAND_INTELLIGENCE_SYSTEM.md` | Talep istihbaratı çerçevesi |
| `REVIEW_INTELLIGENCE_SYSTEM.md` | Play Store yorum analizi |
| `FORUM_INTELLIGENCE_PLAN.md` | Forum/sosyal sinyal planı |
| `competitor_catalog.json` | Rakip kataloğu |
| `demand_intelligence_catalog.json` | Talep sinyali kataloğu |
| `YEAR1/2/3_ORGANIC_FINANCIAL_MODEL.md` | Organik büyüme finans modelleri |
| `QUARTERLY_GROWTH_SCORECARD.md` | Çeyreklik büyüme skoru |

**İlişkili departmanlar:** LIUD (`governance/linguistic/`), Trends (`governance/trends/`), Mavi Okyanus (`governance/blue_ocean/`)

---

## Denetim zinciri

| Katman | Departman |
|--------|-----------|
| L1 | **CPO** — ürün vizyonu ve monetizasyon uyumu |
| L2 | **CAO** — kanıt kalitesi, halüsinasyon sıfır |
| L3 | **CEO** — sprint lock, reality uyumu |

---

## Yasaklar

- İyimser projeksiyon without evidence
- LIUD dil derinliğini Growth tek başına override etmez
- B2B Yıl2+ eşiği `B2B_GATE_CRITERIA.md` olmadan açılmaz

---

## Bootstrap

Market verisi proje özeldir. `init-governance.sh` generic seed üretir; pazar araştırması Growth ajanı + MCP Browser ile doldurulur.

Kılavuz: [README.md](README.md) · [DEMAND_INTELLIGENCE_SYSTEM.md](DEMAND_INTELLIGENCE_SYSTEM.md)
