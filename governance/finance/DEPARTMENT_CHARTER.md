# Finance Intelligence Department (FID)

**Soru:** Bu özellik para kazandırıyor mu?

---

## Üretir

| Dosya | Açıklama |
|-------|----------|
| `output/ltv_model.json` | LTV bantları |
| `output/roi_analysis.json` | Özellik ROI (PDC skorları ile) |
| `output/revenue_forecast.json` | Y1/Y2/Y3 özet |
| `output/premium_conversion.json` | Premium dönüşüm projeksiyonu |

**Script:** `scripts/finance/build_fid_output.py`  
**Girdi:** `YEAR*_ORGANIC_FINANCIAL_MODEL.md`, `monetization_research.json`, PDC revenue scores

---

## Not

Finans modelleri `governance/market/` altında — FID bunları **CEO skor kartına** normalize eder.
