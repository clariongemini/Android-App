# Clinical Intelligence Department (CLID)

**Soru:** Bu içerik bilimsel olarak doğru mu?  
**Agent:** CAO denetir; CLID charter — dedicated `.mdc` yok (v1 stub + script)

---

## Üretir

| Dosya | Açıklama |
|-------|----------|
| `output/clinical_validation.json` | Onay / veto / koşullu |
| `output/age_norms.json` | Fonem yaş normları (genişletilecek) |
| `output/evidence_matrix.json` | Kanıt seviyesi |
| `output/risk_report.json` | Klinik risk bayrakları |

**Script:** `scripts/clinical/build_clid_output.py`

---

## CEO durdurma

`risk_report.json` → `risk_level: high` → CEO STOP tetikleyici

**Index:** `CLINICAL_EVIDENCE_INDEX.md`
