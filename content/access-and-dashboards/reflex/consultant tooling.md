---
title: Consultant Tooling
---

Three things get a project's Reflex dashboards from nothing to reviewed: a command that writes a working page for one of your models, a command that checks the dashboards the way CI does, and a complete example to copy from.

| Tool | What it gives you |
|---|---|
| `lex reflex add` | A page bound to a model — a table, a record dashboard or an overview — that runs as it is |
| `lex reflex check` | RFDS's strict lint over your dashboards, and its health check over the project |
| `_reflex_structure.py`, the reference | Every feature Lex App gives a dashboard, on one set of pages |

## `lex reflex add`

```bash
lex reflex add list_report --model Fund --nav Finance
```

That writes one dashboard module for `Fund`, registers it with the app, and prints each file it wrote. The next time the app compiles, the page is there, signed in, in Lex App's chrome, reading its data through Lex App's API as the user.

### The blocks

| Block | Writes | Where it shows |
|---|---|---|
| `list_report` | The model's records in a `lex_table`, paged and filtered on the server — see [[access-and-dashboards/reflex/tables and records\|Tables & Records]] | Its own page, `/fund`, in the navigation |
| `overview` | A tile counting the model's records, then the same table | Its own page, `/fund-overview`, in the navigation |
| `object_page` | One record's dashboard: its name, and Lex App's own record page beside it through `lex_view` | The model's record dashboard, once you return it from `reflex_main` — see [below](#wiring-an-object_page) |

Every page is gated on read access to the model — `requires=` on the page, and on the overview an `auth=has_permission(...)` check on the handler that counts. The counting is the one read that goes to the database directly; everything else goes through the API.

### The options

| Option | Default | What it does |
|---|---|---|
| `--model` | — (required) | The model's class name, as written: `Fund`, `CashPosition` |
| `--route` | `/<model>`, or `/<model>-overview` | The page's path, the model's name with hyphens: `/cash-position`. It must start with `/` |
| `--title` | `<Model> list`, `<Model> overview` | The page's title, in the browser tab and the navigation |
| `--nav` | `Dashboards` | The navigation heading the page is listed under |
| `--force` | off | Replace a module the command wrote before |
| `--no-register` | off | Write the module, and leave `_reflex_structure.py` alone |

A module that already exists is refused unless you pass `--force` — it is yours to change once written, and a second run would overwrite your changes. A model name that is not a class name, an unknown block, or a route without its `/` is refused too; the command then exits with status `2` and writes nothing.

### Where the files go

```text
<your_repo>/
├── _reflex_structure.py           ← gains: from ._dashboards import fund_list_report
└── _dashboards/
    ├── __init__.py                ← created on first use
    ├── fund_list_report.py
    ├── fund_overview.py
    └── fund_object_page.py
```

Each module is `<model>_<block>.py`, the model's name in snake case. `list_report` and `overview` add one import line to `_reflex_structure.py` — once, however often you run the command — and importing the module is what registers its page. With no `_reflex_structure.py` yet, the command creates one, with a `main()` for `/`. `object_page` has no route of its own, so it is never imported there.

> [!note] Why `_dashboards`, with an underscore
> Django imports every module of the project in every process it starts — `lex start`, each Celery worker — to find the models. It skips names that start with an underscore. A dashboard module imports Reflex and defines states; under a plain name, all of that would be created in every one of those processes. The underscore keeps it in the Reflex app alone, as [[access-and-dashboards/reflex/dashboards on your models|Dashboards on Your Models]] explains.

The modules find the model through Django — `apps.get_model(...)` — rather than importing its file, so they work wherever in the project the model lives.

### Wiring an `object_page`

`lex reflex add object_page --model Fund` writes `_dashboards/fund_object_page.py`, holding a `LexRecordState` for the record and `fund_record_page()`, the component. Return it from the model's `reflex_main`, and import it inside the method, under the project's own package — `your_repo` here stands for its folder's name:

```python title="Input/Fund.py"
from lex.core.models.LexModel import LexModel


class Fund(LexModel):
    ...

    @classmethod
    def reflex_main(cls):
        from your_repo._dashboards.fund_object_page import fund_record_page

        return fund_record_page()
```

The generated module's docstring holds these lines, with your package's name already filled in from the project folder's. Keep the package in the import, and never make it relative: from a model in a subfolder, such as `Input/Fund.py`, `from ._dashboards…` looks inside that subfolder.

The record page then opens for `?model=fund&pk=42`, and in the record's [[using-the-app/record-detail/analytics tab|Analytics tab]]. It shows the record only if Lex App's API shows it to this user; otherwise it says the record is not theirs to see, or does not exist. When Lex App cannot answer at all, the generated page keeps showing its spinner: add an `"unavailable"` case to its `rx.match` to say so — see [[access-and-dashboards/reflex/tables and records#LexRecordState: the record, as the user may see it|Tables & Records]].

## `lex reflex check`

```bash
lex reflex check
```

The check CI runs, from the project root:

1. **RFDS's lint, strict**, over `_reflex_structure.py` and the `_dashboards/` package — whichever exist. Strict means a warning fails too.
2. **RFDS's doctor** over the project: the versions, the pins and `rxconfig.py`.

The command fails when either does. With neither file in the project, only the doctor runs. It does not compile the app, so it takes seconds; the compile-time checks are separate, and fail in CI too — see [[access-and-dashboards/reflex/design system#Conformance|Conformance]].

`add` and `check` are Lex App's own. Every other argument after `lex reflex` still goes to Reflex's command line — see [[reference/CLI Commands#lex reflex|CLI Commands]].

## The reference example

`lex/lex_app/reflex/examples/_reflex_structure.py`, in your installed copy of lex-app, uses every feature Lex App gives a Reflex dashboard, each where a project would use it. It runs on any project: its pages are about one model, `FEATURED_MODEL` — set it to one of your class names, `"Fund"`; left `None`, it is the project's first model. Copy it to `<your_repo>/_reflex_structure.py`, run `lex reflex`, and delete what you do not need.

| Page | What it shows | What it demonstrates |
|---|---|---|
| `/` | Tiles and a bar chart of how many rows each model holds, a CSV export of the counts, and the Keycloak resources the user holds a permission on | `main()`, `run_orm` behind an `auth=` check, RFDS's charts and export, `can(permission(...))` |
| `/records` | The featured model's records, paged on the server | `@lex_page`, `lex_table` |
| `/grid` | The same records in AG Grid, with a status bar | `lex_grid` |
| `/in-lex-app` | Lex App's own table, reporting the user's selection, and its create form, chained back to the table | `lex_view`, `Flow`, event handlers |
| `/calculations` | Pick a record in Lex App's table; its calculation and execution tree appear below, with the last status | `lex_widgets`, `calculation`, `calculation_log`, `on_status` |
| `/edit` | Change one field of a record, through Lex App's API | `lex_api`, `LexApiError` |
| a record dashboard | One record, only if the API shows it to the user | `LexRecordState`, for a model's `reflex_main` |

The pages are listed in the navigation under **Example**. The `/` page shows a **Change a record** link only to users Keycloak lets edit the featured model — what they see, not access control: the API refuses the write itself for anyone else.

The example's record dashboard, `RecordState` and `record_dashboard()`, sits in `_reflex_structure.py` itself. To use it, return `record_dashboard()` from a model's `reflex_main`, imported under the project's package as [above](#wiring-an-object_page): `from your_repo._reflex_structure import record_dashboard`.

## Related

- [[access-and-dashboards/reflex/design system|Design System]] — `lex_page`, the chrome, and the conformance the checks enforce
- [[access-and-dashboards/reflex/tables and records|Tables & Records]] — what the generated pages are built from
- [[reference/CLI Commands#lex reflex|CLI Commands]] — `lex reflex` and its other uses
