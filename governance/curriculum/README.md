# Curriculum Intelligence (CIKA)

**Agent:** `.cursor/rules/08-curriculum-intelligence.mdc`  
**Charter:** [DEPARTMENT_CHARTER.md](DEPARTMENT_CHARTER.md)

Talep kanıtını eğitim mimarisine dönüştürür. UI/kod/pazarlama yönetmez.

---

## JSON çıktılar

Tüm çıktılar: [`/curriculum/`](../curriculum/)

---

## İlişkili departmanlar

| Departman | Rol |
|-----------|-----|
| [LIUD](../linguistic/) | Kullanıcı dili, JTBD, gap — birincil girdi |
| [Market Intelligence](../market/) | Rakip, forum, monetizasyon |
| [Clinical Evidence](../clinical/) | Clinical score, veto |
| Growth | Kanal — CIKA içerik derinliği |
| [PDC](../product_decision/) | CIKA çıktısı → ürün kararı (en üst mercii) |

---

## Çalıştırma

```bash
./scripts/curriculum/run_curriculum_intelligence.sh
```

**Önerilen sıra:** LIUD → CIKA → **PDC**

```bash
./scripts/linguistic/run_linguistic_intelligence.sh
./scripts/curriculum/run_curriculum_intelligence.sh
./scripts/product_decision/run_product_decision_council.sh
```
