---
title: CLI Commands
---

Lex App ships with a `lex` CLI tool for managing your application. Here's every command at a glance.

## Everyday Commands

| Command         | What It Does                                                  |
| --------------- | ------------------------------------------------------------- |
| `lex setup`     | Generate `.run/`, `.env`, and `migrations/` for a new project |
| `lex Init`      | Apply migrations + sync models/permissions to Keycloak        |
| `lex start`     | Start the development server                                  |
| `lex --version` | Print the installed `lex-app` version                         |

## Testing Commands

| Command | What It Does |
|---|---|
| `lex pytest` | Run your project's test suite with Django bootstrapped |
| `lex pytest-groups` | List configured test groups and the tests they contain (no tests run) |

`lex pytest` behaves like plain `pytest` — any flags you pass are forwarded directly. Two extra flags are intercepted:

| Flag | What It Does |
|---|---|
| `--report` | Generate a branded PDF test report after the run |
| `--report-and-email` | Generate the PDF report and send it to configured recipients |

Use `-m` marker expressions to run only a subset of tests:

```bash
lex pytest -m creation                   # only tests in the "creation" group
lex pytest -m "creation or validation"   # union of two groups
lex pytest -m "not slow"                 # exclude a group
```

Test groups, recipients, and the tests entry point are configured in `lex_test_config.yaml` at your project root. Use `lex pytest-groups` to inspect what groups are registered and which tests belong to each.

## Keycloak Commands

| Command                | What It Does                                      |
| ---------------------- | ------------------------------------------------- |
| `lex Init`             | Sync models to Keycloak (also applies migrations) |
| `lex generate-configs` | Regenerate Keycloak configuration files           |

## Database Commands

| Command              | What It Does                                  |
| -------------------- | --------------------------------------------- |
| `lex migrate`        | Apply pending Django migrations               |
| `lex makemigrations` | Create new migration files from model changes |
| `lex sqlflush`       | Print SQL statements to flush the database    |

## AI Commands

| Command | What It Does |
|---|---|
| `lex setup-with-ai` | Configure LEX AI integration (GitHub Copilot MCP, remote MCP server) |
| `lex ai-update` | Apply incremental updates to an existing LEX AI setup (e.g. remove stale config keys) |
| `lex ai-dashboard` | Open a local web dashboard to switch MCP mode, update credentials, and inspect server status |
| `lex ai-verify` | Verify that required AI asset files are present and restore any that are missing or have drifted |
| `lex ai-faq` | Open the LEX AI FAQ page in your browser |

`lex setup-with-ai` prompts for a GitHub token and a remote MCP API key, then writes the necessary entries to your `.env` and `mcp.json`. It also verifies that all required AI asset directories (docs, `.github`, etc.) are present and restores any that are missing. If no project markers are found, it uses the directory you ran the command from (it won't jump up to your home folder).

`lex ai-update` is safe to run at any time — it only removes keys that are no longer needed and reports exactly what it changed.

`lex ai-dashboard` opens a browser page where you can switch between forward and backward MCP mode, update your GitHub token and remote MCP API key, and see the current server status. With lex-mcp-local ≥ 0.2.3, mode changes are instant — the server restarts itself and the IDE picks up the new tool surface automatically.

`lex ai-verify` checks the AI asset files for the active MCP mode and restores any that are missing or out of date. It resolves the active mode from the CLI `--mode` flag, then the override file, then your `.env`, then `mcp.json`, defaulting to `forward`. Pass `--silent` to suppress all output on success — useful in automated or MCP pre-flight contexts.

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
