---
title: "Step 1 — Capture DB Tables"
---
# Step 1 — Capture Pre-Migration DB Tables


## What Happens

```bash
lex capture_db_tables --output .lex_tables_before.json
```

This snapshots the **physical table list** from your database before any schema changes.

> [!important]
> This is a real DB-level snapshot — not inferred from model definitions.

## Why It's Needed

V2 code can't reliably identify all V1-era tables because some may have no model definitions, may have been renamed, or were dynamically created by old modules. Without this snapshot, the freeze manifest (Steps 4/8) becomes guesswork.

## What Can Go Wrong

| Issue | Fix |
|---|---|
| Wrong DB connection | Check `DB_NAME` env var |
| Permissions error | Verify DB user can read `INFORMATION_SCHEMA` |
| Empty output | Confirm you're connecting to the right database |

> [!caution]
> If this command fails, **stop**. Do not continue the migration.

## Success Criteria

- [ ] `.lex_tables_before.json` exists and is valid JSON
- [ ] Table list is non-empty and matches expected project size

*Next: [[Step 2 — Prepare Migration Files]]*
