---
title: "Model Structure & Navigation"
description: Control how your models appear in the frontend sidebar
---

# Model Structure & Navigation

[[Home]] / Guides / Model Structure

---

## Overview

By default, LEX shows all your models in a flat list in the frontend sidebar. The `model_structure.yaml` file lets you organize them into groups, rename those groups, and exclude specific models from history tracking.

Create this file in your **project root** — LEX picks it up automatically.

---

## The Three Sections

| Section | Purpose |
|---|---|
| `model_structure` | Define the navigation tree (folders and models) |
| `model_styling` | Rename folders as they appear in the frontend |
| `untracked_models` | Exclude models from bitemporal history |

---

## `model_structure` — Navigation Tree

This defines the folder hierarchy in the frontend sidebar. Each top-level key is a group name, and the leaf nodes are model names (**lowercase**).

```yaml
model_structure:
  Funds:
    fund: null
    investor: null
  Transactions:
    cashflow: null
    distribution: null
  Reports:
    nav_report: null
```

This creates:

```
📁 Funds
   ├── Fund
   └── Investor
📁 Transactions
   ├── Cashflow
   └── Distribution
📁 Reports
   └── Nav Report
```

### Rules

- **Leaf nodes must be lowercase** and match the model class name (e.g., `Fund` → `fund`)
- **Set leaf values to `null`** — the value is not used
- **Nesting** — you can nest groups inside groups for deeper hierarchies:

```yaml
model_structure:
  Portfolio:
    Equity:
      stock: null
      option: null
    Fixed Income:
      bond: null
```

> [!important]
> Models **not listed** in `model_structure` will still appear in the frontend — they are placed in a default group. To control the full sidebar, list all your models.

---

## `model_styling` — Rename Groups

By default, groups appear with the key name you used in `model_structure`. Use `model_styling` to display a different name (with emoji, abbreviations, etc.):

```yaml
model_structure:
  InvestorRelations:
    investor: null
    commitment: null

model_styling:
  InvestorRelations:
    name: "🤝 IR & Commitments"
```

In the frontend sidebar, the group shows as **🤝 IR & Commitments** instead of **InvestorRelations**.

### Multiple Groups

```yaml
model_styling:
  InvestorRelations:
    name: "🤝 IR & Commitments"
  PortfolioMgmt:
    name: "📈 Portfolio"
  BackOffice:
    name: "⚙️ Operations"
```

---

## `untracked_models` — Exclude from History

By default, every `LexModel` gets full bitemporal history tracking. For models where history isn't useful (calculated summaries, temporary data, logs), you can exclude them:

```yaml
untracked_models:
  nav_report: null
  temp_import: null
```

These models will still work normally — they just won't create history records when saved.

> [!tip]
> Good candidates for `untracked_models`:
> - `CalculationModel` subclasses (results can be re-calculated)
> - Temporary import/staging tables
> - Cache or summary models

---

## Full Example

Here's a complete `model_structure.yaml`:

```yaml
model_structure:
  Fund Management:
    fund: null
    investor: null
    commitment: null
  Transactions:
    cashflow: null
    distribution: null
  Calculations:
    nav_report: null
    track_record: null

model_styling:
  Fund Management:
    name: "🏦 Funds & Investors"
  Transactions:
    name: "💶 Cash Flows"
  Calculations:
    name: "📊 Reports"

untracked_models:
  nav_report: null
  track_record: null
```

---

## Where to Place It

The file goes in your **project root**, next to your model files:

```
YourProject/
├── .env
├── .run/
├── model_structure.yaml      ← Here
├── Team.py
├── Employee.py
└── ...
```

LEX discovers it automatically during `Init` — no configuration needed.

---

> **See also:** [[Bitemporal History]] for details on how history tracking works.
