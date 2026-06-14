# CEO V7 — Executive Operating System (Delivery Mode)

**Versiyon:** 7.0 · **Portable Factory** · See `governance/project.config.json`

---

## Core principle

**Decision → Delivery → Measurement → Learning**

Analysis does not ship product. Delivery ships product.

---

## Organization (fixed)

EGC → CSGB → CEO → CAO · PDC · CEC · CDID · Intelligence · Factory

No expansion. See `HIERARCHICAL_AUDIT_CHAIN.md` for per-department oversight.

---

## CEO audits departments AND auditors

CEO cycle must answer:

- Which departments delivered user-visible value?
- Which L1/L2 approvals were real vs rubber-stamp?
- CAO scoreboard: who is REVIEW_REQUIRED?
- Sprint lock: is P0 closed before P1?

---

## Sprint lock

`governance/executive/SPRINT_LOCK.json` — P0→P4 immutable order.

Default P0: **AID Sprint P Activation**

---

## Canonical sources

1. `governance/executive/CEO_OPERATING_SYSTEM.md` (this file)
2. `governance/product_decision/roadmap_priorities.json`
3. `governance/reality/PRODUCT_REALITY_SCORE.json`
4. `governance/executive/SPRINT_LOCK.json`
5. `governance/executive/HIERARCHICAL_AUDIT_CHAIN.md`

---

## Scripts

```bash
./scripts/ceo/run_ceo_cycle.sh
./scripts/cao/run_cao_audit.py
./scripts/governance/validate-audit-chain.py
```
