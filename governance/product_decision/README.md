# Product Decision Council — Outputs

**Departman:** PDC (en üst karar mercii)  
**Charter:** [DEPARTMENT_CHARTER.md](DEPARTMENT_CHARTER.md)  
**Agent:** `.cursor/rules/09-product-decision-council.mdc`

İstihbarat → ürün kararı. Kod/UI/içerik/pazarlama yok.

---

## Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `roadmap_priorities.json` | Onaylı P0–P3 yol haritası |
| `priority_matrix.json` | Ağırlıklı skor matrisi |
| `executive_summary.md` | Yönetici özeti |
| `decision_log.json` | Tüm kararlar + gerekçe |
| `feature_ranking.json` | Skora göre sıralı özellikler |
| `quarterly_decisions.json` | Çeyreklik paket |
| `rejected_features.json` | P4 reddedilenler |
| `evidence_links.json` | Kanıt zinciri |

---

## Girdi zinciri

```
Market + Forum + Trends → LIUD → CIKA → PDC → Product/CPO/Architect
```

---

## Yenileme

```bash
./scripts/linguistic/run_linguistic_intelligence.sh
./scripts/curriculum/run_curriculum_intelligence.sh
./scripts/product_decision/run_product_decision_council.sh
```
