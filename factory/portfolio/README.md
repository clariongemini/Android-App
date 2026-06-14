# Factory Portfolio Registry (V4 Productization)

**Fabrika kendi başarısını kanıtlar — meta-sistem değil, üretilen uygulamalar.**

Intelligence Layer (proof, memory, benchmark…) **donduruldu**. V4 yüzeyleri: **portföy + outcomes**.

## Ne ölçülür?

| Eski (iç sağlık) | Yeni (dış başarı) |
|------------------|-------------------|
| Factory Health 100/100 | **Factory Success Health** |
| Company Health | apps_released, apps_profitable |
| Delivery Health | avg_time_to_first_apk_days |
| Reality Health (tek app) | **Tüm portföy** tek registry |

## Runtime dosyalar (`runtime/factory/portfolio/`)

| Dosya | İçerik |
|-------|--------|
| `apps.json` | Kayıtlı uygulamalar (slug + package — proje bazlı) |
| `portfolio_scorecard.json` | Portföy özeti + Factory Success Health |
| `release_history.json` | App başına release kanıtları |
| `revenue_summary.json` | App başına MRR/ARR rollup |
| `factory_kpi.json` | CEO dashboard — tek sayfa KPI |

Outcome metrikleri: [`../outcomes/README.md`](../outcomes/README.md)

## Komutlar

```bash
python3 scripts/factory/register-app.py --name "My App" --package com.example.myapp --slug my-app
python3 scripts/factory/record-outcome.py --slug my-app --users 100 --retention-d30 25.0 --mrr 500
python3 scripts/factory/build-portfolio-outcomes.py
python3 scripts/factory/build-factory-kpi.py
```

## V4 doğrulama (30–60 gün)

Gerçek veri olmadan yeni katman eklenmez. Hedef: **3 production release** + outcome validation.

Detay: [`docs/FACTORY_V4_PRODUCTIZATION.md`](../docs/FACTORY_V4_PRODUCTIZATION.md)

## Dondurulmuş (eklenmez)

Risk Engine · Forecast Engine · Strategy Engine · yeni ajan · yeni council
