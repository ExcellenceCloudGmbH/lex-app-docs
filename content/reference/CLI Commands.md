---
title: CLI Commands
---

Lex App ships with a `lex` CLI tool for managing your application. Here's every command at a glance.

## Everyday Commands

| Command | What It Does |
|---|---|
| `lex setup` | Generate `.run/`, `.env`, and `migrations/` for a new project |
| `lex Init` | Apply migrations + sync models/permissions to Keycloak |
| `lex start` | Start the development server |
| `lex --version` | Print the installed `lex-app` version |

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

We recommend using PyCharm's run configurations (Init, Start, Streamlit) which auto-load `.env` for you. If you prefer the terminal:

**Linux / macOS:**

```bash
# Load environment variables first
set -a; source .env; set +a

# Then run any lex command
lex Init
lex start
```

**Windows PowerShell:**

```powershell
# Load environment variables first
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}

# Then run any lex command
lex Init
lex start
```
