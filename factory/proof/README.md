# Proof Engine — Feature Proven

**Soru:** WP tamamlandı — kanıtı nerede?

## Durum geçişi

```
PLANNED → IN_PROGRESS → COMPLETED → PROVEN
```

`PROVEN` için minimum kanıt tipleri (projeye göre yapılandırılır):

| Tip | Örnek | Kaynak |
|-----|--------|--------|
| `commit` | `a81f7e2` | git |
| `apk` | `build-260-debug.apk` | Gradle CI |
| `analytics` | `phrase_completed` | Sprint P / AID |
| `test` | `maestro/smoke.yaml` | Maestro |
| `audit` | `docs/AUDIT_REPORT.md` | factory audit |

## Şema

Runtime: `factory/runtime/proof/proof_registry.json`

```json
{
  "version": "1.0",
  "features": [
    {
      "feature_id": "F002",
      "wp_id": "WP-25",
      "status": "PROVEN",
      "proofs": [
        { "type": "commit", "value": "a81f7e2", "recorded_at": "2026-06-14T12:00:00Z" },
        { "type": "apk", "value": "assembleDebug-260", "recorded_at": "2026-06-14T12:05:00Z" },
        { "type": "analytics", "value": "phrase_completed", "recorded_at": "2026-06-14T12:10:00Z" }
      ],
      "proven_at": "2026-06-14T12:10:00Z"
    }
  ]
}
```

## Komutlar

```bash
python3 scripts/factory/record-proof.py --feature F002 --type commit --value $(git rev-parse --short HEAD)
python3 scripts/factory/record-proof.py --feature F002 --type analytics --value phrase_completed
python3 scripts/factory/record-proof.py --status   # özet tablo
```

**Sahip:** CDID (WP kapanışı) · **L1:** CEC
