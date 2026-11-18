---
title: Running & Deploying
---

A Reflex dashboard runs as a process of its own beside the application, the way Streamlit does: `lex start` serves Lex App, `lex reflex` serves the dashboards.

## Running it locally

`lex setup` generates a **Reflex** run configuration for PyCharm (`.run/Reflex.run.xml`) and for VS Code (**LEX: Reflex** in `.vscode/launch.json`), beside the Streamlit one. Pick it and run. From a terminal:

```bash
set -a; source .env; set +a
lex reflex
```

`lex reflex` on its own is `lex reflex run`: the development server, with hot reload. The dashboards are at `http://localhost:8502`, and Reflex's backend listens on `8503` — beside Streamlit's `8501`, and clear of Lex App's `8000`.

Set `IS_REFLEX_ENABLED=true` in `.env` and restart `lex start`, and Lex App's sidebar gains a **Reflex** entry that frames them. `REFLEX_URL` tells it where they are, when that is not `http://localhost:8502`.

### What the first run does

- **Writes `rxconfig.py`** at the project root — the file Reflex reads its configuration from — and says so. It holds one call, `config = lex_config()`; commit it. Later runs leave it alone, so it is yours to edit: `lex_config()` takes any `rx.Config` option and it replaces lex-app's default of the same name, e.g. `lex_config(telemetry_enabled=True)`; a `REFLEX_<OPTION>` environment variable overrides both. Settings that differ between environments — the public URLs below — belong in environment variables instead.
- **Prepares the project for Reflex**, which is Reflex's own start-up rather than Lex App's: it downloads Reflex's JavaScript toolchain and packages — so the first run needs network access — builds the frontend into `.web/`, creates `.states/` and `assets/external/`, and adds those to `.gitignore`. Commit the `.gitignore` change; `.web/` is rebuilt whenever it is missing.
- **Appends `reflex==<version>` to `requirements.txt`**, when the file does not name Reflex. Lex App already requires the Reflex version it supports, and a second pin will conflict with it on the next upgrade. Replace the line with a bare `reflex`: Reflex only checks that the file names it.

> [!warning] `plugins` replaces the whole list
> The design system comes as two plugins, and `lex_config()` lists them in this order:
> `theme_plugin()`, Reflex's Radix themes with RFDS's root theme; and `rfds_plugin()`, RFDS itself —
> see [[access-and-dashboards/reflex/design system#The plugins|The plugins]].
> A `plugins=` you pass replaces that list rather than adding to it. Put RFDS before Radix, or leave
> either out, and the app refuses to start. Keep both, in this order, and add yours after them — in
> the generated `rxconfig.py`, below its `prepare_environment()` call, which loads the project's `.env`:
>
> ```python
> from lex.lex_app.reflex.config import lex_config
> from lex.lex_app.reflex.design import rfds_plugin, theme_plugin
>
> config = lex_config(
>     plugins=[theme_plugin(), rfds_plugin(base_currency="USD")],
> )
> ```
>
> `rfds_plugin()` takes any of RFDS's options. Sign-in is not a plugin: Lex App adds it to the app
> itself, so no `plugins=` can leave it out.

### Hot reload

The development server restarts when a file of the project changes — models, `_reflex_structure.py`, dashboard modules, `rxconfig.py` — and ignores what is not source: hidden entries such as `.web/`, virtual environments, `migrations/`, `media/`, build output and caches. `REFLEX_HOT_RELOAD_OVERRIDE_PATHS` replaces the list, when you want to choose.

### Ports

Every argument after `lex reflex` goes to Reflex's own CLI, so ports are Reflex's options. `lex reflex` only supplies the defaults, and only the ones a run can use — Reflex refuses a frontend port on a backend-only run:

| Run                              | Gets                            |
| -------------------------------- | ------------------------------- |
| `lex reflex` / `lex reflex run`  | frontend `8502`, backend `8503` |
| `lex reflex run --backend-only`  | backend `8503`                  |
| `lex reflex run --frontend-only` | frontend `8502`                 |
| `lex reflex run --env prod`      | one port for both, `8502`       |

A port you choose always wins — `--frontend-port` / `--backend-port`, `REFLEX_FRONTEND_PORT` / `REFLEX_BACKEND_PORT`, or `frontend_port` / `backend_port` in `lex_config()` — and `lex reflex` then adds nothing for it. Leave them out of `rxconfig.py` unless you mean them for every run: a frontend port configured there makes `--backend-only` refuse to start.

## In production

```bash
lex reflex run --env prod
```

Production mode builds an optimised frontend and serves it and the backend on **one port**, `8502` unless you choose another. What it needs:

| What                                                                              | Why                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **HTTPS** | the dashboard's sign-in cookie is `Secure`, `SameSite=None` and partitioned only over HTTPS — what keeps it inside Lex App's frame. See [[access-and-dashboards/reflex/sessions and authentication#Inside Lex App's frame\|Inside Lex App's frame]] |
| **`REFLEX_API_URL`** and **`REFLEX_DEPLOY_URL`**, both the dashboards' public URL | the browser connects back to the backend on `REFLEX_API_URL`; it is built into the frontend, so set it before the run. **Leave `REFLEX_API_URL` unset when the dashboards answer on more than one hostname** — a hosted instance with a customer-owned domain attached does. Unset, Reflex's frontend rewrites its localhost default to `window.location` and one build serves every hostname; pinned, every hostname but that one opens a cross-origin websocket carrying no cookies. List the hostnames in `REFLEX_CORS_ALLOWED_ORIGINS` (Lex App fills it from `LEX_REFLEX_HOSTS`) |
| **`REFLEX_URL`**, or `LEX_INSTANCE_HOSTS`, on the dashboards too | the sign-in: the dashboards answer it only on a host the instance lists, and Lex App hands a sign-in only to such a host. See [[access-and-dashboards/reflex/sessions and authentication#What to configure\|What to configure]] |
| **`IS_REFLEX_ENABLED=true`** and **`REFLEX_URL`** on the Lex App backend          | the sidebar entry, and the address it frames                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **`DOMAIN_HOSTED`**, and `LEX_APP_HOSTS` when it is set, on the dashboards too | who may frame the dashboards: Lex App's hosts. Without them only `localhost` may, and the Analytics tab stays blank — see [[access-and-dashboards/reflex/design system#Who may frame a dashboard\|Who may frame a dashboard]]. `DOMAIN_HOSTED` is also where the dashboards reach Lex App's API |
| **`LEX_API_URL`**, when the public address is not reachable from the dashboards' backend | where `lex_api`, `lex_table`, `lex_grid` and `LexRecordState` call Lex App's API — inside a cluster, the application's internal service address. See [[access-and-dashboards/reflex/tables and records#Where it reaches the API\|Where it reaches the API]] |
| **The dashboards' origin in `LEX_EMBED_ALLOWED_ORIGINS`**, on the Lex App backend, when it is set | `lex_view`'s filters and filter events, and — once the variable is set — Lex App's pages and controls in a frame at all. See [[access-and-dashboards/reflex/embedding app pages#Allowed sites\|Allowed sites]] |

Behind a reverse proxy, forward the public scheme and host — the sign-in builds the address it comes back to from them — let WebSocket upgrades through on `/_event`, the channel every event travels on, and send `/auth/`, the sign-in's routes, to the backend.

Reflex keeps each user's page state on its backend. One replica needs nothing more; more than one needs a shared Redis, `REFLEX_REDIS_URL`, so that a user's next event can reach any of them.

The sign-in needs no Redis: it lives in Lex App's database, which every replica reads — see [[access-and-dashboards/reflex/sessions and authentication#Staying signed in|Staying signed in]].

### One port for a development run

`--env prod` serves everything on one port; a development run has two servers. With `REFLEX_USE_SINGLE_PORT=true`, Lex App puts a development run behind one port too: the backend answers its own routes and passes every other request on to the frontend server — HTTP, and the WebSocket the development server reloads pages through. The platform serves hosted dashboards this way, because a pod exposes one port.

Lex App reads the variable itself, in the app it builds, so `rxconfig.py` plays no part. It changes nothing in production mode, which needs no proxy, nor on a backend-only run (`--backend-only`, or `REFLEX_BACKEND_ONLY`).

`lex_config()` switches off the _Built with Reflex_ badge, and plain Reflex leaves it off in every run mode.

## Related

- [[access-and-dashboards/reflex/sessions and authentication|Sessions & Authentication]] — HTTPS, the hosts the sign-in needs, and how long it lasts
- [[reference/CLI Commands|CLI Commands]] — `lex reflex` among the rest
- [[reference/Environment Variables|Environment Variables]] — every setting named on this page
- [[ship-and-operate/deploying|Deploying]] — the other processes a deployment runs
