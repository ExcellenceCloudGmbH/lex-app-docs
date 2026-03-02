---
title: LexLogger API
description: Complete method reference for the LexLogger class
---

# LexLogger API Reference

[[Home]] / Reference / LexLogger API

---

## Import

```python
from lex.audit_logging.handlers.LexLogger import LexLogger
```

---

## Usage Pattern

LexLogger uses a **builder pattern** — chain methods, then call `.log()`:

```python
LexLogger() \
    .add_heading("My Report") \
    .add_text("Everything looks good.") \
    .log()  # ← REQUIRED — saves to database
```

> [!warning]
> **Always end with `.log()`** — without it, nothing is written to the database.

---

## Method Reference

### Text Content

| Method | Description | Example |
|---|---|---|
| `.add_text(text)` | Add a plain text paragraph | `.add_text("Processing complete")` |
| `.add_heading(text, level=1)` | Add a heading (h1–h6) | `.add_heading("Summary", level=2)` |
| `.add_quote(text)` | Add a blockquote | `.add_quote("Important note")` |
| `.add_raw_markdown(md)` | Add raw markdown string | `.add_raw_markdown("**bold** text")` |

### Data Display

| Method | Description | Example |
|---|---|---|
| `.add_table(headers, rows)` | Add a markdown table | See example below |
| `.add_dataframe(df)` | Add a Pandas DataFrame as a table | `.add_dataframe(my_df)` |
| `.add_code(code, language="")` | Add a fenced code block | `.add_code(json_str, language="json")` |
| `.add_list(items, ordered=False)` | Add a bullet or numbered list | `.add_list(["A", "B", "C"])` |

### Media & Links

| Method | Description | Example |
|---|---|---|
| `.add_link(text, url)` | Add a hyperlink | `.add_link("Docs", "https://...")` |
| `.add_image(alt, url)` | Add an image | `.add_image("Chart", "/path/to/img.png")` |
| `.add_horizontal_rule()` | Add a horizontal separator | `.add_horizontal_rule()` |

### Finalize

| Method | Description |
|---|---|
| `.log()` | **Commit everything to the database** — always required |

---

## Examples

### Table

```python
headers = ["Invoice", "Amount", "Status"]
rows = [
    ["INV-001", "€500.00", "Paid"],
    ["INV-002", "€1,200.00", "Pending"],
    ["INV-003", "€750.00", "Overdue"],
]

LexLogger().add_heading("Invoice Summary") \
           .add_table(headers, rows) \
           .log()
```

### DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
    'Revenue': [100000, 120000, 115000, 130000]
})

LexLogger().add_text("Quarterly Revenue:") \
           .add_dataframe(df) \
           .log()
```

### JSON / Code Block

```python
import json

config = {"tax_rate": 0.19, "currency": "EUR"}

LexLogger().add_text("Config:") \
           .add_code(json.dumps(config, indent=2), language="json") \
           .log()
```

### Mixed Report

```python
LexLogger() \
    .add_heading("Migration Report", level=1) \
    .add_text("Migration completed successfully.") \
    .add_horizontal_rule() \
    .add_heading("Summary", level=2) \
    .add_table(
        ["Model", "Rows", "Status"],
        [
            ["Invoice", "1,234", "✅ Migrated"],
            ["Payment", "567", "✅ Migrated"],
        ]
    ) \
    .add_heading("Notes", level=2) \
    .add_list(["No errors encountered", "All constraints valid"]) \
    .log()
```

---

## Context-Aware Logging

LexLogger **automatically resolves** execution context:

| Context | Resolved Automatically |
|---|---|
| Calculation ID | Linked to the correct `CalculationLog` entry |
| Model instance | Identifies which model is executing |
| Parent/child | Nested calculations linked properly |

You never need to pass context manually.

### Nested Calculations

```python
from lex.audit_logging.utils.ModelContext import model_logging_context

# Inside parent model
def calculate(self):
    LexLogger().add_text("Starting parent").log()

    child = ChildModel.objects.filter(quarter=self.quarter).first()
    with model_logging_context(child):
        child.is_calculated = "IN_PROGRESS"
        child.save()

    LexLogger().add_text("Child done.").log()
```

---

*See also: [[../guides/Logging|Logging Guide]]*
