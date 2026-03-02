---
title: "Step 2 — Prepare Migration Files"
---

# Step 2 — Prepare V1 Migration Files

[[Home]] / [[Migration Workflow Overview]] / Step 2

---

## What Happens

The workflow selects one of two paths:

| Path | When | Behavior |
|---|---|---|
| **Copy mode** | V1 source path provided | Copies V1 migration files into V2 `migrations/` |
| **In-place mode** *(default)* | No V1 source | Uses existing files in V2 `migrations/` |

---

## Why It's Needed

V2 must replay from a migration chain that reflects the V1 schema history. Generated V2 migrations alone aren't enough — existing production DBs were built from V1 definitions.

---

## What Can Go Wrong

| Issue | Fix |
|---|---|
| Wrong V1 source path | Verify the path exists and contains `.py` files |
| No migration files found | Check that `migrations/` is populated |
| Stale content from prior runs | Use `--pre-clean-jsons` or manually clean |

---

## Success Criteria

- [ ] `migrations/` directory exists with at least one migration file
- [ ] Logs show whether **copy mode** or **in-place mode** was used

---

*Previous: [[Step 1 — Capture DB Tables]] · Next: [[Step 3 — Rewrite Migrations]]*
