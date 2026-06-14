# Chief Audit Officer (CAO)

**CEO denetim kolu** — hiçbir departman kendi çıktısını nihai doğru ilan edemez.

**Agent:** `.cursor/rules/12-chief-audit-officer.mdc`

---

## Soru

> «Tüm departmanlar doğru çalışıyor mu?»

---

## Üretir

| Dosya | Açıklama |
|-------|----------|
| `audit_report.json` | Tam denetim |
| `consistency_report.json` | Çelişen raporlar |
| `integrity_report.json` | Pipeline bütünlüğü |
| `governance_report.json` | Charter / approval uyumu |
| `department_scoreboard.json` | CEO skor kartı girdisi |

**Script:** `scripts/cao/run_cao_audit.py`

---

## CEO döngüsü

Adım **13** — PDC sonrası, Factory gates öncesi.

CAO `REVIEW_REQUIRED` sayısı > 0 ve critical conflict varsa → `CEO_STOP.json`
