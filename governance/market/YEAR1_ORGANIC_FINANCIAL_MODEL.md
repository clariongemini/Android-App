# Yıl 1 Organik Büyüme ve Finansal Model

**Proje:** Konuşma Gelişim Platformu (`com.konusma`)  
**Departman:** Pazarlama ve Büyüme (Growth Hacker)  
**Tarih:** 2026-06-12 (rev. — B2B Yıl1 çıkarıldı, Demand Intelligence)  
**Kısıt:** **Ücretli reklam yok** · **B2B/B2B2C Yıl 1 = $0 trafik**  
**B2B Yıl 2+:** `B2B_GATE_CRITERIA.md`  
**Demand Intelligence:** `DEMAND_INTELLIGENCE_SYSTEM.md`

---

## Yönetici özeti (revize — Play Store verisine bağlı)

> **Önceki tablo (4,2K / 11,5K / 24K indirme) spekülatifti.** Aşağıdaki senaryolar, TR niş rakiplerin kanıtlı ölçeğine (Logue 10K+, Adım Adım 50K+, Diksiyon 100K+) ve Speech Blubs’ın **5M+** global hacmine karşı **sıfır marka + organik** varsayımına dayanır.

| Senaryo | Yıl 1 indirme | Yıl sonu aktif abone* | Yıl sonu MRR (net) | Yıl 1 net gelir | Yıl 1 gider | **Yıl 1 net** |
|---------|---------------|------------------------|--------------------|-----------------|-------------|---------------|
| **Kötümser (P10)** | 400 | **25** | $113 | $180 | $1.500 | **−$1.320** |
| **Baz (P50)** | 2.200 | **70** | $315 | $1.400 | $1.750 | **−$350** |
| **İyi (P75)** | 4.500 | **150** | $675 | $4.200 | $1.900 | **+$2.300** |
| **Çok başarılı (P90)** | 7.000 | **200** | $900 | $6.500 | $2.100 | **+$4.400** |

\*B2B trafik **dahil değil**. Organik tüketici kanalları + düşük marka bilinirliği.  
**Başabaş:** P75 senaryoda ~Ay 10; P50 yıl sonu hafif zarar — gerçekçi pre-launch beklenti.

### Ücretli abone bandları (Growth ajanı zorunlu)

| Band | Yıl 1 aktif ücretli | Bu modeldeki hedef |
|------|---------------------|---------------------|
| Gerçekçi | 50–150 | P50 = **70** |
| İyi | 150–400 | P75 = **150** |
| Çok başarılı | 400+ | P90 = **200** |

> **620 abone yasak.** **B2B Yıl 1 yasak** — eşik: `B2B_GATE_CRITERIA.md`

### Rakip ölçek referansı (Play Store, 2026-06-12)

| Rakip | Install aralığı | EN ★ | Fiyat yorum sinyali |
|-------|-----------------|------|---------------------|
| Speech Blubs | **5.000.000+** | 4,47 | **%13** mention (yüksek şikâyet) |
| MITA | 1.000.000+ | 4,64 | %2,0 |
| Otsimo (özel eğitim) | 100.000+ | 3,17 | %9,0 |
| Stamurai | 100.000+ | 4,62 | %2,0 |
| TR Diksiyon Dersleri | 100.000+ | 4,01 | %0 (IAP yok) |
| TR Adım Adım Konuşuyorum | 50.000+ | — | düşük hacim yorum |
| TR Logue (kekemelik) | 10.000+ | 4,35 | %4,9 |
| **Konuşma** | **0 (pre-launch)** | — | — |

Detay: `docs/COMPETITOR_ANALYSIS.md`

---

## 1. Kısıtlar ve varsayımlar

### 1.1 Sabit kısıt: reklam bütçesi = 0

| Kanal | Durum |
|-------|--------|
| Google UAC / Apple Search Ads | ❌ Kullanılmayacak |
| Meta / TikTok Ads | ❌ |
| Ücretli influencer | ❌ |
| PR ajansı | ❌ |

### 1.2 Yıl 1 organik kanal dağılımı (B2B hariç)

| Kanal | Pay | Rol |
|-------|-----|-----|
| **ASO** (Play 6 locale + App Store) | **30%** | Mağaza keşfi |
| **SEO + blog + backlink** | **25%** | Long-tail, arama niyeti |
| **Organik sosyal** (YouTube, Reels, TikTok) | **20%** | İçerik + kanca |
| **Topluluk / forum / Reddit** | **15%** | Talep zekâsı + trafik |
| **Viral döngü + referral** | **10%** | In-app paylaşım |

| Kanal | Maliyet | Yıl 1 |
|-------|---------|-------|
| Klinik / DKT / SLP | — | **❌ Finans varsayımı yok** |
| Play + App Store ASO | $0 | ✅ |
| SEO landing + blog | ~$15/yıl domain | Q2+ |
| YouTube / Shorts içerik | $0 emek | Haftalık 1–2 içerik hedefi |
| Reddit / forum batch | $0 | `FORUM_INTELLIGENCE_PLAN.md` |
| PR fırsatları | $0 | Düşük olasılık, yüksek etki |

### 1.3 Fiyatlandırma (net gelir hesabı)

| Plan | Liste fiyatı | Play komisyonu (%15)* | **Net / abone / ay** |
|------|--------------|------------------------|----------------------|
| TR Aylık | ₺149 (~$4,20) | $0,63 | **$3,57** |
| TR Yıllık | ₺990 (~$28) → $2,33/ay | — | **$1,98/ay** |
| DE Aylık | €6,99 (~$7,60) | $1,14 | **$6,46** |
| EN Aylık | $7,99 | $1,20 | **$6,79** |
| Aile yıllık | $49,99/yıl → $4,17/ay | — | **$3,54/ay** |

\*Google Play ilk $1M gelirde %15 (Small Business Program varsayımı).

**Baz senaryo blended net ARPU:** **$4,50/abone/ay** (TR ağırlıklı erken, DE/EN + yıllık plan Q3+).

### 1.4 Dönüşüm hunisi (baz)

```
Mağaza gösterimi → Liste tıklama (CTR 12%) → İndirme (CR 28%) → D1 açılış (55%)
→ D7 aktif (32%) → Deneme başlat (18% of installs) → Deneme→Ücretli (22%) → Aylık churn (7%)
```

**Efektif install→ücretli (revize):** P10 **%1,0** · P50 **%2,0** · P90 **%2,5** — `PLAY_STORE_BENCHMARKS.json` endüstri bandı (%0,5–3,5) ile uyumlu; Speech Blubs yüksek fiyat şikâyeti nedeniyle üst banda çıkmak riskli.

### 1.5 Gider kalemleri (nakit)

| Kalem | Q1 | Q2 | Q3 | Q4 | Yıl 1 |
|-------|----|----|----|----|-------|
| Play Console (tek sefer)* | $0 | $0 | $0 | $0 | $0* |
| Domain + e-posta | $15 | $0 | $0 | $15 | $30 |
| Firebase / analitik (ücretsiz katman aşımı) | $0 | $25 | $50 | $75 | $150 |
| Hukuk şablon (genel) | $0 | $0 | $100 | $0 | $100 |
| Muhasebe / vergi danışmanlığı | $0 | $0 | $200 | $300 | $500 |
| Scraper / araçlar | $0 | $0 | $25 | $25 | $50 |
| Beklenmedik | $50 | $75 | $100 | $125 | $350 |
| **Çeyrek toplam** | **$65** | **$250** | **$375** | **$440** | **$1.230** |
| **+ tampon %20** | | | | | **+$620** |
| **Planlanan gider** | **$150** | **$450** | **$500** | **$750** | **~$1.850** |

\*$25 kayıt ücreti Gün 0 öncesi ödenmiş sayılır.

---

## 2. Gün 0 — İlk yükleme günü planı

**Tanım:** Play Store’da **production / open testing** ilk kullanıcıya açık an.

| Saat | Aksiyon | Sorumlu |
|------|---------|---------|
| T-7 gün | **6 locale** screenshot + ASO (`tr,en,de,fr,it,es`), `validate-store-listing.sh` yeşil | Growth + Android |
| T-3 gün | Demand Intelligence baseline (`run_demand_intelligence.sh`) | Growth |
| T-1 gün | Sprint P 10/10 tester D7 raporu ≥ hedef | CPO |
| **Gün 0 09:00** | Play Console Production — **6 locale** aynı anda | Mimar onay |
| Gün 0 | Organik LinkedIn / Instagram duyuru (1 post) | Growth |
| Gün 0 | Product Hunt (organik, ücretsiz) | Growth |
| Gün 0–7 | ASO indeksleme izleme (Play Console) | Growth |
| Gün 7 | İlk hafta retro: CTR, D1, crash | Tüm ajanlar |

**Gün 0 hedef (olasılık):**

| Metrik | P10 | P50 | P90 |
|--------|-----|-----|-----|
| İlk hafta indirme | 40 | 120 | 350 |
| İlk hafta ücretli | 0 | 3 | 12 |

---

## 3. Aylık ilerleme tablosu (P50 — B2B yok, abone hedefi **70**)

| Ay | Yeni indirme | Küm. indirme | Aktif abone | MRR net | Aylık gelir | Aylık gider | Aylık net |
|----|--------------|--------------|-------------|---------|-------------|-------------|-----------|
| 1 | 50 | 50 | 1 | $5 | $5 | $45 | −$40 |
| 2 | 80 | 130 | 3 | $14 | $12 | $45 | −$33 |
| 3 | 120 | 250 | 8 | $36 | $30 | $50 | −$20 |
| 4 | 180 | 430 | 14 | $63 | $55 | $100 | −$45 |
| 5 | 220 | 650 | 22 | $99 | $85 | $120 | −$35 |
| 6 | 250 | 900 | 30 | $135 | $120 | $130 | −$10 |
| 7 | 240 | 1.140 | 38 | $171 | $155 | $140 | +$15 |
| 8 | 260 | 1.400 | 48 | $216 | $200 | $150 | +$50 |
| 9 | 280 | 1.680 | 55 | $248 | $230 | $160 | +$70 |
| 10 | 260 | 1.940 | 62 | $279 | $260 | $180 | +$80 |
| 11 | 240 | 2.180 | 66 | $297 | $280 | $200 | +$80 |
| 12 | 220 | 2.200 | **70** | $315 | $295 | $250 | +$45 |

**Kümülatif yıl sonu (P50):** Gelir **~$1.400** − Gider **~$1.750** = **~−$350 net** (pre-launch gerçekçi).

> Eski tablo (620 abone, klinik %40, +$12.950) **geçersiz**.

---

## 4. Çeyrek bazlı analiz (organik-only)

### Q1 — Lansman + Demand Intelligence baseline

| Metrik | P10 | P50 | P90 |
|--------|-----|-----|-----|
| Çeyrek indirme | 100 | 250 | 600 |
| Çeyrek sonu abone | 3 | **8** | 25 |
| Q1 net gelir | $25 | $45 | $150 |

**Q1 kapı:** `run_demand_intelligence.sh` tamamlandı mı?

### Q2 — SEO + içerik

| Metrik | P10 | P50 | P90 |
|--------|-----|-----|-----|
| Çeyrek indirme | 200 | 650 | 1.400 |
| Çeyrek sonu abone | 10 | **25** | 70 |

### Q3 — Sosyal + retention

| Metrik | P10 | P50 | P90 |
|--------|-----|-----|-----|
| Çeyrek indirme | 350 | 780 | 1.800 |
| Çeyrek sonu abone | 18 | **45** | 120 |

### Q4 — Monetizasyon verimliliği

| Metrik | P10 | P50 | P90 |
|--------|-----|-----|-----|
| Çeyrek indirme | 400 | 520 | 1.400 |
| Çeyrek sonu abone | 25 | **70** | 200 |

---

## 5. Senaryo karşılaştırması (yıl sonu)

| | P10 | P50 | P75 | P90 |
|---|-----|-----|-----|-----|
| Toplam indirme | 400 | 2.200 | 4.500 | 7.000 |
| Aktif abone | **25** | **70** | **150** | **200** |
| Yıl 1 net gelir | $180 | $1.400 | $4.200 | $6.500 |
| Yıl 1 gider | $1.500 | $1.750 | $1.900 | $2.100 |
| **Yıl 1 net** | **−$1.320** | **−$350** | **+$2.300** | **+$4.400** |
| Başabaş | — | — | ~Ay 10 | ~Ay 8 |

---

## 6. Organik büyüme formülü (B2B yok)

```
Aylık yeni indirme = ASO + SEO + Sosyal + Topluluk + Viral + Spike_organik

ASO(t)        = 40 × (1 + 0,10×t) × locale_katsayı     # 6 locale
SEO(t)        = 15 × (1 + 0,15×t)                       # blog + long-tail
Sosyal(t)     = 10 × (1 + 0,08×t)                       # YT + Shorts
Topluluk(t)   = 8 × (1 + 0,05×t)                        # Reddit + forum
Viral(t)      = MAU × K × 0,06                            # K ≈ 0,08
Spike         = 0 | 100–400 (Product Hunt / PR)
```

---

## 7. KPI panosu (B2B satırı yok)

| KPI | Q1 | Q2 | Q3 | Q4 |
|-----|----|----|----|-----|
| Organik indirme / ay | 80+ | 200+ | 260+ | 240+ |
| Demand katman tamamlama | 6/10 | 8/10 | 10/10 | 10/10 |
| D7 retention | ≥26% | ≥28% | ≥30% | ≥32% |
| Store CTR | ≥8% | ≥9% | ≥10% | ≥10% |
| MRR net | $36 | $135 | $248 | $315 |

---

## 8. Risk kaydı

| # | Risk | Mitigasyon |
|---|------|------------|
| R1 | ASO 90 gün gecikme | SEO + YouTube paralel |
| R2 | Billing gecikmesi | WP-09 |
| R3 | Tek veri kaynağı (Play) | Demand Intelligence 10 katman |
| R4 | Erken B2B baskısı | **Yıl 1 yasak** — eşik bekle |

---

## 9. Aksiyon takvimi

| Hafta | Aksiyon |
|-------|---------|
| W1 | `run_demand_intelligence.sh` |
| W2 | 6 locale ASO revizyon |
| W3 | SEO landing + Reddit batch |
| W4 | Gün 0 (6 locale + App Store) |
| W8 | YouTube ilk video |
| W12 | Q1 Demand raporu |
| W24 | Search intent + ASO harita revizyon |
| W52 | Yıl 1 kapanış · B2B eşik değerlendirmesi |

---

## 10. Revizyon protokolü

| Tetikleyici | Aksiyon |
|-------------|---------|
| İndirme < P10 | Kötümser senaryo |
| D7 < 24% | CPO — onboarding |
| B2B eşik tamam | Yıl 2 model + CPO onay |
| Demand katman eksik | Rapor «tamamlandı» sayılmaz |

**Yıl 2–3:** `YEAR2_ORGANIC_FINANCIAL_MODEL.md` · `YEAR3_ORGANIC_FINANCIAL_MODEL.md`

**Yapılacaklar:** ASO, SEO, içerik, sosyal, topluluk, viral — **B2B Yıl 1 değil**.
