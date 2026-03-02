---
title: "Step 9 — Backfill History"
---

# Step 9 — Backfill Bitemporal History

[[Home]] / [[Migration Workflow Overview]] / Step 9

---

## What Happens

Three sub-steps run in sequence:

### 9.1 — Normalize `is_calculated` Values
```bash
lex normalize_is_calculated --chunk-size <N>
```
Converts legacy boolean `is_calculated` values → canonical `SUCCESS` / `ERROR` strings.

### 9.2 — Backfill Bitemporal History
```bash
lex backfill_bitemporal_history --chunk-size <N> \
  --reason "V1 migration snapshot" [--timestamp <ISO8601>]
```
Seeds V2 bitemporal (Level 1 + Level 2) history rows for all eligible models.

### 9.3 — Backfill Audit Logging
```bash
lex backfill_audit_logging --chunk-size <N> \
  --reason "V1 audit log migration snapshot"
```
Seeds audit log rows from legacy archive tables. Skippable with `--skip-auditlog-backfill`.

---

## Why ORM/Signal Path Is Mandatory

> [!important]
> **Never backfill history via raw SQL.** Direct SQL insertion bypasses tested invariants, chaining logic, and synchronization hooks.

ORM + signal execution ensures records are produced using the **same rules** that govern normal runtime changes.

---

## Key Properties

| Property | Detail |
|---|---|
| **Idempotent** | Models with existing history rows are skipped |
| **Chunked** | Configurable batch size (default: 500) |
| **Dry run** | `--dry-run-backfill` runs without writing |

---

## Success Criteria

- [ ] Eligible models receive baseline history and meta-history records
- [ ] Re-running skips already-seeded models ✅
- [ ] Audit log backfill shows expected counts (or was intentionally skipped)

---

*Previous: [[Step 8 — Final Freeze Manifest]]*
*See also: [[Verification Checklist]] | [[Migration Workflow Overview]]*
