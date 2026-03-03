---
title: "Part 1 — Project Setup"
---

In this first part, you'll create a new LEX project, configure your environment, and verify everything works. By the end, you'll have a running (empty) LEX application.

## Create a Project Folder

Open **PowerShell** and create your project:

```powershell
mkdir C:\Projects\TeamBudget
cd C:\Projects\TeamBudget
```

## Create a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` at the start of your prompt.

> [!tip]
> On some Windows installations, you may need to use `py` instead of `python`.

## Create `requirements.txt`

Create a file called `requirements.txt` in your project root:

```
lex-app
pandas
openpyxl
```

Then install:

```powershell
python -m pip install -r requirements.txt
```

> [!important]
> Always use `python -m pip` instead of just `pip` on Windows. This ensures you're using the pip from your virtual environment.

## Run the Setup Wizard

```powershell
python -m lex setup
```

> [!important]
> Always use `python -m lex` instead of just `lex` on Windows. The `lex` command may not be on your PATH.

After the wizard completes, you'll have:

```
TeamBudget/
├── .env
├── .run/
│   ├── Init.run.xml
│   ├── Start.run.xml
│   └── Streamlit.run.xml
└── migrations/
```

The `.run/` folder contains PyCharm run configurations — these are pre-configured and will be the primary way to interact with your project.

> [!note]
> Notice there's no `manage.py` or nested app folder. LEX uses a **flat layout** — no Django boilerplate. Your model files can go at the project root or be organized into subfolders.

## Open in PyCharm

1. Open PyCharm
2. **File → Open** → select `C:\Projects\TeamBudget`
3. When prompted, set the Python interpreter to `.venv\Scripts\python.exe`

You'll see the run configurations appear in the top-right dropdown:

| Run Configuration | What It Does |
|---|---|
| **Init** | Creates/updates the database and syncs Keycloak |
| **Start** | Runs the development server |
| **Streamlit** | Starts the Streamlit dashboard server |

## Create the Database

In PyCharm's terminal (**View → Tool Windows → Terminal**):

```powershell
python -m lex create_db
```

## Initialize

Select **"Init"** from the run configuration dropdown in PyCharm → click ▶️.

This runs migrations and sets up Keycloak. You should see:

```
Running migrations...
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
Syncing models to Keycloak... OK
```

<details>
<summary>Terminal alternative</summary>

```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}
python -m lex Init
```

> [!note]
> PyCharm's run configurations auto-load `.env` for you — this is why using PyCharm is easier.

</details>

## Verify It Works

Select **"Start"** from the run configuration dropdown → click ▶️.

Open `http://localhost:8000` in your browser. You should see the LEX interface — empty for now, but working.

<details>
<summary>Terminal alternative</summary>

```powershell
python -m lex start
```

Press `Ctrl+C` to stop.

</details>

## Checkpoint

At this point you have:
- A working LEX project with a flat layout
- PyCharm run configurations ready (Init, Start, Streamlit)
- Database created and migrations applied
- Server starts without errors

Next up: [[tutorial/Part 2 — Data Models|Part 2 — Data Models]] where you'll define the Team, Employee, and Expense models.
