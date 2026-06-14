# LIUD Rapor Şablonu

Dosya adı: `governance/linguistic/reports/LIUD_REPORT_YYYY-MM-DD.md`

---

```markdown
# LIUD Raporu — [Tarih]

**Departman:** Linguistic Intelligence & User Demand  
**Dönem:** [haftalık / aylık]  
**Locale kapsamı:** TR, US, GB, DE, FR, ES, IT  
**JSON çıktıları:** `governance/linguistic/output/`

---

## 1. Yönetici özeti

[3–5 madde — kullanıcı dili bulguları, en kritik boşluk, acil öncelik]

---

## 2. Google Trends — keyword keşfi

| Locale | Rising / Breakout | Seasonal | Long-tail yeni | RSV / büyüme |
|--------|-------------------|----------|----------------|--------------|

Kaynak: `governance/trends/trends_data.json`, `TERM_DISCOVERY_REPORT.md`

---

## 3. Uzman dili vs kullanıcı dili

| Uzman terimi | Kullanıcı terimi | Locale | Arama gücü | Sıklık (forum/store) |
|--------------|------------------|--------|------------|----------------------|

Kaynak: `output/expert_vs_user_language.json`

---

## 4. JTBD özeti

| Keyword / tema | Job kategorisi | Duygusal yük | Kanıt |
|----------------|----------------|--------------|-------|

Kaynak: `output/jtbd.json`

---

## 5. Topluluk dili (Reddit / Forum / Quora)

### En sık sorular
### En çok şikayet
### Gerçek cümleler (alıntılı, URL'li)
### Başarısız çözüm girişimleri
### Duygusal ifadeler

Kaynak: `output/*_questions.json`, `emotion_map.json`

---

## 6. Store yorumları — 1★ / 2★ / 3★

| Rakip | 1★ tema | 2★ tema | 3★ tema | {{APP_NAME}} fırsatı |
|-------|---------|---------|---------|-----------------|

Kaynak: `scraper_output/`, `content_gaps.json`

---

## 7. Eğitim içeriği dayanıklılığı

| Modül | Mevcut envanter | Hedef | Tahmini gün/ay | «İçerik bitti» riski |
|-------|-----------------|-------|----------------|----------------------|

Kaynak: `output/exercise_scope_audit.json`, `exercise_scope_targets.json`

---

## 8. İçerik / özellik / AI boşlukları

| Boşluk türü | Kullanıcı talebi | Rakiplerde | {{APP_NAME}} durumu | Öncelik |
|-------------|------------------|------------|----------------|---------|

Kaynak: `output/content_gaps.json`

---

## 9. Yol haritası öncelikleri

| Öncelik | Öneri | Beklenen etki | Talep | Rakip boşluğu | Gelir | Retention |
|---------|-------|---------------|-------|---------------|-------|-----------|

Kaynak: `output/roadmap_priorities.json`

---

## 10. INTER-DEPARTMENT FINDINGS

### Uyumlu Bulgular
-

### Çelişen Bulgular
-

### Riskler
-

### Kaçırılan Fırsatlar
-

### Diğer Departmanlardan Beklenen Aksiyonlar
| Departman | Aksiyon | Deadline |
|-----------|---------|----------|

### Ortak Yol Haritası Önerileri
1.
2.
3.

---

## Ekler

- JSON: `governance/linguistic/output/`
- Trends: `governance/trends/`
- Market: `governance/market/USER_INTENT_SIGNALS.md`
- Önceki LIUD: `governance/linguistic/reports/`
```
