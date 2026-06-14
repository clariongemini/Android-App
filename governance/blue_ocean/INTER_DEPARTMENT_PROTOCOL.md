# Mavi Okyanus — Departmanlar Arası Protokol

## Girdi alır

| Kaynak | Veri |
|--------|------|
| **Growth** | `COMPETITOR_ANALYSIS.md`, `PLAY_STORE_BENCHMARKS.json`, `demand_output/`, `scraper_output/` (READ ONLY) |
| **Discovery** | `discovery/candidates.json`, `WEEKLY_CANDIDATES.md` (keşif radarı çıktısı) |
| **LIUD** | `governance/linguistic/output/` — öbek, JTBD, intent |
| **PDC** | Önceki `rejected_features.json`, roadmap öncelikleri |
| **Clinical** | `governance/clinical/` — sağlık türleri için |

## Çıktı verir

| Hedef | Ne zaman | İçerik |
|-------|----------|--------|
| **Mimar** | Her değerlendirme | `projects/{slug}.md` özeti |
| **PDC** | Karar YAP | Öncelik önerisi (P1–P3), kanıt linkleri |
| **Growth** | Karar YAP | ASO/sosyal/forum hipotezi |
| **CPO** | Karar YAP veya BEKLE | Konumlandırma cümlesi |

## Çakışma çözümü

| Konu | Merci |
|------|--------|
| Yeni proje inşaatı başlasın mı | Mimar L1 + Overmind L2 |
| Konuşma roadmap önceliği | PDC (Mavi Okyanus sadece önerir) |
| Finansal model resmi rakam | Growth `YEAR*_` belgeleri |
| Kullanıcı dili / öbek | LIUD |

## Sıklık

- Talep üzerine (Mimar sorar)
- Çeyrek: `project_index.json` gözden geçirme
