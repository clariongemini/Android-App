# Factory Upgrade Strategy — BACKLOG (Not Implemented)

**Status:** BACKLOG · **Mode:** MAINTENANCE · **Do not implement until production evidence exists**

---

## Why this document exists

The factory has evolved through multiple versions (v2 → v3 → v4). Future projects will be created at different factory versions. Eventually the question will arise:

> *How do I upgrade an existing app from Factory v3.1 to v4.x?*

That problem is **real** but **not urgent**. There is not yet a single production app built and validated on v3.1 with outcome data.

Implementing migration tooling now would be **over-engineering** before **production evidence**.

---

## Trigger conditions (when to implement)

Start `migrate-project.sh` design only when **all** are true:

| # | Condition |
|---|-----------|
| 1 | At least **1 app** shipped from factory v3.x with recorded outcomes |
| 2 | A **breaking factory release** (e.g. v4 → v5) with documented delta |
| 3 | At least **1 app** stuck on an older factory version in the wild |
| 4 | Manual `sync-standards.sh` upgrade caused measurable pain (conflicts, regressions) |

Until then: **`sync-standards.sh` + manual merge** is the supported path.

---

## Planned surface (future — not built)

```
./scripts/migrate-project.sh --from 3.1 --to 4.0 /path/to/app
```

Expected outputs (design only):

- Version compatibility report
- Files to merge vs overwrite
- Governance/runtime migration steps
- Rollback checkpoint

Related future doc: **Factory Compatibility Matrix** (app slug × factory version × last sync date) — also backlog until portfolio has 2+ apps on different versions.

---

## Current supported upgrade path

```bash
# Refresh standards from factory template repo
/path/to/Android-App/scripts/sync-standards.sh /path/to/your-app
cd /path/to/your-app && ./scripts/governance/init-governance.sh  # if governance schema changed
```

See: [`docs/BOOTSTRAP.md`](BOOTSTRAP.md) · [`governance/FACTORY_REPO_POLICY.md`](../governance/FACTORY_REPO_POLICY.md)

---

## Policy

| Now (MAINTENANCE) | Later (post-validation) |
|-------------------|-------------------------|
| Document only | Implement migration engine |
| Bugfix `sync-standards.sh` | Compatibility matrix |
| No V5 | `migrate-project.sh` scaffold |

**North star:** [`FACTORY_MISSION.md`](../FACTORY_MISSION.md) · **Freeze:** [`FACTORY_FREEZE.md`](FACTORY_FREEZE.md)
