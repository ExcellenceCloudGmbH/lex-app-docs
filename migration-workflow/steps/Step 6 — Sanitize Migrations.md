---
title: "Step 6 — Sanitize Migrations"
---

# Step 6 — Sanitize Generated Migrations

[[Home]] / [[Migration Workflow Overview]] / Step 6

---

> [!note]
> This step is **optional** — disabled by default. Enable with `--enable-sanitization`.

## What Happens

```bash
python lex/sanitize_v2_migrations.py --migrations-dir <dir> \
  --manifest .lex_legacy_freeze_manifest.pre_migrate.json \
  --app-name <app> --only-files <new_files>
```

Removes destructive operations (`DROP TABLE`, etc.) from newly generated migrations that would affect **frozen legacy tables**.

Only **newly generated files** from Step 5 are sanitized — historical migrations are never touched.

---

## Why Default Is Off

Sanitization **modifies generated migration files**. Teams with strict review processes may prefer explicit human review instead.

---

## Success Criteria

| Scenario | Expected |
|---|---|
| Sanitization **enabled** | Sanitized files exist; destructive ops removed |
| Sanitization **disabled** *(default)* | No rewrite; logs show "skipped" |

---

*Previous: [[Step 5 — Run makemigrations]] · Next: [[Step 7 — Apply Migrations]]*
