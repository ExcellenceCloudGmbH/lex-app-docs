---
title: Streamlit Dashboards
---

LEX lets you attach interactive [Streamlit](https://docs.streamlit.io/) dashboards directly to your models. These dashboards appear in the frontend UI and can display charts, tables, forms, or any [Streamlit](https://docs.streamlit.io/) widget.

There are two levels of dashboards:

| Level | Method | When It Shows |
|---|---|---|
| **Table-level** | `streamlit_class_main(cls)` | When viewing the model's table (list view) |
| **Record-level** | `streamlit_main(self)` | When viewing a specific record (detail view) |

## Table-Level Dashboard

A `@classmethod` that receives the model class. Use it for aggregate views — summaries, charts across all records, filtered tables.

```python title="Expense.py"
import streamlit as st
from lex.core.models.LexModel import LexModel
from django.db import models


class Expense(LexModel):
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    @classmethod
    def streamlit_class_main(cls):
        st.header("Expense Overview")

        expenses = cls.objects.all().values('category', 'amount')
        import pandas as pd
        df = pd.DataFrame(expenses)

        st.bar_chart(df.groupby('category')['amount'].sum())
        st.dataframe(df)
```

<!-- 📸 TODO: Add screenshot of Streamlit icon in the frontend table view -->

## Record-Level Dashboard

An instance method that receives `self`. Use it for record-specific visualizations — history charts, related data, drill-downs.

```python title="Quarter.py"
class Quarter(LexModel):
    name = models.CharField(max_length=50)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    def streamlit_main(self):
        st.header(f"Dashboard: {self.name}")

        expenses = Expense.objects.filter(quarter=self).values('category', 'amount')
        df = pd.DataFrame(expenses)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Spent", f"€{df['amount'].sum():,.2f}")
        with col2:
            st.metric("Remaining", f"€{self.budget - df['amount'].sum():,.2f}")

        st.bar_chart(df.groupby('category')['amount'].sum())
```

## Running Streamlit

Streamlit dashboards run as a separate process alongside your LEX application. See [[running your app]] for how to start the Streamlit server.

> [!note]
> When running Streamlit standalone via the terminal, you must set `PROXY_MODE=true` so Streamlit can connect to your Django backend.

## Tips

- Use `st.cache_data` for expensive queries to keep dashboards responsive
- Use `st.columns()` for side-by-side layouts
- Any Streamlit widget works — `st.plotly_chart()`, `st.map()`, `st.selectbox()`, etc.
- Record-level dashboards have full access to `self` and can query related models
