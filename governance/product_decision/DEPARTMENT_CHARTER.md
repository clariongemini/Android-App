# Product Decision Council (PDC)

**Türkçe:** Ürün Karar Konseyi  
**Otorite:** Konuşma ekosisteminde **en üst karar mercii**

---

## Misyon

Tüm departmanların bulgularını **ürün önceliğine** dönüştürmek.

Yol haritası kaosunu önlemek.

---

## Sorumluluk sınırı

| Yapar | Yapmaz |
|-------|--------|
| Ne inşa · ertele · iptal · hızlandır | Kod, UI, içerik, pazarlama, araştırma |

---

## Temel soru

> «Ekip sırada ne inşa etmeli?»

---

## Karar felsefesi

En gürültülü departman değil — **en güçlü kanıt** kazanır.

Çelişkide oylama yok — skorlu kanıt karşılaştırması.

---

## Girdi departmanları

CIKA · LIUD · Growth · Demand · Search Intent · Forum · Competitor · Monetization · Product Analytics · Clinical · Localization · Architecture · QA

---

## Öncelik modeli

| Skor | Ağırlık |
|------|---------|
| User Demand | 0.25 |
| Retention Impact | 0.20 |
| Revenue Impact | 0.15 |
| Strategic Value | 0.15 |
| Competitive Advantage | 0.10 |
| Clinical Importance | 0.10 |
| Localization Impact | 0.05 |

Technical Complexity ayrı alan — yüksek complexity + düşük skor → erteleme sinyali.

---

## Öncelik seviyeleri

| Seviye | Eşik (tipik) | Anlam |
|--------|--------------|-------|
| P0 | ≥ 82 veya content protection | Hemen |
| P1 | 70–81 | Bu çeyrek |
| P2 | 55–69 | Gelecek çeyrek |
| P3 | 40–54 | Backlog |
| P4 | < 40 veya kanıt yok / politika | Red |

---

## Koruma kuralları

1. **Content Protection** — Coverage < %70 → P0 inceleme
2. **Retention First** — eşit değerde retention kazanır
3. **Localization** — 6 locale analizde temsil zorunlu
4. **Yıl 1 B2B yasağı** — `B2B_GATE_CRITERIA.md`
5. **No New P0 (CEO V5 binding)** — Execution Coverage < **80%** **veya** Product Reality Score < **80** iken PDC **yeni P0 üretemez**. Gate: `governance/reality/NO_NEW_P0_RULE.json`. Sebep: karar eksikliği değil, teslimat eksikliği.

---

## Anti-bias

Kurucu fikri kanıtsız · rakip kopyası · trend · varsayım · politika · shiny object — **yasak**

---

## Çıktılar

| Dosya | Açıklama |
|-------|----------|
| `roadmap_priorities.json` | P0–P3 sıralı yol haritası |
| `priority_matrix.json` | Skor matrisi |
| `executive_summary.md` | Yönetici özeti |
| `decision_log.json` | Karar geçmişi |
| `feature_ranking.json` | Tüm özellikler sıralı |
| `quarterly_decisions.json` | Çeyreklik paket |
| `rejected_features.json` | P4 + gerekçe |
| `evidence_links.json` | Kanıt → karar zinciri |

---

## Product Health Dashboard (izleme)

Content Coverage · Retention · Churn · Feature Adoption · Learning Completion · Premium Conversion · Daily Practice Rate · Session Length · Localization Coverage · Clinical Coverage

---

## Döngü

| Sıklık | Aktivite |
|--------|----------|
| Haftalık | Yeni bulgular → decision_log |
| Aylık | feature_ranking re-rank |
| Çeyreklik | quarterly_decisions yeniden inşa |

**Script:** `./scripts/product_decision/run_product_decision_council.sh`

**Önerilen sıra:** LIUD → CIKA → **PDC**

---

## Başarı koşulu

Yol haritası her zaman yansıtır:
- Kullanıcının en çok ihtiyaç duyduğu
- Retention'ı en çok artıran
- Rekabet avantajı en yüksek
- Global konuşma gelişimi liderliğine en çok yaklaştıran

**PDC özellik inşa etmez — ürünün geleceğine karar verir.**
