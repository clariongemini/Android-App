# Hiyerarşik Denetim Zinciri — Her Departmanın Üst Denetimi

**Sürüm:** 1.0  
**Kapsam:** Tüm Factory projeleri — tek ajan onayı yasak  
**Protokol eki:** `AGENT_APPROVAL_PROTOCOL.md` v3.0

---

## İlke

> **Hiçbir departman kendi işini nihai doğru ilan edemez.**  
> **Hiçbir denetçi kendi denetimini nihai doğru ilan edemez.**

Her çıktı en az **3 katman** geçer:

1. **Uygulayan ajan** (üretir → `review`)
2. **Üst departman** (L1 — teknik/domain doğrulama)
3. **Denetim kolu** (L2 — CAO veya vekili)
4. **CEO** (L3 — sprint lock + reality uyumu)
5. **EGC** (L4 — şirket sağlığı — periyodik)

Overmind + Mimar = nihai insan kapısı (L5).

---

## Organizasyon ağacı (Denetim yönü ↑)

```
Mimar (Ulaş) — nihai onay
    ↑
Overmind (.cursorrules) — L2 kapı + koordinasyon
    ↑
EGC — CEO performansı, strategic debt, company health
    ↑
CSGB — CEO stratejik denetimi
    ↑
CEO — sprint lock, reality, tüm kol denetimi
    ↑
┌──────────┬──────────┬──────────┬──────────────────────────┐
│ CAO      │ PDC      │ CEC      │ Intelligence Division     │
│ (denetim │ (karar   │ (exec    │ LIUD·CIKA·AID·LID·FID·   │
│  kalitesi)│  kalitesi)│  hizası) │ Market·Trends·BlueOcean  │
└──────────┴──────────┴──────────┴──────────────────────────┘
    ↑              ↑              ↑              ↑
Factory Division: CPO → Architect → Android → Security → OEM
    ↑
MCP Orkestratör (araç hazırlığı — Baş Mimar denetir)
```

---

## Departman → Üst Denetim eşlemesi

| Departman / Ajan | Üretir | L1 (üst departman) | L2 (denetim) | L3 (CEO) |
|------------------|--------|--------------------|--------------|----------|
| **CPO** (01) | Vizyon, pazar, monetizasyon | **PDC** — roadmap uyumu | **CAO** — kanıt kalitesi | Sprint lock |
| **Architect** (02) | Mimari, modül haritası | **CEC** — teslimat hizası | **CAO** — borç/ihlal | Reality |
| **Android** (03) | UI/kod | **Architect** — mimari | **CPO** — ürün uyumu | Sprint |
| **Security** (04) | Güvenlik, QA | **Architect** — teknik | **CAO** — audit integrity | Release gate |
| **OEM** (05) | ROM uyumu | **Android** — UX/teknik | **Security** — risk | Release gate |
| **MCP** (06) | MCP kurulum | **Architect** | **Security** | — |
| **LIUD** (07) | Talep istihbaratı | **PDC** — karar tüketimi | **CAO** — evidence | CEO cycle |
| **CIKA** (08) | Müfredat | **PDC** + **LIUD** girdi | **CAO** | CEO cycle |
| **PDC** (09) | Roadmap | **CAO** — kanıt | **CEO** | EGC |
| **Mavi Okyanus** (10) | Fikir keşfi | **PDC** — öneri only | **CAO** | — |
| **Growth** (17) | GTM, ASO | **CPO** | **CAO** | — |
| **AID** (16) | Analytics, ölçüm | **CAO** — measurement integrity | **CEO** — live data | Sprint P0 |
| **CEC** (13) | Execution alignment | **CEO** | **CSGB** | EGC |
| **CDID** (15) | WP engine | **CEC** | **CAO** | CEO |
| **CAO** (12) | Denetim raporları | **CEO** | **EGC** | CSGB |
| **CEO** (11) | Orchestration | **CSGB** | **EGC** | — |

---

## CAO’nun özel görevi: Denetçileri denetlemek

CAO yalnızca çıktı saymaz. Her departman için:

| Boyut | Soru |
|-------|------|
| **Input Sources** | Beklenen girdiler mevcut mu? |
| **Output Files** | Charter’daki dosyalar var mı? |
| **Evidence Count** | Kanıt referansı yeterli mi? |
| **Freshness** | Son üretim ne kadar eski? |
| **Audit Quality** | Üst departman L1 gerçekten yaptı mı? |
| **Cross-Department** | Çelişen rapor var mı? |

CAO `department_scoreboard.json` → CEO Master Report girdisi.

CEO sorar: **«Hangi departman doğru çalışıyor? Hangi denetim eksik?»**

---

## Zorunlu WP akışı (çok katmanlı)

```
1. Talep → APPROVAL_QUEUE.md (feature_id zorunlu)
2. PDC check → roadmap + rejected_features
3. Uygulama ajanı → review
4. L1 → Üst departman (tablo) → approved_l1
5. L2 → CAO veya vekili (Security/OEM/PDC) → approved_l2
6. CEC gate → alignment ≥ 80
7. CEO sprint lock check → P0 uyumu
8. agent-approval-gate.sh → completed
```

**Tek ajan onayı ile `completed` yasak.**

---

## Doğrulama scriptleri

```bash
python3 scripts/cao/run_cao_audit.py              # Departman skor kartı
python3 scripts/execution/run_cec_audit.py        # Execution alignment
python3 scripts/governance/validate-audit-chain.py # L1/L2 eşleme
python3 scripts/execution/validate_roadmap_consumption.py
./scripts/agent-approval-gate.sh WP-XX
```

---

## CEO döngüsünde denetim sırası

1. Intelligence üretir (LIUD → CIKA → …)
2. **PDC** karar verir
3. **CAO** tüm intelligence + PDC denetler
4. **CDID** WP üretir
5. **CEC** execution hizası ölçer
6. **CEO** sprint lock + reality
7. **EGC** company health + CEO performance

Denetim atlanamaz.
