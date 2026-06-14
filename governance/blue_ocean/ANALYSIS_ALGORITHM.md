# Mavi Okyanus — Derin Analiz Algoritması

**Versiyon:** 1.0  
**Sahip:** Mavi Okyanus ajanı (`10-mavi-okyanus.mdc`)

Bu belge, proje değerlendirme raporlarının (`projects/{slug}.md`) **zorunlu hesaplama ve karar mantığını** tanımlar.

---

## 1. Karar akışı

```
Proje kartı
    → Uygulama türü seç (APP_TYPE_PROFILES.md)
    → Geçitler G1–G10 (FAIL = RED, skor yok)
    → Veri toplama (yerel → canlı)
    → Ağırlıklı skor (türe özel)
    → Finansal band (Yıl 1 organik)
    → YAP / BEKLE / RED
    → projects/{slug}.md + project_index.json
```

---

## 2. Geçit kontrol listesi (G1–G10)

Tek **FAIL** → karar **RED** (skor bilgilendirme amaçlı yazılabilir).

| ID | Geçit | PASS |
|----|--------|------|
| G1 | Kırmızı okyanus değil | Global platform lideri 12 ayda özellik paritesiyle ezebilir kategoride değil |
| G2 | Talep kanıtı var | Arama, forum, mağaza yorumu veya epidemiyoloji/benzeri **en az bir** kanıt |
| G3 | Monetizasyon mantığı | Tek seferlik değil veya tek sefer fiyatı fabrika emeğini karşılar |
| G4 | Mağaza / politika | Play (ve hedef iOS) politikasına uygun konumlanabilir |
| G5 | Fabrika uyumu | Mevcut fabrika modüllerinin ≥%50 yeniden kullanımı mümkün |
| G6 | Dağıtım gerçekçiliği | Solo + AI fabrika ile Yıl 1'de 50+ hedef kullanıcı/abone hipotezi savunulabilir |
| G7 | Etik / güven | Yanıltıcı tıbbi/finansal iddia veya çocuk verisi riski yönetilebilir |
| G8 | Portföy korelasyonu | Portfolio rank #1 app ile öbek/rakip/GTM örtüşmesi **%40 altı** (üstü → BEKLE notu, FAIL değil) |
| G9 | Halüsinasyon güvenliği | Kritik iddiaların ≥%70'i cite edilebilir kaynakta |
| G10 | Mimar onayı kartı | Tek cümle değer önerisi net yazıldı |

**G8 yüksek korelasyon:** Geçit PASS ama skordan **−15 puan** portföy cezası.

---

## 3. Skor boyutları (temel 1–5 → 100 ölçeğe)

Her boyut 1–5 puanlanır; **uygulama türü** ağırlıkları `APP_TYPE_PROFILES.md`'den gelir.

| Kod | Boyut | Açıklama |
|-----|--------|----------|
| D | Talep yoğunluğu | Pazar büyüklüğü, arama, acı/ihtiyaç sıklığı |
| C | Rekabet boşluğu | Rakip sayısı, ★ düşük, özellik boşluğu |
| M | Monetizasyon kanıtı | Rakip IAP, ödeme yorumları, fiyat ankrajı |
| L | Abonelik ömrü / LTV | Tekrar kullanım, churn beklentisi |
| F | Fabrika yeniden kullanım | Kod, i18n, billing, offline, content JSON |
| A | ASO / keşif | Long-tail, store arama netliği |
| S | Sosyal / forum intent | «Ne önerirsiniz?» thread yoğunluğu |
| P | Portföy çeşitliliği | Flagship app'ten farklı vertical |
| R | Rakip memnuniyetsizlik | Negatif VOC yoğunluğu, fırsat |
| G | Gelir geri dönüş potansiyeli | Yıl 1 P50 MRR bandı vs fabrika maliyeti |

**Formül:**

```
Raw = Σ (boyut_puanı × ağırlık)   // ağırlıklar toplamı = 1.0
Skor_100 = Raw × 20
Portföy cezası uygula (varsa)
Güven = min(100, cite_edilen_kaynak_sayısı × 8 + veri_tazeliği_bonus)
```

### Karar eşikleri

| Skor_100 | Karar | Anlam |
|----------|--------|--------|
| ≥ 75 | **YAP** | Portföy adayı — PDC sıraya al |
| 60–74 | **BEKLE** | PMF / veri eksik — 90 gün sonra yenile |
| < 60 | **RED** | Fabrika önceliği düşük |

Güven **< 50** ise karar bir kademe düşür (YAP→BEKLE, BEKLE→RED notu).

---

## 4. Rakip memnuniyetsizlik analizi (zorunlu)

Her raporda doldur:

| Metrik | Nasıl |
|--------|--------|
| Analiz edilen yorum sayısı | Play/App Store scrape veya mevcut `COMPETITOR_ANALYSIS` |
| Negatif tema sayısı | Fiyat, çökme, «işe yaramadı», «çocuksu», «duymuyor» vb. |
| Negatif oran | negatif / toplam (band) |
| En güçlü 3 memnuniyetsizlik | Alıntı veya parafraz + kaynak |
| Değerlendirilen fikir bunu çözer mi? | EVET / KISMEN / HAYIR |

**Fırsat skoru R:** negatif oran yüksek + lider ★ düşük → R yüksek.

---

## 5. Abone / gelir bandı (Yıl 1, organik, $0 ads)

Fabrika varsayımı: `YEAR1_ORGANIC_FINANCIAL_MODEL.md` metodolojisi.

```
Tahmini_yıllık_indirme_P50 = ASO_trafik + sosyal + forum (segment bazlı)
Dönüşüm_band = %0.5 – %3.5 install→paid (segment benchmark)
Aktif_ücretli_P50 = indirme × dönüşüm (ortası)
MRR_P50 = ücretli × aylık_fiyat (bölgesel blend)
```

**Zorunlu çıktı tablosu:**

| Senaryo | Yıl 1 indirme | Ücretli abone | MRR (USD) | MRR (TRY @ kur) |
|---------|---------------|---------------|-----------|-----------------|
| P10 (kötü) | | | | |
| P50 | | | | |
| P90 (iyi) | | | | |

Kur: rapor tarihinde belirtilen veya `YEAR1` modelindeki varsayım — **kaynak cite**.

**Geri dönüş potansiyeli cümlesi (zorunlu):**

> «Yıl 1 P50 ile fabrika geliştirme + dağıtım emeği **karşılanır / sınırda / karşılanmaz** — gerekçe: …»

---

## 6. Rakip ücretli kullanıcı tahmini

Play Store abone sayısı yayınlamaz. Band hesabı:

```
Ücretli_band = install_mid × conversion_mid
```

| Kaynak | conversion_mid |
|--------|----------------|
| `PLAY_STORE_BENCHMARKS.json` `conversion_note` | %0.5–3.5 |
| Segment subscription_mention_rate yüksek | üst band |
| Niş B2B / hobby | alt band |

Her rakip için: install aralığı, ★, tahmini ücretli bandı — tablo.

---

## 7. Veri kaynağı önceliği

1. `governance/market/` — mevcut scrape ve raporlar  
2. `docs/COMPETITOR_ANALYSIS.md`  
3. `governance/market/demand_output/monetization/`  
4. `governance/market/demand_output/app_store/`  
5. Browser MCP — yeni rakip paketleri  
6. `scripts/scrapers/run_demand_intelligence.sh` — proje özel çekim  
7. Web search — epidemiyoloji, endüstri raporu  

**Veri yok kuralı:** Tahmin üretme; «VERİ YOK — güven düşür» yaz.

---

## 8. İhtiyaç türleri (sadece acı değil)

Değerlendirmede en az birini etiketle:

| Tür | Örnek | Monetizasyon |
|-----|--------|--------------|
| **Acı** | Çocuk konuşmuyor | Acil ödeme |
| **Korku** | Zorbalık, iş kaybı | Premium |
| **Verimlilik** | Seans arası pratik | Abonelik |
| **Statü** | Hitabet, diksiyon | Abonelik |
| **Tasarruf** | Klinik yerine ev | Fiyat ankrajı |
| **Alışkanlık** | Günlük egzersiz | Retention |
| **Uyum** | Doktor/okul önerisi | Güven |

Türe göre D ve M ağırlıkları `APP_TYPE_PROFILES.md`'de değişir.

---

## 9. Rapor kalite kontrolü (ajan self-check)

Yayınlamadan önce:

- [ ] 10 geçit tablosu dolu  
- [ ] Uygulama türü seçildi ve ağırlıklar uygulandı  
- [ ] ≥3 rakip satırı  
- [ ] Memnuniyetsizlik analizi sayısal  
- [ ] P10/P50/P90 tablosu  
- [ ] YAP/BEKLE/RED + güven %  
- [ ] «Yapmaya değer mi?» tek paragraf cevap  
- [ ] Handoff (PDC/Growth)  
- [ ] Halüsinasyon: her rakamın yanında kaynak veya «tahmin bandı»

---

## 10. Revizyon

Algoritma değişikliği: Mimar onayı + `project_index.json` `algorithm_version` bump.
