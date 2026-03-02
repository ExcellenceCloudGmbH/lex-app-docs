---
title: "Tutorial: Build TeamBudget from Scratch"
description: A complete step-by-step guide to building your first LEX app on Windows
---

# 🚀 Tutorial: Build TeamBudget from Scratch

[[Home]] / Tutorial

---

## What We're Building

**TeamBudget** is an expense tracking app for a small consulting firm. By the end of this tutorial, you'll have a working application with:

- ✅ Data models for **Teams**, **Employees**, and **Expenses**
- ✅ **Automatic budget calculations** that compute utilization on demand
- ✅ **Rich calculation logs** showing exactly what was computed
- ✅ **Role-based permissions** — employees, managers, and CFO see different data
- ✅ **Interactive Streamlit dashboards** with charts and metrics
- ✅ **Bitemporal history** tracking every change with time-travel

---

## The Story

> You're the lead developer at **Apex Consulting**, a growing firm with three teams: Design, Engineering, and Marketing. The CFO asks you to build an internal tool where employees submit expenses, managers approve them, and leadership gets real-time budget dashboards.
>
> Previously, this was done in spreadsheets. Corrections were lost, there was no audit trail, and nobody knew the budget status until month-end. Your LEX-powered app will fix all of that — in about 30 minutes.

---

## Prerequisites

Before you start, make sure you have:

- [ ] **Windows 10/11** with **Python 3.12** installed
- [ ] **PyCharm** (Community or Professional)
- [ ] **PostgreSQL** running locally (or via Docker)

> [!tip]
> If you haven't installed LEX yet, see [[../getting-started/Setup & Installation|Setup & Installation]] first.

---

## Project Structure

When we're done, your project will look like this:

```
TeamBudget/
├── .env
├── .run/
│   ├── Init.run.xml
│   ├── Start.run.xml
│   └── Streamlit.run.xml
├── requirements.txt
├── model_structure.yaml
├── migrations/
├── sample_data/
│   ├── teams.csv
│   ├── employees.csv
│   └── expenses.csv
├── Team.py
├── Employee.py
├── Expense.py
├── TeamUpload.py
├── EmployeeUpload.py
├── ExpenseUpload.py
└── BudgetSummary.py
```

> [!important]
> LEX uses a **flat project layout** — all model files live directly at the project root. No nested app folders, no `manage.py`. One file per model class (e.g., `Team.py`, `Employee.py`).

---

## Tutorial Parts

| Part                                          | What You'll Build                             | Time   |
| --------------------------------------------- | --------------------------------------------- | ------ |
| [[Part 1 — Project Setup\|Part 1]]            | Create the project and run the setup wizard   | ~5 min |
| [[Part 2 — Data Models\|Part 2]]              | Define Team, Employee, and Expense models     | ~5 min |
| [[Part 3 — Calculations & Logging\|Part 3]]   | Add automatic budget utilization calculations | ~5 min |
| [[Part 4 — Validation & Permissions\|Part 4]] | Add business rules and role-based access      | ~5 min |
| [[Part 5 — Streamlit Dashboards\|Part 5]]     | Build interactive visual dashboards           | ~5 min |
| [[Part 6 — History in Action\|Part 6]]        | See bitemporal tracking work end-to-end       | ~5 min |

---

## Sample Data Included

We've provided CSV files in `sample_data/` that you can use to quickly populate your app:

| File | Contents |
|---|---|
| `teams.csv` | 3 teams: Design, Engineering, Marketing |
| `employees.csv` | 9 employees across all teams |
| `expenses.csv` | 14 realistic expenses across categories |

---

> **Ready?** Let's start → [[Part 1 — Project Setup]]
