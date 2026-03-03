---
title: "Part 6 — History in Action"
---

Your app already has full [[features/bitemporal history|bitemporal history]] — you didn't write a single line for it. In this final part, you'll see it in action by making corrections and exploring the timeline.

## Scenario: Correcting an Expense After Quarter Close

> It's February 5th. Anna from the Design team notices that her "Flight to Munich" expense was entered as **€450**, but the actual receipt shows **€380**. The quarter has already closed, but the correction needs to be recorded properly.

### Edit the Expense

1. Navigate to **Expense** in the frontend
2. Find Anna's "Flight to Munich" record
3. Change the amount from **€450.00** to **€380.00**
4. Save

### Open the History Panel

Click the **History icon** on the record. You'll see:

| Version | Amount | Valid From | Valid To | Changed By |
|---|---|---|---|---|
| v2 *(current)* | €380.00 | Feb 5, 10:15 AM | — | Anna Schmidt |
| v1 *(superseded)* | €450.00 | Jan 20, 2:30 PM | Feb 5, 10:15 AM | Anna Schmidt |

> [!tip]
> Both values are preserved. The original €450 entry is never deleted — it's superseded. This is exactly what auditors need: a complete, tamper-proof trail.

## Timeline Editing: Backdating the Correction

Now suppose Anna realizes the correct amount (€380) was actually valid **since January 20** (when the flight happened), not since today. She needs to backdate the correction.

### Edit `valid_from` in the History Panel

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

The v1 entry still exists in the system history (Level 2) — you can always answer: "On February 4th, what did the system think this expense was?" Answer: **€450**, because the backdated correction hadn't been entered yet.

## What the Two Levels Show

### Level 1 — Valid Time ("What was true?")

After the backdating, valid time shows:

| Amount | Valid From | Valid To |
|---|---|---|
| €380.00 | Jan 20, 2:30 PM | *current* |

This is the business reality: the flight always cost €380.

### Level 2 — System Time ("When did we know?")

System time tells the complete knowledge story:

| Knowledge | Sys From | Sys To |
|---|---|---|
| "We thought it was €450" | Jan 20, 2:30 PM | Feb 5, 10:15 AM |
| "We now know it's €380" | Feb 5, 10:15 AM | *current* |

> [!important]
> You never lose information. Even after the backdating correction, both the original belief AND the correction are preserved in the system history.

## Recalculate After the Correction

After correcting the expense:

1. Navigate to **BudgetSummary** → Design team, Q1 2026
2. Click **Calculate** ▶️

The calculation will reflect the corrected amount (€380 instead of €450). The calculation log shows the updated numbers — and the previous calculation log is still accessible in the history.

## You're Done!

Congratulations! You've built a complete business application with:

| Feature | What You Wrote |
|---|---|
| **4 data models** | Four short Python files |
| **Automatic CRUD + API** | Zero lines — the framework handles it |
| **Budget calculations** | One `calculate()` method |
| **Rich logging** | A few `LexLogger` calls |
| **Validation** | One `pre_validation()` method |
| **Role-based permissions** | Two `permission_*()` methods |
| **Interactive dashboards** | Two Streamlit methods |
| **Full bitemporal history** | Zero lines — completely automatic |
| **Timeline editing** | Zero lines — built into the frontend |

**Total code: ~330 lines** (including whitespace, docstrings, and imports). Everything else — the web UI, API, authentication, history, real-time updates — is provided by the framework.

## What's Next?

Now that you've completed the tutorial, explore the rest of the documentation:

- [[features/index|All features]] — everything LEX gives you out of the box
- [[features/calculations|Calculations]] — deep-dive into the state machine and Celery support
- [[features/bitemporal history|Bitemporal History]] — understand the two-level architecture
- [[features/streamlit dashboards|Streamlit Dashboards]] — build more complex visualizations
- [[reference/CLI Commands|CLI Commands]] — every `lex` command at a glance
