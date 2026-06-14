# Linguistic Intelligence & User Demand (LIUD)

**Türkçe:** Kullanıcı Dil Analizi ve Talep İstihbarat Departmanı

Konuşma terapisi alanında **kullanıcı dili veri istihbaratının** merkezi. Keyword listesi değil — gerçek problem, gerçek dil, gerçek çözüm beklentisi.

---

## Belgeler

| Dosya | Açıklama |
|-------|----------|
| [DEPARTMENT_CHARTER.md](DEPARTMENT_CHARTER.md) | Departman charter — 10 görev |
| [INTER_DEPARTMENT_PROTOCOL.md](INTER_DEPARTMENT_PROTOCOL.md) | Departmanlar arası iletişim |
| [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md) | Rapor şablonu |
| [output_catalog.json](output_catalog.json) | JSON çıktı katalogu |
| [exercise_scope_targets.json](exercise_scope_targets.json) | Modül minimum hedefleri |

---

## Raporlar

| Rapor | Açıklama |
|-------|----------|
| [reports/LIUD_REPORT_*.md](reports/) | Dönemsel birleşik rapor + INTER-DEPARTMENT FINDINGS |

---

## JSON çıktıları (`output/`)

| Dosya | İçerik |
|-------|--------|
| `keywords.json` | Trends + long-tail keşif |
| `expert_vs_user_language.json` | Uzman ↔ kullanıcı dili |
| `intent_map.json` | Birleşik niyet haritası |
| `jtbd.json` | Jobs To Be Done |
| `content_gaps.json` | İçerik/özellik/AI boşlukları |
| `exercise_scope_audit.json` | İçerik dayanıklılığı |
| `training_words.json` / `training_sentences.json` | Envanter hedef vs mevcut |
| `emotion_map.json` | Duygusal ifadeler |
| `*_questions.json` | Modül soru havuzları |
| `roadmap_priorities.json` | Acil → düşük öncelik |

---

## İlişkili kaynaklar

| Departman | Klasör |
|-----------|--------|
| Google Trends | [../trends/](../trends/) |
| Market Intelligence | [../market/](../market/) |
| Clinical Evidence | [../clinical/](../clinical/) |
| Growth ajanı | `.cursor/rules/17-marketing-growth.mdc` |
| LIUD ajanı | `.cursor/rules/07-linguistic-intelligence.mdc` |

---

## Çalıştırma

```bash
./scripts/linguistic/run_linguistic_intelligence.sh
```

Tekil:
```bash
python scripts/linguistic/build_output_json.py
python scripts/linguistic/generate_liud_report.py
```

**Downstream:** [CIKA — Curriculum Intelligence](../../curriculum/README.md) tüketir → `curriculum/*.json` → [PDC](../product_decision/README.md)

---

## Kritik kural

> Asla uzman bakış açısıyla çalışma.  
> Kullanıcı ne arıyor? Ne hissediyor? Ne söylemeye çalışıyor?
