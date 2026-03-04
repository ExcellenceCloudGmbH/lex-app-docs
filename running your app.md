---
title: Running Your App
---

Once you've [[installation|installed and initialized]] your LEX application, you can run it locally. There are two ways to do this: through PyCharm (recommended) or via the terminal.

## Using PyCharm

The `lex setup` command generates ready-to-use run configurations in the `.run/` folder. Open the **Run Configuration** dropdown in the top-right toolbar and you'll see:

| Configuration | What It Does |
|---|---|
| **Init** | Applies migrations and syncs to Keycloak |
| **Start** | Starts the development server |
| **Streamlit** | Runs the Streamlit dashboard server |

Select **"Start"** and click the green ▶️ button. Your app is now running at `http://localhost:8000`.

> [!tip]
> PyCharm run configurations automatically load your `.env` file. No manual sourcing needed.

<!-- 📸 TODO: Add screenshot of PyCharm run configuration dropdown -->

## Using the Terminal

If you're not using PyCharm, you'll need to load environment variables manually before running any `lex` command:

```bash
# Load environment variables
set -a; source .env; set +a

# Start the development server
python -m lex start --reload --loop asyncio lex_app.asgi:application
```

The `--reload` flag enables hot-reloading so the server restarts automatically when you change code.

## Running Streamlit Dashboards

If your models define [[features/access-and-ui/streamlit dashboards|Streamlit dashboards]], you need to start the Streamlit server separately:

### Via PyCharm

Select **"Streamlit"** from the Run Configuration dropdown.

### Via Terminal

```bash
set -a; source .env; set +a

PROXY_MODE=true \
DJANGO_SETTINGS_MODULE=lex_app.settings \
streamlit run lex_app/streamlit_entrypoint.py --server.port 8501
```

> [!note]
> `PROXY_MODE=true` is required when running Streamlit standalone. Without it, Streamlit won't be able to connect to your Django backend.

## What's Next?

Now that your app is running, explore the [[features/index|features]] to see what LEX gives you out of the box. If you want a guided walkthrough, try the [[tutorial/index|TeamBudget Tutorial]].
