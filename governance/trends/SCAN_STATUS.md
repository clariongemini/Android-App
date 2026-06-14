# Google Trends Tarama Durumu

**Son güncelleme:** 2026-06-13  
**Dönem:** Son 5 yıl (`today 5-y`)

---

## Tamamlanma özeti

| Aşama | Durum | Oran |
|-------|-------|------|
| **Phase 1 — Yaş grubu batch'leri** | ✅ Tamam | **28/28** (7 dil × 4 segment) |
| **Phase 2 — Kanonik terimler** | ⚠️ Neredeyse tamam | **34/35** (1 hata: FR mülakat) |
| **Phase 3 — İlgili aramalar (related)** | ⚠️ Kısmi | **73/91** seed |
| **Phase 4 — Alternatif terim karşılaştırması** | ⚠️ Kısmi | **36/54** batch |

**Sonuç:** Ana veri seti (Phase 1) **%100 tamam**. Yol haritası kararları için yeterli. Alternatif keşif (Phase 4) FR genç/yetişkin + IT + ES için eksik batch'ler tamamlanıyor.

---

## Phase 1 — Dil × yaş grubu kazanan terimler

| Dil | Çocuk | Ergen | Genç | Yetişkin |
|-----|-------|-------|------|----------|
| 🇹🇷 TR | dil ve konuşma terapisi (7) | **özgüven (13)** | **mülakat (33)** | **diksiyon (13)** |
| 🇺🇸 US | **speech delay (52)** | social anxiety speaking (16) | **job interview (47)** | **speech therapy (75)** |
| 🇬🇧 GB | **speech delay (54)** | teen stammering (1) | **presentation skills (50)** | **speech therapy (70)** |
| 🇩🇪 DE | **Kind spricht nicht (65)** | — (0) | Vorstellungsgespräch Angst (1) | **Sprachtherapie (64)** |
| 🇫🇷 FR | **enfant ne parle pas (45)** | — (0) | peur parler en public (1) | **orthophonie (49)** |
| 🇮🇹 IT | **bambino non parla (59)** | — (1) | **comunicazione (74)** | **logopedia (59)** |
| 🇪🇸 ES | **dislalia (40)** | — (0) | **oratoria (52)** | **logopedia (68)** |

*(RSV = 5 yıllık ortalama göreli ilgi, 0–100)*

---

## TR — öne çıkan bulgular

### Çocuk
| Terim | Ort. RSV | Zirve |
|-------|----------|-------|
| dil ve konuşma terapisi | 7 | 50 |
| kekemelik | 5 | 100 |
| konuşma bozukluğu | 3 | 7 |

**İlgili aramalar (kekemelik seed):** kekemelik tedavisi (100), kekemelik nasıl geçer (68), kekemelik neden olur (66), çocuklarda kekemelik (47), kekemelik egzersizleri (30)

### Genç
**mülakat (33)** >> hitabet (2), diksiyon (6) — kariyer odaklı arama baskın

### Yetişkin
**diksiyon (13)** >> kekemelik (5), hitabet (4)

---

## Yanlış kelime uyarıları (doğrulandı)

| Dil | Eski/klinik terim | Gerçek kullanıcı dili |
|-----|-------------------|----------------------|
| TR çocuk | çocuk konuşma gecikmesi (1) | kekemelik, dil ve konuşma terapisi |
| TR genç | hitabet, sunum teknikleri | **mülakat** |
| DE çocuk | Sprachverzögerung (1) | **Kind spricht nicht (65)** |
| ES çocuk | retraso del habla (1) | **dislalia (40)**, niño no habla |
| FR çocuk | retard de langage (25) | **enfant ne parle pas (45)** |
| US/GB genç | public speaking anxiety | **presentation skills / job interview** |
| ES genç | miedo hablar en público | **oratoria (52)** |

---

## Dosyalar

| Dosya | İçerik |
|-------|--------|
| `trends_data.json` | Phase 1 + Phase 2 ham RSV |
| `discovery_data.json` | Related queries + alternatif batch'ler + `term_insights` |
| `TERM_DISCOVERY_REPORT.md` | Yol haritası çıkarımları |
| `fetch_log.txt` | Çekim günlüğü |

---

## Eksik kalan (tamamlanıyor)

- Phase 4: FR/young, FR/adult, IT (tüm), ES (tüm) — 18 batch
- Phase 3: 18 related seed
- Phase 2: `peur entretien embauche` (FR mülakat)
