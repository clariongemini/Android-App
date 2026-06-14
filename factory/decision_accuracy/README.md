# Decision Accuracy Engine

**Soru:** PDC doğru karar verdi mi?

Governance karar **kaydeder**; bu motor karar **kalitesini ölçer**.

## Şema

Runtime: `factory/runtime/decision_accuracy/registry.json`

```json
{
  "version": "1.0",
  "decisions": [
    {
      "decision_id": "DEC-2026-001",
      "feature": "F002",
      "title": "F002 Priority — phrase loop P0",
      "decided_at": "2026-06-01",
      "review_due": "2026-09-01",
      "expected": { "retention_delta_pct": 8, "trial_conversion_delta_pct": 2 },
      "actual": { "retention_delta_pct": 3, "trial_conversion_delta_pct": 1.2 },
      "accuracy_score": 0.73,
      "status": "reviewed"
    }
  ],
  "pdc_accuracy_pct": 73
}
```

## Komutlar

```bash
python3 scripts/factory/record-decision.py --feature F002 --expected-retention 8
python3 scripts/factory/record-decision.py --feature F002 --actual-retention 3 --review
python3 scripts/factory/compute-decision-accuracy.py
```

**Sahip:** PDC · **Tüketen:** EGC (`PDC_DECISION_QUALITY.json` ile hizalı)
