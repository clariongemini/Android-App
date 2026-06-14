# Telemetry — Cycle Meta

CEO / AID / EGC / Intelligence cycle çalıştırma kayıtları.  
Büyük raporlar burada; charter ve şablonlar git'te kalır.

Runtime: `factory/runtime/telemetry/cycle_log.json`

```json
{
  "entries": [
    {
      "cycle": "intelligence",
      "script": "run-intelligence-cycle.sh",
      "started_at": "2026-06-14T12:00:00Z",
      "exit_code": 0,
      "motors_updated": ["proof", "memory", "decision_accuracy", "revenue", "benchmark"]
    }
  ]
}
```

**Not:** `governance/**/*.json` raporları runtime politika gereği projede üretilir; fabrika template reposunda `factory/runtime/` altında toplanır.
