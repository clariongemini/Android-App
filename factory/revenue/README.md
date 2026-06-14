# Revenue Reality — Money Reality (AID)

**Soru:** Ürün gerçeği var — para gerçeği nerede?

Product Reality (`governance/reality/`) özellik teslimatını ölçer.  
Revenue Reality **ekonomik sonucu** ölçer — yeni ajan yok, AID üretir.

## Şema

Runtime: `factory/runtime/revenue/revenue_snapshot.json`

```json
{
  "generated_at": "2026-06-14T12:00:00Z",
  "source": "AID + Play Billing",
  "status": "PIPELINE_READY",
  "mrr": null,
  "arr": null,
  "arpu": null,
  "ltv": null,
  "trial_conversion_pct": null,
  "churn_pct": null,
  "paid_subscribers": null,
  "notes": "Populate after Play Console / Billing sync"
}
```

## Üretim

```bash
./scripts/analytics/run_aid_cycle.sh    # revenue_snapshot.json dahil
python3 scripts/factory/build-revenue-snapshot.py --manual-mrr 2400
```

**Sahip:** AID · **L1:** CAO → CEO
