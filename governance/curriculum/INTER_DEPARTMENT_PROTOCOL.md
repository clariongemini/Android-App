# CIKA — Departmanlar Arası Protokol

**Departman:** Curriculum Intelligence & Knowledge Architect  
**Kural:** Müfredat varsayımla tasarlanamaz.

---

## Girdi okuma (her döngü)

| Kaynak departman | Dosya | CIKA kullanımı |
|------------------|-------|----------------|
| LIUD / Demand | `governance/linguistic/output/*.json` | Gap, JTBD, intent → learning path |
| Search Intent | `demand_output/search_intent/` | SEO/ASO kelime → content title |
| Forum Intelligence | `USER_INTENT_SIGNALS.md`, `forum_output/` | Gerçek cümle → exercise copy |
| Competitor Intelligence | `COMPETITOR_ANALYSIS.md`, reviews | Rakip boşluğu → backlog |
| Monetization | `monetization_research.json` | Premium content tier |
| Clinical Validation | `governance/clinical/` | Clinical score, veto |
| Growth | `DEMAND_INTELLIGENCE_REPORT.md` | Kanal önceliği ≠ curriculum önceliği ayrımı |
| Localization | 6 locale kuralı | language_content_map parity |
| Product Analytics | (gelecek) | Fatigue detection gerçek veri |

---

## Geri yayın (CIKA → organizasyon)

| Çıktı | Tüketiciler |
|-------|-------------|
| `content_gap_report.json` | LIUD, Product, CPO |
| `future_content_backlog.json` | Product & Education, Android (içerik pipeline) |
| `exercise_requirements.json` | Clinical (doğrulama), LIUD (hedef uyumu) |
| `content_capacity_report.json` | Finance (retention ROI), Growth |
| `skill_tree.json` | Product UX (ilerleme gösterimi — spec only) |

---

## Çelişki çözümü

| Çelişki | Karar |
|---------|-------|
| LIUD talep yüksek, Clinical henüz onaylamadı | İçerik planlanır, release Clinical gate |
| Growth hızlı locale, CIKA parity eksik | **Parity önce** — kısmi locale launch yasak |
| Rakip feature kopyası vs demand gap | Demand + gap score birincil |
| Miktar hedefi vs variety düşük | Variety skoru düşükse hedef sayılmaz |

---

## INTER-DEPARTMENT FINDINGS (rapor sonu)

CIKA aylık notunda (opsiyonel `governance/curriculum/reports/`):

- Uyumlu Bulgular
- Çelişen Bulgular
- Riskler (capacity, parity)
- Kaçırılan Fırsatlar
- Beklenen Aksiyonlar
- Ortak backlog maddeleri
