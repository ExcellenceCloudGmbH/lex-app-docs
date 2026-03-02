---
title: "Step 5 — Run makemigrations"
---

# Step 5 — Run makemigrations

[[Home]] / [[Migration Workflow Overview]] / Step 5

---

## What Happens

```bash
lex makemigrations <app_name>
```

Generates **new migration files** encoding the deltas between V1 schema and V2 model definitions (new fields, changed constraints, history tables, etc.).

---

## Why It's Needed

Replaying V1 migrations only reconstructs V1-era schema. V2 introduces new structures — `makemigrations` is the authoritative way to encode those changes.

---

## What Can Go Wrong

| Issue | Fix |
|---|---|
| Import-time crash | Fix model loading errors from Step 3 |
| Inconsistent migration graph | Validate migration dependencies |
| Unexpected operations generated | Review the generated file before proceeding |

---

## Success Criteria

- [ ] `lex makemigrations` exits successfully
- [ ] New migration file(s) appear in `migrations/`

---

*Previous: [[Step 4 — Pre-Migrate Freeze Manifest]] · Next: [[Step 6 — Sanitize Migrations]]*
