---
title: Design System
---

Every Reflex dashboard in Lex App is drawn with **RFDS**, the Reflex Finance Design System (`rfds` on PyPI). RFDS brings the look: tokens, components, charts, tables and page templates. Lex App keeps everything that is about the platform: sign-in, data, permissions, the app itself, routing and embedding. This page is where the two meet.

Lex App installs RFDS together with Reflex, at the version it supports. There is nothing to add to `requirements.txt`.

## What Lex App sets up, and what you write

| Lex App configures, once, for every dashboard | You write |
|---|---|
| The Reflex app itself, with RFDS installed into it | Pages: `main()`, and a function per `@lex_page` |
| The plugins in `rxconfig.py`: sign-in, Radix with RFDS's theme, RFDS | Components from `rfds`: `rfds.page`, `rfds.page_header`, `rfds.card`, `rfds.kpi_tile`, the charts |
| The brand: Lex App's teal, its navy chrome, its font | States, and the event handlers that fill them |
| How numbers, money and dates are written | Which parts of a page each user sees: `can(permission(...))` |
| The chrome around a page: header, user menu, side navigation | |
| Who may frame a dashboard: Lex App, and nobody else | |
| Light or dark, following Lex App | |

So a project never builds an `rx.App`, never passes one a `theme=` — RFDS forbids it, the theme is set once in the plugins — and never calls `rfds.install()`. Lex App does all of that when the app starts.

## Two imports

A dashboard imports from two places, and the rule for which is short:

- **UI comes from `rfds`**, and from plain `reflex` where RFDS has nothing to say.
- **Anything that knows about Lex App comes from `lex.lex_app.reflex`**: pages in the chrome, the user, permissions, a model's data, Lex App's own pages and controls.

```python title="_reflex_structure.py"
import reflex as rx
import rfds

from lex.lex_app.reflex import LexUser


def main() -> rx.Component:
    return rfds.page(
        rfds.page_header(title="Overview", path="/", subtitle=LexUser.display_name),
        rfds.card(rx.text("The figures go here."), title="Figures"),
    )
```

Plain `reflex` components still work beside RFDS's. RFDS's [conformance checks](#conformance) say where a page steps outside the design system.

## What is configured for you

### The plugins

`lex_config()` — the one call in the project's `rxconfig.py` — lists three plugins, in this order:

| Plugin | Built by | What it does |
|---|---|---|
| Sign-in | `lex_auth_plugin()` | Reflex Enterprise's `AuthPlugin`, against the project's Keycloak — see [[access-and-dashboards/reflex/sessions and authentication\|Sessions & Authentication]] |
| Radix | `theme_plugin()` | Reflex's Radix themes, carrying RFDS's root theme |
| RFDS | `rfds_plugin()` | RFDS's stylesheets and fonts, the brand's contrast check and the page conformance checks, at compile time |

The order matters: RFDS must come after Radix, or its stylesheets lose and `rfds.install()` refuses to start. A `plugins=` you pass to `lex_config()` replaces the whole list, so keep all three, in this order.

`rfds_plugin()` takes any of `RFDSPlugin`'s fields, and a field you pass wins over Lex App's value — a project whose figures are in US dollars, say:

```python title="rxconfig.py"
from lex.tools.django_bootstrap import prepare_environment

prepare_environment()

from lex.lex_app.reflex.config import lex_auth_plugin, lex_config  # noqa: E402
from lex.lex_app.reflex.design import rfds_plugin, theme_plugin  # noqa: E402

config = lex_config(
    plugins=[lex_auth_plugin(), theme_plugin(), rfds_plugin(base_currency="USD")],
)
```

### The brand

RFDS's brand colour is Lex App's teal: RFDS derives its accent colours from it, and checks them for contrast when the app compiles. On top of RFDS's styles, every page carries Lex App's own: the navy of Lex App's sidebar for the header and the navigation, in light mode and dark, and Lex App's font.

### Numbers, money and dates

RFDS writes every number, amount and date the same way across a dashboard. Four variables decide how:

| Variable | Default | What it sets |
|---|---|---|
| `LEX_FORMAT_LOCALE` | `en-US` | How numbers, amounts and dates are written — `de-DE` writes `1.234,56` |
| `LEX_UI_LANGUAGE` | `en` | The language of RFDS's own labels, and the page's `lang` |
| `LEX_BASE_CURRENCY` | `EUR` | The currency of an amount that does not name one |
| `LEX_TIME_ZONE` | `Europe/Berlin` | The zone dates and times are shown in — the same variable, and the same default, the rest of Lex App uses |

They are read when `rxconfig.py` loads, so restart `lex reflex` after changing one. A field passed to `rfds_plugin()` wins over its variable.

## Pages in Lex App's chrome: `lex_page`

A dashboard opened on its own gets RFDS's application shell: a header with the dashboard's name, an environment badge and the user's menu, and a side navigation listing the project's pages. Opened inside Lex App, it gets neither — Lex App's own chrome already shows both.

| Part | Shows |
|---|---|
| The name in the header | `LEX_DASHBOARD_TITLE`; unset, the project's name, made readable — `northwind_analytics` becomes *Northwind Analytics* |
| The environment badge | `LEX_ENVIRONMENT`: `prod`, `uat` or `dev`; unset, or any other value, no badge |
| The user menu | The user's name and email, and **Sign out** |
| The side navigation | **Overview** (`/`), then every page added with `nav=`, under its heading. A project with no such page has no navigation |

Add a page with `@lex_page`, the counterpart of Reflex's `@rx.page`:

```python title="_reflex_structure.py"
import reflex as rx
import rfds

from Input.Fund import Fund
from lex.lex_app.reflex import lex_page, lex_table, permission


def main() -> rx.Component:
    return rfds.page(rfds.page_header(title="Overview", path="/"))


@lex_page("/funds", title="Funds", nav="Finance", requires=permission(Fund, "read"))
def funds() -> rx.Component:
    return rfds.page(
        rfds.page_header(title="Funds", path="/funds"),
        lex_table(Fund),
    )
```

| Argument | What it does |
|---|---|
| `route` | The page's path. It must start with `/`, or `lex_page` raises `ValueError` |
| `title` | The browser tab's title, and the page's label in the navigation |
| `nav` | The navigation heading to list the page under. Left out, the page is not in the navigation and is reached by a link |
| `icon` | An RFDS icon for the navigation entry |
| `requires` | A permission string — see [below](#what-a-user-may-see). A user without it sees RFDS's *access denied* message instead of the page, and no navigation entry |
| `on_load` | The page's own load events, one or a list. They run after the user's grants are loaded |
| anything else | Passed on to `rxe.page`: `meta`, `image` and the rest |

Every `lex_page` requires sign-in, like every page of the app. The decorator returns your function unchanged, so it can still be called — from a test, say. When the development server reloads, a page registered again keeps its place in the navigation.

> [!warning] `requires` decides what a user sees, not what they can reach
> It hides the page's content and its entry from users without the grant. The data the page loads is protected by whatever loads it: `lex_table`, `lex_grid` and `LexRecordState` read through Lex App's API as the user — see [[access-and-dashboards/reflex/tables and records|Tables & Records]] — and a handler of your own needs its own `auth=` check.

A page declared with `@rxe.page` still works, outside the chrome. To put any component in the chrome yourself, wrap it: `lex_chrome(component)`.

### Inside Lex App's frame

Lex App opens a dashboard with `?lex_embed=1`. The page then hides its header and its navigation, and the content fills the frame. The page is compiled once for both cases — the chrome is hidden, not left out — so it keeps exactly one main region and one heading, which RFDS's checks count.

`?is_logout_enabled=false` keeps the header but replaces the user menu with the user's name, without **Sign out**. Both parameters, and how your own components can follow them, are under [[access-and-dashboards/reflex/standalone dashboards#Framed by Lex App|Framed by Lex App]].

## What a user may see

RFDS shows or hides a part of a page by a **permission string**. Lex App gives RFDS the user's Keycloak grants — the ones the grid and the REST API enforce — as one string per grant:

```text
<app_label>.<ModelName>:<scope>        e.g.  northwind_analytics.Fund:edit
```

`permission()` spells one for a model, so a page never types it:

```python
import rfds
from rfds.auth import can

from Input.Fund import Fund
from lex.lex_app.reflex import permission

revalue = can(
    permission(Fund, "edit"),
    rfds.button("Revalue", intent="primary", on_click=FundActions.revalue),
    fallback=rfds.inline_message("You may look, not change.", tone="neutral"),
)
```

`permission(target, scope="read")` takes a model, or a Keycloak resource name as a string, and one of the scopes Lex App registers — `list`, `read`, `create`, `edit`, `delete`, `export`. An empty scope, or one containing `:`, raises `ValueError`. The same string is what `lex_page(requires=...)` takes.

The rules are those of `has_permission`, described under [[access-and-dashboards/reflex/sessions and authentication#What they may see|What they may see]]:

- **Only model-wide grants count.** A grant scoped to single records does not open the whole model.
- **The grants are loaded with the page.** `LexAccessState.load` asks Keycloak for them; every `lex_page` and `/` run it before anything else. On a page of your own declared with `@rxe.page`, add it — `on_load=LexAccessState.load` — or `can` shows nothing.
- **They count for five minutes.** Lex App remembers each user's grants, by Keycloak issuer and user ID, for five minutes after the page loaded them; after that it answers with nothing until the next page load fetches them again. A user Keycloak never answered for holds nothing.

`can` is what a user **sees**, read once when the page loads. Check a handler with `auth=has_permission(...)`: it checks the grants of the user's current access token, however long the page has been open. RFDS's own `rfds.auth.requires(...)` check answers from the remembered grants instead, so on a page open longer than five minutes it refuses until the page is loaded again.

## Conformance

When the app compiles, RFDS checks the brand's colours for contrast, and the pages against the design system — that they use its components and tokens. `LEX_RFDS_CONFORMANCE` decides what a page's finding does:

| Value | A finding |
|---|---|
| `warn` | is logged, and the app compiles. The default on a developer's machine |
| `error` | stops the compile. The default when `CI` is set to `1`, `true`, `yes`, `y` or `on` |
| `off` | is ignored |

An explicit value wins over `CI`; any other value means the default. Left to the defaults, the edit loop never stops over a finding, and CI always does. `lex reflex check` runs RFDS's linter the strict way CI does, without compiling — see [[access-and-dashboards/reflex/consultant tooling#lex reflex check|Consultant Tooling]].

## Who may frame a dashboard

RFDS's default headers forbid every frame: `X-Frame-Options: DENY`, and `frame-ancestors 'none'`. Inside Lex App's Analytics tab that would be a blank page, so Lex App changes them:

- `X-Frame-Options` is left out — it cannot name a site.
- Every response carries an enforcing `Content-Security-Policy: frame-ancestors 'self'` followed by Lex App's origins.
- RFDS's other headers stay as they are, `nosniff` and its report-only policy among them.

Lex App's origins are `https://` and each host Lex App answers on: the hosts in `LEX_APP_HOSTS`, or `DOMAIN_HOSTED` when that lists none. On a machine with neither — every local run — they are any port of `http://localhost` and of `http://127.0.0.1`, wherever you run Lex App's interface.

The consequence: Lex App, and the dashboards themselves, are the only pages that can frame a Reflex dashboard. A page of your own that frames one shows the browser's refusal.

## Light and dark

A dashboard takes Lex App's light or dark mode, without anything to write:

- Lex App's interface opens the frame with `?lex_theme=light` or `?lex_theme=dark`, and the dashboard starts in that mode.
- When the user switches mode in Lex App, Lex App tells the frame, and the dashboard switches without a reload. Only a message from the window that frames the dashboard, and only from one of Lex App's origins above, is listened to.

Opened on its own, a dashboard follows `?lex_theme=` when the URL carries it.

## Signing in inside the frame

When a dashboard inside Lex App's frame cannot sign the user in without a click, its `/login` page tells Lex App's interface so; once the user is signed in again, the dashboard tells it that too. Lex App can then offer the way back around the frame instead of showing a frame that waits. The messages carry no secret, and there is nothing to configure. What the click is for is under [[access-and-dashboards/reflex/sessions and authentication#Inside Lex App's frame|Inside Lex App's frame]].

## Related

- [[access-and-dashboards/reflex/tables and records|Tables & Records]] — a model's rows and one record, through Lex App's API
- [[access-and-dashboards/reflex/standalone dashboards|Standalone Dashboards]] — `main()`, and the parameters a framed page reads
- [[access-and-dashboards/reflex/sessions and authentication|Sessions & Authentication]] — the grants behind `permission` and `has_permission`
- [[reference/Environment Variables#Reflex|Environment Variables]] — every variable on this page
