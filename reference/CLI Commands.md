---
title: CLI Commands
description: All lex CLI commands at a glance
---

# CLI Commands Reference

[[Home]] / Reference / CLI Commands

---

## Everyday Commands

| Command | Purpose | When to Use |
|---|---|---|
| `lex setup` | Run setup wizard — generates `.run/`, `.env`, `migrations/` | First-time project setup |
| `lex Init` | Apply migrations + sync models to Keycloak | After adding models, fields, or permission changes |
| `lex makemigrations <app>` | Generate new migration files | After changing model definitions |
| `lex migrate` | Apply all pending migrations | Usually called by `lex Init` |
| `lex start` | Start the ASGI dev server | Daily development |

---

## Migration Workflow Commands

| Command | Purpose |
|---|---|
| `lex full_migration_workflow` | Run the full V1→V2 migration pipeline |
| `lex capture_db_tables --output <file>` | Snapshot current database tables to JSON |
| `lex capture_migration_state --output <file>` | Capture migration state for rollback |
| `lex rollback_migration_state --input <file>` | Restore migrations from a captured state |
| `lex generate_legacy_freeze_manifest --before <file> --output <file>` | Generate legacy freeze manifest |
| `lex normalize_is_calculated --chunk-size <N>` | Convert boolean `is_calculated` → enum strings |
| `lex backfill_bitemporal_history --chunk-size <N> --reason <text>` | Seed V2 bitemporal history |
| `lex backfill_audit_logging --chunk-size <N> --reason <text>` | Seed audit log entries |

---

## Keycloak Commands

| Command | Purpose |
|---|---|
| `lex sync_keycloak` | Sync models/permissions to Keycloak |
| `lex bootstrap_keycloak` | Initial Keycloak realm setup |

---

## Database Commands

| Command                    | Purpose                                          |
| -------------------------- | ------------------------------------------------ |
| `lex create_db`            | Create the database                              |
| `lex detect_model_changes` | Detect model changes without creating migrations |

---

## Usage Pattern

```bash
# Always load environment first (terminal only — PyCharm does this automatically)
set -a; source .env; set +a

# Then run any command
lex <command> [options]
```

---

*See also: [[../migration-workflow/Invocation Modes|Migration Workflow Flags]] | [[../getting-started/Running Your App|Running Your App]]*
