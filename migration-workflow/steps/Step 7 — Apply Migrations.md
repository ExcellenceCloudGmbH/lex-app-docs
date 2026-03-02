---
title: "Step 7 — Apply Migrations"
---

# Step 7 — Apply Migrations

[[Home]] / [[Migration Workflow Overview]] / Step 7

---

## What Happens

```bash
lex migrate
```

Applies **all pending migrations** across all installed apps in dependency order.

> [!caution]
> **This is the irreversible schema boundary.** All prior steps are preparation. Once this runs, schema changes are written to the database.

---

## Why Full Migrate

Running `lex migrate` (without specifying an app) resolves the migration graph **globally** — catching cross-app dependencies that app-specific migrate commands would miss.

---

## What Can Go Wrong

| Issue | Fix |
|---|---|
| Constraint conflicts | Existing data violates new constraints |
| Dependency ordering | Malformed migration `dependencies` |
| Import errors | Model classes fail to load during execution |

> [!warning]
> If migration fails mid-run, **investigate before retrying**. Partial schema changes can leave the DB inconsistent.

---

## Rollback Safety

If `--rollback-on-failure` was set, the workflow automatically restores migration state:

```bash
lex rollback_migration_state --input .lex_migration_state_before.json
```

---

## Success Criteria

- [ ] `lex migrate` exits with code `0`
- [ ] `django_migrations` table reflects expected revisions
- [ ] Application starts without errors

---

*Previous: [[Step 6 — Sanitize Migrations]] · Next: [[Step 8 — Final Freeze Manifest]]*
