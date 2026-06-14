# Uygulama Türü Profilleri — Derinlik Matrisi

**Versiyon:** 1.0  
Mavi Okyanus ajanı, proje değerlendirmesine başlamadan önce **tek bir primary type** seçer. İkincil tag eklenebilir.

---

## Taxonomy (primary types)

| `type_id` | Ad | Örnek vertical |
|-----------|-----|----------------|
| `health_clinical_adjacent` | Sağlık — klinik yakın | Konuşma terapisi, fizik tedavi ev, kronik takip |
| `health_wellness_lifestyle` | Sağlık — wellness | Uyku, stres, mindfulness, beslenme takibi |
| `parenting_family` | Ebeveynlik / aile | Gelişim takibi, disiplin, güvenlik |
| `education_skill` | Eğitim / beceri | Dil, müzik pratiği, sınav hazırlık |
| `productivity_personal` | Kişisel verimlilik | Alışkanlık, odak, not |
| `productivity_b2b_smb` | B2B / KOBİ araç | Saha servis, envanter, randevu |
| `finance_personal` | Kişisel finans | Bütçe, borç, yatırım takibi |
| `finance_niche` | Finans niş | Freelancer vergi, gig ekonomi |
| `hobby_niche_tool` | Hobby / niş araç | Özel koleksiyon, craft, pet |
| `local_regional` | Yerel / bölgesel | TR/DE özel regülasyon veya kültür |
| `creative_creator` | İçerik üretici | Küçük kanal araçları (red ocean riski yüksek — dikkat) |
| `accessibility_assistive` | Erişilebilirlik | Görme/işitme/motor destek |

**Kırmızı flag types (ekstra G1 sıkı):** `creative_creator`, `social_community` (tanımlı değilse ekleme), `messaging`, `game`.

---

## Ağırlık matrisi (boyut → ağırlık)

Değerler toplamı = **1.00** per type.

### `health_clinical_adjacent` (Konuşma referans türü)

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .14 | .12 | .14 | .12 | .10 | .08 | .10 | .08 | .10 | .12 |

**Ek derin sorular:**
- Klinik seans maliyeti ankrajı?
- Etik: tedavi iddiası gerekli mi?
- Terapist / doktor kanalı (Yıl 2+)?
- Epidemiyoloji veya prevalans kaynağı?

**Veri önceliği:** `MARKET_DEMAND_RESEARCH`, `VOC_JTBD`, `governance/clinical/`, forum batch.

---

### `health_wellness_lifestyle`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .12 | .10 | .12 | .14 | .10 | .10 | .12 | .08 | .10 | .12 |

**Ek sorular:** Retention 30 gün? Calm/Headspace overlap? Mevsimsellik?

---

### `parenting_family`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .14 | .10 | .11 | .10 | .10 | .10 | .14 | .08 | .11 | .12 |

**Ek sorular:** Ebeveyn forum intent? Çocuk verisi COPPA/Play Families?

---

### `education_skill`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .12 | .11 | .10 | .11 | .10 | .12 | .08 | .08 | .10 | .18 |

**Ek sorular:** Tamamlama oranı? Okul takvimi mevsimselliği? Duolingo/Babbel overlap?

---

### `productivity_personal`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .10 | .08 | .12 | .14 | .12 | .10 | .06 | .10 | .10 | .18 |

**Ek sorular:** Notion/Todoist paritesi? Günlük aktif kullanım şart mı?

---

### `productivity_b2b_smb`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .10 | .10 | .14 | .12 | .10 | .06 | .04 | .10 | .12 | .22 |

**Ek sorular:** Seat pricing? Satış döngüsü uzunluğu? Yıl 1 B2C köprüsü var mı? (**Yıl 1 B2B gelir varsayımı yasak** — sadece tüketici köprüsü)

---

### `finance_personal`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .11 | .09 | .13 | .13 | .10 | .09 | .05 | .09 | .11 | .20 |

**Ek sorular:** Regülasyon? Banka entegrasyonu şart mı? Güven / veri hassasiyeti?

---

### `finance_niche`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .12 | .11 | .14 | .11 | .09 | .10 | .05 | .10 | .10 | .18 |

---

### `hobby_niche_tool`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .10 | .14 | .10 | .08 | .11 | .14 | .10 | .09 | .12 | .12 |

**Ek sorular:** TAM küçük ama ödeme güçlü mü? Passion premium?

---

### `local_regional`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .13 | .12 | .11 | .10 | .09 | .11 | .12 | .07 | .10 | .15 |

**Ek sorular:** Sadece TR mi? Dil/regülasyon bariyeri rakibi azaltıyor mu?

---

### `accessibility_assistive`

| D | C | M | L | F | A | S | P | R | G |
|---|---|---|---|---|---|---|---|---|---|
| .13 | .11 | .11 | .12 | .10 | .08 | .09 | .08 | .12 | .16 |

**Ek sorular:** Erişilebilirlik standartları? Devlet / sigorta ödemesi?

---

## İhtiyaç türü × type bonus

Ajan, primary type seçtikten sonra **dominant need** işaretler:

| Dominant need | Hangi boyutlara +0.5 (max 5) |
|---------------|------------------------------|
| Acı | D, M |
| Korku | D, S |
| Verimlilik | L, G |
| Statü | S, M |
| Tasarruf | M, R (rakip pahalı) |
| Alışkanlık | L |
| Uyum | R, C (rakip zayıf) |

Bonus sonrası boyutlar 5'i geçmez; normalize et.

---

## Konuşma (#1) referans benchmark

Yeni projeler portföy skoru **P** boyutunda Konuşma ile karşılaştırılır:

| Korelasyon | P puanı rehberi |
|------------|-----------------|
| Farklı vertical, farklı öbek | 4–5 |
| Aynı kullanıcı, farklı problem | 2–3 |
| Aynı rakip seti, farklı özellik | 2–3 |
| Konuşma modülü spin-off | 1–2 (+ BEKLE önerisi) |
| Konuşma klonu | 1 (+ portföy cezası) |

---

## Tür seçimi kararsızsa

1. Ana gelir kaynağına bak (B2B → `productivity_b2b_smb`)  
2. Regülasyon (sağlık → clinical vs wellness)  
3. İki tür eşitse → daha yüksek **G** ağırlıklı olanı seç; ikincil tag ekle  

---

## Yeni tür ekleme

Mimar talebi + DEPARTMENT_CHARTER revizyonu + ağırlık satırı toplamı 1.00 doğrulaması.
