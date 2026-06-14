# Terim Keşif Raporu — Kullanıcılar Ne Arıyor?

**Amaç:** Eğitim yol haritasında hangi hece/kelime/cümle önceliklerine odaklanacağımızı belirlemek için *gerçek arama dili* ile *klinik terimlerimizi* karşılaştırmak.  
**Kaynak:** `trends_data.json` (kısmi, 2026-06-10/11) + `VOC_JTBD_DEMAND_RESEARCH.md` + alternatif aday listesi  
**Durum:** Ultra yavaş çekim (`--sleep 300 --cooldown 900`, 429'da 10–120 dk bekleyip oturum yenileme). TR/child tamamlandı.

---

## Kritik bulgu: Yanlış kelimeye yönelme riski

Google Trends RSV (0–100, göreli ilgi) verileri şunu gösteriyor: **birçok dilde klinik/ürün terimlerimiz, kullanıcıların gerçekte aradığı ifadelerden farklı.**

| Dil | Bizim terim (düşük RSV) | Kullanıcı dili (yüksek RSV / VOC) | Fark |
|-----|-------------------------|-----------------------------------|------|
| 🇹🇷 TR | çocuk konuşma gecikmesi (mean **1**, peak 79) | **artikülasyon bozukluğu** (mean **16**, peak 100) | Batch içinde kazanan: artikülasyon |
| 🇹🇷 TR | çocuk konuşmuyor (mean 0, peak **48**) | «Konuşmuyor» seyrek ama zirvede güçlü | Günlük dil — ortalama düşük, spike yüksek |
| 🇹🇷 TR | toplu konuşma korkusu (eksik/0*) | **hitabet**, **diksiyon**, **konuşma korkusu**, **sunum** | “Toplu konuşma korkusu” günlük dil değil |
| 🇪🇸 ES genç | miedo hablar en público (**0**) | **oratoria** (**52**) | Kaygı değil beceri araması |
| 🇬🇧 GB genç | public speaking anxiety (**2**) | **presentation skills** (**50**) | Beceri > kaygı |
| 🇮🇹 IT yetişkin | balbuzie trattamento (**0**) | **logopedia** (**59**), **dizione** (24) | Tedavi değil hizmet kategorisi |
| 🇪🇸 ES yetişkin | tartamudez tratamiento (**0**) | **logopedia** (**68**) | Aynı pattern |
| 🇩🇪 DE çocuk | Sprachverzögerung (**1**) | muhtemelen **Sprachtherapie**, **Kind spricht nicht** | Klinik terim zayıf |
| 🇺🇸 US | speech delay (**52**) ✓ | late talker, speech therapy (**76**) | US'te clinical term çalışıyor |

\*TR toplu konuşma korkusu rate limit nedeniyle henüz ölçülemedi; VOC'ta bu ifade yok.

---

## Yaş segmenti × dil — öncelik sıralaması (mevcut veri)

### Çocuk (0–12) — ebeveyn araması

| Öncelik | Dil | En güçlü sinyal | RSV | Eğitim/yol haritası çıkarımı |
|---------|-----|-----------------|-----|------------------------------|
| 1 | US/GB | speech delay | 51–52 | Gecikme + milestone kelimeleri (late talker, not talking) |
| 2 | IT | ritardo linguaggio | 33 | Ritardo + bambino non parla |
| 3 | FR | retard de langage | 25 | Retard + enfant ne parle pas |
| 4 | TR | kekemelik > çocuk konuşma gecikmesi | 5 vs 1 | **Çocuk modülünde “gecikme” değil “konuşmuyor/kekeliyor” dili** |
| 5 | DE/ES | Sprachverzögerung / retraso del habla | 1 | Alternatif terimler zorunlu |

**TR çocuk batch (2026-06-11, canlı veri):**

| Terim | Ort. RSV | Zirve RSV | Yorum |
|-------|----------|-----------|-------|
| **artikülasyon bozukluğu** | **16** | 100 | En yüksek sürekli ilgi |
| çocuk konuşma gecikmesi | 1 | 79 | Klinik terim — düşük ortalama |
| kekemelik çocuk | 0 | 64 | Zirve yüksek, ortalama düşük |
| çocuk konuşmuyor | 0 | 48 | Ebeveyn günlük dili |
| geç konuşan çocuk | 0 | 44 | Niş |

**TR için önerilen odak kelimeler (VOC + Trends uyumu):**
- **Artikülasyon / sesletim** («r» çıkaramıyor, «s» yanlış») — en yüksek arama sinyali
- «Çocuğum konuşmuyor» / «2 yaşında konuşmuyor» — zirve aramaları yüksek
- «Kekeliyor» / «Kekemelik» — zirve 64, VOC heat yüksek
- «Dil ve konuşma terapisi» — hizmet araması
- «Evde ne yapmalıyım» (VOC #3)

**Öncelik hece/kelime (çocuk TR):** basit fiil + isim («konuş-», «söyle-», «bak», «ver», «anne», «baba»), iki kelimelik cümle («anne ver», «baba gel»)

---

### Ergen (13–17)

Mevcut batch'lerde tüm dillerde RSV çok düşük (0–1). Bu segment **doğrudan arama ile değil**, ebeveyn veya genel terim üzerinden geliyor olabilir.

| Dil | En iyi batch terimi | RSV | Not |
|-----|---------------------|-----|-----|
| IT | ansia sociale parlare | 1 | Genel sosyal kaygı |
| GB | teen stammering / social anxiety speaking | 1 | Niş |
| DE | tümü | 0 | Ergen-spesifik terim yok |

**Yol haritası:** Ergen modülünde arama terimi değil **VOC dili** kullan: «utanç», «sınıfta konuşamıyorum», «arkadaşlarım dalga geçiyor», «sunum yapamıyorum»

---

### Genç (18–29)

| Dil | Kazanan terim | RSV | Kaybeden terim | RSV |
|-----|---------------|-----|----------------|-----|
| ES | **oratoria** | 52 | miedo hablar en público | 0 |
| GB | **presentation skills** | 50 | public speaking anxiety | 2 |
| US | public speaking anxiety | 33 | job interview anxiety | 9 |

**Çıkarım:** Genç segmentte **kaygı çerçevesi değil, beceri çerçevesi** aranıyor (oratoria, presentation skills). Eğitim içeriği:
- Sunum açılışı cümleleri
- İş görüşmesi kısa yanıtlar (STAR formatı)
- «Kendini tanıt» / «Projemi anlat» kalıpları

**Öncelik cümle tipleri:** 1. tekil tanıtım, 2. görüş nedenleme, 3. kısa özet, 4. soru sorma

---

### Yetişkin (30+)

| Dil | 1. terim | RSV | 2. terim | RSV |
|-----|----------|-----|----------|-----|
| US | speech therapy | 76 | — | — |
| GB | speech therapy | 70 | elocution | 5 |
| DE | Sprachtherapie | 66 | — | — |
| ES | logopedia | 68 | hablar en público | 2 |
| IT | logopedia | 59 | dizione | 24 |
| TR | konuşma terapisi | 15 | kekemelik | 5 |

**Çıkarım:** Yetişkinler **hizmet kategorisi** arıyor (terapi/logopedia), spesifik «tedavi» terimlerini değil. TR'de hacim düşük ama **diksiyon** ve **hitabet** alternatif batch'te test edilmeli.

---

## Tema bazlı kanonik karşılaştırma (7 dil)

### Konuşma terapisi / logopedia

```
US speech therapy    ████████████████████ 76
DE Sprachtherapie    █████████████████ 66
ES logopedia         █████████████████ 68
GB speech therapy    █████████████████ 70
IT logopedia         ███████████████ 59
TR konuşma terapisi  ███ 15
```

### Çocuk gecikmesi

```
US/GB speech delay   ████████████ 52
IT ritardo           ████████ 33
FR retard langage    ██████ 25
TR çocuk gecikmesi   ▏ 1
DE Sprachverzögerung ▏ 1
ES retraso habla     ▏ 1
```

### Kekemelik

```
GB stammering        ███████████ 49
FR bégaiement        ████████ 33
TR kekemelik         █ 5
```

---

## VOC ile arama uyumu — eğitim öncelik matrisi

| VOC problemi (sık) | Kullanıcı dili (arama) | Eğitimde öncelik |
|--------------------|------------------------|------------------|
| Çocuk konuşmuyor (#1) | çocuk konuşmuyor, kekeliyor | Günlük 2–3 kelimelik cümleler, oyun dili |
| Terapi bekleme (#2) | konuşma terapisi, logopedia | Evde pratik modülleri, «terapist yokken» |
| Evde ne yapmalıyım (#3) | evde konuşma, oyun | Ebeveyn rehberi + çocuk egzersizi |
| Utanç/kaçınma (#12) | kekemelik, stammering | Yavaş konuşma, nefes, kısa cümle |
| Kamu konuşması (#33 heat) | oratoria, presentation skills | Sunum kalıpları, açılış cümleleri |
| STT/uygulama hatası (#11) | speech therapy apps (Accio: apps peak 86) | Uygulama içi güvenilir STT önceliği |

---

## Önerilen güncellenmiş kanonik terimler

`queries.json` canonical_terms güncellemesi önerisi (keşif sonrası):

| Tema | TR (eski → yeni) | ES (eski → yeni) | GB genç (eski → yeni) |
|------|------------------|------------------|----------------------|
| Çocuk gecikmesi | çocuk konuşma gecikmesi → **çocuk konuşmuyor** | retraso del habla → **niño no habla** | — |
| Performans kaygısı | toplu konuşma korkusu → **hitabet** / **diksiyon** | miedo hablar → **oratoria** | public speaking anxiety → **presentation skills** |
| Terapi | konuşma terapisi → **dil ve konuşma terapisi** | logopedia ✓ | speech therapy ✓ |

---

## Veri tamamlama

```bash
# Ultra yavaş — 429 alana kadar tekrar dener (tahmini 12–24 saat)
./governance/trends/run_slow_fetch.sh

# veya tek dil önce
PYTHONUNBUFFERED=1 .venv-trends/bin/python governance/trends/discover_and_fetch.py \
  --only TR --sleep 300 --cooldown 900
```

Tamamlandığında `discovery_data.json` içinde:
- `related_queries` → Google'ın önerdiği gerçek aramalar (top + rising)
- `alternative_rankings` → 10+ aday terimin RSV karşılaştırması
- `term_insights` → otomatik «yanlış terim» uyarıları

---

## Yol haritası için 5 somut öncelik (şimdilik)

1. **TR çocuk:** «Konuşma gecikmesi» yerine «konuşmuyor / kekeliyor» dili; 2–4 kelimelik ev cümleleri
2. **ES/IT genç-yetişkin:** «Oratoria / logopedia» ekseninde beceri modülleri
3. **US/GB/DE:** «Speech delay / speech therapy» — klinik terim burada çalışıyor; milestone tabanlı içerik
4. **Tüm diller kekemelik:** Utanç azaltma + kısa cümle pratiği (arama düşük ama VOC heat yüksek)
5. **Genç kariyer:** «Presentation skills» / «oratoria» — mülakat kaygısından çok sunum becerisi

---

*Bu rapor `discover_and_fetch.py` tamamlandıkça güncellenecektir.*
