# Forum ve Topluluk Zekâsı Planı

**Durum:** Planlı — henüz otomatik çekim yok  
**Öncelik:** Yüksek (Growth ajanı bunu **görmezden gelemez**)  
**Katalog:** `forum_query_catalog.json`

---

## Neden gerekli?

Play Store yorumları **«ne kadar insan var?»** sorusuna kısmen cevap verir.  
Forum / Reddit / TR toplulukları **«tam olarak ne istiyorlar?»** sorusunun ana kaynağıdır:

- «Çocuğum konuşmuyor»
- «R harfini söyleyemiyor»
- «Peltek konuşuyor»
- «Terapist ödev verdi, evde ne kullanalım?»

Bu ifadeler ASO anahtar kelimesinden daha derin **ürün niyeti** taşır.

---

## Hedef kaynaklar

| Kaynak | Örnek değer | Erişim |
|--------|-------------|--------|
| Reddit | r/speechtherapy, r/stuttering, r/autism | JSON API / manuel |
| Quora | «best speech app for kids» | Manuel örnekleme |
| Ekşi Sözlük | kekemelik, peltek, konuşma terapisi | Manuel (ToS) |
| Kadınlar Kulübü | çocuğum konuşmuyor | Manuel örnekleme |
| Donanım Haber | diksiyon / uygulama | Manuel |
| Facebook ebeveyn grupları | otizm konuşma | Sınırlı API |

---

## Çıktı formatı

```
governance/market/forum_output/
├── reddit/speech_therapy_app.json
├── turkish/eksi_peltek.json
└── manifest.json
```

Her kayıt: `source`, `query`, `text`, `date`, `matched_intents[]`, `locale`

---

## Growth ajanı döngüsü

| Hafta | Aksiyon |
|-------|---------|
| W1 | Reddit r/speechtherapy — son 50 «app recommendation» thread özeti |
| W2 | TR: Ekşi + KHK — «çocuk konuşmuyor» 20 entry |
| W3 | Quora — articulation / stuttering soruları |
| W4 | `USER_INTENT_SIGNALS.md` birleştir (Play + forum) |

**Script (iskelet):** `scripts/scrapers/forum_intelligence.py --source reddit --dry-run`

---

## Konuşma ürün eşlemesi (forumdan beklenen talepler)

| Forum kalıbı | Ürün yanıtı |
|--------------|-------------|
| «Terapist ödevi takibi» | Klinik QR + haftalık rapor PDF |
| «Video gibi göstersin» | Ayna + model video (Speech Blubs beklentisi) |
| «İlerlemeyi göremiyorum» | İlk gün vs bugün + premium analiz |
| «Her gün hatırlatsın» | Journey + bildirim (offline) |
| «Türkçe R/Ş çalışması» | Fonem seti + TR ASO |
| «Yetişkin için çocuk uygulaması değil» | UserPurpose onboarding |

---

## Yasak (Growth ajanı)

- Forum verisi olmadan «kullanıcı ihtiyacını tam anladık» demek
- Yalnızca Play Store ile «altın insight» iddiası
- TR/EN/DE dışı locale’leri raporda yok saymak (fr/it/es eşit)

**Revizyon:** İlk forum batch sonrası CPO + Growth çift onay.
