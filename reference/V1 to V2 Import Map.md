---
title: V1 to V2 Import Map
description: Complete find-and-replace table for updating V1 imports to V2
---

# V1 → V2 Import Map

[[Home]] / Reference / Import Map

---

Quick-reference table for updating imports. Use your IDE's **Find and Replace in Files** (`Ctrl+Shift+R`).

## Model Base Classes

| Find (V1) | Replace With (V2) |
|---|---|
| `from generic_app.generic_models.upload_model import ConditionalUpdateMixin` | `from lex.core.models.CalculationModel import CalculationModel` |
| `from generic_app.generic_models.upload_model import UploadModelMixin` | `from lex.core.models.LexModel import LexModel` |
| `class MyModel(ConditionalUpdateMixin):` | `class MyModel(CalculationModel):` |
| `class MyModel(UploadModelMixin):` | `class MyModel(LexModel):` |

## Field & Model Imports

| Find (V1) | Replace With (V2) |
|---|---|
| `from generic_app import models` | `from django.db import models` |

## Logging

| Find (V1) | Replace With (V2) |
|---|---|
| `from generic_app.submodels.CalculationLog import CalculationLog` | `from lex.audit_logging.handlers.LexLogger import LexLogger` |
| `CalculationLog.create(...)` | `LexLogger().add_text(...).log()` |

## Permissions

| Find (V1) | Replace With (V2) |
|---|---|
| `from generic_app.generic_models.ModelModificationRestriction import ModelModificationRestriction` | *(remove — use permission methods on model)* |
| `modification_restriction = MyRestriction()` | *(remove — add `permission_*` methods instead)* |

## User Context

| Find (V1) | Replace With (V2) |
|---|---|
| `from generic_app.rest_api.views.model_entries.One import user_name, user_email` | *(remove — automatic in V2)* |

## Method Names

| Find (V1) | Replace With (V2) |
|---|---|
| `def update(self):` (on ConditionalUpdateMixin subclass) | `def calculate(self):` |
| `@ConditionalUpdateMixin.conditional_calculation` | *(remove decorator entirely)* |
| `def update(self):` (on UploadModelMixin subclass) | `@hook(AFTER_CREATE)` + rename to descriptive name |

## Lifecycle Hooks (New Import)

```python
# Add this import for lifecycle hooks:
from django_lifecycle import hook, AFTER_CREATE, AFTER_UPDATE, BEFORE_SAVE
```

---

*See also: [[../guides/Import Migration|Import Migration Guide]]*
