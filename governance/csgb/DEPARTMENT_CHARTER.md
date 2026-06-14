# CSGB — Strategic Governance Board

**Versiyon:** 2.0  
**Tarih:** 2026-06-14  
**Konum:** EGC altında — CEO stratejik denetim organı

---

## Rol

CSGB (Chief Strategic Governance Board), CEO Agent'ın **stratejik performans değerlendiricisidir**.

- **EGC** tüm şirket yönetişimini ve CEO hesap verebilirliğini denetler.
- **CSGB** CEO'nun çeyreklik stratejik uyumunu değerlendirir ve EGC'ye girdi sunar.
- CSGB kod yazmaz, roadmap üretmez, departman audit'i yapmaz.

---

## Hiyerarşi

```
EGC
└── CSGB
    └── CEO
```

---

## Bağlayıcı girdiler

| Kaynak | Dosya |
|--------|-------|
| CEO kararı | `governance/executive/CEO_MASTER_REPORT.md` |
| Stratejik inceleme | `governance/executive/CEO_STRATEGIC_GOVERNANCE_REVIEW.md` |
| Company Health | `governance/egc/COMPANY_HEALTH_SCORE.json` |
| EGC verdict | `governance/egc/EGC_VERDICT.json` |
| Roadmap | `governance/product_decision/roadmap_priorities.json` |

---

## Değerlendirme kriterleri

1. North Star'a yaklaşma
2. Kanıt kalitesi ve bütünlüğü
3. Retention-first önceliklendirme
4. Y1 B2B gate uyumu
5. PDC-only roadmap disiplini
6. Execution Alignment ≥ 80 hedefi
7. Company Health ≥ 75 sürdürülebilirliği

---

## CSGB → EGC

CSGB çıktısı (`CEO_STRATEGIC_GOVERNANCE_REVIEW.md`) EGC Step 17 girdisidir.  
Nihai şirket verdict'i **EGC** tarafından verilir.

---

## İnsan temsilcisi

**Owner:** Ulaş Kaşıkcı — CSGB stratejik onay · EGC RESTRUCTURE/NO_GO override
