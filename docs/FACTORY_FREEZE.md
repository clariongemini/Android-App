# Factory Freeze — Build Less, Ship More

**North star:** [`FACTORY_MISSION.md`](../FACTORY_MISSION.md)

Fabrika geliştirmesi **3 uygulama production release** olana kadar donduruldu.

## Kural (`.factory/freeze.json`)

```json
{
  "until_apps_released": 3,
  "required_apps": [],
  "frozen": {
    "new_agents": true,
    "new_councils": true,
    "new_layers": true,
    "new_intelligence_motors": true
  }
}
```

App slug'ları fabrika şablonunda tanımlı değildir — yalnızca hedef projede `runtime/factory/portfolio/apps.json` içinde.

## Evrim

| Sürüm | Anlam |
|-------|--------|
| V1 | Android Template |
| V2 | Android Factory |
| V3 | Android Factory OS |
| V4 | Android Product Portfolio OS |

## 96 → 99 GitHub'da değil

| Gerekli | Nerede |
|---------|--------|
| Production release + kullanıcı + gelir | Play Store |
| Outcome validation | `runtime/factory/outcomes/` |

## V4 izin verilen yüzeyler (scaffold only)

1. **Portfolio** — register + release + KPI  
2. **Outcomes** — users, retention, MRR, ROI  
3. **Certification** — `certify-app.py`  
4. **Regression DB** — `scan-regression.py`  
5. **ROI Dashboard** — `build-factory-kpi.py`

Yeni ajan · yeni council · yeni katman → **YASAK** (`python3 scripts/factory/check-freeze.py`)

Detay: [`FACTORY_V4_PRODUCTIZATION.md`](FACTORY_V4_PRODUCTIZATION.md)
