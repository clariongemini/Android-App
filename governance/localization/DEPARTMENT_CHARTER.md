# Localization Intelligence Department (LID)

**Soru:** Tüm locale'ler eşit kalitede mi?

---

## Üretir

| Dosya | Açıklama |
|-------|----------|
| `output/locale_parity.json` | TR/EN/DE/FR/IT/ES parity |
| `output/translation_gaps.json` | Eksik çeviri / içerik |
| `output/cultural_adaptation.json` | Kültürel uyarlama notları |

**Script:** `scripts/localization/build_lid_output.py`  
**Girdi:** `curriculum/language_content_map.json`, `validate-store-listing.sh` sonuçları, CPO audit

---

## CEO kuralı

Yalnızca EN optimizasyonu **yasak** — 6 locale zorunlu.
