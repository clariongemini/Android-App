# LIUD — Departmanlar Arası İletişim Protokolü

**Departman:** Linguistic Intelligence & User Demand (LIUD)  
**Kural:** Bu departman bağımsız çalışamaz.

---

## Her rapor döneminde okunacak kaynaklar

| Departman | Son rapor / dosya | Okuma amacı |
|-----------|-------------------|-------------|
| **LIUD** (önceki) | `governance/linguistic/reports/LIUD_REPORT_*.md` | Trend devamlılığı |
| **Clinical Evidence** | `governance/clinical/CLINICAL_EVIDENCE_INDEX.md` | Uzman terim doğrulama |
| **Market Intelligence** | `governance/market/demand_output/DEMAND_INTELLIGENCE_REPORT.md` | Rakip + kanal + monetizasyon |
| **Market Intelligence** | `governance/market/USER_INTENT_SIGNALS.md` | Play + forum birleşik niyet |
| **Finance** | `governance/market/YEAR1_ORGANIC_FINANCIAL_MODEL.md` (+ Y2/Y3) | Gelir etkisi sınırları |
| **Product & Education** | `docs/01-VISION/PRODUCT_BRIEF.md`, `docs/33-LAYER-MANIFEST.yaml` | Ürün kapsamı uyumu |

---

## Rapor oluşturma akışı

```
1. Kendi bulgularını üret (Trends + VOC + Forum + Store + içerik envanteri)
        ↓
2. Diğer departman raporlarını oku
        ↓
3. Çelişkileri tespit et (ör. klinik terim yüksek öncelik vs düşük arama)
        ↓
4. Riskleri belirt (içerik dayanıklılığı, yanlış dil ASO'da)
        ↓
5. Ortak öneriler oluştur
        ↓
6. INTER-DEPARTMENT FINDINGS bölümünü yaz
```

---

## INTER-DEPARTMENT FINDINGS — zorunlu alt bölümler

Her `LIUD_REPORT_*.md` dosyası şu bölümü içermelidir:

### Uyumlu Bulgular
LIUD ile diğer departmanların aynı yönde söylediği sinyaller.

Örnek: Market «geç konuşma forum ağırlıklı» + LIUD «çocuğum konuşmuyor» kullanıcı dili yüksek.

### Çelişen Bulgular
Departmanlar arası çatışma — hangi veri kaynağı haklı?

Örnek: Clinical «artikülasyon modülü zorunlu» vs Trends TR «artikülasyon bozukluğu» yüksek ama Product henüz fonem derinliği planlamamış.

### Riskler
Organizasyonel risk — LIUD tespiti.

Örnek: Çocuk modülü kelime envanteri hedefin %12'sinde → 3 hafta sonra «içerik bitti» churn.

### Kaçırılan Fırsatlar
Başka departmanın gördüğü ama LIUD'un henüz derinleştirmediği alan.

### Diğer Departmanlardan Beklenen Aksiyonlar

| Departman | Beklenen aksiyon |
|-----------|------------------|
| Market Intelligence | ASO listing dilini LIUD `expert_vs_user_language.json` ile güncelle |
| Product & Education | `roadmap_priorities.json` Acil maddelerini sprint'e al |
| Clinical Evidence | Uzman terim ↔ kullanıcı dili eşlemesini doğrula/reddet |
| Finance | İçerik yatırımı ROI'sini P50 modelde satır olarak göster |
| CPO | Premium paket isimlendirmesini kullanıcı diliyle hizala |

### Ortak Yol Haritası Önerileri
En az 3 madde — çok departmanlı, öncelik etiketli.

---

## Sorumluluk ilkesi

LIUD yalnızca kendi JSON çıktılarının başarısından değil, **tüm organizasyonun** doğru dil, doğru içerik ve doğru öncelikle ilerlemesinden sorumludur.

---

## Çakışma çözümü

| Durum | Karar mercii |
|-------|--------------|
| Arama dili vs klinik doğruluk | Clinical Evidence veto; LIUD alternatif kullanıcı dili önerir |
| İçerik derinliği vs Yıl 1 finans | Finance P50 sınırı; LIUD minimum viable content bandı önerir |
| ASO keyword vs kullanıcı dili | LIUD birincil; Growth ikincil (dönüşüm testi) |
| B2B / terapist özelliği | Yıl 1 **yasak** — `B2B_GATE_CRITERIA.md`; LIUD ev ödevi dili Yıl 1'de ebeveyn raporu olarak çerçevelenir |
