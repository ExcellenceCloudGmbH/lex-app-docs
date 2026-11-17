---
title: Embedding App Controls
---

A Reflex dashboard can host the application's *own* controls: the real Calculate button, wired to the real record, with the same status, the same live log and the same permissions as the grid. Use it where the work happens on the dashboard — a report whose reader should be able to re-run the calculation they are looking at, without leaving for the grid.

These are the Reflex twins of [[access-and-dashboards/streamlit/embedding app controls|Streamlit's controls]], built from the same widget specs and shown by the same widget host inside Lex App. Two things differ: a block is a function call rather than a `with` block, and a status change **runs an event handler** of yours rather than a rerun.

## One control

Each control has a one-call form. It takes the model's name and the record's primary key:

```python
from lex.lex_app.reflex import lex_calculation

lex_calculation("navcalc", 1)
```

That draws the full control: the status, the **Calculate** button and the button that opens the live log.

| Call | What it draws |
|---|---|
| `lex_calculation(model, pk)` | The Calculate control: status, button, log button |
| `lex_calculation_log(model, pk)` | The calculation's log, as a live stream |
| `lex_calculation_log_tree(model, pk)` | The finished run's execution tree |

The stream shows what is happening now; the tree shows how a finished run was structured. Both follow the record's latest run; pass `calculation_id="…"`, a string, to show one particular run instead — the id the audit log records for it.

## The record, at run time

The page is compiled once, so the record is often not known when the control is declared. `pk` can be a state var — the record the dashboard is about, or the row a user picked — and the control follows it:

```python
lex_calculation("fund", FundRecord.pk, show_log=True)
```

## Several controls, one frame

Every one-call form is a frame of its own, and each frame boots Lex App's whole widget host. That is fine for one or two, and slow for ten. Put several in one `lex_widgets()` call instead, and they share a single frame:

```python
from lex.lex_app.reflex import calculation, calculation_log, lex_widgets

lex_widgets(
    calculation("navcalc", 1, title="Net asset value"),
    calculation("feecalc", 1, title="Fees"),
    calculation_log("navcalc", 1, height=420),
    calculation_log("navcalc", 1, tree=True, height=300),
)
```

`calculation()` and `calculation_log()` only describe a widget; `lex_widgets()` draws them, top to bottom, in one frame. The count of widgets is free, the count of frames is not — the diagram under [[access-and-dashboards/streamlit/embedding app controls#Several widgets|Several widgets]] shows why. `lex_calculation` is a `lex_widgets` of one.

| `lex_widgets` argument | Default | What it does |
|---|---|---|
| the widgets | — | One or more `calculation(...)` and `calculation_log(...)`. None at all raises `WidgetSpecError` |
| `on_status` | none | The handler that gets each status change — see [Reacting to a result](#reacting-to-a-result) |
| `on_open_log` | the log dialog | The handler that gets a log button's click — see [The log dialog](#the-log-dialog) |
| `min_height` | `48` | The least the frame shrinks to, in pixels — a floor, not a size |
| `base_url` | as for `lex_view` | Lex App's address — see [[access-and-dashboards/reflex/embedding app pages#Where the frame points\|Where the frame points]] |
| `title` | `"lex-app controls"` | The frame's accessible title |

The frame grows to the height its widgets report. `min_height` is the height before they report: raise it only to avoid a jump when a block is known to be tall.

## Shaping a control

`calculation(model, pk, ...)` draws as little as you ask for:

| Argument | Default | Effect |
|---|---|---|
| `variant` | `"full"` | `"full"` (status and button), `"status"` (the status alone), `"action"` (the button alone) |
| `title` | none | A heading above the control |
| `fields` | none | Record fields beside the control, a list of names, drawn as the grid draws them |
| `show_log` | `False` | The log, inline under the control |
| `log_height` | none | That inline log's height, in pixels |
| `show_log_button` | `True` | The button that opens the run's log in a dialog |
| `on_status` | `False` | Report this control's status to `lex_widgets`'s `on_status` handler |
| `id` | derived | The widget's name — see [Widget ids](#widget-ids) |

`calculation_log(model, pk, ...)` takes `height`, `calculation_id`, `id`, and `tree=True` for the execution tree. The inline log takes `log_height` and the standalone log takes `height`; giving one to the other raises `TypeError` before anything is drawn.

## Reacting to a result

Give `lex_widgets` an `on_status` handler, and mark each control it should hear from with `on_status=True`:

```python
import reflex as rx

from lex.lex_app.reflex import calculation, lex_widgets


class Revalue(rx.State):
    status: str = ""

    @rx.event
    def changed(self, payload: dict):
        self.status = str(payload.get("status") or "")


def revalue() -> rx.Component:
    return rx.vstack(
        lex_widgets(calculation("navcalc", 1, on_status=True), on_status=Revalue.changed),
        rx.cond(Revalue.status == "SUCCESS", rx.text("Recalculated — the figures below are current.")),
    )
```

For one control, `lex_calculation` takes the handler directly: `lex_calculation("navcalc", 1, on_status=Revalue.changed)`.

The handler gets the payload:

| Key | Holds |
|---|---|
| `widget_id` | Which control this is about, when a block has several |
| `model` | The model the control is wired to |
| `pk` | The record's primary key |
| `status` | The calculation's state — `SUCCESS`, `ERROR`, `IN_PROGRESS`, and the rest of the [[calculations/calculation models#The State Machine\|state machine]] |

The control reports the record's current status as soon as it loads, so a record that already succeeded reports `SUCCESS` before anyone has clicked.

> [!warning] Each status reaches the handler once per frame
> The frame passes on each status of a control once, until the page is loaded again: a later report of a status it has already passed on is dropped. A record that last succeeded reports `SUCCESS` on load; re-run it, and the handler hears `IN_PROGRESS` — and not the `SUCCESS` that ends the run. Treat `IN_PROGRESS` as "the figures are changing", and reload the data you show when the user asks, rather than waiting on a second `SUCCESS`.

## The log dialog

The log button opens the run's log in a dialog over the **page**, not inside the frame — a frame is a small box, and a log is long. The dialog is RFDS's, wide, and holds the live log 760 pixels tall, titled with the model and the record.

To do something else with the click, pass `on_open_log`: your handler then gets `{widget_id, model, pk, calculationId}`, and no dialog is drawn.

## Widget ids

A widget's id is derived from what it is about — its kind, model and primary key, like `calculation_navcalc_1` — so a widget behind an `rx.cond` does not renumber the others. With a state var as `pk`, the id is fixed when the page compiles instead.

Two widgets of the same kind, model and record in one block need ids of their own:

```python
lex_widgets(
    calculation("navcalc", 1, variant="action", id="nav_button"),
    calculation("navcalc", 1, variant="status", id="nav_pill"),
)
```

> [!warning] A malformed widget stops the page from being built
> `WidgetSpecError`, a `ValueError`, is raised when the page is built — at compile time, not in front of a reader — for a `variant` other than the three, `fields` given as a bare string, a height that is not a positive whole number, a `pk` that is neither a string, an integer nor a state var, two widgets with one id, or `lex_widgets()` with no widget at all. A misspelled argument is a `TypeError`.
>
> A model or record that does not *exist* is different: that widget draws an error card, and the others keep working.

## Sites allowed to embed Lex App

The controls are Lex App pages in a frame. When the deployment sets `LEX_EMBED_ALLOWED_ORIGINS`, browsers show Lex App in a frame only on the sites it lists, so the dashboards' origin must be one of them — see [[access-and-dashboards/reflex/embedding app pages#Allowed sites|Allowed sites]].

## Coming from Streamlit

| | Streamlit | Reflex |
|---|---|---|
| Several controls | `with lex_widgets() as page:` and `page.calculation(...)` | `lex_widgets(calculation(...), ...)` |
| The execution tree in a block | `page.calculation_log_tree(...)` | `calculation_log(..., tree=True)` |
| A status change | the next rerun returns the envelope | your `on_status` handler gets the payload |
| `on_status` on one control | `lex_calculation(..., on_status=True)` returns it | `lex_calculation(..., on_status=handler)` |
| The record | a value, per rerun | a value, or a state var |
| `key`, blocks in a loop | needed | none — nothing reruns |
| The log button | a Streamlit dialog | an RFDS dialog, or your `on_open_log` |
| `base_url` | none | on `lex_widgets` |

## Related

- [[access-and-dashboards/reflex/embedding app pages|Embedding App Pages]] — a whole Lex App page, and where the frames point
- [[access-and-dashboards/streamlit/embedding app controls|Streamlit's Embedding App Controls]] — the same widgets, from Streamlit
- [[calculations/logging|Logging]] — what appears in the log these controls show
