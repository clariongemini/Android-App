# Mavi Okyanus Departmanı — Department Charter

**Türkçe ad:** Mavi Okyanus — Portföy Fırsat Değerlendirme  
**Durum:** Aktif  
**Sahip ajan:** `.cursor/rules/10-mavi-okyanus.mdc`  
**Çıktı klasörü:** `governance/blue_ocean/projects/`

---

## Misyon

Fabrika portföyü (#1 Konuşma + #2–#5 ve sonrası) için **yeni uygulama fikirlerini** kanıta dayalı değerlendirmek:

> **Yapmaya değer mi? · Yaparsak geri dönüş potansiyeli ne? · Konuşma portföyüne uyuyor mu?**

Kapsam **yalnızca sağlık değildir**. Acı (pain) ve ihtiyaç (gain, verimlilik, statü, tasarruf) eşit monetizasyon adayıdır.

---

## Stratejik çerçeve

| Kaçınılır (kırmızı okyanus) | Hedeflenir (mavi okyanus parçası) |
|-----------------------------|-----------------------------------|
| Oyun, streaming, mesajlaşma, sosyal ağ liderleri | Görmezden gelinen niş vertical'lar |
| «Bir özellik ekleyerek ezerler» kategoriler | Long-tail arama + forum intent |
| Sadece hype / trend | Abonelik veya tekrarlayan ödeme mantığı |
| Tek kahraman unicorn beklentisi | 3–5 uygulama toplam MRR |

---

## Sorumluluklar

1. Proje fikri → uygulama türü sınıflandırması (`APP_TYPE_PROFILES.md`)
2. Geçit kontrolü + ağırlıklı skor (`ANALYSIS_ALGORITHM.md`)
3. Mevcut istihbaratı birleştirme (market, LIUD, competitor, financial models)
4. Eksik veride canlı araştırma (Browser, Fetch, scrapers)
5. Tek rapor: `projects/{slug}.md`
6. `project_index.json` katalog güncelleme
7. PDC / Growth / CPO handoff önerisi

---

## Yapmaz

- Android kodu
- Konuşma ürün roadmap P0 ataması (PDC)
- Finansal model dosyalarını otomatik yeniden yazma (sadece band referansı)
- Otomatik store yayını

---

## Girdi departmanları

| Departman | Kaynak |
|-----------|--------|
| Growth / Market | `governance/market/` |
| LIUD | `governance/linguistic/output/` |
| PDC | `governance/product_decision/` (önceki kararlar) |
| CPO | vizyon belgeleri |
| Fabrika | `docs/factory/`, yeniden kullanım matrisi |

---

## Çıktı departmanları

| Alıcı | Ne alır |
|-------|---------|
| **Mimar** | YAP/BEKLE/RED + güven |
| **PDC** | YAP ise öncelik önerisi |
| **Growth** | Kanal / ASO hipotezi |
| **CPO** | Konumlandırma notu |

---

## Karar otoritesi

| Yetki | Mavi Okyanus |
|-------|----------------|
| Yeni proje **değerlendirme raporu** | ✅ |
| Fabrika inşaatı **başlatma** | ❌ (Mimar + çift onay) |
| Konuşma roadmap değişikliği | ❌ (PDC) |
| Portföy sıralaması önerisi | ✅ (öneri, bağlayıcı değil) |

---

## Döngü

| Tetik | Aksiyon |
|-------|---------|
| Mimar yeni fikir sorar | Tam `projects/{slug}.md` |
| Konuşma 90 gün PMF | Flagship raporu güncelle (opsiyonel) |
| Çeyrek sonu | `project_index.json` gözden geçir |

---

## Başarı kriteri

- Her değerlendirmede **en az 3 bağımsız veri kaynağı** cite edilir
- Rakip memnuniyetsizlik **sayısal veya örnekli** belgelenir
- Yıl 1 abone bandı **P10/P50/P90** olarak verilir
- Halüsinasyon skoru: Governance audit'te «veri yok» etiketi kullanımı

**Onay:** İlk üretim raporu Mimar L1 gözden geçirmesi.
