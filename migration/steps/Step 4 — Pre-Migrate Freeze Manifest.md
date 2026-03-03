---
title: "Step 4 — Pre-Migrate Freeze Manifest"
---
# Step 4 — Generate Pre-Migrate Freeze Manifest


> [!note]
> This step is **optional** — it only runs when `--enable-sanitization` is passed. Skipped by default.

## What Happens

```bash
lex generate_legacy_freeze_manifest \
  --before .lex_tables_before.json \
  --output .lex_legacy_freeze_manifest.pre_migrate.json
```

Captures the freeze set **before** migration operations that might alter table structure. Used by [[Step 6 — Sanitize Migrations|Step 6]] to protect V1-only tables.

## Success Criteria

| Scenario | Expected |
|---|---|
| Sanitization **enabled** | Pre-manifest exists and is valid JSON |
| Sanitization **disabled** *(default)* | Logs say "skipped" |

*Previous: [[Step 3 — Rewrite Migrations]] · Next: [[Step 5 — Run makemigrations]]*
