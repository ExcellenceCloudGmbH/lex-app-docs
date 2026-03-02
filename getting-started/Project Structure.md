---
title: Project Structure
description: Understanding the LEX flat project layout and environment requirements
---

# Project Structure

[[Home]] / [[Getting Started]] / Project Structure

---

## Flat Layout

LEX uses a flat project structure — all model files and configuration live directly at the project root. One file per model class.

```
YourProject/
├── .env                        ← Environment config
├── .run/                       ← PyCharm run configs (generated)
│   ├── Init.run.xml
│   └── Start.run.xml
├── migrations/                 ← Django migrations
├── Tests/
│   ├── basic_test/
│   │   └── test_data.json
│   └── UploadFiles/
├── model_structure.yaml        ← Frontend sidebar layout (optional)
├── requirements.txt
├── _authentication_settings.py ← Test data + group config
├── Team.py                     ← One file per model
├── Employee.py
├── Expense.py
└── BudgetSummary.py
```

| Benefit | Explanation |
|---|---|
| **Simpler navigation** | No nested app folders — models are at the root |
| **Shorter imports** | `from lex.core.models...` for framework classes |
| **Cleaner CI/CD** | No path gymnastics in deployment scripts |
| **Easier onboarding** | New team members find things faster |

---

## Environment Requirements

### Python & Django

| Package | Required Version | Notes |
|---|---|---|
| **Python** | 3.12 | Required for type hints and performance improvements |
| **Django** | 5.x | Stricter timezone handling (see below) |

### Pandas & Numpy

These are **no longer bundled** as `lex-app` dependencies, but V2 is fully compatible with their latest versions.

> [!warning]
> Legacy versions of Pandas and Numpy are **no longer supported**. If your project uses them, you must upgrade to current versions.

Verify your environment:
```bash
pip list | grep -E "django|pandas|numpy"
```

---

## Django 5.x Timezone Changes

Django 5.x enforces stricter timezone handling. All datetime objects must be **timezone-aware**.

If you see this warning:
```
RuntimeWarning: DateTimeField received a naive datetime
```

Here's the fix:

```python
# ❌ OLD (V1 / Django < 5.0) — NO LONGER WORKS
from django.utils.datetime_safe import datetime
current_time = datetime.now()

# ✅ NEW (V2 / Django 5.x) — CORRECT
from django.utils import timezone
current_time = timezone.now()
```

> [!important]
> The `django.utils.datetime_safe` module has been **removed** in Django 5.0. Replace all usages with `django.utils.timezone`.

---

## Third-Party Package Updates

When upgrading, some packages may have breaking changes. Recommended approach:

1. **Review changelogs** for packages you depend on:
   - [Pandas changelog](https://pandas.pydata.org/docs/whatsnew/)
   - [Numpy changelog](https://numpy.org/doc/stable/release.html)
2. **Run your test suite** after upgrading
3. **Update deprecated API calls** following the official documentation

---

> **Next:** [[Running Your App]] →
