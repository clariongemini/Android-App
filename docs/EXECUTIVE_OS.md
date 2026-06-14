# Executive Operating System — Factory Guide

Production-grade **CEO + Agents + hierarchical audit** system — portable to every Android project bootstrapped from this factory.

## Factory vs application project

| Location | Role |
|----------|------|
| **This repo (Factory)** | Canonical source — rules, charters, scripts, templates, generic seeds |
| **Application project** | Live data — sprint lock, approval queue, roadmap, analytics output |

Runtime governance files (sprint lock, approval queue, project config) are **generated per project** by `init-governance.sh`, not copied from another app's live state.

## Hiyerarşik denetim (tek ajan onayı yasak)

`governance/executive/HIERARCHICAL_AUDIT_CHAIN.md`

- Her departmanın **üst departmanı** (L1) vardır
- **CAO** denetçileri ve denetim kalitesini ölçer
- **CEO** hangi departmanın doğru çalıştığını ve hangi denetimin eksik olduğunu ölçer
- **EGC/CSGB** CEO performansını ölçer

## Bootstrap

```bash
./scripts/init-new-app.sh "MyApp" "com.company.app"
# otomatik: init-governance.sh + YAPILACAKLAR.md

./scripts/run-ceo-cycle.sh
python3 scripts/cao/run_cao_audit.py
python3 scripts/governance/validate-audit-chain.py
python3 scripts/governance/validate-yapilacaklar.py
./scripts/agent-approval-gate.sh
```

## AID Sprint P (default P0)

`governance/analytics/SPRINT_P_EVENT_CATALOG.json`  
Proje `google-services.json` + cihaz kanıtı sonrası gate ACTIVE.

## Script ağacı (Executive OS)

```
scripts/
├── run-ceo-cycle.sh          # wrapper → ceo/run_ceo_cycle.sh
├── init-governance.sh        # wrapper → governance/init-governance.sh
├── agent-approval-gate.sh    # canonical approval gate
├── ceo/run_ceo_cycle.sh
├── cao/run_cao_audit.py
├── cdid/run_cdid_cycle.py
├── egc/run_egc_governance_cycle.py
├── execution/run_cec_audit.py
├── execution/validate_roadmap_consumption.py
├── reality/run_product_reality_layer.py
├── analytics/build_aid_output.py
├── product_decision/
├── governance/init-governance.sh
├── governance/validate-audit-chain.py
└── governance/validate-yapilacaklar.py
```

## Cursor rules (16 ajan + Overmind)

`.cursor/rules/00` … `16` + `17-marketing-growth` + Overmind `.cursorrules`

Import: `./scripts/sync-standards.sh /path/to/project`
