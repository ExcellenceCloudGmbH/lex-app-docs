---
title: Verification Checklist
---

Run through this checklist after any full migration to confirm everything completed successfully.

## Pre-Run Artifacts

- [ ] `.lex_tables_before.json` exists with plausible table count
- [ ] Rollback state file captured (if `--rollback-on-failure` was set)

## Migration Steps

- [ ] Step 3 rewrite completed without unresolved patterns
- [ ] `lex makemigrations` succeeded
- [ ] `lex migrate` exited with code `0`
- [ ] `django_migrations` table reflects expected applied revisions

## Legacy Freeze

- [ ] `.lex_legacy_freeze_manifest.json` exists and is valid JSON
- [ ] Manifest table list matches expectations
- [ ] Legacy models appear in admin as read-only
- [ ] No write operations succeed for frozen records

## Bitemporal Backfill

- [ ] History backfill shows expected created/skipped counts per model
- [ ] History table row counts align with main tables
- [ ] Audit-log backfill completed (or was intentionally skipped)

## Application Health

- [ ] Application starts without errors
- [ ] Summary JSON block present in logs:
  ```
  MIGRATION_WORKFLOW_SUMMARY_START
  {"backfill_only":false,...}
  MIGRATION_WORKFLOW_SUMMARY_END
  ```

## Artifact Files

| File | Status |
|---|---|
| `.lex_tables_before.json` | Required |
| `.lex_legacy_freeze_manifest.json` | Required |
| `.lex_legacy_freeze_manifest.pre_migrate.json` | Only with `--enable-sanitization` |
| `.lex_migration_state_before.json` | Only with `--rollback-on-failure` |
