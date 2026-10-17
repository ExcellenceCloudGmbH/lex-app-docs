---
title: "Read Models"
---

Overviews, dashboards and many lists are not one table: a join, a union, the answer of a database function, or one table shown another way. A **read model** serves such rows on the generic list and record endpoints — filtered, sorted, paged and exported like any model — and refuses every write.

> [!note]
> Since Lex App 3.0.

There are two kinds: a database **view**, and a **projection** of a model you already have.

## A view

```python title="Reports/InvoiceSummary.py"
from django.db import models
from lex.core.models.LexReadModel import LexReadModel


class InvoiceSummary(LexReadModel):
    id = models.IntegerField(primary_key=True)
    customer = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    overdue = models.BooleanField()

    class Meta:
        managed = False
```

`LexReadModel` is a `LexModel` without Lex App's audit columns (`created_at`, `edited_at`, `created_by`, `edited_by`), which a view does not have. `managed = False` keeps Django from creating a table. The view itself comes from a migration, after the `CreateModel` that `makemigrations` writes for the model:

```python title="migrations/0012_invoicesummary.py"
from django.db import migrations, models
from lex.core.read_models import CreateView


class Migration(migrations.Migration):
    dependencies = [("myproject", "0011_invoice_paid")]   # your project folder is the app label

    operations = [
        migrations.CreateModel(name="InvoiceSummary", fields=[...], options={"managed": False}),  # from makemigrations
        CreateView("InvoiceSummary", """
            SELECT i.id, c.name AS customer, i.total, (i.due_date < now() AND NOT i.paid) AS overdue
            FROM {table:Invoice} i JOIN {table:Customer} c ON c.id = i.customer_id
        """),
    ]
```

`CreateView(model_name, sql, security_invoker=True)` creates the view under the read model's own table name. `{table:Model}` placeholders become the table names Lex App assigns to models of the same app, so the SQL never spells one out. The view needs a column for every field of the model, the primary key included. Reversing the migration drops the view.

On PostgreSQL the view is created `WITH (security_invoker = true)`: it reads its tables with the caller's rights, so their [[ship-and-operate/row-level-security|row-level security]] still decides who sees which rows. Pass `security_invoker=False` only if you mean the view to see past those policies.

## A projection

A projection shows an existing model's rows with its own serializer, its own list selection and computed fields:

```python title="Input/InvoiceCard.py"
from Input.Invoice import Invoice


class InvoiceCard(Invoice):
    lex_read_model = True
    api_serializers = {"default": InvoiceCardSerializer}

    class Meta:
        proxy = True

    @classmethod
    def lex_list_queryset(cls, queryset, request):
        return queryset.exclude(status="archived")
```

A projection inherits the actions of the model it projects; they run on the underlying row.

## What the endpoints do

| | A read model |
|---|---|
| List, filter, sort, page, export, read one record | as for any model |
| Create, update, delete, bulk, `run_step` | 405 |
| History, and `?as_of=` on a list or record | 400 `HISTORY_NOT_TRACKED` |
| [[access-and-dashboards/custom-api#Record actions\|Actions]] | allowed |

No history tables are created for a read model. A model with `lex_read_model = True` that has a table of its own — neither `managed = False` nor `proxy = True` — stops the server at startup.

## Two hooks for any model

**The default selection of a list.** `lex_list_queryset(cls, queryset, request)` narrows what the list endpoint shows when nobody filters — "without archived rows", "newest first". It applies to the list only: a record outside it stays reachable by its id.

**Computed fields for a whole page.** A serializer's `lex_prepare_page(cls, instances, context)` classmethod runs once per list page, before the rows are serialized, and once for a single record. Load what the computed fields need in one query and leave it in `context`:

```python
class InvoiceCardSerializer(serializers.ModelSerializer):
    paid_amount = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceCard
        fields = ["id", "number", "total", "paid_amount"]

    @classmethod
    def lex_prepare_page(cls, instances, context):
        paid = Payment.objects.filter(invoice__in=instances).values("invoice").annotate(sum=Sum("amount"))
        context["paid"] = {row["invoice"]: row["sum"] for row in paid}

    def get_paid_amount(self, invoice):
        return self.context["paid"].get(invoice.pk, 0)
```

Without it, a `SerializerMethodField` that queries runs one query per row.

## See also

- [[model-your-data/serializers]] — the serializer a read model answers with
- [[ship-and-operate/row-level-security]] — policies a `security_invoker` view keeps
