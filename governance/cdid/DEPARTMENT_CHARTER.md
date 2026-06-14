# CDID — Chief Delivery Intelligence Department

**Versiyon:** 1.0  
**Tarih:** 2026-06-14  
**Agent:** `.cursor/rules/15-chief-delivery-intelligence.mdc`  
**Script:** `./scripts/cdid/run_cdid_cycle.py`

---

## Konum

```
CEO
├── CAO
├── PDC
├── CEC
├── CDID  ← karar → iş paketi dönüşümü
└── Factory
```

---

## Tek soru

> «Bu kararın uygulanabilmesi için hangi WP'ler açılmalı?»

---

## V4 ilkesi

**Hiçbir kritik bulgu aksiyonsuz kalamaz.**

Her P0/P1 kararının otomatik execution karşılığı olmalıdır.

---

## Otomatik Work Package Engine

**Girdi:** `governance/product_decision/roadmap_priorities.json`

Her feature için zincir:

Research → Content → Android → QA → Release

**Çıktı:** `governance/cdid/GENERATED_WORK_PACKAGES.json`

---

## Metrikler

| Metrik | Formül | Hedef |
|--------|--------|-------|
| Execution Coverage | implemented / approved | ≥ 90% |
| Unowned Gaps | owner veya WP eksik | 0 RED FLAG |
| Escalation | P0 14g ilerlemez veya alignment < 70 | CEO → CEC |

---

## Kanonik çıktılar

- `governance/execution/EXECUTION_COVERAGE.json`
- `governance/execution/UNOWNED_GAPS.json`
- `governance/execution/ESCALATION_REPORT.md`
- `governance/execution/DELIVERY_PREDICTION_ACCURACY.json`
- `governance/memory/ORGANIZATIONAL_MEMORY.json`
- `governance/executive/CEO_AUTONOMOUS_REPORT.md` (CEO V4)

---

## Organizational Memory

`governance/memory/` — DECISION · DELIVERY · FAILURE · SUCCESS history

Learning loop: Beklenen Etki vs Gerçek Etki → PDC · CEO · EGC girdisi

---

## Sınırlar

CDID roadmap **yazmaz** (PDC). Kod **yazmaz** (Factory). Audit **yapmaz** (CAO).

WP üretir · coverage ölçer · gap tespit eder · escalate eder · öğrenir.
