---
title: Standalone Dashboards
---

Some dashboards are not about one model: an overview that spans several, a report, a control panel. In Reflex those are the project's own dashboard — what `/` shows when the URL names no model — and any further pages the project wants.

It takes one file. Put `_reflex_structure.py` at your project root and give it a `main()` that **returns** a component:

```python title="_reflex_structure.py"
import reflex as rx

from lex.lex_app.reflex import LexUser


def main() -> rx.Component:
    return rx.vstack(
        rx.heading("Northwind Analytics"),
        rx.text("Signed in as ", LexUser.display_name, "."),
    )
```

`lex reflex` imports the module when the app compiles and uses what `main()` returns as the page at `/`, inside Lex App's chrome: a header with the dashboard's name and the user's menu, with **Sign out** in it, and a side navigation once the project has pages of its own. Framed by Lex App, it leaves both out, because Lex App's own chrome already shows them. The page's parts are RFDS's — `rfds.page`, `rfds.page_header`, `rfds.card` — or plain Reflex; [[access-and-dashboards/reflex/design system|Design System]] covers both.

## Two rules that catch people first

> [!warning] `main()` is called once, when the app compiles
> Not per visit and not per user: it builds the component tree, and Reflex compiles that tree into the frontend. Whatever changes at run time — the data, the user — lives in a state and reaches the page as vars. A query written directly in `main()` runs once, at start-up, and its result is baked into the page for everyone.

> [!warning] `main()` is the only name the framework looks for
> A function named `app()` or `render()` is never called, and `/` keeps showing the placeholder that asks for a `_reflex_structure.py`. A `main()` that returns something other than a component stops the app when it compiles, with a message saying so.

A `_reflex_structure.py` that fails to import stops the app too, with the traceback. Only a missing file is quiet: `/` then shows a note saying what to add.

## Data, per visit

The same shape as on a model's dashboard: a state, a handler that reads the models, and `on_mount` to run it when the page appears.

```python title="_reflex_structure.py"
import reflex as rx

from Input.Fund import Fund
from lex.lex_app.reflex import LexUser


class Overview(rx.State):
    funds: int = 0

    @rx.event
    async def load(self):
        self.funds = await Fund.objects.acount()


def main() -> rx.Component:
    return rx.vstack(
        rx.heading("Northwind Analytics"),
        rx.text("Signed in as ", LexUser.display_name, "."),
        rx.text(Overview.funds, " funds"),
        on_mount=Overview.load,
    )
```

The module is imported by the Reflex app alone — Django's model discovery skips names that start with an underscore — so it can import Reflex and define states at the top level. [[access-and-dashboards/reflex/the django orm|The Django ORM]] explains `acount()` and its synchronous alternative.

## More pages

`main()` is the page at `/`. Any other page is declared with `@lex_page`, in the same module — or in a module it imports:

```python title="_reflex_structure.py"
import reflex as rx
import rfds

from lex.lex_app.reflex import lex_page


def main() -> rx.Component:
    return rfds.page(
        rfds.page_header(title="Overview", path="/"),
        rfds.link("Monthly report", href="/report"),
    )


@lex_page("/report", title="Monthly report", nav="Reports")
def report() -> rx.Component:
    return rfds.page(rfds.page_header(title="Monthly report", path="/report"))
```

A `lex_page` is drawn in Lex App's chrome, listed in the side navigation under its `nav=` heading, and can be shown only to users holding a permission — see [[access-and-dashboards/reflex/design system#Pages in Lex App's chrome: lex_page|Pages in Lex App's chrome]]. Every page requires sign-in, whether or not it says so. A page declared with Reflex Enterprise's `@rxe.page` still works, outside the chrome; [[access-and-dashboards/reflex/sessions and authentication|Sessions & Authentication]] covers what it can narrow.

## Framed by Lex App

Lex App's **Reflex** sidebar entry opens the dashboards at `/?lex_embed=1`. Two query parameters decide what the page draws around your dashboard, and a frame of your own can send either:

| Parameter | Effect |
|---|---|
| `lex_embed` | `1`, `true`, `yes` or `on`: the page is framed, and hides its header — the user and **Sign out** — and its navigation |
| `is_logout_enabled` | `0`, `false`, `no`, `n` or `off`: the header keeps the user's name but drops **Sign out** |

Your own components can follow the same URL through `LexDashboardState`, which `lex.lex_app.reflex` exports:

| Var | Holds |
|---|---|
| `LexDashboardState.embedded` | `True` when `lex_embed` says the page is framed |
| `LexDashboardState.logout_enabled` | `False` only when `is_logout_enabled` turns sign-out off |
| `LexDashboardState.view` | What `/` shows: `"structure"` (your `main()`), `"record"`, `"table"`, or `"missing_model"`, `"missing_record"`, `"unsupported_record"`, `"unsupported_table"`; `""` while it is still deciding |
| `LexDashboardState.model` | The model the URL names, as its lowercase name |
| `LexDashboardState.pk` | The primary key the URL names |

```python title="_reflex_structure.py"
import reflex as rx

from lex.lex_app.reflex import LexDashboardState


def main() -> rx.Component:
    return rx.vstack(
        rx.cond(LexDashboardState.embedded, rx.fragment(), rx.heading("Northwind Analytics")),
        rx.text("The dashboard itself."),
    )
```

`embedded` and `logout_enabled` only restate the URL, and are public. `view`, `model` and `pk` are set once the viewer has signed in, like any other state.

## Start from one that works

`lex/lex_app/reflex/examples/_reflex_structure.py` in your installed copy of lex-app is a complete, maintained example that uses every feature Lex App gives a Reflex dashboard, one page each: an overview with a chart, a table and a grid of one of your models, Lex App's own table and form inside the dashboard, a calculation with its log, and a write through Lex App's API. Copy it to `<your_repo>/_reflex_structure.py` and delete what you do not need — [[access-and-dashboards/reflex/consultant tooling#The reference example|Consultant Tooling]] lists the pages.

To start smaller, `lex reflex add list_report --model Fund` writes one page for one model, and creates `_reflex_structure.py` if the project has none.

## Related

- [[access-and-dashboards/reflex/dashboards on your models|Dashboards on Your Models]] — when the dashboard *is* about one model
- [[access-and-dashboards/reflex/design system|Design System]] — `lex_page`, RFDS, and the chrome around every page
- [[access-and-dashboards/reflex/the django orm|The Django ORM]] — reading and writing models from a handler
- [[access-and-dashboards/streamlit/standalone dashboards|Streamlit's standalone dashboards]] — the same idea, in Streamlit
