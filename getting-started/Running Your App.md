---
title: Running Your App
description: How to run your LEX application locally using PyCharm or the terminal
---

# Running Your App

[[Home]] / [[Getting Started]] / Running Your App

---

## Generated Run Configurations

After running `lex setup`, your `.run/` directory contains ready-to-use PyCharm configurations:

```
.run/
├── Init.run.xml
├── Start.run.xml
└── Streamlit.run.xml
```

---

## Three Configurations

| Config | Purpose | When to Use |
|---|---|---|
| **Init** | Apply migrations + sync Keycloak resources | Initial setup, after adding models/fields/permissions |
| **Start** | Launch the ASGI development server | Daily development, testing API endpoints |
| **Streamlit** | Launch interactive dashboards | Building visualizations |

---

## Using PyCharm (Recommended)

1. Look at the **Run Configuration dropdown** (top-right toolbar)
2. Select the configuration you need (e.g. "Init" or "Start")
3. Click the green ▶️ **Run** button (or press `Shift+F10`)

> [!tip]
> PyCharm automatically loads environment variables from your `.env` file when using the generated configurations. No manual `source .env` needed.

<!-- 📸 TODO: Add screenshot of PyCharm run configuration dropdown -->

---

## Using the Terminal

If you prefer the terminal, **always load your environment first**:

```bash
set -a; source .env; set +a
```

Then run the command you need:

### Init (Migrations + Keycloak Sync)

```bash
lex Init
```

### Start (Development Server)

```bash
python -m lex start --reload --loop asyncio lex_app.asgi:application
```

### Streamlit (Dashboards)

```bash
export PROXY_MODE=passthrough
export DJANGO_SETTINGS_MODULE=lex_app.settings
streamlit run .venv/lib/python3.12/site-packages/lex/streamlit_app.py
```

---

## When to Use Each Configuration

| Scenario | Configuration |
|---|---|
| Initial project setup | **Init** |
| Added a new model or field | **Init** (creates migration + syncs to Keycloak) |
| Changed permission methods | **Init** (syncs scopes to Keycloak) |
| Daily development | **Start** |
| Testing API endpoints | **Start** |
| Building interactive visualizations | **Streamlit** |

---

## Example: Your First Run

Here's a complete example from a fresh project setup to a running server:

```bash
# 1. Install the framework
pip install lex-app

# 2. Run setup wizard (generates .run/, .env, migrations/)
lex setup

# 3. Configure .env (follow the prompts or fill in manually)

# 4. Load environment
set -a; source .env; set +a

# 5. Initialize (migrations + Keycloak sync)
lex Init

# 6. Start the server
python -m lex start --reload --loop asyncio lex_app.asgi:application
```

Your application is now running at `http://localhost:8000` 🎉

---

> **You're all set up!** Continue to the refactoring guides: [[../guides/Import Migration|Import Migration]] →
