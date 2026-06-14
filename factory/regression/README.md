# Factory Regression Database

**Memory güzel — regression agresif kullanılmalı.**

Her bilinen hata bir kez çözülür, bir daha tekrarlanmamalı.

## Kayıt şeması (memory failure genişletmesi)

```
FAIL-2026-001
  → root_cause
  → fix_pattern
  → affected_modules
  → preventive_check    # quality gate tarar
```

## Örnek kayıtlar (seed)

| ID | Konu | Preventive check |
|----|------|------------------|
| FAIL-2026-001 | Compose Navigation Loop | SavedStateHandle in navigation |
| FAIL-2026-002 | Samsung background kill | OEM battery whitelist |
| FAIL-2026-003 | Room migration failure | Migration spec + fallback |
| FAIL-2026-004 | FCM delivery | FCM token refresh handler |
| FAIL-2026-005 | Billing restore | BillingClient acknowledge |

## Komutlar

```bash
python3 scripts/factory/seed-regression-catalog.py   # memory → catalog
python3 scripts/factory/scan-regression.py             # quality gate hook
./scripts/factory/query-memory.sh "billing restore"
```

**Soru:** Bu hata daha önce yaşandı mı? → **Evet, ve fix pattern biliniyor.**
