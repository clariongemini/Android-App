# EGC — Executive Governance Council

**Versiyon:** 1.0  
**Tarih:** 2026-06-14  
**Agent:** `.cursor/rules/14-executive-governance-council.mdc`  
**Script:** `./scripts/egc/run_egc_governance_cycle.py`

---

## Konum

```
EGC
├── CSGB
└── CEO
     ├── CAO · PDC · CEC
     ├── Intelligence Division
     └── Factory Division
```

EGC, organizasyonun **en üst yönetim kurulu** katmanıdır.  
CEO operasyonel otoritedir; EGC **CEO'nun patronudur**.

CSGB CEO performansını değerlendirir; EGC tüm şirket yönetişimini denetler.

---

## Tek soru

> «Bu şirket bizi dünya liderliğine götürüyor mu?»

CEO yalnızca şu soruya cevap verir:

> «Bu çeyrek ne yapacağız?»

---

## 7 görev

| # | Görev | Çıktı |
|---|-------|-------|
| 1 | CEO Performans Denetimi | `CEO_PERFORMANCE_SCORECARD.json` |
| 2 | PDC Karar Kalitesi | `PDC_DECISION_QUALITY.json` |
| 3 | Roadmap Drift Kontrolü | `ROADMAP_DRIFT_REPORT.json` |
| 4 | Department ROI | `DEPARTMENT_ROI.json` |
| 5 | Global Leadership Score | `GLOBAL_LEADERSHIP_SCORE.json` |
| 6 | Strategic Debt | `STRATEGIC_DEBT_REGISTER.json` |
| 7 | 5 Yıllık Vizyon Kontrolü | `FIVE_YEAR_VISION_ALIGNMENT.md` |

---

## Company Health V3

```
Execution Health
Intelligence Health
Strategy Health
Governance Health
Market Health
Product Health
        ↓
Company Health Score
```

Kanoni̇k: `governance/egc/COMPANY_HEALTH_SCORE.json`

---

## EGC Verdict (bağlayıcı)

| Verdict | Anlam |
|---------|-------|
| **WORLD_CLASS** | Dünya liderliği yörüngesinde · tüm boyutlar güçlü |
| **GO** | Sağlıklı · execution + intelligence hizalı |
| **REVIEW_REQUIRED** | Kritik gap · CEO/departman müdahalesi |
| **RESTRUCTURE** | Organizasyon borcu · yapısal müdahale gerekli |
| **NO_GO** | Bütünlük/strateji krizi · execution dondurulur |

CEO Master Report operasyonel özet sunar; **nihai şirket verdict'i EGC'dendir.**

---

## Bağlayıcı girdiler

- `governance/executive/CEO_MASTER_REPORT.md`
- `governance/executive/CEO_SCORECARD.json`
- `governance/executive/CEO_STRATEGIC_GOVERNANCE_REVIEW.md`
- `governance/cao/audit_report.json`
- `governance/execution/ROADMAP_CONSUMPTION_REPORT.json`
- `governance/product_decision/roadmap_priorities.json`

---

## İnsan temsilcisi

**Owner:** Ulaş Kaşıkcı — EGC nihai insan onayı · 5 yıllık vizyon · RESTRUCTURE/NO_GO override

---

## Sınırlar

EGC kod yazmaz · roadmap üretmez · departman audit'i yapmaz (CAO) · execution ölçmez (CEC).

EGC **karar doğruluğunu** ve **uzun vadeli liderlik yörüngesini** ölçer.
