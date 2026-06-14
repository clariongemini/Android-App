# Factory V3 — AI-Native Software Company OS

**Sürüm hedefi:** `3.1.0-intelligence-operational`  
**Durum:** V3 Skeleton ✅ · V3.1 Operational hooks ✅  
**Sonraki (V4):** Factory Productization — portfolio registry + gerçek app verisi. **Intelligence frozen.**

> ⚠️ V3.2+ yok. Risk/Forecast/Strategy Engine eklenmez. Detay: [`FACTORY_V4_PRODUCTIZATION.md`](FACTORY_V4_PRODUCTIZATION.md)

---

## İlke: Governance karar verir · Factory öğrenir

| | Governance | Factory |
|---|------------|---------|
| **Soru** | Ne yapacağız? Onaylandı mı? | Ne öğrendik? Kanıtlandı mı? |
| **Konum** | `governance/` | `factory/` |
| **Runtime** | Sprint lock, roadmap, CEO cycle | memory, proof, revenue, benchmark |

**Durdur listesi (V3):**

- Yeni ajan ekleme — AGENTS.md **16 ajan freeze**
- Yeni council ekleme — CEO/CAO/PDC/CEC/CDID/AID/EGC yeterli
- 33 katmanı büyütme — 33 sabit

---

## V3 Motor Önceliği

### 1. Proof Engine (P0)

`COMPLETED` → `PROVEN` — commit + apk + analytics minimum.

```bash
python3 scripts/factory/record-proof.py -f F002 -t commit -v $(git rev-parse --short HEAD)
python3 scripts/factory/record-proof.py --status
```

### 2. Memory Engine

Sorgulanabilir hafıza — governance/memory kayıt tutar, factory/memory **arar**.

```bash
./scripts/factory/query-memory.sh "navigation"
python3 scripts/factory/record-memory.py --type failure --title "Compose Navigation Loop" --tags navigation
```

### 3. Decision Accuracy

PDC beklenen vs gerçek — `pdc_accuracy_pct`.

```bash
python3 scripts/factory/record-decision.py -f F002 --expected-retention 8
python3 scripts/factory/record-decision.py -f F002 --actual-retention 3 --review
python3 scripts/factory/compute-decision-accuracy.py
```

### 4. Revenue Reality (AID)

Money Reality — MRR, ARPU, trial conversion, churn.

```bash
python3 scripts/factory/build-revenue-snapshot.py --manual-mrr 2400
./scripts/analytics/run_aid_cycle.sh   # revenue_snapshot sync
```

### 5. Benchmark (3 katman)

| Katman | Dosya |
|--------|--------|
| Factory | `factory/runtime/benchmark/factory.json` |
| Product | `factory/runtime/benchmark/product.json` |
| Market | `factory/runtime/benchmark/market.json` |

```bash
python3 scripts/factory/build-benchmark.py
```

---

## Orkestrasyon

```bash
./scripts/factory/init-intelligence.sh       # İlk seed
./scripts/factory/run-intelligence-cycle.sh  # Tüm motorlar
./scripts/factory/validate-intelligence.sh   # Canonical yapı
```

`init-governance.sh` otomatik olarak `init-intelligence.sh` çağırır.

---

## Runtime vs Canonical

| Git (canonical) | Runtime (gitignore) |
|-----------------|---------------------|
| `factory/*/README.md` | `factory/runtime/**` |
| `templates/factory/*.template.json` | `docs/AUDIT_REPORT.md` |
| `scripts/factory/*` | `governance/**/*.json` (proje) |

Politika: [`governance/FACTORY_REPO_POLICY.md`](../governance/FACTORY_REPO_POLICY.md)

---

## Entegrasyon (yeni ajan yok)

| Motor | Mevcut sahip |
|-------|--------------|
| Proof | CDID → CEC |
| Memory | CDID + CAO |
| Decision Accuracy | PDC → EGC |
| Revenue | AID |
| Benchmark | Growth + EGC |

---

## V3.1 — Operational Complete (hedef)

### Learning loop (kapalı döngü)

```
WP Closed → Proof Required → Feature PROVEN
     ↓
Product Reality → Application Revenue → Decision Accuracy (90g)
     ↓
Benchmark (velocity) → Yeni PDC Kararı
```

```bash
./scripts/factory/run-learning-loop.sh   # Tam operasyonel döngü
```

### Proof ↔ CDID

CDID cycle sonunda otomatik: `wp-proof-gate.py --sync-cdid`  
WP kapanınca: `python3 scripts/factory/wp-proof-gate.py --close-wp WP-25 -f F002`

### Memory graph

```bash
./scripts/factory/query-memory.sh "room migration" --graph
python3 scripts/factory/record-memory.py --type lesson --title "..." --related FAIL-2026-004,ADR-2026-008
```

### Decision 90-day rule

`enforce-decision-reviews.py` — review_due geçmiş kararlar `OVERDUE_REVIEW` → loop exit 1

### Application Revenue (NOT factory revenue)

```json
{ "scope": "application", "app": "{{APP_NAME}}", "mrr": 0 }
```

### Velocity benchmark

`runtime/factory/benchmark/velocity.json` — `idea_to_release_days` vs `industry_average_days: 64`

### Runtime consolidation (V3.1)

```
runtime/
├── governance/
├── factory/
├── analytics/
└── telemetry/
```

Init: `./scripts/runtime/init-runtime.sh`
