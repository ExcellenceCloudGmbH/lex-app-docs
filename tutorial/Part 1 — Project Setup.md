---
title: "Part 1 — Project Setup"
description: Create your LEX project and run the setup wizard on Windows
---

# Part 1 — Project Setup

[[Tutorial Overview]] / Part 1

---

## Step 1: Create a Project Folder

Open **PowerShell** and create your project:

```powershell
mkdir C:\Projects\TeamBudget
cd C:\Projects\TeamBudget
```

## Step 2: Create a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` at the start of your prompt.

> [!tip]
> **Trouble with `python`?** On some Windows installations, you may need to use `py` instead of `python`.

## Step 3: Create `requirements.txt`

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
> **Always use `python -m pip`** instead of just `pip` on Windows. This ensures you're using the pip from your virtual environment, not a system-level one.

## Step 4: Run the Setup Wizard

The setup wizard must be run from the terminal:

```powershell
python -m lex setup
```

> [!important]
> **Always use `python -m lex`** instead of just `lex` on Windows. The `lex` command may not be on your PATH, but `python -m lex` always works.

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

The `.run/` folder contains **PyCharm run configurations** — these are pre-configured for you and will be the primary way to interact with your project from now on.

> [!note]
> Notice there's no `manage.py` or nested app folder. LEX uses a **flat layout** — the framework handles everything. Your model files will go directly in the project root.

## Step 5: Open in PyCharm

1. Open PyCharm
2. **File → Open** → select `C:\Projects\TeamBudget`
3. When prompted, set the Python interpreter to `.venv\Scripts\python.exe`

You'll see the run configurations appear in the top-right dropdown:

| Run Configuration | What It Does |
|---|---|
| **Init** | Creates/updates the database and syncs Keycloak |
| **Start** | Runs the development server |
| **Streamlit** | Starts the Streamlit dashboard server |

## Step 6: Create the Database

In PyCharm's terminal (**View → Tool Windows → Terminal**):

```powershell
python -m lex create_db
```

## Step 7: Initialize

Select **"Init"** from the run configuration dropdown in PyCharm → click ▶️.

This runs migrations and sets up Keycloak. You should see in the Run panel:

```
Running migrations...
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
Syncing models to Keycloak... OK
```

<details>
<summary>💻 Terminal alternative</summary>

If you prefer the terminal, you'll need to load the `.env` first:

```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}
python -m lex Init
```

> [!note]
> PyCharm's run configurations auto-load `.env` for you — this is why using PyCharm is the easier option.

</details>

## Step 8: Verify It Works

Select **"Start"** from the run configuration dropdown → click ▶️.

Open `http://localhost:8000` in your browser. You should see the LEX interface — empty for now, but working!

Click the 🔴 stop button in PyCharm to stop the server.

<details>
<summary>💻 Terminal alternative</summary>

```powershell
python -m lex start
```

Press `Ctrl+C` to stop.

</details>

---

## ✅ Checkpoint

At this point you have:
- [x] A working LEX project with a flat layout
- [x] PyCharm run configurations ready (Init, Start, Streamlit)
- [x] Database created and migrations applied
- [x] Server starts without errors

---

> **Next:** [[Part 2 — Data Models]] — Let's build our models →
