# Google Trends Araştırması

Konuşma rahatsızlığı, terapi ve performans kaygısı ile ilgili **7 dil × 4 yaş segmenti** arama analizi.

**Sahip departman:** [LIUD — Linguistic Intelligence](../linguistic/README.md) (Katman 1: Trends keşfi)

| Dosya | Açıklama |
|-------|----------|
| [SCAN_STATUS.md](SCAN_STATUS.md) | **Tarama durumu** — tamamlanma oranı + özet tablolar |
| [GOOGLE_TRENDS_BY_LANGUAGE.md](GOOGLE_TRENDS_BY_LANGUAGE.md) | Ana rapor — RSV seviyeleri, dil/yaş tabloları, yorumlar |
| [queries.json](queries.json) | Tüm arama terimleri (TR, US, GB, DE, FR, IT, ES) |
| [trends_data.json](trends_data.json) | Ham RSV çıktısı (pytrends) |
| [TERM_DISCOVERY_REPORT.md](TERM_DISCOVERY_REPORT.md) | **Terim keşfi** — yanlış kelime uyarıları, yol haritası öncelikleri |
| [discovery_candidates.json](discovery_candidates.json) | Alternatif + seed terim listeleri |
| [discover_and_fetch.py](discover_and_fetch.py) | Yavaş keşif + tam veri çekimi (önerilen) |
| [run_slow_fetch.sh](run_slow_fetch.sh) | Rate-limit güvenli arka plan çekimi |
| [fetch_trends.py](fetch_trends.py) | Basit veri çekici (legacy) |

**Kaynak:** [Google Trends](https://trends.google.com/trends/?hl=tr)

**Diller:** Türkçe, İngilizce (US + UK), Almanca, Fransızca, İtalyanca, İspanyolca (7 locale).

**Yaş segmentleri:** Çocuk (0–12), Ergen (13–17), Genç (18–29), Yetişkin (30+).
