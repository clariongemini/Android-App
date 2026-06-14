# Ajan Onay Protokolü — Hiyerarşik Çok Katmanlı Onay

**Sürüm:** 3.0  
**Tarih:** 2026-06-14  
**Kapsam:** Executive OS — tüm Factory projeleri  
**Denetim zinciri:** [HIERARCHICAL_AUDIT_CHAIN.md](HIERARCHICAL_AUDIT_CHAIN.md)

---

## İlke

**Tek ajan onayı yasak.** Her iş paketi üst departman + denetim kolu + CEO sprint uyumu geçer.

---

## Hiyerarşi (Alt → Üst)

```
Mimar — nihai onay
    ↑
Overmind (.cursorrules) — L2 kapı + koordinasyon
    ↑
EGC → CSGB → CEO
    ↑
CAO · PDC · CEC · CDID · Intelligence · Factory
    ↑
Factory: CPO · Architect · Android · Security · OEM · MCP
```

Detaylı L1/L2 eşlemesi: `HIERARCHICAL_AUDIT_CHAIN.md`

---

## PDC → Execution Zorunlu Tüketim

Execution ajanları **her oturumda** okur:

1. `governance/product_decision/roadmap_priorities.json`
2. `governance/product_decision/rejected_features.json`
3. `governance/executive/CEO_OPERATING_SYSTEM.md`
4. `governance/executive/SPRINT_LOCK.json`

Contract: `governance/execution/PDC_CONSUMPTION_CONTRACT.md`  
Doğrulama: `python3 scripts/execution/validate_roadmap_consumption.py`

---

## Zorunlu Akış (v3)

1. **Talep** — APPROVAL_QUEUE.md — **feature_id zorunlu**
2. **PDC check** — roadmap + rejected
3. **Uygulama** — `review`
4. **L1** — Üst departman (HIERARCHICAL_AUDIT_CHAIN tablosu) → `approved_l1`
5. **L2** — CAO veya vekili (Security/OEM/PDC) → `approved_l2`
6. **CEC gate** — alignment ≥ 80
7. **CEO** — sprint lock + reality check
8. **Kapı** — `./scripts/agent-approval-gate.sh <WP-ID>` → `completed`

---

## İş Paketi → Onay eşlemesi

| İş türü | Uygulayan | L1 | L2 |
|---------|-----------|----|----|
| Ürün / onboarding | CPO | PDC | CAO |
| Mimari / repository | Architect | CEC | CAO |
| UI / Compose / i18n | Android | Architect | CPO |
| Güvenlik / review | Security | Architect | CAO |
| OEM / bildirim | OEM | Android | Security |
| MCP / CI / script | MCP | Architect | CAO |
| Content / curriculum | CIKA | PDC | CAO |
| Analytics / AID | AID | CAO | CEO |
| Roadmap | PDC | CAO | CEO |
| Execution alignment | CEC | CEO | CSGB |

---

## Durum Kodları

| Kod | Anlam |
|-----|-------|
| `pending` | Sırada |
| `in_progress` | Ajan çalışıyor |
| `review` | L1 bekliyor |
| `approved_l1` | L1 tamam, L2 bekliyor |
| `approved_l2` | L2 tamam |
| `completed` | Gate geçti |
| `blocked` | Dış kapsam |

---

## Gate Komutları

```bash
./scripts/agent-approval-gate.sh
./scripts/agent-approval-gate.sh WP-01
python3 scripts/execution/validate_roadmap_consumption.py
python3 scripts/execution/run_cec_audit.py
python3 scripts/governance/validate-audit-chain.py
python3 scripts/cao/run_cao_audit.py
```
