---
title: Serializers
---

LEX automatically generates a REST API for every model. By default, all fields are exposed as-is. When you need custom validation, computed fields, or different views of the same model, you create a `serializers.py` file using [Django REST Framework](https://www.django-rest-framework.org/api-guide/serializers/).

## How It Works

1. Create a `serializers.py` file in the same folder as your model
2. Define one or more serializer classes
3. Attach them to your model via `Model.api_serializers`

The framework picks them up automatically — no registration or configuration needed.

## Basic Example

```python title="Upload/serializers.py"
from rest_framework import serializers
from lex.api.views.model_entries.mixins.PermissionAwareSerializerMixin import add_permission_checks

from Upload.Quarter import Quarter


@add_permission_checks
class QuarterDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = '__all__'


Quarter.api_serializers = {
    'default': QuarterDefaultSerializer,
}
```

> [!tip]
> The `@add_permission_checks` decorator integrates your serializer with the [[features/access-and-ui/permissions|permission system]]. It ensures that field-level permissions from `permission_read()` and `permission_edit()` are enforced on the API level too.

## Field-Level Validation

Add `validate_<fieldname>` methods to enforce rules on individual fields:

```python title="Upload/serializers.py"
from django.utils import timezone
from rest_framework import serializers


@add_permission_checks
class QuarterDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = '__all__'

    def validate_name(self, value):
        """Name must not be blank."""
        if not value or not value.strip():
            raise serializers.ValidationError("Name cannot be blank.")
        return value

    def validate_report_date(self, value):
        """Report date must not be in the future."""
        if value > timezone.now():
            raise serializers.ValidationError("Report date cannot be in the future.")
        return value
```

When validation fails, the error message appears directly in the frontend UI.

## Object-Level Validation

Use `validate()` to enforce rules that span multiple fields:

```python
    def validate(self, attrs):
        """Locked quarters must have a report date."""
        locked = attrs.get('locked', False)
        report_date = attrs.get('report_date')
        if locked and report_date is None:
            raise serializers.ValidationError({
                'report_date': "Locked quarters must have a report date."
            })
        return attrs
```

## Multiple Serializer Views

You can define multiple serializers for the same model — for example, a default view and a more detailed view:

```python title="Cashflows/serializers.py"
from rest_framework import serializers

from Cashflows.InvestorCashflow import InvestorCashflow


class InvestorCashflowDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorCashflow
        fields = '__all__'


class InvestorCashflowDetailSerializer(serializers.ModelSerializer):
    extra_info = serializers.CharField(read_only=True)

    class Meta:
        model = InvestorCashflow
        fields = ['id', 'investor', 'vehicle', 'amount_eur',
                  'transaction_date', 'extra_info']


InvestorCashflow.api_serializers = {
    'default': InvestorCashflowDefaultSerializer,
    'detail': InvestorCashflowDetailSerializer,
}
```

| Key | When It's Used |
|---|---|
| `'default'` | List view and standard API calls |
| `'detail'` | Detail view when a specific record is opened |
| `'tree'` | Tree/hierarchical views |

## Where to Put `serializers.py`

Place the file in the same folder as the models it serializes:

```
Upload/
├── __init__.py
├── Quarter.py
├── UploadBalanceSheet.py
└── serializers.py         ← serializers for Upload models
```

> [!note]
> You don't *have* to create serializers. Without them, LEX generates a default serializer that exposes all fields. Custom serializers are for when you need validation, computed fields, or restricted views.

For more on the REST API and [Django REST Framework](https://www.django-rest-framework.org/), see the official DRF documentation.
