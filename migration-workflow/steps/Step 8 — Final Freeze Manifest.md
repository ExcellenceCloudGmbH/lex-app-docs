---
title: "Step 8 — Final Freeze Manifest"
---

# Step 8 — Generate Final Legacy Freeze Manifest

[[Home]] / [[Migration Workflow Overview]] / Step 8

---

## What Happens

```bash
lex generate_legacy_freeze_manifest \
  --before .lex_tables_before.json \
  --output .lex_legacy_freeze_manifest.json
```

This manifest is the **runtime contract** between migration-time analysis and legacy model registration.

---

## Why It's Needed

Without this artifact, legacy table registration is either static (incomplete) or heuristic (unsafe). The manifest makes legacy visibility **explicit and repeatable**.

For why dynamic registration is preferred over static, see [[Dynamic vs Static Legacy Registration]].

<details>
<summary>🔧 Technical Details: How the manifest is computed</summary>

The command:
1. Computes legacy table candidates by diffing current tables vs V2 model tables
2. Applies exclusion rules
3. Filters out invalid entries (e.g., tables with no usable primary key)

Tables listed in the manifest are guaranteed to exist post-migration and be safe for dynamic unmanaged model registration.

</details>

---

## Success Criteria

- [ ] `.lex_legacy_freeze_manifest.json` exists and is valid JSON
- [ ] Listed tables exist in the DB
- [ ] Legacy models appear in admin as **read-only**

---

*Previous: [[Step 7 — Apply Migrations]] · Next: [[Step 9 — Backfill History]]*
