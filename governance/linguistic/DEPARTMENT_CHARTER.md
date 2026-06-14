# Linguistic Intelligence & User Demand Department (LIUD)

**Türkçe ad:** Kullanıcı Dil Analizi ve Talep İstihbarat Departmanı  
**Durum:** Aktif — sürekli çalışır  
**Sahip ajan:** `.cursor/rules/07-linguistic-intelligence.mdc`

---

## Misyon

Kullanıcıların yaşadığı **gerçek problemleri**, kullandıkları **gerçek dili** ve bekledikleri **gerçek çözümleri** keşfetmek.

Bu departman yalnızca keyword araştırması yapmaz. Konuşma terapisi alanında **kullanıcı dili veri istihbarat sisteminin** merkezidir.

---

## Etki alanı

| Sistem | Etki türü |
|--------|-----------|
| Eğitim sistemleri | Fonem/cümle/senaryo önceliği |
| İçerik sistemleri | Kelime havuzu, tekrar oranı, modül derinliği |
| SEO | Long-tail, kullanıcı dili, JTBD landing |
| ASO | Store listing dili (uzman ≠ kullanıcı) |
| Yol haritası | Acil / yüksek / orta / düşük öncelik |
| Premium içerik | «Neye para ödüyor» sinyali |
| Yeni özellikler | İçerik/özellik/AI boşlukları |

---

## Kapsanan diller

| Kod | Dil | Not |
|-----|-----|-----|
| TR | Türkçe | Ebeveyn dili ağırlıklı |
| US | İngilizce (ABD) | Clinical + late talker karışımı |
| GB | İngilizce (BK) | Stammering, elocution |
| DE | Almanca | Sprachtherapie, Stottern |
| FR | Fransızca | Orthophonie, bégaiement |
| ES | İspanyolca | Logopedia, oratoria |
| IT | İtalyanca | Logopedia, dizione |

---

## 10 temel görev

### 1. Google Trends analizi

Mevcut keywordleri tekrarlama — **yeni keyword keşfi**.

Bul: Related Queries · Rising Queries · Breakout Queries · Seasonal Queries · Long-tail Queries

Her raporda çıkar: arama hacmi (RSV/bant) · büyüme oranı · mevsimsellik · yaş segmenti tahmini · kullanıcı niyeti

**Kaynak:** `governance/trends/` (`discover_and_fetch.py`, `trends_data.json`)

---

### 2. Kullanıcı dili analizi

Uzman dili ↔ kullanıcı dili eşlemesi.

| Uzman dili | Kullanıcı dili |
|------------|----------------|
| Artikülasyon Bozukluğu | R harfini söyleyemiyorum |
| Speech Delay | 3 yaşındaki çocuğum konuşmuyor |
| Public Speaking Anxiety | Topluluk önünde konuşurken donup kalıyorum |

Her konu için: uzman terimi · kullanıcı terimi · arama gücü · kullanım sıklığı

**Çıktı:** `output/expert_vs_user_language.json`, `output/intent_map.json`

---

### 3. JTBD analizi

Her aramanın arkasındaki amacı bul.

Kategoriler:
- Bilgi arıyor · Çözüm arıyor · Egzersiz arıyor · Terapist arıyor
- Kendini test etmek istiyor · Çocuğunu değerlendirmek istiyor
- Utanç duygusundan kurtulmak istiyor · Sunum becerisi geliştirmek istiyor
- İş görüşmesine hazırlanıyor

**Çıktı:** `output/jtbd.json`

---

### 4. Reddit / Quora / Forum / topluluk analizi

Bul: en sık sorulan sorular · en çok şikayet · gerçek cümleler · başarısız çözüm girişimleri · duygusal ifadeler

**Kaynak:** `governance/market/forum_output/`, `USER_INTENT_SIGNALS.md`, `VOC_JTBD_DEMAND_RESEARCH.md`

**Çıktı:** `output/*_questions.json`, `output/emotion_map.json`

---

### 5. App Store / Play Store analizi

Rakip uygulamaların **1★, 2★, 3★** yorumları ayrı analiz edilir.

Tespit: içerik yetersiz · egzersiz az · tekrar · çok kolay/zor · çocuk sıkılıyor · STT kötü · ses tanıma yanlış · AI yetersiz · içerik tekrarı

**Kaynak:** `governance/market/scraper_output/`, `review_intelligence.py`

---

### 6. Eğitim içeriği açık analizi

Her problem için:
- Kullanıcı uygulamayı **kaç ay** kullanabilir?
- İçerik **kaç gün** dayanıyor?
- İçerik **tekrar oranı** nedir?

**Hedef:** Hiçbir kullanıcı «içerikler bitti» dememeli.

**Çıktı:** `output/exercise_scope_audit.json`

---

### 7. Egzersiz kapsam analizi

Minimum hedefler: `exercise_scope_targets.json`

| Modül | Kelime | Cümle | Diğer |
|-------|--------|-------|-------|
| Çocuk | 1300+ | 3000+ | — |
| Kekemelik | 500+ | 1500+ | 500+ okuma, 100+ senaryo |
| Diksiyon | 1000+ | 2000+ | 500+ tekerleme, 500+ artikülasyon |
| Sunum/Hitabet | — | — | 300+ açılış/kapanış, 500+ senaryo, 500+ S&C |
| İş görüşmesi | — | — | 1000+ soru, 3000+ cevap, STAR set |

---

### 8. İçerik boşluk analizi

Rakiplerde olmayan ama kullanıcıların istediği:
- İçerik boşlukları · Özellik boşlukları · Yapay zeka boşlukları · Eğitim boşlukları

**Çıktı:** `output/content_gaps.json`

---

### 9. JSON üretimi

Tüm bulgular `governance/linguistic/output/` altında ayrı dosyalara yazılır.

Katalog: `output_catalog.json`

---

### 10. Yol haritası çıktısı

Öncelik: **Acil · Yüksek · Orta · Düşük**

Her öneri için: beklenen etki · kullanıcı talebi · rakip boşluğu · tahmini gelir etkisi · retention etkisi

**Çıktı:** `output/roadmap_priorities.json` + rapor son bölümü

---

## Çalışma döngüsü

| Sıklık | Aktivite |
|--------|----------|
| Sürekli | Forum/Reddit batch, yorum scrape güncellemesi |
| Haftalık | Intent + JTBD JSON yenileme |
| Aylık | Tam LIUD raporu + INTER-DEPARTMENT FINDINGS |
| Trends tamamlandıkça | Keyword keşif + expert vs user güncelleme |

**Script:** `./scripts/linguistic/run_linguistic_intelligence.sh`

---

## İlişkili departmanlar

| Departman | Klasör | LIUD ile ilişki |
|-----------|--------|-----------------|
| Market Intelligence (Growth) | `governance/market/` | Kanal, rakip, finans — LIUD dil/içerik derinliği |
| Google Trends (LIUD katman 1) | `governance/trends/` | Arama dili keşfi |
| Clinical Evidence | `governance/clinical/` | Uzman terim doğrulama — çelişki kontrolü |
| Finance | `governance/market/YEAR*_ORGANIC_FINANCIAL_MODEL.md` | Gelir etkisi tahmini |
| Product & Education | `docs/01-VISION/`, CPO | Ürün kararları |

Detay: `INTER_DEPARTMENT_PROTOCOL.md`
