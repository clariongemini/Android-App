# Memory Engine — Sorgulanabilir Kurumsal Hafıza

**Soru:** Bu hata daha önce çözüldü mü?

Governance `memory/*.json` karar kaydı tutar; Factory Memory **arama ve ders çıkarma** katmanıdır.

## Dosyalar (runtime)

| Dosya | İçerik |
|-------|--------|
| `failures.json` | FAIL-* kayıtları |
| `successes.json` | WIN-* kayıtları |
| `lessons.json` | LESSON-* özetleri |
| `adr_index.json` | ADR-* mimari karar indeksi |

## Failure kaydı şeması

```json
{
  "id": "FAIL-2026-014",
  "title": "Compose Navigation Loop",
  "tags": ["navigation", "compose", "backstack"],
  "cause": "Wrong backstack restore on process death",
  "resolution": "SavedStateHandle + singleTop launch mode",
  "affected_modules": ["feature:home"],
  "recorded_at": "2026-06-14T10:00:00Z",
  "proof_ref": "commit:abc123"
}
```

## Sorgu

```bash
./scripts/factory/query-memory.sh "navigation"
./scripts/factory/query-memory.sh --id FAIL-2026-014
python3 scripts/factory/record-memory.py --type failure --title "..." --tags navigation
```

**Sahip:** CDID + CAO · **L1:** CEO
