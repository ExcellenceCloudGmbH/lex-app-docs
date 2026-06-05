---
title: lex_view Callbacks
---

`lex_view()` lets you embed a Lex App page inside a Streamlit app.

If you only want an embedded page, call it without callback flags and it behaves like before (plain iframe, returns `None`).

If you want Python to react to user actions in the embedded app, turn on one or more `on_*` flags.

## Basic usage

```python
import streamlit as st
from lex.lex_app.streamlit.embed import lex_view

event = lex_view("investor", on_select=True)

if event and event["type"] == "select":
    st.write("Selected row IDs:", event["payload"]["ids"])
```

When callbacks are enabled, `lex_view()` returns the latest event dict (or `None` until the first event arrives).

## Available callback flags

- `on_create`
- `on_update`
- `on_delete`
- `on_select`
- `on_navigate`
- `on_flow_step`

Turn on only what you need. For example, `on_select=True` is opt-in so you don't trigger Streamlit reruns on every grid click unless you explicitly want that behavior.

## Redirect flows (`flow=`)

For multi-step flows, pass a routing table with `flow=`. Each key is `<resource>/<operation>` (`create` or `update`), and each value is the route to open next.

```python
event = lex_view(
    "investor",
    on_create=True,
    flow={
        "investor/create": "/cashflow/{id}/edit",
        "cashflow/update": "/investor",
    },
)
```

You can use `{resource}` and `{id}` in targets.

You can also build this declaratively with `Flow()`:

```python
from lex.lex_app.streamlit.embed import Flow

flow = (
    Flow()
    .after_create("investor", "/cashflow/{id}/edit")
    .after_update("cashflow", "/investor")
)
```

## Choosing a serializer

Use `serializer=` when the embedded view should use a specific API serializer:

```python
lex_view("investor", serializer="InvestorWithFundSerializer")
```

If the serializer name is unknown for that model, Lex App now returns HTTP `400` with a helpful validation error.

## Existing embed options still work

You can keep using existing options like `hide_toolbar`, `hide_actions`, `redirect_after_*`, `extra_params`, and `base_url` with `lex_view()`.
