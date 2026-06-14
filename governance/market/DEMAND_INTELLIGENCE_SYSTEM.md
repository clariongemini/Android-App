# Kullanıcı Talep Zekâsı (Demand Intelligence)

**Amaç:** Rakipleri kopyalamak değil — **insanların gerçek problemlerini** keşfetmek.  
**Sahip:** Pazarlama ve Büyüme (Growth Hacker)  
**Kullanıcı dili / içerik / JTBD derinliği:** [LIUD](../linguistic/DEPARTMENT_CHARTER.md) (Linguistic Intelligence & User Demand)  
**Birleşik çıktı:** `governance/market/demand_output/DEMAND_INTELLIGENCE_REPORT.md`

---

## Temel sorular (Growth ajanı her raporda yanıtlar)

| # | Soru |
|---|------|
| 1 | İnsanlar gerçekten **ne istiyor**? |
| 2 | İnsanlar **neye para ödüyor**? |
| 3 | İnsanlar **neden abonelik iptal ediyor**? |
| 4 | İnsanlar **neden rakipleri bırakıyor**? |
| 5 | Hangi **problem** için uygulama arıyorlar? |
| 6 | Hangi **özellik** için ödeme yapmaya razı? |
| 7 | Hangi **özellik** için şikayet ediyorlar? |

Play Store yorumları **tek başına yeterli değil**. Aşağıdaki 10 katman birleştirilir.

---

## 10 araştırma katmanı

| # | Katman | Script / plan | Çıktı |
|---|--------|---------------|-------|
| 1 | **Play Store** | `play_store_analyzer.py` | `scraper_output/` |
| 2 | **App Store (iOS)** | `app_store_analyzer.py` | `demand_output/app_store/` |
| 3 | **YouTube talep** | `youtube_demand_analyzer.py` | `demand_output/youtube/` |
| 4 | **Google arama niyeti** | `search_intent_analyzer.py` | `demand_output/search_intent/` |
| 5 | **Forum / Reddit** | `forum_intelligence.py` | `forum_output/` |
| 6 | **Rakip trafik / SEO** | `competitor_traffic_analyzer.py` | `demand_output/traffic/` |
| 7 | **Viral döngü** | `viral_loop_analyzer.py` | `demand_output/viral_loops/` |
| 8 | **Shorts / Reels / TikTok** | `social_shorts_analyzer.py` | `demand_output/social_shorts/` |
| 9 | **ASO kelime haritası** | `aso_keyword_map.py` | `demand_output/aso_keyword_map/` |
| 10 | **Monetizasyon** | `monetization_research.py` | `demand_output/monetization/` |

**Katalog:** `demand_intelligence_catalog.json` — sorgular, rakipler, locale'ler.

---

## Yıl 1 vs Yıl 2+ strateji ayrımı

### Yıl 1 — B2B/B2B2C **YOK**

Pre-launch gerçeği: marka yok, sosyal kanıt yok, terapist erken ortaklığı düşük dönüşüm.

**Yıl 1 kanallar (finansal modelde varsayılır):**

| Kanal | Hedef pay |
|-------|-----------|
| ASO (6 locale Play + App Store ASO) | **%30** |
| SEO + blog + backlink | **%25** |
| Organik sosyal (YouTube, Reels, TikTok, LinkedIn) | **%20** |
| Topluluk / forum / Reddit | **%15** |
| Viral döngü + kullanıcı tavsiyesi | **%10** |

**Yasak:** Yıl 1 finansal projeksiyonda klinik/DKT/SLP trafik varsayımı.

### Yıl 2+ — B2B/B2B2C yeniden değerlendirme

**Eşik (tümü sağlanmalı):** `B2B_GATE_CRITERIA.md`

| Eşik | Değer |
|------|-------|
| İndirme | **≥10.000** |
| Ücretli kullanıcı | **≥500** |
| Mağaza puanı | **≥4,5★** |
| Başarı hikâyeleri | ≥5 doğrulanmış |
| Retention | D30 ≥25% kanıtı |

Eşik sonrası B2B kanal Yıl 2/3 modellerine eklenir.

---

## Çalıştırma (tam döngü)

```bash
source .venv-scraper/bin/activate
pip install -r scripts/scrapers/requirements.txt

# Tek tek
python scripts/scrapers/play_store_analyzer.py --locale tr,en,de,fr,it,es
python scripts/scrapers/app_store_analyzer.py --dry-run   # veya --locale us,tr
python scripts/scrapers/youtube_demand_analyzer.py --dry-run
python scripts/scrapers/search_intent_analyzer.py
python scripts/scrapers/forum_intelligence.py --dry-run
python scripts/scrapers/competitor_traffic_analyzer.py --dry-run
python scripts/scrapers/viral_loop_analyzer.py
python scripts/scrapers/social_shorts_analyzer.py --dry-run
python scripts/scrapers/aso_keyword_map.py
python scripts/scrapers/monetization_research.py
python scripts/scrapers/analyze_user_intent.py

# Birleşik rapor
python scripts/scrapers/generate_demand_report.py
```

---

## Finans modelleri

| Dönem | Belge | B2B |
|-------|-------|-----|
| Yıl 1 | `YEAR1_ORGANIC_FINANCIAL_MODEL.md` | ❌ |
| Yıl 2 | `YEAR2_ORGANIC_FINANCIAL_MODEL.md` | Eşik sonrası |
| Yıl 3 | `YEAR3_ORGANIC_FINANCIAL_MODEL.md` | Olgunlaşmış |

Senaryolar: **P10 · P50 · P75 · P90**

---

## Veri durumu (şeffaflık)

| Katman | Durum |
|--------|-------|
| Play Store | ✅ Scraper çalıştırıldı (2026-06-12) |
| App Store | ⏳ Script hazır — ilk çekim bekliyor |
| YouTube | ⏳ Script iskelet — API key veya manuel batch |
| Google arama | ⏳ Trends + manuel hacim tahmini |
| Forum | ⏳ Plan + iskelet |
| Trafik / backlink | ⏳ Manuel + ücretsiz araç snapshot |
| Viral döngü | ⏳ Play/App açıklama + in-app analiz |
| Shorts/Reels | ⏳ Manuel örnekleme şablonu |
| ASO harita | ⏳ Play listing metinlerinden |
| Monetizasyon | ⏳ Play/App fiyat sinyali |

Growth ajanı **«tamamlandı»** demeden her katmanın durumunu raporlar.

**Revizyon:** Ayda 1 tam döngü; çeyrek sonu CPO briefing.
