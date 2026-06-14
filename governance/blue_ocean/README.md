# Mavi Okyanus — Portföy Proje Değerlendirmeleri

**Departman:** Mavi Okyanus  
**Ajan:** `.cursor/rules/10-mavi-okyanus.mdc`

---

## Ne yapar?

Yeni uygulama fikirlerini **yapmaya değer mi** sorusuyla değerlendirir. Çıktı: tek Markdown rapor.

| Belge | Açıklama |
|-------|----------|
| [DEPARTMENT_CHARTER.md](DEPARTMENT_CHARTER.md) | Misyon, yetki, handoff |
| [ANALYSIS_ALGORITHM.md](ANALYSIS_ALGORITHM.md) | Geçitler, skor, abone bandı |
| [APP_TYPE_PROFILES.md](APP_TYPE_PROFILES.md) | Uygulama türüne göre derinlik |
| [PROJECT_EVAL_TEMPLATE.md](PROJECT_EVAL_TEMPLATE.md) | Rapor şablonu |
| [DISCOVERY_SYSTEM.md](DISCOVERY_SYSTEM.md) | Fikirsiz keşif radarı (Play Store) |
| [discovery/](discovery/) | `WEEKLY_CANDIDATES.md`, `candidates.json`, ham tarama |
| [projects/](projects/) | `{slug}.md` değerlendirme dosyaları |
| [project_index.json](project_index.json) | Katalog |

---

## Nasıl kullanılır?

**Sohbet (Mimar):**

```text
@mavi-okyanus [Proje adı]: [fikir özeti]. Tür: education_skill. Değerlendir.
```

**Script (iskelet):**

```bash
./scripts/blue_ocean/run_blue_ocean_eval.sh --project "Proje Adı" --type hobby_niche_tool
./scripts/blue_ocean/run_blue_ocean_discovery.sh   # fikirsiz haftalık tarama
```

---

## Kapsam

- **Genel:** Sağlık, eğitim, verimlilik, finans, hobby, B2B…
- **İhtiyaç türleri:** Sadece acı değil — verimlilik, statü, tasarruf, alışkanlık
- **Portföy:** Konuşma = #1; bu departman #2–#5 ve sonrası

---

## İlişkili departmanlar

| Departman | İlişki |
|-----------|--------|
| Growth | Rakip scrape, finans modelleri |
| LIUD | Kullanıcı dili (sağlık/eğitim nişi) |
| PDC | YAP kararı → roadmap önerisi |
| CPO | Konumlandırma |

---

## Flagship

`projects/konusma.md` — Konuşma referans değerlendirmesi (isteğe bağlı; tamamlandıkça güncellenir).
