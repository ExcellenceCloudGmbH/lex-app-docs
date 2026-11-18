---
title: Dashboards on Your Models
---

A model can carry its own Reflex dashboards, the same two a model can carry for [[access-and-dashboards/streamlit/dashboards on your models|Streamlit]]: one for a single record and one for the whole table. You add a classmethod, and the dashboard route shows it when the URL names the model.

| Level | Method | Shown for | Returns |
|---|---|---|---|
| **Record-level** | `reflex_main(cls)` | `?model=fund&pk=42` | a component; its state reads the record with `current_record` |
| **Table-level** | `reflex_class_main(cls)` | `?model=fund` | a component |

Both are **classmethods that return a component**, and that is the one real difference from Streamlit's pair. Reflex compiles every page before anyone visits it, so there is no record — and no user — when the method runs. What varies from visit to visit is read at run time by the component's own state, in an event handler: the record the URL names with `current_record`, anything else through the [[access-and-dashboards/reflex/the django orm|Django ORM]].

## Both, in two files

The model says *which* component; a second module holds the component and its state:

```python title="Input/Fund.py"
from django.db import models

from lex.core.models.LexModel import LexModel


class Fund(LexModel):
    name = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @classmethod
    def reflex_main(cls):
        """Record-level: ?model=fund&pk=<id>."""
        from your_repo.Input._fund_dashboard import fund_record

        return fund_record()

    @classmethod
    def reflex_class_main(cls):
        """Table-level: ?model=fund."""
        from your_repo.Input._fund_dashboard import fund_table

        return fund_table()
```

`your_repo` is the project's own package — the name of its folder.

```python title="Input/_fund_dashboard.py"
import reflex as rx

from Input.Fund import Fund
from lex.lex_app.reflex import current_record


class FundRecord(rx.State):
    name: str = ""
    budget: str = ""

    @rx.event
    async def load(self):
        fund = await current_record(self)
        self.name = fund.name if fund else ""
        self.budget = f"{fund.budget:,.2f}" if fund else ""


class FundTable(rx.State):
    funds: list[dict[str, str]] = []

    @rx.event
    async def load(self):
        self.funds = [
            {"name": fund.name, "href": f"/?model=fund&pk={fund.pk}"}
            async for fund in Fund.objects.order_by("name")
        ]


def fund_record() -> rx.Component:
    return rx.vstack(
        rx.heading(FundRecord.name),
        rx.text("Budget: ", FundRecord.budget),
        on_mount=FundRecord.load,
    )


def fund_table() -> rx.Component:
    return rx.vstack(
        rx.heading("Funds"),
        rx.foreach(FundTable.funds, lambda fund: rx.link(fund["name"], href=fund["href"])),
        on_mount=FundTable.load,
    )
```

`on_mount` runs the handler when the dashboard appears, for the user looking at it. The table's rows link to each fund's record dashboard; following one mounts `fund_record`, which reads that fund.

`current_record(self)` returns the record `?model=&pk=` names, fetched through the ORM — the Reflex counterpart of the `self` a `streamlit_main` receives — or `None` when there is no `pk`, or no such record. Pass the class as well, `current_record(self, Fund)`, when one component serves several models' pages.

The ORM reads as the dashboard, not as the user: `current_record` hands any record to anyone who can open the URL. For a record the user should only see when the grid would show it to them, use `LexRecordState`, below.

> [!warning] Keep Reflex states out of Django's model discovery
> Django imports every module of the project in **every** process it starts —
> `lex start`, each Celery worker, `lex init` — to find the models. A state
> class defined in one of those modules is created in all of them, and with it
> Reflex itself. Modules whose names start with an underscore are skipped, so
> put a model's states in one — `Input/_fund_dashboard.py` above — and import it
> inside the method, never at the top of the model's file. Import it under the
> project's package, `from your_repo.Input._fund_dashboard import …`, so it is
> loaded once, under one name. Not with a relative import: from a model in a
> subfolder, `Input/Fund.py`, `from ._dashboards…` looks for `Input/_dashboards`,
> not the project's `_dashboards/`.

## The record, as the user may see it

`LexRecordState` reads the same record, but asks Lex App's API first, as the signed-in user: only if the API shows them the record does the dashboard get it. Beside it, `lex_view` can show Lex App's own record page — its fields, actions and history, as that user may see them:

```python title="Input/_fund_dashboard.py"
import reflex as rx
import rfds

from Input.Fund import Fund
from lex.lex_app.reflex import LexRecordState, lex_view


class FundRecord(LexRecordState):
    model = Fund
    budget: str = ""

    @rx.event
    async def load(self):
        fund = await self.record()
        self.budget = f"{fund.budget:,.2f}" if fund else ""


def fund_record() -> rx.Component:
    return rx.box(
        rx.match(
            FundRecord.record_state,
            ("ok", rx.vstack(
                rx.heading(FundRecord.record_title),
                rx.text("Budget: ", FundRecord.budget),
                lex_view(f"fund/{FundRecord.pk}/show", height=600),
            )),
            ("denied", rfds.inline_message("You may not see this record.", tone="warning")),
            ("missing", rfds.inline_message("This record does not exist.", tone="neutral")),
            ("unavailable", rfds.inline_message("Lex App cannot be reached. Try again shortly.", tone="warning")),
            rfds.spinner(label="Loading"),
        ),
        on_mount=FundRecord.load,
    )
```

`record()` returns the instance, or `None`, and sets `record_state` to `"ok"`, `"denied"`, `"missing"` or — when Lex App could not answer at all — `"unavailable"`, for the page to show. `FundRecord.pk` is the primary key from the URL, as a var, so `lex_view`'s address is put together in the browser for whichever record is open. [[access-and-dashboards/reflex/tables and records#LexRecordState: the record, as the user may see it|Tables & Records]] has the details, and [[access-and-dashboards/reflex/embedding app pages|Embedding App Pages]] everything `lex_view` takes.

`lex reflex add object_page --model Fund` writes a dashboard of this shape for you — see [[access-and-dashboards/reflex/consultant tooling|Consultant Tooling]].

## What the reader sees

| URL | Shows |
|---|---|
| `?model=fund&pk=42` | `Fund.reflex_main()`, with `current_record` returning fund 42 |
| `?model=fund` | `Fund.reflex_class_main()` |
| `?model=fund&pk=42`, and `Fund` defines no `reflex_main` | *No instance-level visualization available for this model.* |
| `?model=fund`, and `Fund` defines no `reflex_class_main` | *No class-level visualization available for this model.* |
| `?model=nope` | *Model 'nope' not found* |
| `?model=fund&pk=999`, with no such fund | *Object with ID 999 not found* |
| `?model=…&pk=…` for a plain Django model, not a `LexModel` | *This model doesn't support visualization* |
| `?model=…` for a plain Django model | *This model doesn't support class-level visualization* |

The messages are Streamlit's, word for word, so a reader meets one set whichever framework drew the page. `model` is matched case-insensitively against the model's name, as for Streamlit.

## Mistakes are caught when the app compiles

Each model's own methods run once, when `lex reflex` compiles the app, so a broken one stops the app with a message rather than failing in front of a reader:

- **An instance method** — the shape `streamlit_main` has — is refused with *must be a @classmethod returning a Reflex component*. There is no record to call it on.
- **A method that returns something other than a component** — a string, `None` — is refused with *must return a Reflex component*.

## Where they show up

A record or table dashboard is a URL on the Reflex app: `http://localhost:8502/?model=fund&pk=42` locally. Link to one from the project's own dashboard, from another dashboard as the table above does, or from anywhere else a user will click.

Lex App opens them too. The record page's [[using-the-app/record-detail/analytics tab|Analytics tab]] frames the model's record dashboard, and the table's Analytics toggle its table dashboard. Which framework draws each is decided per model, and separately for the record and the table. It is Reflex when all three hold:

- `IS_REFLEX_ENABLED=true`;
- `LEX_DASHBOARD_SURFACE` is not `streamlit`;
- the model defines its own `reflex_main` — for the Analytics tab — or `reflex_class_main` — for the table's toggle.

In every other case it is Streamlit, as it always was. So a model with both kinds of dashboard opens its Reflex one while Reflex is on, and its Streamlit one when Reflex is off. `LEX_DASHBOARD_SURFACE=streamlit` keeps every model on Streamlit whatever it defines — for a project moving its dashboards over one at a time; its default is `auto`.

Lex App's interface learns the answer from `GET /api/project-info`, which reports `reflex_enabled`, `reflex_home` — whether Reflex is on and the project has a `_reflex_structure.py` to show as its home page — and `dashboards`, one entry per model with a dashboard of either kind:

```json
{"dashboards": {"fund": {"record": "reflex", "table": "streamlit"}}}
```

The Django process decides this without importing Reflex: a model's methods are compared with `LexModel`'s defaults, and `_reflex_structure.py` is looked for, not imported. An interface that does not read these fields keeps opening Streamlit dashboards, as it always has.

Framed by Lex App, the dashboard is opened with `?lex_embed=1`, so its own header and navigation stay hidden — see [[access-and-dashboards/reflex/design system#Inside Lex App's frame|Inside Lex App's frame]].

## Tips

- Keep the tree static and the data in state vars. The method runs once, at compile time; a Python `if` in it cannot depend on the record.
- Use `rx.cond` and `rx.foreach` for what does depend on it — they are evaluated in the browser, against the vars.
- Keep the queries narrow: `values()` of the columns you chart, not every field of every row. Everything a handler assigns is sent to the browser.
- A var holds what the browser may see. Anything that must stay on the server belongs in a backend var — a name that starts with an underscore, such as `_raw_rows`.

## Related

- [[access-and-dashboards/reflex/standalone dashboards|Standalone Dashboards]] — a dashboard that is not about one model
- [[access-and-dashboards/reflex/tables and records|Tables & Records]] — the record and the model's rows, as the user may see them
- [[access-and-dashboards/reflex/the django orm|The Django ORM]] — reading and writing models from a handler
- [[access-and-dashboards/reflex/sessions and authentication|Sessions & Authentication]] — narrowing a dashboard to the users allowed to see it
