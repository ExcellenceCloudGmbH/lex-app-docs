---
title: "TeamBudget Tutorial"
---

In this tutorial, you'll build a complete LEX application from scratch — a **team budget tracker** called TeamBudget. By the end, you'll have used every major LEX feature: models, calculations, lifecycle hooks, logging, permissions, Streamlit dashboards, and bitemporal history.

## What You'll Build

TeamBudget is a simple application that tracks teams, employees, and expenses. It includes:

- **Data models** — `Team`, `Employee`, `Expense`, and `BudgetSummary`
- **Calculations** — automatic budget summaries with state tracking
- **File processing** — upload Excel files that auto-populate models via lifecycle hooks
- **Rich logging** — formatted calculation logs with tables and context
- **Permissions** — field-level and row-level access control
- **Dashboards** — interactive Streamlit visualizations
- **History** — full bitemporal audit trail

## Prerequisites

Before starting, make sure you have:

- LEX installed and configured (see [[installation]])
- PyCharm (recommended) or any Python-capable editor
- Access to [excellence-cloud.de](https://excellence-cloud.de) for Keycloak setup

## Project Structure

LEX uses a flat project layout — no `manage.py`, no nested Django app folders. Your model files can live at the project root or be organized into subfolders:

```
TeamBudget/
├── .env
├── .run/
│   ├── Init.run.xml
│   └── Start.run.xml
├── migrations/
├── Tests/
│   ├── basic_test/
│   │   └── test_data.json
│   └── UploadFiles/
│       └── sample_expenses.xlsx
├── Team.py
├── Employee.py
├── Expense.py
└── BudgetSummary.py
```

> [!important]
> LEX uses a **flat project layout** — no nested Django app folders, no `manage.py`. One file per model class. Models at the root are imported with `from .Team import Team`; models in subfolders with `from Upload.TeamUpload import TeamUpload`.

## Tutorial Parts

Work through these in order:

1. [[tutorial/Part 1 — Project Setup|Part 1 — Project Setup]] — create the project, configure your environment, run Init
2. [[tutorial/Part 2 — Data Models|Part 2 — Data Models]] — define `Team`, `Employee`, and `Expense` models
3. [[tutorial/Part 3 — Calculations & Logging|Part 3 — Calculations & Logging]] — build `BudgetSummary` as a `CalculationModel` with `LexLogger`
4. [[tutorial/Part 4 — Validation & Permissions|Part 4 — Validation & Permissions]] — add `pre_validation()`, `post_validation()`, and `permission_*` methods
5. [[tutorial/Part 5 — Streamlit Dashboards|Part 5 — Streamlit Dashboards]] — attach interactive dashboards to your models
6. [[tutorial/Part 6 — History in Action|Part 6 — History in Action]] — explore the bitemporal history panel

## Sample Data

The tutorial includes sample data you can use:

| File | Contents |
|---|---|
| `Tests/basic_test/test_data.json` | Pre-populated teams, employees, and expenses |
| `Tests/UploadFiles/sample_expenses.xlsx` | Excel file for testing upload hooks |
