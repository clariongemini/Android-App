# Fabrika Repo — Governance Politikası

Bu belge **Ulas Autonomous Android APP Factory** reposunda hangi governance dosyalarının git'te kalması gerektiğini tanımlar.

## İlke

| Tür | Git'te | Açıklama |
|-----|--------|----------|
| **Charter & protokol** | ✅ | `DEPARTMENT_CHARTER.md`, `README.md`, executive MD |
| **Şablon kurallar** | ✅ | `dependency-rules.json` (generic package placeholder) |
| **Governance templates** | ✅ | `templates/governance/*.template.*` |
| **Runtime JSON/MD** | ❌ | Sprint lock, approval queue, CEO cycle çıktıları |
| **Proje belgeleri** | ❌ | PRODUCT_BRIEF, MODULE_MAP (init-new-app üretir) |

## Runtime dosyalar (gitignore)

`init-governance.sh` veya CEO/CAO döngüleri tarafından üretilir; **fabrika reposuna commit edilmez**:

- `governance/executive/SPRINT_LOCK.json`
- `governance/executive/APPROVAL_QUEUE.md`
- `governance/project.config.json`
- `governance/product_decision/roadmap_priorities.json`
- `governance/reality/*.json` (PRODUCT_REALITY_SCORE hariç charter MD'ler kalır)
- `governance/execution/*.json`
- `governance/cao/*.json`
- `governance/egc/*.json`
- `governance/analytics/output/`
- `governance/memory/*.json`

## Charter-only departmanlar (cursor rule yok)

Bu departmanların charter'ı vardır; fabrika ajan kuralları başka ajanlar üzerinden tüketilir:

| Departman | Charter | Tüketen ajan |
|-----------|---------|--------------|
| Finance | `governance/finance/DEPARTMENT_CHARTER.md` | CPO, PDC, EGC |
| Localization | `governance/localization/DEPARTMENT_CHARTER.md` | LIUD, Android |
| Clinical | `governance/clinical/DEPARTMENT_CHARTER.md` | CIKA, CPO |
| Trends | `governance/trends/DEPARTMENT_CHARTER.md` | Growth, LIUD |
| CSGB | `governance/csgb/DEPARTMENT_CHARTER.md` | CEO charter (rule 11) |

Growth için cursor rule: `17-marketing-growth.mdc`

## Doğrulama

```bash
bash scripts/governance/validate-factory-governance.sh
python3 scripts/governance/validate-audit-chain.py   # proje init sonrası
```

## Uygulama projesinde

```bash
./scripts/sync-standards.sh /path/to/app
cd /path/to/app && ./scripts/init-governance.sh
```

Runtime dosyalar hedef projede oluşur; fabrika seed snapshot'ı taşınmaz.
