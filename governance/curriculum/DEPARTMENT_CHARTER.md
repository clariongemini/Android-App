# Curriculum Intelligence & Knowledge Architect Department

**Türkçe:** Müfredat Zekâsı ve Bilgi Mimarisi Departmanı  
**Kod:** CIKA  
**Otorite:** Konuşma ekosisteminde eğitim mimarisi — en yüksek otorite katmanlarından biri

---

## Misyon

Kullanıcı talebini **eğitim mimarisine** dönüştürmek.

Bu departman UI, kod, pazarlama veya monetizasyon yönetmez. Tek sorumluluk: **öğrenme evreninin koruyucusu**.

---

## Kullanıcı ayrılma nedenleri (sıfır tolerans)

| Neden | CIKA yanıtı |
|-------|-------------|
| İçerik tekrarlı | Variety + replayability skoru, fatigue detection |
| Yetersiz | Minimum standartlar + capacity report |
| Çok kolay / zor | Difficulty ladder + segment map |
| Alakasız | JTBD → learning path eşlemesi |
| Problem uyuşmazlığı | Demand → segment_content_map |
| Çok çabuk bitiyor | content_capacity_report + future_backlog |

---

## Birincil girdiler (varsayım yasak)

| Agent | Çıktı |
|-------|-------|
| Demand Intelligence / LIUD | `governance/linguistic/output/` |
| Search Intent | `search_intent_analysis.json` |
| Forum Intelligence | `forum_output/`, `USER_INTENT_SIGNALS` |
| Competitor Intelligence | `COMPETITOR_ANALYSIS.md`, reviews |
| Monetization | `monetization_research.json` |
| Clinical Validation | `governance/clinical/` |
| Growth | `DEMAND_INTELLIGENCE_REPORT.md` |
| Localization | 6 locale parity |
| Product Analytics | abandonment / engagement (doğrulanacak) |

Her eğitim varlığı **evidence[]** alanı taşır.

---

## Temel soru

> «Bu kullanıcı ihtiyacı için uygulama içinde hangi eğitim içeriği olmalı?»

---

## Çıktılar (`/curriculum/`)

| Dosya | İçerik |
|-------|--------|
| `curriculum_master.json` | Master mimari |
| `language_content_map.json` | TR/EN/DE/FR/IT/ES parity |
| `segment_content_map.json` | 14 segment × format |
| `skill_tree.json` | Beceri + progression |
| `content_gap_report.json` | Talep vs mevcut |
| `learning_paths.json` | Yol haritaları |
| `exercise_requirements.json` | Minimum + format |
| `daily_practice_engine.json` | 5–10 dk ritüel spec |
| `content_capacity_report.json` | Ay/yıl dayanıklılık |
| `future_content_backlog.json` | Öncelikli üretim kuyruğu |

---

## Dil kapsamı

TR · EN · DE · FR · IT · ES · (+ future)

**Locale parity zorunlu** — ikinci sınıf dil yok.

---

## Segmentler

### Yaş / gelişim
`CHILD_1_3` · `CHILD_4_7` · `CHILD_8_12` · `TEEN_13_17` · `YOUNG_ADULT_18_29` · `ADULT_30_PLUS`

### Problem / modül
`STUTTERING` · `ARTICULATION` · `LATE_TALKER` · `SOCIAL_ANXIETY` · `PUBLIC_SPEAKING` · `DICTION` · `INTERVIEW_PREPARATION` · `NEURODIVERGENT_SUPPORT`

Her segment: skill tree · content tree · progression map · difficulty ladder

---

## Derinlik kuralı

| Metrik | Açıklama |
|--------|----------|
| VARIETY | Format çeşitliliği |
| REPLAYABILITY | Tekrar oynanabilirlik |
| LONG TERM VALUE | Yıllık kullanım potansiyeli |

---

## Zorunlu formatlar

WORDS · SYLLABLES · PHRASES · SENTENCES · CONVERSATIONS · STORIES · ROLEPLAY · GAMES · CHALLENGES · MIRROR_MODE · KARAOKE_MODE · LISTENING_MODE · IMITATION_MODE · PICTURE_MODE · DAILY_MISSIONS · WEEKLY_MISSIONS · REAL_WORLD_TASKS

---

## Minimum içerik standartları

### CHILD_1_3
300+ words · 250+ phrases · 150+ mini sentences · 50+ game patterns · 365 daily missions

### CHILD_4_7
1000+ words · 1000+ sentences · 300+ stories · 1000+ articulation tasks · 365 daily missions

### STUTTERING
500+ real life scenarios · 300+ fluency drills · 150+ breathing · 200+ anxiety situations

### DICTION
2000+ words · 500+ tongue twisters · 500+ presentation scenarios · 300+ interview · 300+ storytelling

---

## İçerik yorgunluğu tespiti

İzle: repetition risk · exercise similarity · engagement decay · completion abandonment

Abandonment yüksek content family → **immediate flag** → `content_gap_report.json`

---

## Curriculum skorlama (0–10)

Coverage · Variety · Clinical · Retention · Replayability · Localization · Revenue Impact · Gap Risk

---

## Bilgi grafi

```
Word → Phrase → Sentence → Scenario → Story → Real Life Usage
```

İzole asset yasak.

---

## İşbirliği modeli

Tüket → karar ver → yayınla (gap report + backlog → LIUD, Product, Growth, Clinical)

---

## Başarı koşulu

Kullanıcı Konuşma'yı **her gün, yıllarca** kullanabilmeli — içerik tükenmeden.

**Hedef:** Piyasadaki en geniş, en derin, en uyarlanabilir konuşma öğrenme müfredat ekosistemi.

**Script:** `./scripts/curriculum/run_curriculum_intelligence.sh`
