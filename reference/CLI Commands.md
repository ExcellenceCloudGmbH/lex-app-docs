---
title: CLI Commands
---

LEX ships with a `lex` CLI tool for managing your application. Here's every command at a glance.

## Everyday Commands

| Command | What It Does |
|---|---|
| `lex setup` | Generate `.run/`, `.env`, and `migrations/` for a new project |
| `lex Init` | Apply migrations + sync models/permissions to Keycloak |
| `lex start` | Start the development server |
| `lex --version` | Print the installed `lex-app` version |

## Migration Workflow Commands

These are used by the automated [[migration/index|migration pipeline]] for V1 → V2 database migration:

| Command | What It Does |
|---|---|
| `lex full-migration-workflow` | Run the complete 9-step migration pipeline |
| `lex makemigrations` | Generate Django migration files |
| `lex migrate` | Apply Django migrations to the database |

> [!tip]
> For migration flags and options, see [[migration/invocation modes]].

## Keycloak Commands

| Command | What It Does |
|---|---|
| `lex Init` | Sync models to Keycloak (also applies migrations) |
| `lex generate-configs` | Regenerate Keycloak configuration files |

## Database Commands

| Command | What It Does |
|---|---|
| `lex migrate` | Apply pending Django migrations |
| `lex makemigrations` | Create new migration files from model changes |
| `lex sqlflush` | Print SQL statements to flush the database |

## Usage Pattern

```bash
# Always load environment variables first (unless using PyCharm)
set -a; source .env; set +a

# Then run any lex command
lex Init
lex start
lex full-migration-workflow --dry-run
```
