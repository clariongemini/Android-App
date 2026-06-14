# V4 — Factory Productization (Not More Intelligence)

**Sürüm:** `4.0.0-productization` (plan) · **Önceki:** v3.1 intelligence-operational  
**Durum:** Intelligence **FROZEN** · Portfolio registry scaffold · **Real app validation next**

---

## Teşhis

V3/V3.1 doğru yönde ama risk şu:

> Repo, ürettiği Android uygulamalarından daha büyük bir meta-sistem haline gelebilir.

**Çözüm:** Yeni katman yazmak değil — fabrikanın **ürettiği uygulamalardan** öğrenmek.

---

## Üç katman — final durum

| Katman | Durum | Aksiyon |
|--------|-------|---------|
| **Android Factory** (scaffold, standards, CI) | Güçlü — koru | F3+ devam |
| **Governance** (CEO…EGC, 16 ajan) | Yeterli — koru | AGENTS freeze |
| **Intelligence** (proof, memory, …) | Tamam — **dondur** | Yeni engine yok |

### Intelligence freeze (V4)

Eklenmez:

- Risk / Forecast / Strategy / Knowledge / Reflection / Learning Engine
- V3.2, V3.3…
- Yeni ajan, yeni council

Mevcut 5 motor yalnızca **gerçek app verisi** ile dolar — kod eklenmez.

---

## V4 tek ekleme: Factory Portfolio Registry

```
factory/portfolio/          ← canonical (git)
runtime/factory/portfolio/  ← canlı veri (gitignore)
  ├── apps.json
  ├── portfolio_scorecard.json
  ├── release_history.json
  ├── revenue_summary.json
  └── factory_kpi.json
```

### Factory Success Health (asıl KPI)

Factory Health = repo iç sağlığı.  
**Factory Success Health** = fabrikanın dışarıda ürettiği sonuç:

```json
{
  "apps_created": 12,
  "apps_released": 8,
  "apps_profitable": 3,
  "avg_time_to_first_apk_days": 2.8,
  "avg_time_to_release_days": 19,
  "avg_playstore_rating": 4.4,
  "portfolio_mrr": 8400
}
```

---

## Komutlar

```bash
python3 scripts/factory/register-app.py --name "My App" --package com.example.myapp --slug my-app
python3 scripts/factory/record-release.py --slug my-app --version 1.0.0 --track production
python3 scripts/factory/record-outcome.py --slug my-app --users 100 --retention-d30 25.0 --mrr 500
python3 scripts/factory/build-portfolio-outcomes.py
python3 scripts/factory/build-factory-kpi.py
```

---

## V4.1 — Outcomes (Portfolio → Outcome)

```
factory/outcomes/           ← canonical (git)
runtime/factory/outcomes/   ← canlı veri (gitignore)
  ├── app_outcomes.json
  ├── portfolio_outcomes.json
  └── roi_history.json
```

Örnek app outcome:

```json
{
  "slug": "my-app",
  "released": true,
  "users": 1240,
  "retention_d30": 28.4,
  "mrr": 940,
  "development_days": 34,
  "roi": 2.7
}
```

Outcome validation durumları: `AWAITING_DATA` → `PARTIAL` → `ACTIVE` → `PROVEN`

---

## 30–60 gün doğrulama

| Hedef | Kanıt |
|-------|--------|
| 3 production release | `runtime/factory/portfolio/apps.json` |
| Outcome validation ACTIVE | users + retention veya gelir |
| Outcome validation PROVEN | release + gelir + ROI |

**Kural:** Gerçek Play Store verisi olmadan V4.2+ meta-genişleme yok.

---

## 95 → 96+ için gerekenler

| Gerekli | Yeni sistem? |
|---------|--------------|
| Factory Portfolio Registry | ✅ (scaffold) |
| Factory Outcomes | ✅ (scaffold) |
| Factory KPI dashboard (`factory_kpi.json`) | ✅ |
| Gerçek app verisi (30–60 gün) | ❌ kod değil — kullanım |

---

## Mimari özeti

```
Executive  → karar verir     (governance/)
Factory    → öğrenir         (runtime/factory/ — frozen motors)
Portfolio  → kaydeder        (runtime/factory/portfolio/)
Outcomes   → kanıtlar        (runtime/factory/outcomes/)
Android    → üretir          (templates/android/)
```

**Fabrika para kazanmaz. Uygulamalar kazanır. Fabrika başarıyı portföyde ölçer.**

---

## Evrim

| Sürüm | Anlam |
|-------|--------|
| V1 | Android Template |
| V2 | Android Factory |
| V3 | Android Factory OS |
| V4 | Android Product Portfolio OS |

---

## FREEZE — Build Less, Ship More

`.factory/freeze.json` — **3 app release** olana kadar yeni ajan/katman/motor yok.

Detay: [`FACTORY_FREEZE.md`](FACTORY_FREEZE.md)

---

## V4 sonrası yüzeyler (scaffold — veri app'lerden gelir)

### 1. Outcomes

```bash
python3 scripts/factory/record-outcome.py --slug my-app --users 100 --mrr 200
python3 scripts/factory/build-portfolio-outcomes.py
```

### 2. Factory Certification

```bash
python3 scripts/factory/certify-app.py --slug my-app --name "My App"
```

### 3. Factory Regression DB

```bash
python3 scripts/factory/scan-regression.py   # quality gate hook
```

### 4. Factory ROI Dashboard

```bash
python3 scripts/factory/build-factory-kpi.py   # → roi_dashboard.json
```

---

## 96 → 99

GitHub'da değil. Play Store'da: yayın, kullanıcı, retention, gelir, ROI.
