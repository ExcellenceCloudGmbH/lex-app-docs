---
title: Example Commands
---

Copy-paste ready commands for common migration scenarios. All commands assume you're in the V2 project root.

## Default Run

```bash
./lex/full_migration_workflow.py db_armiracashflowdb \
  --migration-timestamp "2026-02-19T12:00:00Z" \
  --chunk-size 500
```

## With Sanitization

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

## Dry Run (Backfill Only)

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

## Fresh Slate

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

See [[migration/invocation modes|Invocation Modes]] for the full flag reference.
