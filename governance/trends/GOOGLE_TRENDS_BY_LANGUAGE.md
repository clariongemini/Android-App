# Google Trends — Dil × Yaş Grubu Arama Analizi

**Kaynak:** [Google Trends](https://trends.google.com/trends/?hl=tr)  
**Dönem:** Son 5 yıl (`today 5-y`)  
**Ülke filtresi:** Her dil kendi ana pazarında (TR→Türkiye, US→ABD, GB→İngiltere, DE→Almanya, FR→Fransa, IT→İtalya, ES→İspanya)  
**Veri tarihi:** 2026-06-10  
**Ham veri:** `trends_data.json` · **Sorgu sözlüğü:** `queries.json`  
**Terim keşfi & yol haritası:** [TERM_DISCOVERY_REPORT.md](TERM_DISCOVERY_REPORT.md)

---

## Metodoloji

### RSV (Relative Search Volume) nedir?

Google Trends mutlak arama hacmi vermez; her terim için **0–100** ölçeğinde *göreli ilgi* gösterir. 100, o terimin seçilen dönem ve bölgedeki zirve haftasıdır ([Google Trends yardım](https://trends.google.com/trends/?hl=tr)).

| Ölçek | Yorum (tek terim, tek ülke içinde) |
|-------|-------------------------------------|
| 0–5 | Çok düşük / seyrek arama |
| 6–20 | Düşük |
| 21–40 | Orta |
| 41–60 | Yüksek |
| 61–80 | Çok yüksek |
| 81–100 | Zirveye yakın sürekli ilgi |

### Yaş grubu yaklaşımı

Google Trends doğrudan yaş filtresi sunmaz. Yaş segmentleri **arama niyeti proxy'si** ile modellenmiştir:

| Segment | Hedef yaş | Arama mantığı |
|---------|-----------|---------------|
| **Çocuk** | 0–12 | Ebeveyn araması: gecikme, konuşmuyor, artikülasyon |
| **Ergen** | 13–17 | Ergen + kekemelik / sosyal kaygı |
| **Genç** | 18–29 | Mülakat, sunum, kariyer başı kaygısı |
| **Yetişkin** | 30+ | Tedavi, terapi, diksiyon, topluluk önünde konuşma |

### Sınırlamalar

1. **Ülkeler arası RSV doğrudan karşılaştırılamaz** — farklı terimler farklı ölçeklenir; tabloda “aynı tema, farklı dil” satırları yalnızca *yönsel* kıyas içindir.
2. **Rate limit:** Otomatik çekimde Google HTTP 429 verdi; bazı hücreler eksik. Eksikler `trends_data.json` içinde `"error"` ile işaretli. Tamamlamak için: `fetch_trends.py` (birkaç saat arayla tekrar).
3. **Sıfır RSV ≠ talep yok** — çok niş veya farklı kelimeyle aranan ihtiyaçlar 0 görünebilir.

---

## 7 dil özeti — kanonik terimler (tema bazlı)

Her satırda aynı klinik/duygusal tema, o dildeki doğal arama ifadesiyle ölçülmüştür.

### 1. Çocuk — konuşma gecikmesi

| Dil | Ülke | Arama terimi | Ort. RSV | Seviye |
|-----|------|--------------|----------|--------|
| 🇺🇸 İngilizce (US) | US | speech delay | **52** | Yüksek |
| 🇬🇧 İngilizce (UK) | GB | speech delay | **51** | Yüksek |
| 🇮🇹 İtalyanca | IT | ritardo linguaggio | **33** | Orta |
| 🇫🇷 Fransızca | FR | retard de langage | **25** | Orta |
| 🇹🇷 Türkçe | TR | çocuk konuşma gecikmesi | 1 | Çok düşük* |
| 🇩🇪 Almanca | DE | Sprachverzögerung | 1 | Çok düşük* |
| 🇪🇸 İspanyolca | ES | retraso del habla | 1 | Çok düşük* |

\* Bu terimler çok seyrek aranıyor; alternatifler (`çocuk konuşmuyor`, `Kind spricht nicht`, `niño no habla`) grup karşılaştırmasında daha yüksek çıkabilir — yaş grubu tablolarına bakın.

**Gözlem:** İngilizce pazarlarda çocuk konuşma gecikmesi araması belirgin şekilde daha görünür. TR/DE/ES’te seçilen klinik terim yerine günlük dil (“çocuk konuşmuyor”) tercih ediliyor olabilir.

---

### 2. Kekemelik / akıcılık bozukluğu

| Dil | Ülke | Arama terimi | Ort. RSV | Seviye |
|-----|------|--------------|----------|--------|
| 🇬🇧 İngilizce (UK) | GB | stammering | **49** | Yüksek |
| 🇫🇷 Fransızca | FR | bégaiement | **33** | Orta |
| 🇹🇷 Türkçe | TR | kekemelik | 5 | Düşük |
| 🇺🇸 İngilizce (US) | US | stuttering | — | *eksik (429)* |
| 🇩🇪 Almanca | DE | Stottern | — | *eksik* |
| 🇮🇹 İtalyanca | IT | balbuzie | — | *eksik* |
| 🇪🇸 İspanyolca | ES | tartamudez | — | *eksik* |

**Gözlem:** UK’de “stammering” güçlü ve sürekli bir arama kategorisi. TR’de “kekemelik” düşük ortalama RSV — muhtemelen seyrek zirveler (peak 100) etrafında dağılıyor.

---

### 3. Konuşma terapisi / logopedia

| Dil | Ülke | Arama terimi | Ort. RSV | Seviye |
|-----|------|--------------|----------|--------|
| 🇺🇸 İngilizce (US) | US | speech therapy | **76** | Çok yüksek |
| 🇩🇪 Almanca | DE | Sprachtherapie | **66** | Çok yüksek |
| 🇹🇷 Türkçe | TR | konuşma terapisi | 15 | Düşük |
| 🇬🇧 İngilizce (UK) | GB | speech therapy | — | *eksik* |
| 🇫🇷 Fransızca | FR | orthophonie | — | *eksik* |
| 🇮🇹 İtalyanca | IT | logopedia | — | *eksik* |
| 🇪🇸 İspanyolca | ES | logopedia | — | *eksik* |

**Kısmi yaş grubu verisi (yetişkin batch):**

| Ülke | En yüksek terim | RSV |
|------|-----------------|-----|
| IT | logopedia | 59 |
| ES | logopedia | 68 |
| GB | speech therapy | 70 |

**Gözlem:** “Terapi” araması US ve DE’de çok güçlü. İtalya/İspanya’da `logopedia` baskın kategori adı.

---

### 4. Topluluk önünde konuşma kaygısı

| Dil | Ülke | Arama terimi | Ort. RSV | Seviye |
|-----|------|--------------|----------|--------|
| 🇺🇸 İngilizce (US) | US | public speaking anxiety | **33** | Orta |
| 🇬🇧 İngilizce (UK) | GB | public speaking anxiety | 4 | Çok düşük |
| 🇹🇷 Türkçe | TR | toplu konuşma korkusu | — | *eksik* |
| 🇩🇪 Almanca | DE | Redeangst | — | *eksik* |
| 🇫🇷 Fransızca | FR | peur parler en public | — | *eksik* |
| 🇮🇹 İtalyanca | IT | parlare in pubblico | — | *eksik* |
| 🇪🇸 İspanyolca | ES | miedo hablar en público | — | *eksik* |

**Kısmi yaş grubu verisi:**

| Ülke | Segment | Kazanan terim | RSV |
|------|---------|---------------|-----|
| ES | Genç | oratoria | 52 |
| GB | Genç | presentation skills | 50 |
| IT | Yetişkin | public speaking | 8 |
| ES | Yetişkin | hablar en público | 2 |

**Gözlem:** İspanya’da “oratoria” (hitabet) genç segmentte güçlü. UK’de “presentation skills” kaygı teriminden çok daha yüksek — beceri odaklı arama.

---

### 5. Mülakat / iş görüşmesi kaygısı

| Dil | Ülke | Arama terimi | Ort. RSV | Seviye |
|-----|------|--------------|----------|--------|
| 🇺🇸 İngilizce (US) | US | job interview anxiety | 9 | Düşük |
| 🇬🇧 İngilizce (UK) | GB | job interview nerves | 1 | Çok düşük |
| Diğer diller | — | — | — | *eksik* |

**Gözlem:** Mülakat kaygısı, konuşma terapisi veya çocuk gecikmesine kıyasla tüm dillerde daha düşük RSV — niş veya farklı ifadelerle (“interview tips”, “Bewerbungsgespräch”) aranıyor olabilir.

---

## Dil bazlı yaş grubu detayı

Aşağıdaki tablolar **aynı batch içinde** karşılaştırılabilir (göreli sıralama). RSV değerleri 5 yıllık ortalama.

### 🇹🇷 Türkçe (TR)

| Segment | Durum | Not |
|---------|-------|-----|
| Çocuk | ⏳ Eksik (429) | Sorgular: çocuk konuşma gecikmesi, çocuk konuşmuyor, … |
| Ergen | ⏳ Eksik | ergen kekemelik, genç kekemelik |
| Genç | ⏳ Eksik | mülakat kaygısı, sunum kaygısı |
| Yetişkin | ⏳ Eksik | kekemelik tedavisi, konuşma terapisi |

Kanonik: kekemelik (5), konuşma terapisi (15), çocuk konuşma gecikmesi (1).

---

### 🇺🇸 İngilizce — ABD (US)

| Segment | Durum |
|---------|-------|
| Tüm yaş grupları | ⏳ Batch eksik (429) |

Kanonik: speech delay (52), speech therapy (76), public speaking anxiety (33), job interview anxiety (9).

---

### 🇬🇧 İngilizce — İngiltere (GB)

| Segment | 1. | RSV | 2. | RSV | 3. | RSV |
|---------|-----|-----|-----|-----|-----|-----|
| Ergen | teen stammering | 1 | social anxiety speaking | 1 | GCSE presentation anxiety | 0 |
| Genç | **presentation skills** | **50** | public speaking anxiety | 2 | job interview nerves | 0 |
| Yetişkin | **speech therapy** | **70** | elocution | 5 | public speaking course | 1 |

Çocuk batch: eksik. Kanonik: speech delay (51), stammering (49).

---

### 🇩🇪 Almanca (DE)

| Segment | Durum |
|---------|-------|
| Ergen | Tüm terimler ~0 (Stottern Jugendliche, Soziale Angst Reden, Präsentationsangst) |
| Diğer | ⏳ Eksik |

Kanonik: Sprachtherapie (66), Sprachverzögerung (1).

---

### 🇫🇷 Fransızca (FR)

Tüm yaş batch’leri eksik. Kanonik: retard de langage (25), bégaiement (33).

---

### 🇮🇹 İtalyanca (IT)

| Segment | 1. | RSV | 2. | RSV |
|---------|-----|-----|-----|-----|
| Ergen | ansia sociale parlare | 1 | balbuzie adolescenti | 0 |
| Yetişkin | **logopedia** | **59** | dizione | 24 |

Kanonik: ritardo linguaggio (33).

---

### 🇪🇸 İspanyolca (ES)

| Segment | 1. | RSV | 2. | RSV |
|---------|-----|-----|-----|-----|
| Genç | **oratoria** | **52** | miedo hablar en público | 0 |
| Yetişkin | **logopedia** | **68** | hablar en público | 2 |

Kanonik: retraso del habla (1).

---

## Yaş segmenti — çapraz dil heatmap (mevcut veri)

Özet: hangi yaş/niyet tipi hangi dilde daha görünür?

| Tema / segment | En güçlü sinyal | RSV | Zayıf / niş |
|----------------|-----------------|-----|-------------|
| Çocuk gecikmesi | US, GB | ~52 | TR, DE, ES (seçilen terim) |
| Kekemelik | GB | 49 | TR |
| Terapi genel | US | 76 | TR |
| Terapi (IT/ES yetişkin) | ES logopedia | 68 | — |
| Performans / sunum (genç) | ES oratoria | 52 | TR, DE |
| Mülakat kaygısı | US | 9 | GB, diğer |

```
Çocuk gecikmesi     ████████████ US/GB (52)
                    ██████ IT (33) FR (25)
                    ▏ TR/DE/ES (1)

Konuşma terapisi    ████████████████ US (76) DE (66)
                    ███ TR (15)

Kekemelik           ██████████ GB (49) FR (33)
                    █ TR (5)

Genç — sunum        ████████████ ES oratoria (52) GB presentation skills (50)
```

---

## Manuel doğrulama linkleri

Google Trends Keşfet sayfaları (5 yıl, ilgili ülke):

| Dil | Örnek karşılaştırma URL |
|-----|-------------------------|
| TR | `https://trends.google.com/trends/explore?date=today%205-y&geo=TR&q=kekemelik,konu%C5%9Fma%20terapisi,%C3%A7ocuk%20konu%C5%9Fmuyor` |
| US | `https://trends.google.com/trends/explore?date=today%205-y&geo=US&q=speech%20delay,speech%20therapy,stuttering` |
| DE | `https://trends.google.com/trends/explore?date=today%205-y&geo=DE&q=Sprachtherapie,Stottern,Sprachverz%C3%B6gerung` |
| FR | `https://trends.google.com/trends/explore?date=today%205-y&geo=FR&q=orthophonie,b%C3%A9gaiement,retard%20de%20langage` |
| IT | `https://trends.google.com/trends/explore?date=today%205-y&geo=IT&q=logopedia,balbuzie,ritardo%20linguaggio` |
| ES | `https://trends.google.com/trends/explore?date=today%205-y&geo=ES&q=logopedia,tartamudez,oratoria` |

---

## Veri tamamlama

```bash
cd /path/to/your-project
python3 -m venv .venv-trends
.venv-trends/bin/pip install pytrends pandas
.venv-trends/bin/python governance/trends/fetch_trends.py
```

Rate limit sonrası 2–4 saat bekleyip tekrar çalıştırın; script yalnızca eksik hücreleri doldurur.

---

## İlişkili dokümanlar

- [VOC_JTBD_DEMAND_RESEARCH.md](../market/VOC_JTBD_DEMAND_RESEARCH.md) — kullanıcı şikayetleri (Trends önceki turda çalıştırılmamıştı)
- [MARKET_DEMAND_RESEARCH.md](../market/MARKET_DEMAND_RESEARCH.md) — epidemiyoloji ve klinik talep

---

*Bu rapor arama ilgisini ölçer; klinik prevalans veya ürün önerisi değildir.*
