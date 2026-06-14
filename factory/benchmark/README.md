# Benchmark Engine — Üç Katman

**Soru:** İyi mi, yoksa rakibe göre iyi mi?

Tek skor yetmez. Üç ayrı kıyas:

| Katman | Ne ölçer? | Örnek |
|--------|-----------|--------|
| **Factory** | Fabrika kalitesi vs referans | `factory_score: 92`, `percentile: 97` |
| **Product** | Ürün metrikleri vs kategori | `retention_d7: 41`, `category_avg: 28` |
| **Market** | Pazar / rakip konumu | `play_store_rating: 4.6`, `competitor_avg: 4.2` |

## Runtime dosyalar

- `factory/runtime/benchmark/factory.json`
- `factory/runtime/benchmark/product.json`
- `factory/runtime/benchmark/market.json`
- `factory/runtime/benchmark/summary.json` — birleşik özet

```bash
python3 scripts/factory/build-benchmark.py
```

**Sahip:** Growth + EGC · Kaynak: `factory-health.sh`, AID, `PLAY_STORE_BENCHMARKS.json`
