---
title: "Step 3 — Rewrite Migrations"
---
# Step 3 — Rewrite V1 Migrations for V2 Compatibility


## What Happens

```bash
python lex/fix_v1_migration.py <migrations_dir>
```

Rewrites **import paths** and references from V1 conventions to V2-valid module targets.

## Why It's Needed

Raw V1 migrations reference modules that don't exist in V2. Without rewriting, migration execution fails on import errors before any schema logic runs.

## What Can Go Wrong

| Issue | Fix |
|---|---|
| Unresolved import patterns | Review rewrite summary output |
| Partial rewrites | Do not continue — fix before proceeding |
| Syntax breakage | Manually verify representative files |

> [!caution]
> If the rewriter fails, **stop**. Partially rewritten files cause hard-to-debug migration graph errors later.

## Success Criteria

- [ ] `fix_v1_migration.py` finishes without exceptions
- [ ] Rewritten files remain parseable Python
- [ ] No known unresolved patterns in rewrite summary

*Previous: [[Step 2 — Prepare Migration Files]] · Next: [[Step 4 — Pre-Migrate Freeze Manifest]]*
