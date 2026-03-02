---
title: Logging
description: Rich, context-aware logging with the LexLogger builder pattern
---

# Logging

[[Home]] / Guides / Logging

---

## Overview

**LexLogger** is a builder-pattern logging API that produces rich, Markdown-formatted log entries. It supports text, headings, tables, DataFrames, code blocks, and more — all stored in the database and displayed in the frontend.

LexLogger is **context-aware**: it automatically links log entries to the correct calculation, model instance, and parent/child hierarchy without any manual ID passing.

---

## Basic Usage

Chain builder methods together, then call `.log()` to save:

```python
from lex.audit_logging.handlers.LexLogger import LexLogger


def calculate(self):
    logger = LexLogger()

    # Simple text logging
    logger.add_text("Processing started").log()

    # Rich formatting with heading
    logger.add_heading("Invoice Summary", level=2) \
          .add_text("Processing completed successfully.") \
          .log()
```

> [!warning]
> **Always call `.log()` at the end of your chain.** Without it, nothing is written to the database!

---

## Real-World Examples

### Logging a Summary Table

```python
headers = ["Invoice ID", "Amount", "Status"]
rows = [
    ["INV-001", "500.00", "Paid"],
    ["INV-002", "1200.00", "Pending"],
    ["INV-003", "750.00", "Overdue"],
]

LexLogger().add_heading("Invoice Summary") \
           .add_table(headers, rows) \
           .log()
```

### Logging a Pandas DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
    'Revenue': [100000, 120000, 115000, 130000]
})

LexLogger().add_text("Quarterly Revenue Report:") \
           .add_dataframe(df) \
           .log()
```

### Logging JSON / Config Data

```python
import json

config = {
    "tax_rate": 0.19,
    "currency": "EUR",
    "fiscal_year": 2024
}

LexLogger().add_text("Current Configuration:") \
           .add_code(json.dumps(config, indent=2), language="json") \
           .log()
```

---

## Context-Aware Logging

LexLogger **automatically resolves** the current execution context — you don't need to pass IDs manually:

| Context | How It Works |
|---|---|
| **Calculation ID** | Links logs to the correct `CalculationLog` entry |
| **Model Instance** | Identifies which model is currently executing |
| **Parent/Child** | Links nested calculations properly |

---

## Nested Calculations (Parent/Child Logging)

When a parent calculation triggers a child, use `model_logging_context` to maintain the log hierarchy:

```python
from lex.audit_logging.utils.ModelContext import model_logging_context


class ParentCalculation(CalculationModel):
    def calculate(self):
        LexLogger().add_text("Starting Parent Calculation").log()

        # Find the child model
        child = CalculateNAV.objects.filter(quarter=self.quarter).first()

        # Wrap child execution in context manager
        with model_logging_context(child):
            child.is_calculated = "IN_PROGRESS"
            child.save()

        # Continue with parent logic
        LexLogger().add_text("Child calculation finished.").log()
```

This ensures logs from the child calculation appear **nested under the parent** in the UI.

---

## Full API Reference

See [[../reference/LexLogger API|LexLogger API Reference]] for the complete method list.

---

<details>
<summary>🔄 Migrating from V1?</summary>

If you're migrating from `CalculationLog.create()`, here's what changes:

| Aspect | V1 (Old) | Current |
|---|---|---|
| **API** | `CalculationLog.create(...)` | `LexLogger()` builder pattern |
| **Formatting** | Plain text only | Rich Markdown (tables, code, headings) |
| **Context** | Manual — pass IDs yourself | Automatic — resolved from call stack |
| **Nested calculations** | Not supported | Built-in parent/child hierarchy |

### V1 Example

```python
from generic_app.submodels.CalculationLog import CalculationLog

def update(self):
    CalculationLog.create(CalculationLog.START + "Processing started")
    # ... business logic ...
    CalculationLog.create(CalculationLog.SUCCESS + "Processing complete")
```

### Migration Checklist

- [ ] Replace all `CalculationLog.create(...)` calls with `LexLogger()`
- [ ] Remove manual context/ID passing
- [ ] Use the builder pattern (`add_*` methods) for formatting
- [ ] Always end chains with `.log()`
- [ ] For nested calculations, wrap child execution with `model_logging_context()`

</details>

---

> **Next:** [[Permissions]] →
