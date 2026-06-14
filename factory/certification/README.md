# Factory Certification — CERTIFIED_BY_FACTORY

**factory-health 100 ≠ kullanıcıya güven.**  
Her uygulama release öncesi fabrika sertifikası üretir.

## Seviyeler

| Level | Koşul |
|-------|--------|
| **GOLD** | quality_gate 100 + audit ≥ 95 + regression scan clean |
| **SILVER** | quality_gate 100 + audit ≥ 90 |
| **BRONZE** | quality_gate pass + audit ≥ 80 |
| **NONE** | Fail |

## Çıktı (`runtime/factory/certification/{slug}.json`)

```json
{
  "certified_by_factory": true,
  "factory_version": "4.0.0-productization",
  "app": "My App",
  "slug": "my-app",
  "certification_level": "GOLD",
  "audit_score": 97,
  "quality_gate": 100,
  "release_ready": true
}
```

## Komut

```bash
python3 scripts/factory/certify-app.py --slug my-app --name "My App"
```

Portföy özeti: `runtime/factory/certification/index.json`
