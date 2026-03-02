---
title: "Part 5 — Streamlit Dashboards"
description: Build interactive visual dashboards
---

# Part 5 — Streamlit Dashboards

[[Tutorial Overview]] / Part 5

---

## What We're Adding

Two interactive dashboards, both added directly to `BudgetSummary.py`:

| Dashboard | Level | What It Shows |
|---|---|---|
| **Company Overview** | Table-level (`streamlit_class_main`) | All teams' budgets side-by-side |
| **Team Deep-Dive** | Record-level (`streamlit_main`) | One team's expenses in detail |

---

## Step 1: Add Imports

Open `BudgetSummary.py` in PyCharm and add these imports at the top of the file:

```python
import streamlit as st
import pandas as pd
```

---

## Step 2: Add the Table-Level Dashboard

Add this **class method** to your `BudgetSummary` class (after `calculate()`):

```python
    @classmethod
    def streamlit_class_main(cls):
        """Company-wide budget overview — all teams at a glance."""
        st.title("📊 Company Budget Overview")

        summaries = cls.objects.select_related("team").filter(
            is_calculated="SUCCESS"
        )

        if not summaries.exists():
            st.warning(
                "No budget summaries calculated yet. "
                "Run calculations first."
            )
            return

        # Build DataFrame
        data = []
        for s in summaries:
            data.append({
                "Team": s.team.name,
                "Quarter": s.quarter,
                "Budget": float(s.team.budget),
                "Spent": float(s.total_expenses),
                "Remaining": float(s.remaining_budget),
                "Utilization %": float(s.utilization_pct),
                "Status": "🔴 Over" if s.is_over_budget else "🟢 OK",
            })
        df = pd.DataFrame(data)

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Budget", f"€{df['Budget'].sum():,.0f}")
        col2.metric("Total Spent", f"€{df['Spent'].sum():,.0f}")
        col3.metric(
            "Overall Utilization",
            f"{(df['Spent'].sum() / df['Budget'].sum() * 100):.1f}%",
        )

        # Bar chart
        st.subheader("Budget vs Actual by Team")
        chart_df = df.groupby("Team")[["Budget", "Spent"]].sum()
        st.bar_chart(chart_df)

        # Data table
        st.subheader("Detailed Breakdown")
        st.dataframe(df, use_container_width=True)
```

> [!tip]
> `streamlit_class_main` is a **`@classmethod`** — it shows when users open the Streamlit page for the BudgetSummary **table** (no specific record selected).

---

## Step 3: Add the Record-Level Dashboard

Add this **instance method** below `streamlit_class_main`:

```python
    def streamlit_main(self, user=None):
        """Single team's budget detail with expense breakdown."""
        st.title(f"📋 {self.team.name} — {self.quarter}")

        # Key metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Expenses", f"€{self.total_expenses:,.2f}")
        col2.metric("Remaining Budget", f"€{self.remaining_budget:,.2f}")
        col3.metric(
            "Utilization",
            f"{self.utilization_pct:.1f}%",
            delta="Over Budget!" if self.is_over_budget else None,
            delta_color="inverse",
        )

        # Breakdown by category
        expenses = Expense.objects.filter(
            employee__team=self.team,
            quarter=self.quarter,
        )

        if expenses.exists():
            st.subheader("Expenses by Category")
            cat_data = (
                expenses.values("category")
                .annotate(total=models.Sum("amount"))
                .order_by("-total")
            )
            cat_df = pd.DataFrame(cat_data)
            cat_df.columns = ["Category", "Amount"]
            st.bar_chart(cat_df.set_index("Category"))

            st.subheader("All Expenses")
            exp_data = expenses.values(
                "description", "amount", "category", "date",
                "employee__first_name", "employee__last_name",
            ).order_by("-date")
            exp_df = pd.DataFrame(exp_data)
            exp_df.columns = [
                "Description", "Amount", "Category", "Date",
                "First Name", "Last Name",
            ]
            exp_df["Submitted By"] = (
                exp_df["First Name"] + " " + exp_df["Last Name"]
            )
            exp_df = exp_df.drop(columns=["First Name", "Last Name"])
            st.dataframe(exp_df, use_container_width=True)
        else:
            st.info("No expenses recorded for this period.")
```

---

## Step 4: Try It Out

### Start Streamlit

Select **"Streamlit"** from the run configuration dropdown in PyCharm → click ▶️.

<details>
<summary>💻 Terminal alternative</summary>

```powershell
python -m lex streamlit
```

</details>

### View the Table-Level Dashboard

In the frontend, navigate to **BudgetSummary** and click the **Streamlit icon** 📊 in the toolbar (not on a specific record). This opens the company-wide overview.

### View the Record-Level Dashboard

Click the **Streamlit icon** 📊 on a **specific BudgetSummary record**. This opens the team deep-dive with per-category breakdowns.

<!-- 📸 TODO: Screenshots of both dashboard levels -->

---

## ✅ Checkpoint

At this point you have:
- [x] Company-wide budget dashboard with charts
- [x] Per-team deep-dive with expense breakdowns
- [x] Everything interactive — Streamlit updates in real time

---

> **Next:** [[Part 6 — History in Action]] — See bitemporal tracking come to life →
