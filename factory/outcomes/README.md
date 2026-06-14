# Factory Outcomes — Portfolio → Outcome

**Zincir:** Factory → Governance → Intelligence → Portfolio → **Outcome**

Portfolio kayıt sayar. Outcome **ürün performansını** ölçer.

## Ne ölçülür?

| Portfolio (kayıt) | Outcome (sonuç) |
|-------------------|-----------------|
| Kaç app üretildi | Kullanıcı sayısı |
| Kaç app release | Retention (D7, D30) |
| Sertifikasyon | MRR / gelir |
| Portföyde mi | Geliştirme maliyeti / gün |
| | **ROI** |

Outcome verisi Play Store / AID / Revenue / Benchmark katmanlarından beslenir — fabrika şablonunda **örnek uygulama adı yok**.

## Runtime (`runtime/factory/outcomes/`)

| Dosya | İçerik |
|-------|--------|
| `app_outcomes.json` | App slug başına kullanıcı, retention, gelir, ROI |
| `portfolio_outcomes.json` | Portföy rollup + outcome validation durumu |
| `roi_history.json` | Zaman serisi ROI snapshot'ları |

## Komutlar

```bash
# Tek app outcome güncelle (AID veya Play Console verisi)
python3 scripts/factory/record-outcome.py \
  --slug my-app \
  --users 1240 \
  --retention-d30 28.4 \
  --mrr 940 \
  --development-days 34 \
  --source manual

# Portföy rollup + roi_history
python3 scripts/factory/build-portfolio-outcomes.py

# KPI + outcomes birlikte
python3 scripts/factory/build-factory-kpi.py
```

## Outcome validation

| Durum | Anlam |
|-------|--------|
| `AWAITING_DATA` | App kayıtlı, outcome yok |
| `PARTIAL` | Bazı metrikler dolu |
| `ACTIVE` | En az 1 app'te users + retention veya gelir |
| `PROVEN` | Release + gelir + ROI kanıtı |

**Not:** Outcome validation Play Store'da çözülür — repo yalnızca veriyi taşır.

Detay: [`docs/FACTORY_V4_PRODUCTIZATION.md`](../../docs/FACTORY_V4_PRODUCTIZATION.md)
