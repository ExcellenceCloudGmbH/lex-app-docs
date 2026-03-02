---
title: "Part 4 — Validation & Permissions"
description: Add business rules and role-based access control
---

# Part 4 — Validation & Permissions

[[Tutorial Overview]] / Part 4

---

## What We're Adding

Two things that turn a data entry form into a **real business application**:

1. **Validation** — Prevent bad data from being saved
2. **Permissions** — Control who sees what

---

## Step 1: Add Pre-Validation to Expense

Open `Expense.py` in PyCharm and add a `pre_validation` method to your `Expense` class:

```python
class Expense(LexModel):
    # ... existing fields ...

    def pre_validation(self):
        """Block invalid expenses before they are saved."""
        if self.amount <= 0:
            raise ValueError("Expense amount must be positive.")

        if self.amount > 10000:
            raise ValueError(
                "Expenses over €10,000 require manual approval. "
                "Please contact the CFO."
            )
```

### Try It Out

1. Select **"Start"** in PyCharm → click ▶️
2. Navigate to **Expense**
3. Try to create an expense with amount **-50** → ❌ Blocked!
4. Try to create an expense with amount **15000** → ❌ Blocked!
5. Create one with amount **250** → ✅ Saved!

The error message appears directly in the UI. No data is written to the database when validation fails.

---

## Step 2: Add Permissions to Expense

First, update the import at the top of `Expense.py`:

```python
from lex.core.models.LexModel import LexModel, UserContext, PermissionResult
```

Then add these methods to your `Expense` class:

```python
class Expense(LexModel):
    # ... existing fields and pre_validation ...

    def permission_read(self, user_context: UserContext) -> PermissionResult:
        """
        - Employees see only their own expenses
        - Managers see their team's expenses
        - CFO sees everything
        """
        if user_context.is_superuser:
            return PermissionResult.allow_all()

        # CFO sees everything
        if "cfo" in user_context.groups:
            return PermissionResult.allow_all()

        # Managers see their team's expenses
        if "manager" in user_context.groups:
            if self.employee.team.manager_email == user_context.email:
                return PermissionResult.allow_all()

        # Employees see only their own
        if self.employee.email == user_context.email:
            return PermissionResult.allow_all()

        return PermissionResult.deny("You can only view your own expenses.")

    def permission_delete(self, user_context: UserContext) -> bool:
        """Only managers and CFO can delete expenses."""
        if user_context.is_superuser:
            return True
        return "manager" in user_context.groups or "cfo" in user_context.groups
```

---

## How Permissions Work

| User Role | Can See | Can Delete |
|---|---|---|
| **Employee** | Only their own expenses | ❌ No |
| **Manager** | Their team's expenses | ✅ Yes |
| **CFO** | All expenses across all teams | ✅ Yes |
| **Superuser** | Everything | ✅ Yes |

The permissions are checked **automatically** by the framework on every API request and frontend interaction. You don't need any middleware or decorators.

---

## Step 3: Sync Permissions

Select **"Init"** in PyCharm → click ▶️.

This syncs your model permissions to Keycloak. You can then assign users to groups (`employee`, `manager`, `cfo`) through the admin dashboard.

<details>
<summary>💻 Terminal alternative</summary>

```powershell
python -m lex Init
```

</details>

---

## How It Looks

When **Anna** (Role: employee, Design team) logs in, she sees:

| Description | Amount | Category |
|---|---|---|
| Flight to Munich | €450.00 | Travel |
| Team lunch with client | €85.00 | Meals |
| Figma Annual License | €180.00 | Software |

When **Thomas** (Role: manager, Design team) logs in, he sees **all Design expenses**:

| Description | Amount | Category | Employee |
|---|---|---|---|
| Flight to Munich | €450.00 | Travel | Anna Schmidt |
| Adobe Creative Suite | €720.00 | Software | Max Weber |
| Team lunch with client | €85.00 | Meals | Anna Schmidt |
| Figma Annual License | €180.00 | Software | Anna Schmidt |
| Train to Berlin | €120.00 | Travel | Max Weber |

When the **CFO** logs in, they see everything across all teams.

<!-- 📸 TODO: Screenshots comparing employee view vs manager view -->

---

## ✅ Checkpoint

At this point you have:
- [x] Validation rules that block bad data
- [x] Role-based permissions (employee, manager, CFO)
- [x] Keycloak integration for group management

---

> **Next:** [[Part 5 — Streamlit Dashboards]] — Build interactive visual dashboards →
