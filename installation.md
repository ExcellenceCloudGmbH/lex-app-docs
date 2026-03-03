---
title: Installation
---

Install the `lex-app` package. This gives you the `lex` CLI tool and all framework dependencies.

```bash
pip install lex-app
```

Verify it worked:

```bash
lex --version
```

> [!tip]
> Make sure you're using **Python 3.12**. Check with `python3.12 --version`.

## Run the Setup Wizard

Navigate to your project directory and run:

```bash
lex setup
```

This generates three things for you:

- `.run/` — PyCharm run configurations (Init, Start, Streamlit)
- `.env` — Environment configuration template
- `migrations/` — Django migrations folder

## Configure Your Environment

The `.env` file is the **single source of truth** for runtime configuration.

### Option A: Automatic (Recommended)

Run `lex setup` and follow the prompts. The wizard will open [excellence-cloud.de](https://excellence-cloud.de) for you, guide you through creating a new Client, and auto-populate your `.env` file.

### Option B: Manual

1. Log in to [excellence-cloud.de](https://excellence-cloud.de)
2. Navigate to your project (or create a new Client)
3. Select client type → **development**
4. Enable **confidential**
5. Copy the credentials into your `.env`:

```env
KEYCLOAK_URL=https://auth.excellence-cloud.de
KEYCLOAK_REALM=lex
OIDC_RP_CLIENT_ID=your_client_id
OIDC_RP_CLIENT_SECRET=your_client_secret
OIDC_RP_CLIENT_UUID=your_client_uuid
DATABASE_DEPLOYMENT_TARGET=default
```

## Initialize the Application

`lex Init` is the primary initialization command. It does three things:

1. **Applies migrations** — creates/updates database tables from your models
2. **Syncs to Keycloak** — registers your models as "Resources" and permissions as "Scopes"
3. **Enables access management** — you can now manage permissions on [excellence-cloud.de](https://excellence-cloud.de)

### Via PyCharm (easiest)

1. Open the **Run Configuration** dropdown (top-right toolbar)
2. Select **"Init"**
3. Click the green ▶️ Run button (or press `Shift+F10`)

PyCharm automatically loads your `.env` file.

### Via Terminal

```bash
# Load environment variables first
set -a; source .env; set +a

# Then initialize
lex Init
```

<details>
<summary>Windows (PowerShell)</summary>

```powershell
# Load environment variables
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}

# Initialize
lex Init
```

</details>

> [!important]
> **When to run `lex Init` again:** Whenever you add a new model, new field, or change permission methods — any change that creates a new migration file.

## Start the Dev Server

### Via PyCharm

Select **"Start"** from the Run Configuration dropdown → click ▶️.

### Via Terminal

```bash
set -a; source .env; set +a
python -m lex start --reload --loop asyncio lex_app.asgi:application
```

Your application is now running at `http://localhost:8000`.

## Troubleshooting

<details>
<summary>"Environment variable not set" errors</summary>

- **PyCharm:** Make sure `.env` is in your project root
- **Terminal:** Always run `set -a; source .env; set +a` before any `lex` command

</details>

<details>
<summary>"ModuleNotFoundError: lex" errors</summary>

- Make sure `lex-app` is installed: `pip install lex-app`
- Verify you're using Python 3.12
- Check that your virtual environment is activated

</details>

<details>
<summary>Keycloak connection errors</summary>

- Verify `KEYCLOAK_URL` in your `.env`
- Check that `OIDC_RP_CLIENT_ID` and `OIDC_RP_CLIENT_SECRET` are correct
- Confirm your client exists on [excellence-cloud.de](https://excellence-cloud.de)

</details>

Got everything set up? Learn about the [[project structure]] or jump straight to [[running your app]].
