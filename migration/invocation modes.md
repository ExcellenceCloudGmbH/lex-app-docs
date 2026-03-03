---
title: Invocation Modes
---

The migration workflow can be invoked in several ways depending on your project setup. All modes run the same pipeline — they differ only in how you specify paths.

## Three Ways to Invoke

### Mode A — External V1 Source (Copy Mode)

Use when V1 migrations live in a separate directory.

```bash
./lex/full_migration_workflow.py <V1_SOURCE> <V2_ROOT> <DB_NAME> [flags...]
```

### Mode B — In-Place Mode

Use when V1 migration files are already in the V2 project.

```bash
./lex/full_migration_workflow.py <V2_ROOT> <DB_NAME> [flags...]
```

### Mode C — Local Mode

Use when running from inside the V2 project root.

```bash
./lex/full_migration_workflow.py <DB_NAME> [flags...]
```

### As a Management Command

```bash
lex full_migration_workflow --db-name <DB_NAME> [--project-root <PATH>] [--v1-source <PATH>] [flags...]
```

## All Flags

| Flag | Default | Description |
|---|---|---|
| `--migration-timestamp <ISO8601>` | Auto | Timestamp for bitemporal backfill baseline |
| `--chunk-size <INT>` | `500` | Batch size for backfill operations |
| `--dry-run-backfill` | off | Run backfill in dry-run mode (no writes) |
| `--enable-sanitization` | off | Activate migration sanitization |
| `--backfill-only` | off | Skip schema steps; run only backfill |
| `--pre-clean-jsons` | off | Delete JSON artifacts before run |
| `--rollback-on-failure` | off | Auto-restore on failure |
| `--rollback-only` | off | Only perform rollback |
| `--rollback-state-file <PATH>` | `.lex_migration_state_before.json` | Rollback state file path |
| `--skip-auditlog-backfill` | off | Skip audit log backfill sub-step |
| `--database-deployment-target` | `default` | Sets `DATABASE_DEPLOYMENT_TARGET` env var |

> [!important]
> `--enable-sanitization` is **OFF by default**. When off, Steps 4 and 6 are skipped entirely.

> [!note]
> `--backfill-only` skips all schema migration steps and runs only: normalization → bitemporal backfill → audit-log backfill.

## Environment Variables Set Internally

| Variable | Source |
|---|---|
| `DB_NAME` | `<DB_NAME>` positional argument |
| `PROJECT_ROOT` | Resolved V2 project root (POSIX path) |
| `DATABASE_DEPLOYMENT_TARGET` | `--database-deployment-target` flag or `"default"` |

See also [[migration/example commands|Example Commands]] and the [[migration/index|Migration Overview]].
