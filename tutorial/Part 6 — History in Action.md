---
title: "Part 6 — History in Action"
description: See bitemporal tracking and time-travel in your app
---

# Part 6 — History in Action

[[Tutorial Overview]] / Part 6

---

## What We're Exploring

Your app already has **full bitemporal history** — you didn't write a single line for it. In this final part, we'll see it in action by making corrections and exploring the timeline.

---

## Scenario: Correcting an Expense After Quarter Close

> It's February 5th. Anna from the Design team notices that her "Flight to Munich" expense was entered as **€450**, but the actual receipt shows **€380**. The quarter has already closed, but the correction needs to be recorded properly.

### Step 1: Edit the Expense

1. Navigate to **Expense** in the frontend
2. Find Anna's "Flight to Munich" record
3. Change the amount from **€450.00** to **€380.00**
4. Save

### Step 2: Open the History Panel

Click the **History icon** 🕐 on the record. You'll see:

| Version | Amount | Valid From | Valid To | Changed By |
|---|---|---|---|---|
| v2 *(current)* | €380.00 | Feb 5, 10:15 AM | — | Anna Schmidt |
| v1 *(superseded)* | €450.00 | Jan 20, 2:30 PM | Feb 5, 10:15 AM | Anna Schmidt |

> [!tip]
> **Both values are preserved.** The original €450 entry is never deleted — it's superseded. This is exactly what auditors need: a complete, tamper-proof trail.

---

## Timeline Editing: Backdating the Correction

Now suppose Anna realizes the correct amount (€380) was actually valid **since January 20** (when the flight happened), not since today. She needs to **backdate** the correction.

### Step 3: Edit `valid_from` in the History Panel

1. In the history panel, click on **v2** (the €380 version)
2. Change `valid_from` from **Feb 5** to **Jan 20, 2:30 PM**
3. Save

The system recalculates the timeline:

**Before:**

```
Jan 20                              Feb 5
├── v1: €450.00 ────────────────────┤── v2: €380.00 ──────────►
```

**After backdating:**

```
Jan 20
├── v2: €380.00 ──────────────────────────────────────────────►
```

The v1 entry still exists in the **system history** (Level 2) — you can always answer: "On February 4th, what did the system think this expense was?" Answer: **€450**, because the backdated correction hadn't been entered yet.

---

## What the Two Levels Show

### Level 1 — Valid Time ("What was true?")

After the backdating, valid time shows:

| Amount | Valid From | Valid To |
|---|---|---|
| €380.00 | Jan 20, 2:30 PM | *current* |

This is the **business reality**: the flight always cost €380.

### Level 2 — System Time ("When did we know?")

System time tells the complete knowledge story:

| Knowledge | Sys From | Sys To |
|---|---|---|
| "We thought it was €450" | Jan 20, 2:30 PM | Feb 5, 10:15 AM |
| "We now know it's €380" | Feb 5, 10:15 AM | *current* |

> [!important]
> **You never lose information.** Even after the backdating correction, both the original belief AND the correction are preserved in the system history.

---

## Recalculate After the Correction

After correcting the expense:

1. Navigate to **BudgetSummary** → Design team, Q1 2026
2. Click **Calculate** ▶️

The calculation will reflect the corrected amount (€380 instead of €450). The **calculation log** shows the updated numbers — and the previous calculation log is still accessible in the history.

---

## 🎉 You're Done!

Congratulations! You've built a complete business application with:

| Feature | What You Wrote |
|---|---|
| **4 data models** | Four Python files at the project root |
| **Automatic CRUD + API** | Zero lines — the framework handles it |
| **Budget calculations** | One `calculate()` method |
| **Rich logging** | A few `LexLogger` calls |
| **Validation** | One `pre_validation()` method |
| **Role-based permissions** | Two `permission_*()` methods |
| **Interactive dashboards** | Two Streamlit methods |
| **Full bitemporal history** | Zero lines — completely automatic |
| **Timeline editing** | Zero lines — built into the frontend |

### Your Final Project

```
TeamBudget/
├── .env
├── .run/
│   ├── Init.run.xml
│   ├── Start.run.xml
│   └── Streamlit.run.xml
├── requirements.txt
├── migrations/
├── sample_data/
│   ├── teams.csv
│   ├── employees.csv
│   └── expenses.csv
├── Team.py               ~20 lines
├── Employee.py            ~28 lines
├── Expense.py             ~85 lines
└── BudgetSummary.py      ~200 lines
```

**Total code: ~330 lines** (including whitespace, docstrings, and imports). Everything else — the web UI, API, authentication, history, real-time updates — is provided by the framework.

---

## What's Next?

| Topic | Link |
|---|---|
| Explore all framework features | [[../Home\|Documentation Home]] |
| Deep-dive into calculations | [[../guides/Calculations\|Calculations Guide]] |
| Understand the history architecture | [[../guides/Bitemporal History\|Bitemporal History Guide]] |
| Build more complex Streamlit pages | [[../guides/Streamlit Dashboards\|Streamlit Guide]] |
| See all CLI commands | [[../reference/CLI Commands\|CLI Commands]] |

---

> **🎓 Tutorial Complete!** You've built TeamBudget from scratch. Go build something amazing.
