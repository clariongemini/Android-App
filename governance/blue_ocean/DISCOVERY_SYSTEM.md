# Mavi Okyanus Keşif Radarı (Discovery System)

**Versiyon:** 1.0  
**Sahip:** Mavi Okyanus ajanı · Orkestrasyon: `scripts/blue_ocean/run_blue_ocean_discovery.sh`  
**Prensip:** Mevcut Growth / LIUD / PDC akışına **dokunmaz** — yalnızca **okur** ve ayrı klasöre **yazar**.

---

## Amaç

Mimar fikir söylemeden, Play Store (ve ileride App Store) + mevcut istihbarattan **potansiyel mavi okyanus adaylarını** listelemek.

> «Hayal gücünün yetmediği nişler» veriyle yüzeye çıkar; **inşaat kararı** yine `projects/{slug}.md` + Mimar onayı.

---

## Mimari (katmanlı — çakışma yok)

```
┌─────────────────────────────────────────────────────────┐
│  Growth (DEĞİŞMEZ)                                       │
│  run_demand_intelligence.sh → governance/market/       │
│  Active product rakipleri, VOC, finans modelleri        │
└───────────────────────────┬─────────────────────────────┘
                            │ READ ONLY
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Discovery Radar (YENİ)                                  │
│  run_blue_ocean_discovery.sh                             │
│    → play_store_discovery_scan.py                        │
│    → ingest_market_snapshots.py (opsiyonel)              │
│    → generate_discovery_report.py                        │
└───────────────────────────┬─────────────────────────────┘
                            │ WRITE
                            ▼
┌─────────────────────────────────────────────────────────┐
│  governance/blue_ocean/discovery/                        │
│    raw/ · candidates.json · WEEKLY_CANDIDATES.md         │
└───────────────────────────┬─────────────────────────────┘
                            │ TOP N
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Mavi Okyanus Eval (MEVCUT)                              │
│  projects/{slug}.md — YAP/BEKLE/RED                      │
└─────────────────────────────────────────────────────────┘
```

**Hiçbir dosya değiştirilmez:**
- `competitor_catalog.json`
- `demand_intelligence_catalog.json`
- `run_demand_intelligence.sh`
- PDC / LIUD / Growth ajan kuralları

---

## Modlar

| Mod | `--mode` | Ne tarar | Ne sıklık |
|-----|----------|----------|-----------|
| **Portföy** | `portfolio` (varsayılan) | `category_seed_catalog.json` — fabrika uyumlu vertical'lar | Haftalık |
| **Geniş** | `broad` | Tüm seed + ek niş kategoriler (yat, dalgıç, hobby…) | Aylık |

Portföy modu #2–#5 adayları; geniş mod «farkında olmadığın» nişleri gösterir — çoğu **fabrika filtresi** ile elenir.

---

## Fırsat sinyalleri (opportunity_scorer)

| Sinyal | Ağırlık | Anlam |
|--------|---------|--------|
| IAP / abonelik kanıtı | yüksek | Para ödeniyor |
| Install orta (10K–1M) | orta | TAM var, dev değil |
| ★ ≤ 3,8 | yüksek | Memnuniyetsizlik boşluğu |
| Fiyat şikâyeti + engagement | yüksek | «Pahalı ama kullanıyorum» |
| Teknik / içerik şikâyeti | orta | Yeniden yapım fırsatı |
| Kırmızı okyanus blocklist | veto | Oyun, mesaj, streaming… |
| Fabrika uyumu (seed tag) | filtre | high / medium / low |

Skor 0–100 → `discovery/candidates.json`

---

## Çıktılar

| Dosya | İçerik |
|-------|--------|
| `discovery/raw/{vertical}_{locale}.json` | Ham tarama |
| `discovery/candidates.json` | Sıralı aday listesi |
| `discovery/WEEKLY_CANDIDATES.md` | İnsan okumalı özet (top 20) |
| `discovery/manifest.json` | Son koşu meta |

---

## App Store (Faz 2)

`app_store_discovery_scan.py` — **planlı**. Faz 1 Play Store + mevcut `demand_output/app_store/` ingest yeterli.

---

## Mimar iş akışı

1. `run_blue_ocean_discovery.sh` (haftalık cron veya manuel)
2. `WEEKLY_CANDIDATES.md` oku (10 dk)
3. İlginç aday → `@mavi-okyanus [ad] değerlendir` → `projects/{slug}.md`
4. YAP + onay → PDC sırası

---

## Tamamlanma hedefi (%40 → ~%95)

| Bileşen | Durum |
|---------|--------|
| Play tarama (seed catalog) | ✅ Faz 1 |
| Opportunity scorer | ✅ |
| Haftalık rapor | ✅ |
| Growth verisi ingest (read-only) | ✅ |
| App Store geniş tarama | ⏳ Faz 2 |
| Review blog / Product Hunt | ⏳ Faz 2 (Browser MCP / Fetch) |
| Otomatik `projects/*.md` (top 3) | ⏳ Faz 3 — Mimar tetiklemeli |

**%100 otomasyon yok** — son karar insan; halüsinasyon ve fabrika uyumsuz niş riski.

---

## Çalıştırma

```bash
./scripts/blue_ocean/run_blue_ocean_discovery.sh
./scripts/blue_ocean/run_blue_ocean_discovery.sh --mode broad --dry-run
./scripts/blue_ocean/run_blue_ocean_discovery.sh --locale en,tr --max-apps 5
```

**Bağımlılık:** `.venv-scraper` + `scripts/scrapers/requirements.txt` (Growth ile aynı venv — paylaşımlı, çakışmasız).

---

## Revizyon

Discovery algoritması değişikliği: `category_seed_catalog.json` `version` bump + Mimar onayı.
