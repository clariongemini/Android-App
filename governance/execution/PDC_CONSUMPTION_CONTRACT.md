# PDC → Execution Mandatory Consumption Contract

**Versiyon:** 1.0  
**Tarih:** 2026-06-14  
**Authority:** CEO V2 — P0 Organizational Fix  
**Binding:** Tüm Execution Division ajanları (CPO, Architect, Android, Security, OEM)

---

## Problem

```
Market → LIUD → CIKA → PDC → ??? → CPO → Architect → Android
```

PDC karar veriyor; Execution Division bu kararları okumak zorunda değildi.  
Bu durum CEO OS'u teorik hale getirir.

---

## Contract

### Zorunlu okuma (her execution oturumu)

1. `governance/product_decision/roadmap_priorities.json` — **tek resmi roadmap**
2. `governance/product_decision/rejected_features.json` — yasak liste
3. `governance/executive/CEO_MASTER_REPORT.md` — P0/P1 ve verdict
4. `governance/execution/ROADMAP_CONSUMPTION_REPORT.json` — CEC alignment durumu

### Zorunlu davranış

| Kural | Açıklama |
|-------|----------|
| P0-first | Yalnızca PDC P0 (veya CEO onaylı P1) üzerinde çalış |
| ID linkage | Her iş paketi (WP) bir PDC `feature_id` (F001…) referansı taşır |
| Reject respect | `rejected_features.json` maddeleri scope'a alınmaz |
| No self-roadmap | Execution ajanları roadmap_priority **yayımlamaz** |
| CEC gate | CEC alignment < 80 → execution scope genişletme yasak |

### Doğrulama

```bash
python scripts/execution/validate_roadmap_consumption.py
./scripts/execution/run_cec_audit.py
```

---

## Enforcement Layer

| Bileşen | Dosya |
|---------|-------|
| CPO rule | `.cursor/rules/01-product-cpo.mdc` |
| Architect rule | `.cursor/rules/02-architect.mdc` |
| Android rule | `.cursor/rules/03-android-elite.mdc` |
| Security rule | `.cursor/rules/04-auditor-security.mdc` |
| OEM rule | `.cursor/rules/05-oem-compat-auditor.mdc` |
| CEC rule | `.cursor/rules/13-chief-execution-council.mdc` |
| Manifest | `governance/execution/ROADMAP_CONSUMPTION_MANIFEST.json` |

---

## Violations

CEC `EXECUTION_BLOCKERS.json` içine yazılır:

- P0 dışı feature without CEO override
- Missing feature_id on active WP
- rejected_features scope creep
- Rule file missing PDC consumption clause
