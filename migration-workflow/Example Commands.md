---
title: Example Commands
description: Copy-paste ready migration workflow commands for common scenarios
---

# Example Commands

[[Home]] / [[Migration Workflow Overview]] / Example Commands

---

## Default Run (from inside V2 project root)

```bash
./lex/full_migration_workflow.py db_armiracashflowdb \
  --migration-timestamp "2026-02-19T12:00:00Z" \
  --chunk-size 500
```

## With Explicit V2 Path + Sanitization

```bash
./lex/full_migration_workflow.py ~/LUND_IT/ArmiraCashflowDB db_armiracashflowdb \
  --enable-sanitization \
  --migration-timestamp "2026-02-19T12:00:00Z" \
  --chunk-size 500
```

## External V1 Source

```bash
./lex/full_migration_workflow.py \
  ~/LUND_IT/test/ArmiraCashflowDB \
  ~/LUND_IT/ArmiraCashflowDB \
  db_armiracashflowdb \
  --enable-sanitization \
  --migration-timestamp "2026-02-19T12:00:00Z" \
  --chunk-size 500
```

## Dry Run Backfill Only

```bash
./lex/full_migration_workflow.py db_armiracashflowdb \
  --backfill-only --dry-run-backfill --chunk-size 200
```

## With Rollback Safety

```bash
./lex/full_migration_workflow.py db_armiracashflowdb \
  --migration-timestamp "2026-02-19T12:00:00Z" \
  --rollback-on-failure
```

## Rollback Only (After Failure)

```bash
./lex/full_migration_workflow.py db_armiracashflowdb --rollback-only
```

## Fresh Slate (Clean + Run)

```bash
./lex/full_migration_workflow.py db_armiracashflowdb \
  --pre-clean-jsons \
  --migration-timestamp "2026-02-19T12:00:00Z"
```

## GCP Target

```bash
./lex/full_migration_workflow.py db_armiracashflowdb \
  --database-deployment-target GCP \
  --migration-timestamp "2026-02-19T12:00:00Z"
```

---

*See also: [[Invocation Modes]] | [[Verification Checklist]]*
