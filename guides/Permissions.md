---
title: Permissions
description: Fine-grained field-level and row-level access control with UserContext
---

# Permissions

[[Home]] / Guides / Permissions

---

## Overview

LEX provides **fine-grained access control** through permission methods defined directly on your models. You can control:

- **Which fields** a user can view, edit, or export
- **Which records** a user can see (row-level filtering)
- **Which actions** a user can perform (create, delete, list)

All permission methods receive a clean `UserContext` dataclass and integrate with **Keycloak** for scope-based authorization.

---

## The UserContext Object

All permission methods receive a `UserContext` with clean user information:

```python
@dataclass(frozen=True)
class UserContext:
    user: Any              # Django User object
    email: str             # User's email address
    is_authenticated: bool # Is user logged in?
    is_superuser: bool     # Is user a superuser?
    groups: Set[str]       # Group names, e.g. {'admin', 'finance'}
    keycloak_scopes: Set[str]  # Keycloak permission scopes
```

---

## Basic Example

```python
from lex.core.models.LexModel import LexModel, UserContext, PermissionResult
from django.db import models


class MyModel(LexModel):
    name = models.CharField(max_length=100)
    sensitive_field = models.CharField(max_length=100)
    owner_email = models.EmailField()

    def permission_read(self, user_context: UserContext) -> PermissionResult:
        """Controls which fields users can view."""
        if user_context.is_superuser:
            return PermissionResult.allow_all()

        if 'admin' in user_context.groups:
            return PermissionResult.allow_all()

        # Regular users can't see sensitive data
        return PermissionResult.allow_all_except({'sensitive_field'})

    def permission_delete(self, user_context: UserContext) -> bool:
        """Controls if user can delete this record."""
        return user_context.is_superuser or self.owner_email == user_context.email
```

---

## Permission Methods Reference

### Field-Level Methods (return `PermissionResult`)

| Method | Purpose |
|---|---|
| `permission_read(user_context)` | Controls which fields the user can **view** |
| `permission_edit(user_context)` | Controls which fields the user can **modify** |
| `permission_export(user_context)` | Controls which fields the user can **export** |

### Action-Level Methods (return `bool`)

| Method | Purpose |
|---|---|
| `permission_create(user_context)` | Can user **create** new instances? |
| `permission_delete(user_context)` | Can user **delete** this instance? |
| `permission_list(user_context)` | Can user **list** instances of this model? |

### `PermissionResult` Factory Methods

| Method | Behavior |
|---|---|
| `PermissionResult.allow_all()` | Allow access to all fields |
| `PermissionResult.allow_fields({'a', 'b'})` | Allow only specific fields |
| `PermissionResult.allow_all_except({'x'})` | Allow all except specified fields |
| `PermissionResult.deny()` | Deny access entirely |

---

## Real-World Examples

### Example 1: HR Salary Visibility (Field-Level)

Only HR managers can see the salary field:

```python
class EmployeeContract(LexModel):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # Sensitive!

    def permission_read(self, user_context: UserContext) -> PermissionResult:
        """HR Managers see everything, others don't see salary."""
        if 'hr_manager' in user_context.groups or user_context.is_superuser:
            return PermissionResult.allow_all()

        # Hide salary for everyone else
        return PermissionResult.allow_all_except({'salary'})
```

### Example 2: Expense Reports — Record Ownership (Row-Level)

Finance sees all reports, employees see only their own:

```python
class ExpenseReport(LexModel):
    employee_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def permission_read(self, user_context: UserContext) -> PermissionResult:
        """Finance sees all, employees see only their own."""
        if 'finance_manager' in user_context.groups:
            return PermissionResult.allow_all()

        # Owner sees their own records
        if self.employee_email == user_context.email:
            return PermissionResult.allow_all()

        # Others see nothing (row hidden)
        return PermissionResult.allow_fields(set())
```

---

## Keycloak Integration

By default, permission methods fall back to Keycloak scopes. You can also use Keycloak scopes in your custom logic:

```python
def permission_read(self, user_context: UserContext) -> PermissionResult:
    if 'read' in user_context.keycloak_scopes:
        return PermissionResult.allow_all()
    return PermissionResult.deny("No read permission in Keycloak")
```

After running `lex Init`, your models are synced to Keycloak. Manage permissions at [excellence-cloud.de](https://excellence-cloud.de).

---

<details>
<summary>🔄 Migrating from V1?</summary>

If you're migrating from `ModificationRestriction`, here's what changes:

| Aspect | V1 (Old) | Current |
|---|---|---|
| **Approach** | Separate `ModificationRestriction` class | Permission methods directly on your model |
| **User info** | Raw `user` object + `violations` list | Clean `UserContext` dataclass |
| **Granularity** | Model-level only | **Field-level** and **row-level** |
| **Return type** | Boolean + side-effect list | `PermissionResult` (fields) or `bool` (actions) |
| **Keycloak** | Manual integration | Built-in scope resolution |

### V1 Example

```python
from generic_app.generic_models.ModelModificationRestriction import ModelModificationRestriction

class MyRestriction(ModelModificationRestriction):
    def can_read_in_general(self, user, violations):
        return True
    def can_modify_in_general(self, user, violations):
        if 'admin' not in user.groups:
            violations.append("Only admins can modify")
            return False
        return True

class MyModel(LexModel):
    modification_restriction = MyRestriction()
```

### Migration Checklist

- [ ] Remove `ModificationRestriction` class definitions
- [ ] Remove `modification_restriction = MyRestriction()` from models
- [ ] Add `permission_*` methods directly to your model
- [ ] Replace `user` parameter with `UserContext`
- [ ] Replace return values with `PermissionResult` or `bool`
- [ ] Run `lex Init` to sync new permission scopes to Keycloak

</details>

---

> **Guides complete!** For database migration automation, see [[../migration-workflow/Migration Workflow Overview|Migration Workflow Overview]].
