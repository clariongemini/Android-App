# Chief Execution Council (CEC) — Department Charter

**Versiyon:** 1.0  
**Tarih:** 2026-06-14  
**Agent:** `.cursor/rules/13-chief-execution-council.mdc`  
**Reports to:** CEO  
**Audit script:** `./scripts/execution/run_cec_audit.py`

---

## Mission

PDC kararlarının Execution Division tarafından **gerçekten okunup uygulandığını** ölçmek ve doğrulamak.

CAO departman kalitesini denetler.  
CEC **karar → uygulama** hattını denetler.

---

## Organization

```
CEO
├── CAO (audit integrity)
├── PDC (decisions)
└── CEC (execution alignment)
    ├── CPO
    ├── Architect
    ├── Android
    ├── Security
    └── OEM
```

---

## Core Question

> «PDC'nin P0 kararları Execution tarafında aktif olarak tüketiliyor ve uygulanıyor mu?»

---

## Outputs (canonical)

| File | Purpose |
|------|---------|
| `EXECUTION_ALIGNMENT_REPORT.md` | Executive summary for CEO/CSGB |
| `ROADMAP_CONSUMPTION_REPORT.json` | Rule enforcement + P0 consumption status |
| `FEATURE_DELIVERY_SCOREBOARD.json` | Per-P0 delivery signals |
| `EXECUTION_BLOCKERS.json` | Active blockers and violations |
| `DELIVERY_VELOCITY_REPORT.md` | WP velocity + queue linkage |

---

## Execution Alignment Score

```
Execution Alignment = (P0 items with active execution signals / P0 total) × 100
```

Rule enforcement layer must be **active** or alignment is capped.

**CEO V3 rule:** IF Execution Alignment < 80 → Verdict ≤ REVIEW_REQUIRED

---

## Boundaries

CEC does **not**:
- Create roadmap priorities (PDC only)
- Audit department output quality (CAO)
- Write production code

CEC **does**:
- Validate PDC → Execution consumption contract
- Score P0 delivery progress
- Flag scope creep and missing feature_id on WPs
- Report blockers to CEO Master Report

---

## Integration

CEO cycle Step 14 (after PDC, before CAO): `./scripts/execution/run_cec_audit.py`
