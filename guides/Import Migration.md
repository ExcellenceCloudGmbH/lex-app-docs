---
title: Import Migration
description: Update your import statements from V1 to V2 — a quick find-and-replace guide
---

# Import Migration

[[Home]] / Guides / Import Migration

> [!note]
> **This guide is for teams migrating from V1 (generic_app).** If you're starting a new project, you can skip this — just use the current import paths shown in the other guides.

---

## What You Need to Do

Replace old `generic_app` imports with their V2 equivalents throughout your codebase. This is mostly a **find-and-replace** task.

> [!tip]
> Use your IDE's "Find and Replace in Files" feature (`Ctrl+Shift+R` in PyCharm) to do this quickly.

---

## The Complete Import Map

| V1 Import (Old) | V2 Import (New) |
|---|---|
| `from generic_app.generic_models.upload_model import UploadModelMixin` | `from lex.core.models.LexModel import LexModel` |
| `from generic_app.generic_models.upload_model import ConditionalUpdateMixin` | `from lex.core.models.CalculationModel import CalculationModel` |
| `from generic_app import models` | `from django.db import models` |
| `from generic_app.submodels.CalculationLog import CalculationLog` | `from lex.audit_logging.handlers.LexLogger import LexLogger` |
| `from generic_app.generic_models.ModelModificationRestriction import ModelModificationRestriction` | *(removed — use permission methods directly on your model)* |
| `from generic_app.rest_api.views.model_entries.One import user_name, user_email` | *(removed — user context is automatic in V2)* |

---

## Full Example

Here's a real model transformation:

### Before (V1)

```python
from generic_app.generic_models.upload_model import UploadModelMixin
from generic_app.generic_models.upload_model import ConditionalUpdateMixin
from generic_app import models
from generic_app.submodels.CalculationLog import CalculationLog


class MyModel(ConditionalUpdateMixin):
    name = models.CharField(max_length=100)
```

### After (V2)

```python
from lex.core.models.CalculationModel import CalculationModel
from lex.audit_logging.handlers.LexLogger import LexLogger
from django.db import models


class MyModel(CalculationModel):
    name = models.CharField(max_length=100)
```

---

## Critical Rule: Never Import `models` from `generic_app`

This is the most common mistake during migration:

```python
# ❌ DELETE this — no longer exists
from generic_app import models

# ✅ USE this instead (for all field types)
from django.db import models
```

This applies to **all** model field definitions: `CharField`, `IntegerField`, `ForeignKey`, `FileField`, etc.

---

## User Context Is Now Automatic

In V1, some projects accessed user context via global variables:

```python
# ❌ V1: Manual user context (OLD — REMOVE)
from generic_app.rest_api.views.model_entries.One import user_name, user_email

class Invoice(ConditionalUpdateMixin):
    def update(self):
        self.modified_by = user_name  # manual tracking
        self.save()
```

In V2, `LexModel` **automatically tracks** `created_by` and `edited_by`. You don't need to do anything:

```python
# ✅ V2: Automatic user context (NEW)
from lex.core.models.CalculationModel import CalculationModel

class Invoice(CalculationModel):
    def calculate(self):
        # created_by and edited_by are set automatically!
        self.total = self.calculate_total()
```

---

## Test JSON Path Changes

Due to the flat project structure, file paths in test JSON files have changed:

| V1 Path | V2 Path |
|---|---|
| `ProjectName/Tests/...` | `Tests/...` |

The test data file path is configured in `_authentication_settings.py`:

```python
# _authentication_settings.py
initial_data_load = "Tests/basic_test/test_data.json"
azure_groups = ["finance_team", "auditors"]
```

> [!note]
> The path is now relative to the **project root** (flat structure), not nested inside a project folder.

---

## Migration Checklist

- [ ] Replace all `from generic_app...` imports using the map above
- [ ] Change `from generic_app import models` → `from django.db import models`
- [ ] Remove manual user context imports (`user_name`, `user_email`)
- [ ] Update test JSON file paths to flat-structure format
- [ ] Search for any remaining `generic_app` references

---

> **Next:** [[Calculations]] →
