---
title: Documentation Audit — November 2026 (lex-app 2.5.0)
draft: true
---

# Documentation Audit — November 2026 (lex-app 2.5.0)

> Internal backlog. Not part of the published site: `draft: true`, `DOCS_AUDIT_*.md` is in
> Quartz's `ignorePatterns`, and `scripts/check_links.py` skips it. Companion to
> [[DOCS_AUDIT_2026-05|the May audit]] and [[DOCS_PLAN_2026-09|the September plan]].

**Status (2026-11-13).** All 115 items are fixed. The fixes were merged in
[PR #271](https://github.com/ExcellenceCloudGmbH/lex-app-docs/pull/271), deployed, and
checked on the published site after the deploy; a follow-up PR pointed the Streamlit pages at
the Northwind demo pages that exist (see MEDIA-6 under [[#Found while fixing]]). Seven
reviewers then fact-checked every line those two PRs added, and a third PR corrected what they
found wrong (see [[#Method]], item 6). A second, independent check of that PR's changes found
one wrong and six loose statements, corrected in a fourth PR, and three more framework issues
(FW-30 to FW-32). FW-28 was then traced to the end: a superuser can edit history rows in place,
and a fifth PR says so on the pages that said otherwise. The release
notes are corrected on GitHub (OUT-1), the framework issues are filed as
[LEX-1569](https://linear.app/lundgroup/issue/LEX-1569/framework-issues-found-while-auditing-the-docs-against-lex-app-250),
and the stale PRs and branches are gone. Where a fix found the source saying something other
than this list, the fix follows the source; [[#Found while fixing]] lists those places.

**What was compared.** lex-app-docs `main` at `b4d0e655` (2026-11-13) against lex-app tag
`v2.5.0` (`6fce6bd3`, 2026-11-12) and the interface that release pins,
`lex-app-frontend~=2.3.0`, built from process-admin-general-client tag `v2.3.0` (`69078bd`).

**Paths.** Source paths are relative to the lex-app repository at `v2.5.0` (`lex/…`,
`requirements.txt`) or to the frontend repository at `v2.3.0` (`src/…`). Docs paths are
relative to `content/`. Line numbers are for those tags and for `b4d0e655`.

## How to read this list

- **IDs** are stable. Use them in branch names and commit messages (`docs: OPS-1 …`).
- **P1** — the docs are wrong in a way that breaks or misleads, a privacy or security fact is
  missing, or a shipped feature cannot be found. **P2** — something people use is only partly
  covered, or covered in the wrong place. **P3** — polish, minor parameters, small
  inconsistencies.
- **Missing** · **Partial** · **Stale** (the docs say something 2.5.0 contradicts).
- **✓** — re-read in the source by hand for this list. Unmarked items come from an area audit
  with file and line evidence and were not read a second time; check the claim as you fix it.
- Tick the box when the fix is on `main`.

## Summary

| Area | P1 | P2 | P3 | Total |
| --- | --: | --: | --: | --: |
| Release, upgrade and install (REL) | 4 | 0 | 0 | 4 |
| Operations, configuration and CLI (OPS) | 4 | 8 | 7 | 19 |
| Auth, sessions and permissions (AUTH) | 3 | 6 | 5 | 14 |
| REST API and data contract (API) | 3 | 10 | 2 | 15 |
| Modelling, calculations, history and audit (CORE) | 2 | 8 | 10 | 20 |
| Dashboards (DASH) | 2 | 5 | 7 | 14 |
| Using the app (UI) | 7 | 10 | 6 | 23 |
| Figures and media (MEDIA) | 0 | 2 | 4 | 6 |
| **Total** | **25** | **49** | **41** | **115** |

Outside this repository: the published 2.5.0 release notes contradict the source three times
(OUT-1), and 31 framework issues turned up along the way (FW-2 to FW-32): ten in the audit,
seventeen while fixing, one in the fact-check after the merge and three in the re-check of its
corrections. OPS-3 and FW-1 (Sentry) were withdrawn after review.

What the mechanical gates say: lex-app's own CI checks pass against this tree. Every
environment variable the framework reads (146) and every shipped `lex` command (37) is
mentioned, and all 56 `from lex…` imports in the docs resolve. The gaps below are behaviour,
parameters, contracts and interface, which the gates cannot see.

### Start here

1. **REL-1, OPS-1** — two five-minute fixes to commands that fail as documented
   (`lex --version`, `lex celery-workers --count`).
2. **OPS-2, REL-3, OUT-1** — what changes when a 2.4 instance is upgraded: a deployed instance
   now refuses to start without a private `DJANGO_SECRET_KEY`, and the release notes misstate
   three settings.
3. **REL-2, REL-4** — the interface package and the exact dependency pins.
4. **AUTH-3, CORE-1, CORE-2** — examples and promises that are wrong in code people copy.
5. **UI-1 to UI-7** — one pass over the grid, record and tutorial pages for frontend 2.3.
6. **AUTH-1 with API-1** — one new REST API reference page carries both.

### Suggested batches

| Batch | Items | Pages |
| --- | --- | --- |
| A. Install and upgrade | REL-1–4, OPS-1, OPS-2, OPS-6 | installation, project structure, upgrading, deploying, configuration, troubleshooting, CLI Commands |
| B. Operating an instance | OPS-4–5, OPS-7–8, OPS-14–20 | monitoring and health, backup and restore, Environment Variables, lex_config |
| C. Interface 2.3 | UI-1–23, MEDIA-1–6 | using-the-app/**, tutorial Parts 3, 5, 6 |
| D. Permissions and sign-in | AUTH-2–14 | permissions, sign-in and sessions, LexModel Internals, Environment Variables |
| E. REST API reference (new page) | AUTH-1, API-1–15 | new `reference/REST API.md`, custom frontend, bitemporal history, serializers, model structure |
| F. Calculations truth pass | CORE-1–20 | CalculationModel Internals, celery and async calculations, lifecycle hooks, logging, LexLogger API, history, audit logs |
| G. Dashboards | DASH-1–14, OPS-11 | streamlit/*, reflex/*, CLI Commands |
| H. CLI reference | OPS-9, OPS-10, OPS-12, OPS-13 | CLI Commands, migrating-from-v1 (new page) |

---

## REL — Release, upgrade and install

- [x] **REL-1** ✓ · P1 · Stale — **`lex --version` works; two pages say it does not.**
  Since 2.3.5 (#802) `lex --version` prints `lex._version`, the version `/health` reports, and
  answers without starting Django. On an image built from a git ref that stamped version can
  differ from `pip show`.
  *Source* `lex/bin/lex.py:203-206`, `:1786` · *Docs* `start-here/installation.md:19-23` (a
  warning box: "Not `lex --version`"), `reference/CLI Commands.md:24` ("There is no
  `lex --version`"), `images/cli/lex-help.svg` · *Fix in* both pages; recapture the figure
  (MEDIA-3).

- [x] **REL-2** ✓ · P1 · Stale — **The interface is the `lex-app-frontend` package, not a
  bundle inside lex-app.** Since 2.2.1 (#766, #779, #782) the UI is a separate PyPI
  distribution, and 2.5.0 pins `lex-app-frontend~=2.3.0`. The installed package is what the
  backend serves; the in-tree `lex/react/build` exists only in a source checkout, and with
  neither every page answers 404 after a boot warning. Missing: which interface each lex-app
  release ships (2.5.0 → 2.3.x); that `pip install lex-app==…` brings the matching interface;
  how a project overrides the pin (`~=` was chosen so it can); that a project pin on 2.2.x now
  conflicts. Keep "a hosted installation serves it from its own pod" only if the platform still
  does (`REACT_APP_URL` / `LEX_FRONTEND_URL` can point at a separately hosted frontend).
  *Source* `requirements.txt:72`, `lex/lex_app/settings.py:454-501` · *Docs*
  `ship-and-operate/index.md:45`, `ship-and-operate/deploying.md:51`,
  `ship-and-operate/upgrading.md:35-39` · *Fix in* those three pages. Also
  `access-and-dashboards/streamlit/embedding app pages.md:501` "newer than 2.2.0" → "2.3.0 and
  later".

- [x] **REL-3** ✓ · P1 · Partial — **"Upgrading to 2.5" leaves out most of what an upgrade
  changes.** The page covers sign-in, `nest_asyncio`, `websockets`, initial data, chunked
  uploads and extra hostnames. It does not mention:
  - the grid's filter bar is replaced by column-header filters (value lists, date and number
    ranges), and saved views that used the old filters are migrated automatically (#822, #579);
  - scheduled jobs: a new `scheduling` app and migration, and the clock starts inside the web
    process by default (`LEX_SCHEDULER_ENABLED` defaults to `true`, `lex/lex_app/settings.py:831`;
    started from `lex/lex_app/asgi.py:110-112`), so a declared `@lex_job` runs after the deploy.
    `LEX_SCHEDULER_ENABLED=false` opts an instance out;
  - two new migrations, `authentication/0002_dashboard_handoff` and `scheduling/0001_initial`;
  - a deployed instance now refuses to start without a private `DJANGO_SECRET_KEY` (OPS-2);
  - GET `__exact` / `__in` values are converted by field type, and a value that does not
    convert matches no rows instead of every row; `__blank` is new. Integrators notice this;
  - `LEX_EMBED_ALLOWED_ORIGINS`: unset leaves framing unrestricted and the host-filter channel
    off, so `lex_view(filters=…)` needs it, and an interface of 2.3.0 or later (DASH-4);
  - the interface pairing (REL-2), and that `lex init` now makes migrations for the project's
    app only (#810, OPS-9).

  *Docs* `ship-and-operate/upgrading.md:41-49, 80-126` (no mention of filters, scheduled jobs,
  `LEX_EMBED_ALLOWED_ORIGINS`, `__in` or `lex-app-frontend`). Its example pin at `:10` is still
  `lex-app==2.2.0`.

- [x] **REL-4** ✓ · P1 · Stale — **The dependency advice contradicts the exact pins.**
  `start-here/project structure.md:104-112` says pandas and numpy are "not bundled" and tells
  readers to add them. 2.5.0 pins `pandas==3.0.6`, `openpyxl==3.1.5`, `django==6.0.9` and
  `streamlit==1.66.1` exactly, so a project pin such as `pandas==2.2.*` makes pip refuse to
  install. Nothing tells a project that its code runs on Django 6 and pandas 3;
  `history-and-audit/bitemporal history.md:255` still says "Django 5.x". *Fix in* installation
  or project structure: a short "What lex-app brings" table (Python 3.12 only, Django 6.0,
  pandas 3, Streamlit 1.66, Reflex 0.9.13, Celery 5.6), and "do not pin these yourself".

## OPS — Operations, configuration and CLI

- [x] **OPS-1** ✓ · P1 · Stale — **`lex celery-workers` takes a plain count.**
  `ship-and-operate/deploying.md:12` documents `lex celery-workers --count N`; the command is
  `lex celery-workers N`, so the documented form fails ("'--count' is not a valid integer").
  Each worker runs with `--concurrency=1 --prefetch-multiplier=1 -n workerN@%h` (plus
  `-P threads` on macOS and Windows), extra arguments go to every worker, and when one exits
  all are stopped. *Source* `lex/bin/lex.py:323-341, 380-417` · *Also*
  `reference/CLI Commands.md:246` never names the count; `reference/Environment Variables.md:24`
  says `lex celery` sets `IS_RUNNING_IN_CELERY` (only `celery-workers` does, `lex.py:385`).

- [x] **OPS-2** ✓ · P1 · Stale — **What a deployed instance refuses to start without.** With
  `DEPLOYMENT_ENVIRONMENT` set, startup raises `ImproperlyConfigured` when `DOMAIN_HOSTED` is
  unset, when `LEX_EXTRA_ALLOWED_HOSTS` contains `*`, when `DJANGO_SECRET_KEY` is unset or the
  published example (**new in 2.5**, #866), and when Redis is the channel layer but
  `REDIS_HOST`, `REDIS_USERNAME` or `REDIS_PASSWORD` is missing.
  *Source* `lex/lex_app/settings.py:410-450` · *Docs* `ship-and-operate/configuration.md:27`
  ("The process starts; users are signed out once per restart") and `:49-53` (lists only two
  other cases); `ship-and-operate/troubleshooting.md:14, 53-57` (random per-process key — now
  true only for the legacy/dual dashboard proxy); `DOMAIN_HOSTED` has no row in Environment
  Variables · *Fix in* configuration "What still refuses to start", troubleshooting, upgrading
  2.5, Environment Variables "Deployment identity".

- [x] **OPS-4** ✓ · P1 · Partial — **A failed migration at deploy time looks like success.**
  `lex lex_migrate` catches every exception, prints "✗ Migration step failed" and exits 0;
  `lex create_db` prints the `OperationalError` and returns. `lex start` runs `collectstatic`
  (when deployed) and uvicorn, no migrations, and the image's Dockerfile runs none either.
  *Source* `lex/lex_app/management/commands/lex_migrate.py:92-126`,
  `lex/lex_app/management/commands/create_db.py:97-101`, `lex/bin/lex.py:1314-1319` · *Docs*
  `ship-and-operate/deploying.md:43` and `ship-and-operate/troubleshooting.md:20` ("The web
  process runs migrations" — confirm whether the platform runs `lex lex_migrate` itself);
  `deploying.md:30-31` shows bare `lex_migrate` (the command is `lex lex_migrate`);
  `reference/CLI Commands.md:176` calls `--no-makemigrations` "what you want on a deployed
  instance" while `deploying.md:34` and `upgrading.md:29` call it unsafe · *Fix* tell readers to
  check the output, and make the three pages agree. See FW-4.

- [x] **OPS-5** ✓ · P1 · Missing — **Where files are stored.** `STORAGE_TYPE=GCS` loads a
  service-account key from `<parent of the project root>/django-storages/gcpCredentials.json`
  as settings load. No variable points elsewhere, and without the file every process fails to
  start. With local storage, `MEDIA_ROOT` is the project root on a laptop and
  `/app/storage/uploads` (reports in `/app/storage/reports/`) when `KUBERNETES_ENGINE` is not
  `NONE` — the volume to persist and back up. *Source* `lex/lex_app/settings.py:187-200,
  1261-1273` · *Docs* `reference/Environment Variables.md:260-272` (`STORAGE_TYPE` and
  `GS_BUCKET_NAME` only), `ship-and-operate/backup and restore.md:11` ("Local disk", no path).
  Workload Identity without a key file exists on a lex-app branch after 2.5.0; document it when
  it ships.

- [x] **OPS-6** ✓ · P2 · Stale — **The CLI loads `.env` itself.** Every `lex` command loads
  `<project root>/.env`; variables already in the shell win, so a value sourced earlier silently
  overrides later edits to the file. *Source* `lex/bin/lex.py:99-108`,
  `lex/tools/project_root.py:79-104` · *Docs* "always `set -a; source .env; set +a`":
  `start-here/installation.md:151, 186, 204`, `reference/CLI Commands.md:326`,
  `start-here/running your app.md:54-91`, `reference/Environment Variables.md:415`.

- [x] **OPS-7** ✓ · P2 · Stale — **Redis and Celery descriptions.** The Celery result backend
  is PostgreSQL (`db+postgresql://…`); Redis is the broker and the channel layer, and `REDIS_*`
  are read only when deployed. `CELERY_VALIDATE_CONFIG` only logs at DEBUG.
  *Source* `lex/lex_app/settings.py:723-735`, `lex/lex_app/celery.py:287-314` · *Docs*
  `reference/Environment Variables.md:236` ("the Celery result backend"), `:283` ("a startup
  error").

- [x] **OPS-8** ✓ · P2 · Stale — **A flat `TAB_DISPLAY_NAMES` stops startup.** It raises
  `ImproperlyConfigured`. *Source* `lex/core/config.py:138-148` (called from
  `lex/lex_app/apps.py:122`) · *Docs* `reference/lex_config.md:66-70` ("accepted and ignored").

- [x] **OPS-9** · P2 · Partial — **`lex init`: ten of twelve flags, and what 2.5 changed.**
  Undocumented: `--no-makemigrations`, `--skip-migrations`, `--migration-verbosity`,
  `--dry-run`, `--[no-]preserve-renamed-permissions`, `--[no-]check-missing`,
  `--ensure-default-authz`, `--makemigrations-args`, `--migrate-args`, `--sync-retries`
  (default 3 with backoff; its help text says 1, FW-5). Since 2.5 (#810) it makes migrations
  for the project's app only, unless another app is named in `--makemigrations-args`. On
  PostgreSQL it runs `create_db` and `createcachetable` first, even under `--dry-run`.
  *Source* `lex/lex_app/management/commands/init.py:1433-1501, 1551-1571, 1714-1734` · *Docs*
  `reference/CLI Commands.md:26-29`.

- [x] **OPS-10** · P2 · Partial — **`lex pytest` in CI.** `--send-emails` (without it the run
  asks for confirmation and fails with no terminal); `LEX_TEST_CONFIG_PAYLOAD` (JSON that
  replaces the YAML), `LEX_TEST_EMAIL_BACKEND`, `LEX_TEST_EMAIL_FILE_PATH` (default
  `<report dir>/email-outbox`; read through constants, so the env-var gate cannot see them);
  without `lex_test_config.yaml` it refuses and points at a `.example` that is not shipped; the
  `group_assignments` key; group names must be identifiers; the plugin refuses when
  pytest-django is active. On the GCP, K8S and DOCKER-COMPOSE profiles the test database is
  `DATABASE_NAME` itself, with keepdb — say that loudly. *Source*
  `lex/tools/test_groups.py:39-41, 195-201, 470-501, 980-990`, `lex/bin/lex.py:1185-1199`,
  `lex/tools/pytest_plugin.py:118-124`, `lex/lex_app/settings.py:674-699` · *Docs*
  `reference/CLI Commands.md:77` ("Two extra flags"), `:96`.

- [x] **OPS-11** · P2 · Partial — **`lex streamlit`.** Arguments go to Streamlit's own CLI;
  with none it runs lex's `streamlit_app.py`. The proxy listens on `0.0.0.0:8501`
  (`LEX_PROXY_PORT`) and Streamlit on 8080; `--server.port` and `--browser.serverPort` move
  both. The LEX theme is passed as `--theme.*` flags and overrides a project's
  `.streamlit/config.toml` theme. It warns below Streamlit 1.58, and refuses a bad
  `SESSION_SAMESITE`, a bad `LEX_STREAMLIT_AUTH`, or a hand-off with no hosts.
  `LEX_THEME_DEBUG` is undocumented. *Source* `lex/bin/lex.py:431-476, 500-666, 669-815`,
  `lex/streamlit_theme.py:497-507` · *Docs* `reference/CLI Commands.md:21` (one line) · *Fix* a
  section like the one `lex reflex` has.

- [x] **OPS-12** · P2 · Partial — **`lex setup-with-ai` is not Copilot-only.** Flags
  `--github-token`, `--remote-mcp-api-key`, `--remote-mcp-url`, `--mcp-mode` (10 modes, default
  `brief`), `-e/--environment` (repeatable: `pycharm-copilot`, `vscode-copilot`, `copilot-cli`,
  `cursor`, `claude-code`, `codex`, `windsurf`, `all`), `--list-environments`, `--no-browser`.
  *Source* `lex/bin/lex.py:1333-1388` · *Docs* `reference/CLI Commands.md:265, 273`.

- [x] **OPS-13** · P2 · Missing — **Moving a V1 database.** `lex full_migration_workflow` takes
  14 flags (`--db-name`, `--project-root`, `--v1-source`, `--database-deployment-target`,
  `--migration-timestamp`, `--chunk-size`, `--dry-run-backfill`, `--enable-sanitization`,
  `--backfill-only`, `--pre-clean-jsons`, `--rollback-on-failure`, `--rollback-only`,
  `--rollback-state-file`, `--skip-auditlog-backfill`) and needs
  `generate_legacy_freeze_manifest --before` first. *Source*
  `lex/lex_app/management/commands/full_migration_workflow.py:21-66`,
  `lex/full_migration_workflow.py:359+` · *Docs* `reference/CLI Commands.md:189` points to
  Migrating from V1, which covers code only · *Fix* a new page, `migrating-from-v1/` "Migrating
  the database". Narrow audience.

- [x] **OPS-14** · P3 — **`lex setup` details.** `.run/` is written only from a PyCharm terminal
  and `launch.json` only from VS Code's (both otherwise); an existing `launch.json` is merged;
  `lex setup -p`; `.env` is never overwritten. *Source* `generate_pycharm_configs.py:197-227,
  509-530` · *Docs* `start-here/installation.md:39` ("if VS Code settings are present").
- [x] **OPS-15** · P3 — `ship-and-operate/troubleshooting.md:71` says `lex --help` lists "ten"
  commands; it lists eleven, plus lex-mcp-local's `ai-*` commands when installed
  (`lex/bin/lex.py:152-161`).
- [x] **OPS-16** · P3 — `PROJECT_ROOT` (`reference/Environment Variables.md:253`) does not
  default to the working directory: it searches for `lex_config.py`, then the git top level,
  then marker files (`lex/tools/project_root.py:32-76`).
- [x] **OPS-17** · P3 — Logs go to stderr (`lex/lex_app/settings.py:1315`);
  `ship-and-operate/monitoring and health.md:55` says stdout.
- [x] **OPS-18** · P3 — `LEX_API_KEY` (`reference/Environment Variables.md:257`): `/health`
  never requires it. The key adds an encrypted `runtime` field and opens
  `api/active-calculations` (`lex/lex_app/runtime_health.py:52`,
  `lex/api/views/calculations/ActiveCalculations.py:10-22`).
- [x] **OPS-19** · P3 — `ship-and-operate/deploying.md:16` runs recovery beat "alongside the
  supervisor"; the Celery page says either driver is enough. Reconcile (medium confidence).
- [x] **OPS-20** · P3 — Undocumented flags: `bootstrap_keycloak --timeout / --poll-interval /
  --no-browser`; `sync_keycloak` and `detect_model_changes` `--input / --dry-run /
  --no-check-missing / --ensure-default-authz / --preserve-renamed-permissions`, and the
  `.model_changes.json` they write to the current directory.

## AUTH — Auth, sessions and permissions

- [x] **AUTH-1** ✓ · P1 · Missing — **API keys are not documented.** A key is a
  `rest_framework_api_key` row created in the Django admin. It is accepted as an `Api-Key:`
  header (which wins), as `Authorization: Api-Key <key>`, or as `?api_key=` (2.4.2, #855 — a key
  in a URL ends up in access logs). The caller gets all six scopes, `client_roles={"api_key"}`,
  no groups, is never a superuser, and is audited as *Technical User*. WebSockets refuse keys
  (AUTH-12). Lists of models that keep the default `permission_read` filter by UMA permissions,
  which a key does not have, so they can come back empty. *Source*
  `lex/api/utils/api_key_requests.py:11-115`, `lex/core/models/LexModel.py:177-204`,
  `lex/lex_app/settings.py:539, 1118`, `lex/api/views/model_entries/filter_backends.py:83-125` ·
  *Docs* only `history-and-audit/audit logs.md:16` and the `LEX_API_KEY` row · *Fix in* an
  "API keys" section in `access-and-dashboards/sign-in and sessions.md`, linked from
  permissions and from the REST API page (API-1).

- [x] **AUTH-2** ✓ · P1 · Missing — **Which record a permission method sees.**
  `permission_create` is asked first on a blank `Model()`, then — with the `CREATE` security
  switch, on by default like all of them — on the record filled from the request, with foreign
  keys set and many-to-many not, before `pre_validation`. `permission_list` and field
  exclusions are judged on a blank record too. A `permission_create` that reads field values
  therefore refuses everyone at the first check. *Source* `lex/api/security.py:286-305,
  389-406`, `lex/api/views/model_entries/One.py:458-501`, `lex/core/security_flags.py:3, 27-29`,
  `lex/api/filter_policy.py:86-99` · *Docs* nothing; the switch list in
  `reference/Environment Variables.md` (around `:338-378`) has `CORS` but not `CREATE` ·
  *Fix in* permissions, LexModel Internals, Environment Variables.

- [x] **AUTH-3** ✓ · P1 · Stale — **The custom-frontend example signs users out on a 403.**
  `ship-and-operate/custom frontend.md:101` and its `lexFetch` (`:115-117`) send the browser to
  sign-in on 401 *or* 403. Under the HTTP auth contract v2, 403 `permission_denied` means stay
  signed in, 403 `csrf_failed` means re-read the cookie and retry, and 503 `auth_unavailable`
  means retry after `Retry-After` — as `access-and-dashboards/sign-in and sessions.md:65-71`
  already says, and as frontend #621 fixed in the bundled UI. *Source*
  `lex/authentication/drf_exceptions.py:1-20`.

- [x] **AUTH-4** ✓ · P2 · Stale — **Refusal status codes.** A refused create and a refused
  single-record delete answer 401/403 with `{message, detail, code}`; only bulk delete and edits
  answer 400. `CREATE_NOT_ALLOWED` does not exist anywhere in the source. *Source*
  `lex/api/views/model_entries/One.py:489-501`,
  `lex/api/views/model_entries/mixins/DestroyOneWithPayloadMixin.py:130-132`,
  `lex/api/views/model_entries/Many.py:133` · *Docs* `reference/Environment Variables.md:352-356`
  ("never a 403", `CREATE_NOT_ALLOWED`).

- [x] **AUTH-5** ✓ · P2 · Stale — **The `allow_fields_if_owner` example can never grant.** The
  helper compares the owner field with `user_context.user`, a `User`; the example passes
  `owner_field="created_by"`, a `TextField` holding a name. Also undocumented: `fields=`, and
  that the default `owner` must be a foreign key to the user. *Source*
  `lex/core/models/LexModel.py:490, 1170-1184` · *Docs* `reference/LexModel Internals.md:170-186`,
  `access-and-dashboards/permissions.md:90`.

- [x] **AUTH-6** ✓ · P2 · Stale — **"admin" is a Django group, not a Keycloak role.** The
  `INTERNAL` switch checks `"admin" in user_context.groups`, and those are the user's Django
  groups; nothing syncs Keycloak roles into them. *Source* `lex/core/security_flags.py:99-112`,
  `lex/core/models/LexModel.py:227` · *Docs* `reference/Environment Variables.md:367-368`
  ("Keycloak client role `admin`"), `reference/LexModel Internals.md:133`, against
  `reference/lex_config.md:50`.

- [x] **AUTH-7** · P2 · Missing — **What may be filtered: `lex_filterable_fields`.** Filterable
  means serializer fields, `limit_choices_to` keys and the model's `lex_filterable_fields`,
  minus credential-like names and fields `permission_read` withholds; `"__all__"` opts a model
  out. *Source* `lex/api/filter_policy.py:1-18, 102-125` · *Fix in* `model-your-data/serializers.md`
  or `reference/Grid Filter API.md`.

- [x] **AUTH-8** · P2 · Stale — **`allow_fields(set())  # row hidden` does not hide the row.**
  Rows are dropped only when `allowed` is false; with an empty set the row is still counted in
  pagination and value lists, and its detail answers `200 {}`. Use `deny()`. *Source*
  `lex/api/views/model_entries/filter_backends.py:279-286`, `One.py:79-84` · *Docs*
  `access-and-dashboards/permissions.md:128`.

- [x] **AUTH-9** · P2 · Partial — **Custom domains with `handoff`/`dual` dashboard sign-in need
  `LEX_INSTANCE_HOSTS`.** The hand-off accepts a host only from `LEX_INSTANCE_HOSTS` (or
  `STREAMLIT_URL` / `DOMAIN_HOSTED`); otherwise the user sees "this host is not one of the
  instance's dashboard hosts". `LEX_STREAMLIT_HOSTS` feeds only the legacy sign-in.
  *Source* `lex/authentication/dashboards/sites.py:146-176`,
  `lex/authentication/views/handoff_views.py:81-85`, `lex/proxy.py:887, 1380-1395, 1608-1610` ·
  *Docs* `ship-and-operate/custom domains.md:55-67` (only the `LEX_*_HOSTS` variables). Medium
  confidence: the platform may set both.

- [x] **AUTH-10** · P3 — `LEX_CORS_ALLOWED_ORIGINS` "replacing the permissive default"
  (`reference/Environment Variables.md:340`) is 2.4 wording; in 2.5 it adds to the instance's
  own origins (`lex/lex_app/settings.py:1159-1196`). The `CORS` bullet also omits
  `LEX_APP_HOSTS`.
- [x] **AUTH-11** · P3 — The test sign-in helper also takes `uma_permissions=`, and the module
  offers `create_sign_in`, `stub_keycloak_uma` and `oidc_test_settings`
  (`lex/lex_app/tests/auth.py:1-30, 170-197`); `ship-and-operate/upgrading.md` shows only
  `client_roles`.
- [x] **AUTH-12** · P3 — WebSockets accept only the session cookie; API keys and bearer tokens
  get close code 4401 under `LEX_WS_AUTH=enforce` (`lex/api/consumers/auth.py:9-13`).
- [x] **AUTH-13** · P3 — `allow_public_fields`, `allow_basic_fields`, and
  `allow_all_except_sensitive`'s default list and `sensitive_fields=`
  (`lex/core/models/LexModel.py:1192-1207`).
- [x] **AUTH-14** · P3 — `access-and-dashboards/sign-in and sessions.md:121` says "(see below)";
  there is nothing below.

## API — REST API and data contract

- [x] **API-1** ✓ · P1 · Missing — **There is no REST API reference.**
  `ship-and-operate/custom frontend.md:98-103` tells a custom UI to use the API "exactly as the
  standard interface does" but names only `api/user/` and the chunked-upload routes. A
  `reference/REST API.md` needs:
  - the routes: `api/model_entries/<model>/list`, `…/filter_values`,
    `…/<calculationId>/one[/<pk>]`, `…/<calculationId>/history/<pk>`, `…/many`, plus
    `model-structure`, `model-permissions`, `project-info`, `global-search`,
    `calculationlog/tree`, `widget_structure`, `htmlreport/<name>`;
  - `calculationId` is chosen by the client (the UI sends `<model>_create_<uuid>`,
    `<model>_<pk>_update_<uuid>`, or `default` for history);
  - calculation triggers on the single-record route: `PATCH {"calculate": "true"}` answers 202
    with the row in progress, 200 if a run is already going, 409 `calculation_closed` for a
    closed record; `{"cancel": "true"}` answers 202 or 409 with a report;
  - **`…/many` without `ids` addresses every row**, so a bulk `DELETE` without `ids` deletes
    every row the caller may delete (FW-3);
  - the fields every row carries (`id`, `id_field`, `short_description`, `lex_reserved_scopes`,
    `lex_reserved_calculation_*`), and the shapes of `model-structure` (`modelHierarchy`,
    `historicalModels`, `available_serializers`, `default_serializer_name`) and
    `model-permissions` (`can_*_in_general`);
  - API keys (AUTH-1), refusal codes (AUTH-4), and links to API-6 to API-10.

  *Source* `lex/process_admin/sites/process_admin_site.py:162-321`,
  `lex/api/views/model_entries/One.py:635-672, 782-862`,
  `lex/api/views/model_entries/Many.py:17-147`,
  `lex/api/views/model_entries/filter_backends.py:21-28`.

- [x] **API-2** ✓ · P1 · Stale — **The bitemporal REST routes do not exist.**
  `history-and-audit/bitemporal history.md:262-268` gives `GET /api/employee/?as_of=…` and
  `/api/employee/42/history/`. The real routes are `api/model_entries/<model>/list?as_of=…` and
  `api/model_entries/<model>/<calculationId>/history/<pk>`. Also missing: `change_reason`,
  `system_history[].task_name`, the 400 for a model without history, the 404 under
  `READ_SURFACES`, and that a date-only `as_of` (`2026-02-01`) is silently ignored, so the live
  rows come back. `reference/LexModel Internals.md:32` links to this section. *Source*
  `lex/process_admin/sites/process_admin_site.py:213-236`,
  `lex/api/views/model_entries/History.py:21-166`, `lex/api/utils/temporal.py:27-30`.

- [x] **API-3** ✓ · P1 · Stale — **The Reflex example reads `["results"]` from an unpaginated
  list.** The list is paginated only when `perPage` is sent (no `PAGE_SIZE` is configured), so
  the answer is a bare array and the snippet raises `TypeError`. Send `perPage` (`-1` returns
  every row) or drop `["results"]`. *Source* `lex/api/views/model_entries/List.py:633-643` ·
  *Docs* `access-and-dashboards/reflex/sessions and authentication.md:205-210`.

- [x] **API-4** ✓ · P2 · Stale — **There is no catch-all "Models" group.** Once
  `model_structure` is defined, a model it does not list gets no sidebar entry at all
  (`auto_include_missing_models=False`); without it, models are grouped by package folder.
  *Source* `lex/lex_app/apps.py:200-208`, `lex/utilities/config/generic_app_config.py:198-205`,
  `lex/process_admin/models/ModelCollection.py:93-155` · *Docs*
  `model-your-data/model structure.md:7, 67, 75` (contradicts
  `model-your-data/index.md:34`). Traced in code, not run — check in a running app.

- [x] **API-5** ✓ · P2 · Stale — **`LEX_METADATA_CACHE_SECONDS` has no effect.** Only
  `lex/api/views/ModelStructureObtainView.py` reads it, and nothing imports that module; the
  routed view is `lex/process_admin/views/model_relation_views.py:12`. *Docs*
  `reference/Environment Variables.md:386` · *Fix* drop the row, or wire the view (FW-2).

- [x] **API-6** · P2 · Stale — **What `DEFAULT_SERIALIZER_NAME` changes.** A request without
  `?serializer=` gets the project's `"default"` serializer, and history and the fields endpoint
  use `"default"` too; the alias surfaces only as `default_serializer_name`, which the UI uses
  for foreign-key loaders. *Source* `lex/api/serializers/base_serializers.py:1298-1370`,
  `lex/api/views/model_entries/mixins/ModelEntryProviderMixin.py:121-142`,
  `lex/api/views/model_entries/History.py:54`, `lex/api/views/model_info/Fields.py:175`,
  `lex/process_admin/views/model_relation_views.py:115-125` · *Docs*
  `reference/lex_config.md:83-89`, `model-your-data/serializers.md:281`.

- [x] **API-7** · P2 · Partial — **The fields endpoint and serializer `Meta` options.**
  Undocumented per-field keys: `readable_name`, `type` (and its vocabulary — a `DecimalField`
  reports `float`), `editable`, `required`, `default_value`, `is_pk`, `is_groupable`, `choices`
  (`[{id, name}]`), `target`, `limit_choices_to`. Undocumented `Meta` options:
  `hide_actions_column`, `lex_field_type_overrides`. An unknown `?serializer=` answers 500
  here, not 400 as on the list. The column-options example lacks its `LexSerializer` import, and
  the `list_ui` sample omits `columns`. *Source* `lex/api/views/model_info/Fields.py:28-44,
  104-299`, `lex/api/serializers/base_serializers.py:422-433, 1116` · *Docs*
  `reference/Grid Filter API.md:18-38`, `model-your-data/serializers.md`.

- [x] **API-8** · P2 · Partial — **The list query language and the grid's POST.** `page` /
  `perPage`; `ordering=a,-b` (dotted paths allowed); `pk_only=true` → `{ids, count}`; `!`
  negation on a parameter name; the lookups `iexact`, `[i]contains`, `[i]startswith`,
  `[i]endswith`, `gt`, `gte`, `lt`, `lte`, `range`, `isnull`, `date…`; unknown fields are
  silently ignored, so a typo returns every row; the POST body is AG Grid's server-side row
  model request (aggregations `sum avg min max count first last`) and answers
  `{rowData, rowCount[, pivotResultFields]}`. *Source*
  `lex/api/views/model_entries/List.py:156-204, 562-643, 678-687, 705-1078, 1413-1431` ·
  *Docs* `reference/Grid Filter API.md` (only `__in`, `__exact`, `__blank`).

- [x] **API-9** · P2 · Missing — **WebSocket message contracts.** `calculation_status_update`
  sends `calculation_reconciliation` on connect, then `calculation_in_progress`, `_success`,
  `_error`, `_aborted`, `_cancelled` with `{record, record_id, model_name, calculation_id}`;
  `model_data_update` sends `record_mutation` with `{model_name, action, record_id}`;
  `calculation_logs/<id>` sends `calculation_log_real_time`. *Source* `lex/api/consumers/*.py`,
  `lex/core/signals/ModelMutationSignal.py:45-65`, `lex/core/signals/CalculationSignals.py:83-91` ·
  *Docs* `ship-and-operate/deploying.md:80-81` (route names only).

- [x] **API-10** · P2 · Partial — **Export and file-download contract.** The export body
  (`ag_export.request`, `ag_export.columns[]`, `ag_export.selection.groupKeyPaths`, base64
  `filtered_export`, `timezone`, `?as_of`); xlsx only, at most 1,000,000 rows, 404 when empty.
  File download needs `?pk=&field=`; it streams on local and SharePoint storage and answers
  `{"download_url"}` on GCS. *Source* `lex/api/views/file_operations/ModelExport.py:34, 100-139,
  242-253, 633-676, 1795-1934`, `lex/api/views/file_operations/FileDownload.py:43-121` · *Docs*
  `history-and-audit/audit logs.md:71-77` (as audit payloads only).

- [x] **API-11** · P2 · Missing — **`HTMLReport` pages.** A subclass of
  `lex.core.models.HTMLReport` in a project module is discovered, registered and served at
  `GET api/htmlreport/<name>`; it implements `get_html(self, user[, request])`. The built-in
  Streamlit and Reflex sidebar entries are HTMLReports. *Source* `lex/core/models/HTMLReport.py`,
  `lex/core/models/__init__.py:5`, `lex/utilities/config/generic_app_config.py:148-175`,
  `lex/process_admin/views/model_relation_views.py:189-232` · *Fix* a new model-your-data page.

- [x] **API-12** · P2 · Partial — **`model_structure` keys and structure modules.** A
  `tracked_models` allow-list (declaring it with `untracked_models` is an error); any
  `*_structure.py` provides `get_model_structure`, `get_model_styling` and
  `get_widget_structure` (served at `api/widget_structure`) and is never scanned for models;
  `model_styling` names rename model entries, not just groups; the built-in `ScheduledJob`
  group. *Source* `lex/process_admin/utils/model_structure.py:84-111`,
  `lex/process_admin/utils/model_structure_builder.py:127-149`,
  `lex/utilities/config/generic_app_config.py:13-24, 63-77, 120-127`,
  `lex/process_admin/models/utils.py:17-38` · *Docs* `model-your-data/model structure.md:11`
  ("five top-level keys", shows four) and the built-in groups table at `:162-171`.

- [x] **API-13** · P2 · Missing — **Reserved model and field names.** Startup aborts on these
  class names: `LexModel`, `CalculationModel`, `History`, `MetaHistory`, `StandardHistory`,
  `HTMLReport`, `PermissionResult`, `UserContext`, `LexManager`, and any name starting with
  `Historical` or `Meta` (which catches `Metadata` and `MetalPrice`). Field names `created_at`,
  `created_by`, `edited_at`, `edited_by` and `is_calculated` are refused, and on tracked models
  `valid_*`, `history_*`, `sys_*` and `meta_*` too. *Source*
  `lex/process_admin/utils/model_registration.py:166-175, 236-300` · *Fix in*
  `model-your-data/model structure.md` or LexModel Internals.

- [x] **API-14** · P3 — For a foreign key with `to_field`, a value-list `key` is the `to_field`
  value, not the related primary key (`lex/api/views/model_entries/FilterValues.py:385-403`;
  `reference/Grid Filter API.md:81`).
- [x] **API-15** · P3 — `using-the-app/record-detail/summary tab.md:99` says the 5 GiB upload
  limit is one "your team sets". The upload and value-list limits are read with
  `getattr(settings, …)` only — no environment variable, no `lex_config` key
  (`lex/api/views/file_operations/ChunkedUpload.py:62-70`,
  `lex/api/views/model_entries/FilterValues.py:44-49`). Also: the upload start request takes an
  optional `content_type`, and a file over the cap gets 413.

## CORE — Modelling, calculations, history and audit

- [x] **CORE-1** ✓ · P1 · Stale — **With Celery there is no rollback, and a decorated
  `calculate()` is not saved for you.** `transaction.atomic()` wraps `calculate()` only on the
  in-process route. The Celery routes open no transaction: on failure the web process re-saves
  its own pre-run copy of the record, so that record reverts and every other row `calculate()`
  wrote stays. A `@lex_shared_task` `calculate()` is never saved by the framework — the success
  callback writes status fields only — so results assigned to `self` are lost unless
  `calculate()` calls `self.save()` (the framework's own fixtures do; medium confidence). On
  Celery the error is stored as `str(exc)` with no traceback. *Source*
  `lex/core/models/CalculationModel.py:1253-1264, 1613-1614`,
  `lex/lex_app/celery_tasks.py:132-151, 199-230, 653-717, 842-907` · *Docs*
  `reference/CalculationModel Internals.md:63` ("Framework saves automatically"), `:75` ("all
  database changes are rolled back"), `calculations/calculation models.md:107` ("Auto-save").

- [x] **CORE-2** ✓ · P1 · Stale — **`WaitForTasks` does not wait for `.delay()`.** `.delay()`
  dispatches without registering the task with the context; only plain calls register. The
  documented example (`compute_portfolio.delay(fund_a)  # dispatched, tracked by outer`) does
  not wait. Also undocumented: leaving `WaitForTasks` re-raises the first failed task; calling a
  decorated function synchronously returns `(result, args)`; `lex_shared_task(**task_opts)`
  passes Celery options such as `name=`; `FireAndForget(force_tasks=, exclude_tasks=)`.
  *Source* `lex/lex_app/celery_tasks.py:344-354, 473-490, 567-644, 647, 717, 725-729` · *Docs*
  `calculations/celery and async calculations.md:268-277, 306, 312`.

- [x] **CORE-3** ✓ · P2 · Stale — **Audit statuses include `cancelled` and `aborted`.** The
  traceback is kept only for `failure`. *Source* `lex/lex_app/celery_tasks.py:241-262`,
  `lex/process_admin/utils/model_registration.py:470-475`,
  `lex/audit_logging/utils/calculation_audit.py:263-272` · *Docs*
  `history-and-audit/audit logs.md:34-45` (`pending` → `success`/`failure`),
  `history-and-audit/index.md`, `using-the-app/record-detail/audit log tab.md`, and
  `migrating-from-v1/refactoring/Part 3 — Calculations.md:191` ("both audit as a failure").

- [x] **CORE-4** ✓ · P2 · Stale — **`QuerySet.update()` writes no history.** It also skips
  hooks, `pre_validation` and the `edited_*` stamps; `LexManager` overrides only `bulk_create`.
  *Source* `lex/core/models/LexModel.py:373-408` · *Docs* `history-and-audit/history.md:66`.

- [x] **CORE-5** ✓ · P2 · Stale — **In-process, `pre_validation()` never sees what
  `calculate()` produced.** The final save is `self.save(skip_hooks=True)`; the Celery route
  saves with hooks, so the behaviour depends on the route. *Source*
  `lex/core/models/CalculationModel.py:1333`, `lex/core/models/LexModel.py:549-558`,
  `lex/lex_app/celery_tasks.py:894` · *Docs* `model-your-data/lifecycle hooks.md:128` ("runs on
  every `save()` … calculation").

- [x] **CORE-6** · P2 · Partial — **`bulk_create` and skipping history.** The default
  `bulk_create` saves row by row, one transaction each, and ignores `batch_size`,
  `ignore_conflicts`, `update_conflicts` and `unique_fields`; `skip_history=True` is a raw
  insert with no hooks, no `pre_validation` and no `created_*`; `untrack()` and
  `save_without_historical_record()` also suppress the `created_*`/`edited_*` stamps. *Source*
  `lex/core/models/LexModel.py:373-408, 934-1045` · *Docs* `reference/LexModel Internals.md:208`.

- [x] **CORE-7** · P2 · Missing — **What a failing or cancelled nested calculation raises.**
  `child.save()` raises `CalculationModelException` (with `calc_obj`, `exception_details`,
  `stack_trace`) into the parent; uncaught, the parent ends ERROR and every record in the chain
  is saved as ERROR. `raise CalculationCancelled(reason)` inside `calculate()` ends the run
  CANCELLED, as do Celery's `SoftTimeLimitExceeded` and `WorkerLostError`. *Source*
  `lex/core/models/CalculationModel.py:105-137, 1636-1646`, `lex/lex_app/celery_tasks.py:61-79` ·
  *Fix in* CalculationModel Internals ("Nested calculations", "Cancelling").

- [x] **CORE-8** · P2 · Partial — **The LexLogger reference.** Undocumented: `add_raw_markdown`,
  `add_list(items, ordered=False)`, `add_quote`, `add_link`, `add_image`, `add_horizontal_rule`.
  `LexLogger` is a process-wide singleton, so concurrent in-process runs that build text before
  `.log()` can flush each other's lines (the tutorial Part 3 pattern; medium confidence).
  *Source* `lex/audit_logging/handlers/LexLogger.py:18-85` · *Docs* `reference/LexLogger API.md`
  ("one instance can be reused"); `calculations/logging.md` uses `add_list` unexplained.

- [x] **CORE-9** · P2 · Partial — **When log output is stored.** With no calculation in context
  (`lex shell`, scripts, management commands) nothing is stored; inside a transaction rows are
  written on commit; when an in-process atomic run fails, its rows roll back and are replaced by
  one flat row on the root record, losing the sections and child nodes. *Source*
  `lex/audit_logging/models/CalculationLog.py:374-425, 427-560`,
  `lex/core/models/CalculationModel.py:1316, 1574` · *Fix in* `calculations/logging.md`.

- [x] **CORE-10** · P2 · Missing — **Writing a backdated or future-dated version from code.**
  `instance._history_date` sets `valid_from`, `_history_change_reason` the reason; the helper
  `resurrect_object(model_class, pk, valid_from, attributes=None, valid_to=None)`. Assigning
  `obj.valid_from` directly is silently overwritten (BUG-021, FW-8). *Source*
  `lex/core/services/StandardHistory.py:61-110`, `lex/core/services/Bitemporal.py:72-104` ·
  *Docs* `history-and-audit/bitemporal history.md` describes corrections with no code.

- [x] **CORE-11** · P3 — `created_by` / `edited_by` values: `Initial Data Upload` with no
  request, `Technical User` for an API key, explicitly passed timestamps kept; rows created
  inside `calculate()` on a Celery worker get `Initial Data Upload` (medium confidence)
  (`lex/core/models/LexModel.py:453-454, 498-501, 880-932`).
- [x] **CORE-12** · P3 — `reset_calculation_on_edit` is documented only in
  `calculations/scheduled jobs.md:220`; it belongs in CalculationModel Internals.
- [x] **CORE-13** · P3 — Cancelling over REST: `PATCH` with `cancel=true` answers 202 with the
  `cancel()` report, or 409 (`lex/api/views/model_entries/One.py:662-672`). Belongs with API-1
  and CalculationModel Internals.
- [x] **CORE-14** · P3 — A bare `@lex_job` (no parentheses) silently registers nothing
  (`lex/scheduling/registry.py:79-134`); say so in `calculations/scheduled jobs.md`.
- [x] **CORE-15** · P3 — The XLSX helper's `formats`, `comments`, `merge_cells`, `index`,
  `ranges_of_pivot_concatenation`; timezone-aware values are written as `TIME_ZONE` wall-clock
  time; files are saved with `save=False`, and the page's example calls `self.save()` inside
  `calculate()` (`lex/core/fields/XLSX_field.py:14-58, 119-190`;
  `reference/Report File Fields.md`).
- [x] **CORE-16** · P3 — `CalculatedModelMixin.input` is documented, but nothing reads it
  (`lex/core/mixins/CalculatedModelMixin.py:1184`; `reference/CalculatedModelMixin Internals.md`).
- [x] **CORE-17** · P3 — Both validation hooks raise `lex.core.exceptions.ValidationError`,
  which carries `.original_exception` (`lex/core/models/LexModel.py:774-783, 818-830`).
- [x] **CORE-18** · P3 — Audit scope and payloads: `history-and-audit/audit logs.md` says "API
  operations only", but initial data, calculation outcomes and startup resets write entries too.
  Payload tables (`:73-77`) lag: the PDF download also records `scope`, `truncated` and
  `delivery`; exports `row_group_cols`, `pivot_mode`, `sheet_name`; GCS downloads
  `delivery: "url"` (`lex/api/views/calculations/DownloadMarkdownPdf.py:353-366`).
  `model-your-data/initial data.md` links "audit logging" to Django's logging docs.
- [x] **CORE-19** · P3 — The row fields `lex_reserved_calculation_id` and
  `lex_reserved_has_calculation_log` (2.2.2, #792) are not documented.
- [x] **CORE-20** · P3 — Self-hosters get no SQL for scheduling `lex_apply_due_activations()`
  with pg_cron, and `lex_pending_activations()` is not mentioned
  (`history-and-audit/bitemporal history.md`).

## DASH — Dashboards

- [x] **DASH-1** ✓ · P1 · Missing — **Streamlit code cannot find out who is looking.** The
  viewer's identity, permissions and token are in `st.session_state`: `user_info` (the claims),
  `permissions` (the Keycloak UMA list), `access_token`, `user_id`, `user_email`,
  `user_username`, `auth_method`. `streamlit_main(user)` receives the `user_info` dict, not a
  Django user; `streamlit_class_main()` receives nothing. Under `handoff`, a Keycloak outage
  leaves no token. *Source* `lex/streamlit_app.py:107, 170, 495-534, 771-809, 1088-1114`,
  `lex/proxy.py:1628-1642` · *Docs* `access-and-dashboards/streamlit/sessions and
  authentication.md:21, 33` promise "call the Lex App API as them" without saying how;
  `access-and-dashboards/streamlit/dashboards on your models.md:66` calls `user` "the signed-in
  user"; no Streamlit page warns that ORM queries ignore `permission_read` (the Reflex page
  does) · *Fix* a "Who is signed in" section mirroring the Reflex page.

- [x] **DASH-2** ✓ · P1 · Missing — **`lex_config(plugins=…)` silently removes sign-in.**
  `plugins` replaces the whole list, dropping `lex_auth_plugin()` and `RadixThemesPlugin`.
  `lex_auth_plugin(**options)` itself — an app-wide `auth=` check, `extra_scopes`, custom pages,
  an audit hook, and the single-port fix — is undocumented. *Source*
  `lex/lex_app/reflex/config.py:128-145, 170-208` · *Docs*
  `access-and-dashboards/reflex/running and deploying.md:25` ("`lex_config()` takes any Reflex
  configuration option").

- [x] **DASH-3** ✓ · P2 · Stale — **Where `lex_view`'s frame points.** The first choice is the
  validated `lex_app_origin` the framing interface sends, then `REACT_APP_URL`,
  `LEX_FRONTEND_URL`, the same-site app host, `http://localhost:8000`. `lex_widgets` uses the
  same base. *Source* `lex/lex_app/streamlit/embed.py:484-520, 533-573`,
  `lex/streamlit_app.py:1033`, `lex/lex_app/streamlit/widgets/host.py:299`,
  `src/components/StreamlitIframe.tsx:185-199` · *Docs*
  `access-and-dashboards/streamlit/embedding app pages.md:517-521`,
  `reference/Environment Variables.md:82`.

- [x] **DASH-4** · P2 · Partial — **`filters` and `on_filter` need interface 2.3.0.** With an
  older interface the filters are ignored, no `filter` event arrives, and `lex_view` keeps
  returning `None`. *Source* `src/utils/embedFilters.ts`, `src/utils/embedOrigins.ts` (new in
  v2.3.0) · *Docs* `embedding app pages.md:500-502` has a version note for `hide_actions`, none
  for filters.

- [x] **DASH-5** · P2 · Partial — **`LEX_EMBED_ALLOWED_ORIGINS` on an instance with a custom
  domain.** The variable is used as given for `frame-ancestors` and the filter allow-list; the
  dashboard hosts from `LEX_STREAMLIT_HOSTS` are not added. Once it is set, a dashboard on its
  custom domain cannot frame `lex_view` or the controls unless that origin is listed.
  *Source* `lex/lex_app/settings.py:386-401`, `lex/react/views.py:53-95` · *Docs*
  `embedding app pages.md:457-461` (list the `STREAMLIT_URL` origin);
  `ship-and-operate/custom domains.md` never mentions the variable. Medium confidence.

- [x] **DASH-6** ✓ · P2 · Stale — **The Reflex sign-in keeps state in Redis.** Refresh locks,
  Fernet-encrypted token sets and back-channel-logout markers live in the instance's Celery
  broker Redis (`REDIS_HOST`, `REDIS_USERNAME`, `REDIS_PASSWORD`); without it each process works
  alone and logs a warning. *Source* `lex/lex_app/reflex/_token_guard.py:1-35, 225-300`,
  `lex/lex_app/settings.py:724-728` · *Docs* `access-and-dashboards/reflex/running and
  deploying.md:64` and `access-and-dashboards/reflex/sessions and authentication.md:56` ("keeps
  nothing on the server").

- [x] **DASH-7** · P2 · Missing — **Reflex single-port mode** (`REFLEX_USE_SINGLE_PORT`), which
  the platform uses to serve dashboards (2.3.3, 2.3.4). *Source*
  `lex/lex_app/reflex/config.py:83-125` · *Fix in* "In production" in
  `reflex/running and deploying.md`.

- [x] **DASH-8** · P3 — The sidebar's "Streamlit" entry frames `/?embed=true` without
  `lex_embed` or `is_logout_enabled=false`, so the dashboard draws its own header and a Log out
  that signs out of everything (`lex/lex_app/streamlit/Streamlit.py:41-55`,
  `lex/streamlit_app.py:1051-1071`); `streamlit/standalone dashboards.md:90-93` says neither
  appears inside lex-app. Fix the page or the code (FW-6).
- [x] **DASH-9** · P3 — `on_status` returns `None` after the log button is clicked, until the
  status changes (`lex/lex_app/streamlit/widgets/host.py:176-183`,
  `lex/lex_app/streamlit/_widget_host_component/frontend/index.html:197-224`); add to "Reacting
  to a result" in `embedding app controls.md:159-186`.
- [x] **DASH-10** · P3 — Embedded tables follow Lex App's saved theme, not the host page; only
  the controls page follows the host (`src/components/CustomLayout/CustomLayout.tsx:158-165`,
  `src/pages/EmbedWidgets/EmbedStandalone.tsx:70`); `embedding app pages.md:544-546` says the
  table takes the host's mode.
- [x] **DASH-11** · P3 — What a Streamlit reader sees on errors: "Model … not found", "Object
  with ID … not found", a one-line `❌ Error:` with no traceback from `streamlit_main`; an
  exception in `main()` is raised unless `DEPLOYMENT_ENVIRONMENT == "PROD"`, which shows the
  traceback in an expander (`lex/streamlit_app.py:1080-1130`). The Reflex page has this table
  (`reflex/dashboards on your models.md:101-114`).
- [x] **DASH-12** · P3 — The framing contract: the `lex_embed`, `is_logout_enabled` and
  `lex_app_origin` query parameters, and the exported `LexDashboardState` (`embedded`,
  `logout_enabled`, `view`, `model`, `pk`) (`lex/lex_app/streamlit/sidebar.py:492-522`,
  `lex/streamlit_app.py:997-1004`, `lex/lex_app/reflex/dashboards.py:46-47, 205-233`).
- [x] **DASH-13** · P3 — Flow rules at run time: a sequence with no ending ends on the last
  step's table; a save that matches no step leaves the flow; a flow rule beats
  `redirect_after_create` / `_update`, which beat `redirect_after`; `redirect_after=STAY` works;
  on a grouped table `row_count` counts top-level groups (`lex/lex_app/streamlit/embed.py:466-472`,
  `src/utils/flowProgram.ts`, `src/utils/useEmbedContext.ts:278-282, 382-410`).
- [x] **DASH-14** ✓ · P3 — `start-here/running your app.md:84` says to set a fixed
  `SESSION_SECRET` in HTTPS deployments; since 2.2.1 the key is derived from
  `DJANGO_SECRET_KEY` (`lex/proxy.py:126-171`), as `streamlit/sessions and
  authentication.md:63-69` says.

## UI — Using the app (frontend 2.3.0)

- [x] **UI-1** ✓ · P1 · Missing — **Running a calculation and reading its log.** No
  using-the-app page covers it: the ▶ *Run calculation* button (greyed with the closed reason,
  "You do not have permission…" or "unavailable in history view"); the status pill and its
  labels; the log icon ("See the calculation log" / "See why this calculation failed", hidden
  on aborted and cancelled rows); the log popup (full screen, Traceback and Log tabs, "no log"
  messages, headlines for failed, aborted and cancelled runs); the log tree page (execution
  tree, consolidated log, *Copy full log*, Log and Details tabs); the toasts when a run
  finishes. *Source* `src/components/model-components/CalculateFunctionality/`
  (`CalculateFunctionality.tsx:117-167, 228-233, 396-420`, `CalculationStatusPill.tsx:30-65`,
  `CalculationLogPopup.tsx:169, 213-225, 318-319`, `calculationRunHeadline.ts:47-77`),
  `src/pages/CalculationLogTree/CalculationLogTree.tsx:471-621`,
  `src/web-sockets/CalculationStatusUpdate.tsx:155-233` (frontend #630, #634) · *Docs*
  `calculations/logging.md:201` still says "a slide-out drawer during calculation"; tutorial
  Part 3 (`:188`) implies the log opens by itself · *Fix* a new
  `using-the-app/the-grid/calculations.md`, linked from logging "In the Frontend".

- [x] **UI-2** ✓ · P1 · Stale — **The grid toolbar table.** It lists a **Cancel** control (there
  is no cancel UI in 2.3.0), **Calculate** "on selected records" (Calculate is per row), and
  Export "as Excel or CSV" (Excel only; the right-click menu offers Copy, Copy with Headers,
  Paste, *Export to Excel*). It leaves out the real controls: Current / As of date… / Full
  history, Analytics, Clear all changes, Save view, Select rows, Export, Auto-fit, and "+" with
  its greyed-out reasons. *Source* `src/components/model-components/list/CustomList.tsx:961-970,
  1422-1613`, `src/components/model-components/list/CustomDatagrid.tsx:3252`,
  `src/components/model-components/list/useAgGridExport.ts:381` · *Docs*
  `using-the-app/the-grid/index.md:54-62`; `using-the-app/the-grid/exporting data.md:35-40, 96`
  (CSV format and CSV datetimes); `calculations/calculation models.md:109` and
  `calculations/scheduled jobs.md:28` (cancel from the UI).

- [x] **UI-3** ✓ · P1 · Missing / Stale — **Selecting and deleting rows.** Row Delete with a
  confirmation, Delete in the edit form; checkboxes only after *Select rows*; the bar "N items
  selected · Delete · Clear"; the header checkbox's "Select Records: Visible Page / All
  Records"; rows you may not delete cannot be ticked. *Source*
  `src/components/model-components/list/RecordActionButtons.tsx:166-188`,
  `src/components/model-components/forms/EditToolbar.tsx`,
  `src/components/model-components/list/CustomDatagrid.tsx:2437-2470, 2844-2849`,
  `src/components/model-components/list/BareDatagridAGClient.tsx:300-312`,
  `src/components/model-components/list/bulkSelectionUtils.ts:67-84` · *Docs* nothing; and
  `using-the-app/the-grid/exporting data.md:86` describes click / Shift+Click selection and a
  "Selected rows only" choice that do not exist.

- [x] **UI-4** ✓ · P1 · Missing / Stale — **Record search (⌘K).** The header's *Search
  records…* (⌘K, Ctrl+K, or `/`) opens a dialog: two characters to search, recent searches with
  Clear, ↑↓↵ and Esc, Retry, "No matches". The backend uses PostgreSQL full-text search — whole
  words, text columns only (not numbers, booleans, foreign keys or files), users and
  calculation logs excluded, readable rows only. *Source*
  `src/components/CustomSearch/CustomSearch.tsx:25, 57`,
  `src/components/CustomSearch/useGlobalSearchHotkey.ts:6-8`,
  `src/components/CustomSearch/GlobalSearchDialog.tsx:46-48, 380-456`,
  `lex/api/views/global_search_for_models/Search.py:11-49` · *Docs*
  `using-the-app/navigation.md:45-49` "Global Search" describes the sidebar's model filter ·
  *Fix* split into "Sidebar search" and "Search records".

- [x] **UI-5** ✓ · P1 · Stale — **Clicking a row does not open the record.** A row click
  selects; a record opens through **View** (or ⌘/Ctrl-click on View for the full page).
  *Source* `src/components/model-components/list/CustomDatagrid.tsx:273`,
  `src/components/model-components/list/RecordActionButtons.tsx:107-118` · *Docs*
  `using-the-app/record-detail/index.md:7` ("Click any row in the grid"),
  `using-the-app/index.md:30`, the note in `images/the-grid/first-look.svg` (MEDIA-2).

- [x] **UI-6** ✓ · P1 · Stale — **Timeline and History tabs describe removed controls.** The
  Timeline shows the valid-time chart, As Of and the version drawer (Valid From/To, Changed By,
  Reason, Diff/Raw, Copy JSON, Delete for superusers); the Audit Feed component is no longer
  used and there is no system/effective-time switch. The History tab has Refresh, Clear, Save,
  the view selector, Export, Auto-fit and density — no As Of. *Source*
  `src/components/HistoryTimeline/HistoryTimeline.tsx:159-174`,
  `src/components/HistoryTimeline/ValidTimeView.tsx:166`,
  `src/components/HistoryTimeline/VersionDetailsDrawer.tsx:73-205`,
  `src/components/HistoryTimeline/AuditFeedView.tsx` (referenced by nothing),
  `src/components/CustomShow/CustomShow.tsx:675-731`,
  `src/components/model-components/list/GridViewToolbar.tsx:64-145` · *Docs*
  `using-the-app/record-detail/timeline tab.md:36, 50, 55-59`, `history-and-audit/audit logs.md:146`,
  `using-the-app/record-detail/history tab.md:26-48` ("At the top of the History tab, the **As
  Of** button", and its video), `using-the-app/record-detail/index.md:42` · *Fix* move the As
  Of text to the Timeline page.

- [x] **UI-7** ✓ · P1 · Stale — **Tutorial Part 6 cannot be followed.** There is no History
  icon (a row has Show, Edit and Delete); history rows can be changed only by superusers by
  default (`HISTORY_WRITE`); the interface has no Valid From editor *(corrected 2026-11-13: a
  superuser can edit Valid From in place in the History tab and Full history — FW-28)*. *Source*
  `src/components/model-components/list/RecordActionButtons.tsx:143-188`,
  `lex/api/security.py:272-280`, `lex/core/security_flags.py:26` · *Docs*
  `start-here/tutorial/Part 6 — History in Action.md:27, 45-49`,
  `using-the-app/record-detail/history tab.md:60`.

- [x] **UI-8** · P2 · Partial — **Saved views live in the browser.** *Clear all changes* and
  *Save changes to the current view*; system views are read-only ("System views are read-only —
  type a name…"); views and gear settings are stored in the browser per table, not per user, and
  density is saved in the view, so a density chosen on *Default* is lost on reload. *Source*
  `src/components/model-components/list/CustomList.tsx:151, 168, 1458, 1483`,
  `src/components/model-components/list/useTableSettingsStore.ts:29-31` · *Docs*
  `using-the-app/the-grid/saved views.md:67` ("Each person saves their own presets"),
  `using-the-app/the-grid/table settings.md:14-16, 73` ("Per user, per table").
- [x] **UI-9** · P2 · Missing — **Current / As of / Full history on a table.** Full history is
  read-only *(corrected 2026-11-13: except that a superuser can edit cells in place — FW-28)*,
  and a historical record opens with a *Live Data* tab. *Source*
  `src/components/model-components/list/HistoryModeSwitch.tsx:70-78, 160-176`,
  `CustomList.tsx:1610`, `src/components/CustomShow/CustomShow.tsx:733-752` · *Docs* only "As
  Of" at `using-the-app/the-grid/index.md:58`.
- [x] **UI-10** · P2 · Stale — **The Summary tab** shows every field in serializer order as plain
  rows, with no "Record details" section or cards; the PDF button is *Export Summary*, a
  one-page snapshot. *Source* `src/components/CustomShow/RecordSummary.tsx:22-43`,
  `src/components/CustomShow/ExportToPdfButton.tsx:27-48` · *Docs*
  `using-the-app/record-detail/summary tab.md:9-24, 65`.
- [x] **UI-11** · P2 · Stale / Missing — **The sidebar.** Below 600 px it is not shown at all;
  menu views (*New menu view*, *Reorder items*); the dock handle (left or right); *Full-height* /
  *Floating card*; folders start collapsed and are remembered. *Source*
  `src/components/CustomSidebar/CustomSidebar.tsx:621, 678, 808-849, 867-883`,
  `src/components/CustomSidebar/MenuViewSelector.tsx:132-186`,
  `src/components/CustomSidebar/useSidebarExpansion.ts:4-12` · *Docs*
  `using-the-app/navigation.md:21` ("collapses to icons on smaller screens").
- [x] **UI-12** · P2 · Missing — **Outage, paused-instance and access-denied screens.**
  "Reconnecting to server…" after 5 s and a full page after 120 s; "Your LEX instance's servers
  are starting up!" (idle instances pause after 30 minutes); "Access Denied … no assigned
  roles"; "Authentication failed repeatedly…"; "Could not load your session…". *Source*
  `src/web-sockets/BackendHealthOverlay.tsx:27-58`, `src/pages/ServerNotReady.tsx:46-60`,
  `src/auth/UnauthorizedPage.tsx:59-63`, `src/auth/SessionAuthGate.tsx:174, 204` · *Docs*
  `using-the-app/index.md:38-56` (sign-in banners only).
- [x] **UI-13** · P2 · Missing / Stale — **Paging and the real default density.** The grid is
  paged (page size 2500 ÷ row height, with a page-size selector); the default density is
  Compact (25 px); the status bar has no row count. *Source*
  `src/components/model-components/list/CustomDatagrid.tsx:2481, 3420-3442, 3703-3707`,
  `src/components/model-components/list/TableSettingsPanel.tsx:113` · *Docs*
  `using-the-app/the-grid/density and display.md:31-35` ("Standard … the balanced default"),
  `using-the-app/the-grid/filtering and sorting.md:97` (row count "in the status bar").
- [x] **UI-14** · P2 · Missing — **Columns panel, Auto-fit, copy and paste.** The Columns tab on
  the right edge, *Auto-fit columns*, right-click Copy / Copy with Headers / Paste, Ctrl+C on a
  range (medium confidence that Paste saves each cell). *Source*
  `src/components/model-components/list/CustomDatagrid.tsx:3539-3560`, `CustomList.tsx:961-969,
  1570` · *Docs* only the Filters tab (`filtering and sorting.md:29`).
- [x] **UI-15** · P2 · Missing — **What cells show.** A linked record's hover card (*Open record*,
  *Filter by this value* — always greyed, FW-7); many-to-many cells ("View N items"); SharePoint
  files (Download, Edit, Preview — Edit resets the record to NOT_CALCULATED). *Source*
  `src/components/CustomTooltips/ForeignKeyHoverCard/ForeignKeyHoverCard.tsx:150-249`,
  `src/components/model-components/list/FieldView.tsx:363-371`,
  `src/components/model-components/list/ManyToManyField/ManyToManyField.tsx:59-72`,
  `src/components/model-components/SharepointField/SharepointField.tsx:60-164` · *Docs*
  `using-the-app/record-detail/summary tab.md:32` only.
- [x] **UI-16** · P2 · Missing — **Header extras.** *Monitoring* opens a Grafana panel, shown to
  every user; admins on SharePoint storage get *Delete Unused SharePoint Files* with a dry run;
  *Logout* ends the sign-in for every app; the feedback button. *Source*
  `src/components/CustomLayout/ContentHeaderBar.tsx:66`,
  `src/components/MonitoringDrawer/MonitoringDrawer.tsx:17-36`,
  `src/pages/Admin/DeleteUnusedFiles.tsx`, `src/react-admin-infrastructure/auth-provider.ts:31` ·
  *Docs* `ship-and-operate/custom frontend.md:76` (variables only), `using-the-app/index.md:55`.
- [x] **UI-17** · P2 · Stale — **Tutorial Parts 5 and 3.** The table button is labelled
  **Analytics** (and turns into *Back to Records*); the record-level dashboard is the record
  page's Analytics tab; rows have no dashboard icon. *Source*
  `src/components/model-components/list/CustomList.tsx:1433-1444`,
  `src/components/CustomShow/CustomShow.tsx:640-656` · *Docs*
  `start-here/tutorial/Part 5 — Streamlit Dashboards.md:166`,
  `start-here/tutorial/Part 3 — Calculations & Logging.md:188`.
- [x] **UI-18** · P3 — `access-and-dashboards/permissions.md:211` says Create and Delete are
  hidden; in 2.3.0 they are greyed out and Create says why
  (`src/components/model-components/list/CustomList.tsx:1608-1611`,
  `RecordActionButtons.tsx:72-78`).
- [x] **UI-19** · P3 — Empty states ("Nothing here yet", "No rows match… [Clear filters]",
  "could not be loaded"), error toasts with *Show Traceback*, the "Applying changes…" overlay
  (`src/components/model-components/list/GridEmptyState.tsx:48-103`,
  `BareDatagridAGClient.tsx:50`).
- [x] **UI-20** · P3 — The home page is the project's Streamlit dashboard, a widget dashboard,
  or a "Welcome" page with project info; sidebar Streamlit and Reflex entries are framed pages
  (`src/components/CustomReactAdmin/CustomReactAdmin.tsx:75-83`, `lex/lex_app/reflex/Reflex.py:7-31`).
- [x] **UI-21** · P3 — Going back to a list reloads its saved view, not unsaved filters
  (`CustomList.tsx:296-307`); `using-the-app/record-detail/index.md:80-88` and its screenshots
  (`⌂ › fund › show`). Medium confidence.
- [x] **UI-22** · P3 — Analytics tab states "Session expired" (*Sign in again*, *Reload
  dashboard*) and "Analytics not configured" (`src/components/StreamlitIframe.tsx:476-597`);
  `using-the-app/record-detail/analytics tab.md:67-75`.
- [x] **UI-23** · P3 — Forms: the 1/2/3-column toggle on full-page forms; fields that can never
  be edited are hidden; PDF and XLSX fields accept only those types
  (`src/components/model-components/forms/FieldInputForCreateUpdate.tsx:72-74, 182-193`).

## MEDIA — Figures and media

- [x] **MEDIA-1** ✓ · P2 · Stale — **All nine videos predate the current interface.** Every
  file in `videos/` was recorded on 2026-03-05, before the 2.2.0 redesign and before 2.5's
  column filters and record drawer: `grid-multi-filter.mp4` (the filter bar),
  `grid-create-saved-view.mp4`, `grid-export.mp4`, `grid-inline-editing.mp4`,
  `grid-drag-to-group.mp4`, `grid-pivot-mode.mp4`, `record-column-toggle.mp4`,
  `record-history-as-of.mp4` (a control that no longer exists, UI-6), `pycharm-configs.mp4`.
  Re-record or remove.
- [x] **MEDIA-2** ✓ · P2 · Stale — `images/the-grid/first-look.svg` carries the note "Click any
  row to open its record page." (UI-5); `images/the-grid/filter-applied.svg` and
  `images/the-grid/saved-views.svg` (2026-09-16) predate column-header filters. Recapture.
- [x] **MEDIA-3** ✓ · P3 — `images/cli/lex-help.svg` shows no `--version` (REL-1).
- [x] **MEDIA-4** ✓ · P3 — `images/tutorial/navigation.png` is used by no page.
- [x] **MEDIA-5** · P3 — Record-detail screenshots show the breadcrumb `⌂ › fund › show`;
  check them when recapturing (UI-21).
- [x] **MEDIA-6** ✓ · P3 — The Northwind demo dashboard is "ten-page" in
  `access-and-dashboards/streamlit/standalone dashboards.md:7` and
  `access-and-dashboards/streamlit/index.md:47`, "five-page" at `standalone dashboards.md:50`.

## Found while fixing

Places where the source, read again while fixing, said something other than this list. The
docs follow the source; the entries above are left as they were written. Each entry below was
re-read in the source by hand on 2026-11-13.

- **REL-1.** The public `/health` answer carries no version; it is only in the encrypted
  `runtime` field, and only when `LEX_API_KEY` is set. The docs say `lex --version` prints
  `lex, version 2.5.0`.
- **REL-3.** Interface 2.3 adds value lists to the column filters it already had. The "filter
  bar" the 2.5.0 release notes speak of existed only while #822 was being built; saved views
  that still carry its settings are converted when they open.
- **OPS-5.** Generated reports land with the uploads, under `MEDIA_ROOT`: the
  `/app/storage/reports/` setting is read by nothing.
- **OPS-13.** `lex full_migration_workflow` runs `capture_db_tables` and
  `generate_legacy_freeze_manifest --before` itself; nothing has to run first.
- **OPS-19.** One recovery driver is enough, running both is harmless, and either needs
  `CELERY_ACTIVE` as well as `LEX_TASK_RECOVERY_ENABLED`.
- **OPS-20.** `detect_model_changes` also takes `--output`; `sync_keycloak`'s
  `--preserve-renamed-permissions` cannot be switched off.
- **AUTH-1.** Lex App 2.5.0 has no admin screen for API keys — its admin config skips
  autodiscovery and nothing registers `APIKey` — so the docs show
  `APIKey.objects.create_key()` in `lex shell`. A refused create or delete answers a key
  `401 not_authenticated`, and in a list's per-row check a key's `keycloak_scopes` are empty.
- **AUTH-4.** `run_step` no longer exists.
- **API-2.** A date-only `as_of` such as `2026-02-01` is not ignored: Django 6 reads it as
  midnight UTC. On the list `as_of` selects valid time, on history system time.
- **API-11.** `from lex.core.models import HTMLReport` imports the module; the class is
  `from lex.core.models.HTMLReport import HTMLReport`.
- **FW-3.** A bulk delete is all or nothing — one unreadable row answers 404, one refused row
  400 — and `?ids=` with an empty value matches no row; only a missing `ids` addresses all.
- **UI-4 / FW-11.** Search skips integer, float, boolean, foreign-key and file columns only;
  dates, decimals and choices are searched.
- **UI-5.** A row click selects nothing: rows are ticked with checkboxes after **Select rows**.
- **CORE-1.** In-process, values `calculate()` assigned before it failed are still saved
  with `ERROR`; only other rows roll back.
- **CORE-2.** `FireAndForget(exclude_tasks=…)` runs those tasks synchronously, and both
  filters match Celery task names — the old `include_tasks={"calc_and_save"}` example never
  matched anything.
- **CORE-10.** Assigning `valid_from` on the live record is ignored rather than overwritten.
- **CORE-15.** `ranges_of_pivot_concatenation` is accepted and ignored.
- **CORE-19.** Only the grid's list `POST` fills `lex_reserved_calculation_id` and
  `lex_reserved_has_calculation_log`; a `GET` of the list carries `null` and `false`.
- **DASH-7.** lex-app never reads `REFLEX_USE_SINGLE_PORT`; Reflex Enterprise does.
- **MEDIA-2.** `filter-applied.svg` and `saved-views.svg` already show the 2.3.0 toolbar and
  were kept; only `first-look.svg` and `tabs.svg` needed new annotations.
- **MEDIA-6.** The Northwind demo's `main` branch has five dashboard pages — *Overview*,
  *The table*, *A narrower view*, *Reacting to the table*, *Calculations* — and only
  `Fund.streamlit_main`, no `streamlit_class_main`. The ten pages the Streamlit pages named
  live on its unmerged branch `docs/streamlit-showcase` (its PR #1). The Streamlit index's
  table, the embedding pages and the other mentions now describe the five on `main`; if that
  PR merges, they can grow with it.

---

## Outside this repository

- [x] **OUT-1** ✓ · P1 — **The published GitHub release notes for v2.5.0 contradict the
  source**, and `ship-and-operate/upgrading.md:15-20` tells readers to read them first. In each
  case the docs are right:
  - "set `LEX_SCHEDULER_ENABLED=true` and run `run_scheduler` as a separate, long-running
    process" — it defaults to `true` and the clock runs in the web process
    (`lex/lex_app/settings.py:831`, `lex/lex_app/asgi.py:110-112`;
    `ship-and-operate/deploying.md:21`);
  - "`LEX_SESSION_COOKIE_AGE_DAYS` … defaults to 7 days" — it is 31
    (`lex/lex_app/settings.py:1054-1055`);
  - "Files larger than the previous 32MB limit" — the limit was about 100 MB, set by the
    infrastructure; 32 MiB is where chunking starts
    (`lex/api/views/file_operations/ChunkedUpload.py:3-6`, `src/api/chunkedUpload.ts:16`).

  Edit the release body on GitHub; the release-notes drafter may need the same facts.

### Framework issues found along the way

Not documentation gaps; raise them with the lex-app and frontend teams. The docs entries that
depend on each are named.

- [x] **FW-2** ✓ — `LEX_METADATA_CACHE_SECONDS` is read only by a view nothing routes
  (`lex/api/views/ModelStructureObtainView.py`). Wire it or delete it. API-5.
- [x] **FW-3** ✓ — `DELETE …/many` without `ids` deletes every row the caller may delete
  (`lex/api/views/model_entries/filter_backends.py:21-28`). Consider requiring `ids`. API-1.
- [x] **FW-4** ✓ — `lex lex_migrate` and `lex create_db` exit 0 on failure. OPS-4.
- [x] **FW-5** — `lex init --sync-retries` help text says 1; the default is 3. OPS-9.
- [x] **FW-6** — The sidebar "Streamlit" entry frames without `lex_embed` /
  `is_logout_enabled=false` (`lex/lex_app/streamlit/Streamlit.py:41-55`). DASH-8.
- [x] **FW-7** — The foreign-key hover card's *Filter by this value* is always disabled
  (`src/components/model-components/list/FieldView.tsx:363-371`). UI-15.
- [x] **FW-8** — BUG-021 is still open: assigning `obj.valid_from` on the live record is
  silently ignored. CORE-10.
- [x] **FW-9** ✓ — `lex/mcp_server/tools/embed.py` imports `lex.mcp_server.config`, which 2.5.0
  does not ship, and nothing imports it: dead code.
- [x] **FW-10** — Dead code: `src/components/HistoryTimeline/AuditFeedView.tsx`;
  `CalculatedModelMixin.input`. UI-6, CORE-16.
- [x] **FW-11** — Record search ignores the `limit`, `offset` and `model` parameters the
  interface sends, and answers the bare string `"No match found"` when nothing matches
  (`lex/api/views/global_search_for_models/Search.py:11-49`). UI-4.

Found while fixing, and added to LEX-1569. Each was re-read in the source by hand on
2026-11-13; what that check showed is in the entry.

- [x] **FW-12** ✓ — `WaitForTasks` / `FireAndForget` scopes leak between threads:
  `tasks_context` and `unblock_tasks_context` are `ContextVar`s whose default is one mutable
  dict, and `tasks_context.set()` is never called, so every thread pushes onto the same
  stack (`lex/lex_app/celery_tasks.py:536-544`, `:452`).
- [x] **FW-13** ✓ (in part) — On a Celery failure the dispatching process always saves its own
  pre-run copy as `ERROR`: the guard that should skip it reads an in-memory marker the worker
  never sets (`lex/core/models/CalculationModel.py:430-434`, `:1608-1614`). Whether that
  overwrites the error text the worker wrote depends on which save lands last. CORE-1.
- [x] **FW-14** ✓ — `lex setup-with-ai --mcp-mode` has no effect: the flag is used only when
  the credentials carry no mode, and their mode defaults to `forward`
  (`lex/bin/lex.py:1442`, `lex/tools/setup_with_ai.py:369`). OPS-12.
- [x] **FW-15** ✓ — `lex sync_keycloak` exits 0 when it fails: every failure writes to stderr
  and returns (`lex/lex_app/management/commands/sync_keycloak.py:71-146`). Like FW-4. OPS-20.
- [x] **FW-16** ✓ — `lex bootstrap_keycloak` prints "✗ … aborted or timed out" after a
  successful setup: `wait_for_keycloak_setup` returns `None` on success
  (`lex/lex_app/management/commands/init.py:247-256`), which the command reads as failure
  (`bootstrap_keycloak.py:106-117`).
- [x] **FW-17** ✓ — A bulk `PATCH` on `…/many` never changes a row: `perform_bulk_update` calls
  `save()` on a `ListSerializer` that has no `update()`, so Django REST framework raises
  `NotImplementedError` (`lex/audit_logging/mixins/BulkAuditLogMixin.py:72-91`,
  `lex/api/serializers/base_serializers.py:196`). API-1.
- [x] **FW-18** ✓ — `api/model_entries/calculationlog/list` lists every calculation log: the
  list's read filter returns all `CalculationLog` rows (`filter_backends.py:56-57`), while
  the log tree shows only logs of records the caller may read under `LEX_SEC_INTERNAL`
  (`CalculationLogTreeView.py:17-55`).
- [x] **FW-19** ✓ — Streamlit: a Keycloak outage while permissions are fetched empties
  `st.session_state.permissions`: `get_uma_permissions` returns `None` instead of raising
  (`KeycloakManager.py:668-670`), so the keep-the-old-list `except` never runs
  (`lex/streamlit_app.py:521-533`). DASH-1.
- [x] **FW-20** ✓ (behaviour; intent to decide) — A finished `lex_view` flow stays finished for
  the whole browser-tab session, reloads included: positions live in `sessionStorage` keyed
  by the flow (`src/utils/flowState.ts:1-20, 85-93`). A design question, not a defect.
- [x] **FW-21** ✓ — The `lex_view` docstring says `hide_actions` hides "the top actions bar
  (Create button, Refresh, Export)" (`embed.py:694-697`); interface 2.3.0 hides each row's
  Actions column (`CustomDatagrid.tsx:2591-2596`).
- [x] **FW-22** ✓ — Nothing sends on `ws/logs` in 2.5.0: no code sends to `log_group`, and a
  message to the socket gets a fixed `STATUS` reply (`lex/api/consumers/LogConsumer.py`).
- [x] **FW-23** ✓ — `lex full_migration_workflow --db-name` only sets `DB_NAME`
  (`lex/full_migration_workflow.py:393`); the settings never read it, and the one script that
  does, `backfill_history_sql.py`, is not a step. OPS-13.
- [x] **FW-24** ✓ — The Streamlit report is registered whether or not `IS_STREAMLIT_ENABLED`
  is set (`generic_app_config.py:208-212`); only its place in the sidebar structure is gated
  (`model_structure_builder.py:207`).
- [x] **FW-25** ✓ — Record search: the 2.5.0 backend sends none of the `title`, `snippet`,
  `rank`, `matched_field`, `model_label` or `meta.per_model` the 2.3.0 dialog types expect
  (`src/api/global-search.ts:14-36`; `Search.py:38-49`). UI-4.
- [x] **FW-26** ✓ (traced) — Export from the History and Audit Log tabs exports the record's
  live table. The export posts to the page's resource (`useAgGridExport.ts:290, 362`), and on a
  record page that is the live model: each tab's toolbar sits outside the tab's `ListBase`
  (`CustomShow.tsx:684-695, 757-761`), and the `resource` it is handed never reaches the button
  (`GridViewToolbar.tsx:129`). Nothing ticked exports the model's current rows; ticked rows send
  their own ids — a version's `history_id` (`process-admin-data-provider.ts:125-141`) or a log
  entry's id — which the export matches against the live model's primary key
  (`ModelExport.py:749-751`). No record filter is sent either: only ticked ids, `serializer` and
  `as_of` (`useAgGridExport.ts:347-366`), not the tab's `listFilter` (`CustomShow.tsx:769`). The
  missing filter was found while fixing, the wrong table in the fact-check after the merge; the
  History and Audit Log tab pages now warn about it. UI-6.
- [x] **FW-27** ✓ — Calculation-finished toasts reach every signed-in user: all sockets join one
  `update_calculation_status` group (`UpdateCalculationStatusConsumer.py:23`), and the
  interface toasts on every success (`CalculationStatusUpdate.tsx:150-158`). UI-1.
- [x] **FW-28** ✓ (traced) — Superusers can edit history rows in place, `Valid From` and
  `Valid To` included, in Full history and on the record's History tab, while the rows' Edit
  and Delete buttons stay greyed out for everyone. The backend adds `valid_from`/`valid_to` to a
  history row's edit scope (`base_serializers.py:599-603`) and empties the scope only for
  non-superusers (`:506-516`); both grids show `historical<model>`, which is not read-only
  (`resourceMutability.ts:1-12`; `CustomList.tsx:196`, `CustomShow.tsx:704-707`), and a cell is
  editable whenever the row's scope names it (`CustomDatagrid.tsx:3019-3027`), whatever
  `isHistoryView` says — only the buttons check it (`RecordActionButtons.tsx:73-78`). The PATCH
  passes for a superuser (`security.py:277-278`; `edit_violations` skips history rows, which have
  no `permission_edit`, `:219-220`), and the save re-chains Valid To, writes a system-time entry
  and syncs the live record (`signal_registry.py:110-121`). lex-app's own tests cover the backend
  half: 4.107 (a superuser's PATCH answers 200), 4.109, 12.65 (the scope includes
  `valid_from`). Decide whether in-place correction is meant; either way the buttons and the
  cells should agree. Traced to the end on 2026-11-13, not run; the pages now describe it. UI-7,
  UI-9.
- [x] **FW-29** ✓ — The Celery route never detects a dead broker: `should_use_celery` checks
  `CELERY_ACTIVE` and constructs `inspect()`, which opens no connection
  (`CalculationModel.py:1119-1127`), so the intended in-process fallback never happens.
  Found by the fact-check after the merge.
- [x] **FW-30** ✓ — An `as_of` date-time that does not exist answers `500`:
  `parse_as_of_datetime` lets Django's `ValueError` through (`temporal.py:28-30`), and no caller
  catches it (`ModelEntryProviderMixin.py:84`; `History.py:94`, whose `try` at 98-102 wraps only
  the query; `ModelExport.py:1802`). A date alone that does not exist (`2026-13-45`) is silently
  ignored instead. Answer `400` for both. Found by the re-check of the fact-check's corrections.
  API-2.
- [x] **FW-31** ✓ — An empty `DEPLOYMENT_ENVIRONMENT` is read two ways: the settings test
  `is not None` (`settings.py:410, 1089, 1152, 1275` among others;
  `authentication/dashboards/sites.py:41`), while `lex start`, `lex init`, the calculation-log
  cache, the platform-API call and the MQ worker test truthiness (`bin/lex.py:1307`,
  `init.py:99`, `CacheManager.py:52`, `LexAPI.py:34`, `apps.py:281`). Use one rule. Found by
  the re-check.
- [x] **FW-32** ✓ — Migration step 6 keeps some operations on the tables it protects: it
  matches `model_name=` on any operation but `name=` only on six operation types
  (`sanitize_v2_migrations.py:8-16, 57-74`), and `RenameModel` names its model with
  `old_name`/`new_name`. An `AlterUniqueTogether`, `AlterOrderWithRespectTo` or `RenameModel` on
  a V1-only table still runs in `migrate`. Found by the re-check.

## Housekeeping

- [x] Close PR #211 (calculation-log export) as superseded: `calculations/logging.md`
  "Downloading the log as PDF" has the scopes, the `include_descendants` alias, the 500-section
  cap and the rendering contract.
- [x] Close draft PRs #200 (2.2.1) and #226 (2.2.2). Their topics landed, except the interface
  packaging point, which is REL-2.
- [x] Keep PR #254 (PostHog usage metrics) open until the release that ships it: neither lex-app
  2.5.0 nor frontend 2.3.0 reads a PostHog variable.
- [x] Delete branches whose content landed reworded: `docs/audit-fixes-1`, `docs/audit-fixes-2`,
  `docs/audit-fixes-3`, `docs/activation-applier`, and the 35 `copilot/*` docs-update branches.
- [x] Optional, local: remove worktrees of merged branches (`cd-docs`,
  `lex-app-docs-hardening`, `lex-app-docs-lex1554`, `.claude/worktrees/auth-long-sessions`,
  `.claude/worktrees/session-cookie-age`, `.worktrees/lex-898`, `.worktrees/generic-frontend`).
  Keep `lex-app-docs-ext` — it holds 3.0 work. Decided on 2026-11-13: keep them all; nothing
  was removed.
- [x] In `DOCS_PLAN_2026-09.md` Phase 4, tick "Root-level duplicate tree": no tracked file is
  left outside `content/`.

## 2.5.0 traceability

Every PR merged between `v2.4.2` and `v2.5.0`, and every frontend PR in `v2.2.1..v2.3.0`.

| lex-app PR | Change | Docs | Status |
| --- | --- | --- | --- |
| #822 | Value-list filters, `filter_values`, `lex_view` filters, `LEX_EMBED_ALLOWED_ORIGINS`, `__blank`, typed `__in`/`__exact` | filtering and sorting, Grid Filter API, embedding app pages, Environment Variables | ✅ — upgrade note (REL-3), interface version (DASH-4), `lex_filterable_fields` (AUTH-7) |
| #869 | Long-lived sessions, `LEX_STREAMLIT_AUTH`, `LEX_INSTANCE_HOSTS`, `LEX_WS_AUTH`, strict CORS | sign-in and sessions, streamlit sessions, upgrading, Environment Variables | ✅ — CORS row wording (AUTH-10) |
| #866 | Auth hotfixes; deployed instances need a private `DJANGO_SECRET_KEY` | sign-in and sessions | ⚠️ the startup refusal (OPS-2) |
| #880 | Scheduled jobs | scheduled jobs, deploying | ✅ — upgrade note (REL-3), bare `@lex_job` (CORE-14) |
| #883 | Chunked uploads | custom frontend, summary tab, troubleshooting, upgrading | ✅ — "your team sets" (API-15) |
| #882 | Streamlit and Reflex on an attached domain | custom domains, embedding app pages | ✅ — hand-off hosts (AUTH-9), embed origins (DASH-5) |
| #885 | `LEX_EXTRA_ALLOWED_HOSTS` | Environment Variables, upgrading | ✅ |
| #853 | Backend Service name in `ALLOWED_HOSTS` | upgrading | ✅ |
| #879 | Long tokens, `WEBSOCKETS_MAX_LINE_LENGTH`, `websockets>=13` | Environment Variables, upgrading | ✅ |
| #878 | `lex_column_options` | serializers | ✅ — other `Meta` options (API-7) |
| #877 | Initial data survives restarts | initial data, upgrading | ✅ |
| #876 | Calculation-log PDF scopes | logging | ✅ — audit payload fields (CORE-18) |
| #874 | A failed run's traceback in the audit log | audit logs | ✅ — `cancelled`/`aborted` (CORE-3) |
| #870–#873 | Log frames for generated rows, sync and Celery runs | logging, LexLogger API, CalculationModel Internals | ✅ |
| #871 | `create()` arguments reach `calculate()` on Celery | CalculatedModelMixin Internals | ✅ |
| #865 | `nest_asyncio` no longer applied | upgrading | ✅ |
| #810 | `lex init` makes migrations for the project only | — | ❌ OPS-9 |
| #895 | `lex-app-frontend~=2.3.0` | — | ❌ REL-2 |
| #863, #854 | Dashboard framing and tab take-over fixes | — | n/a |
| #864, #888, #893, #894, #896–#899 | CI, tests, docs mirror | — | n/a |

| Frontend PR | Change | Docs | Status |
| --- | --- | --- | --- |
| #579 | Value-list column filters, Streamlit filters | filtering and sorting | ✅ — figures (MEDIA-2) |
| #622 | Auth contract v2 client | sign-in and sessions, using-the-app | ✅ |
| #633 | Chunked uploads | summary tab | ✅ |
| #632 | Dashboards framed from the viewer's domain | custom domains | ✅ |
| #631 | View drawer, narrower ID column | the-grid | ✅ — row click (UI-5) |
| #630 | Calculation-log downloads with scopes | logging | ✅ — the end-user log page (UI-1) |
| #634 | The log's Details tab never navigates away | — | ⚠️ UI-1 |
| #621 | A 403 never signs out | using-the-app | ✅ — custom frontend example (AUTH-3) |
| #597 | Only the dashboard frame may take over the tab | — | n/a |
| #580 | Adapt to v2 security hardening | permissions | ⚠️ greyed, not hidden (UI-18) |

Older releases still owed: 2.4.2 `?api_key=` (AUTH-1); 2.4.0 permission hooks on the filled
record (AUTH-2); 2.3.5 `lex --version` (REL-1); 2.3.3–2.3.4 Reflex single port (DASH-7); 2.2.2
run-id row fields (CORE-19); 2.2.1 the frontend package (REL-2).

## Checked and found covered

- **Auth.** `LEX_STREAMLIT_AUTH` modes and the hand-off, `__Host-lex_dash`, `/auth/*` routes,
  the auth contract v2 bodies, `api/auth/session`, `LEX_SESSION_COOKIE_AGE_DAYS`,
  `OIDC_TOKEN_ENCRYPTION_KEYS`, the `oidc_*` and `prune_dashboard_sessions` commands,
  `LEX_WS_AUTH`, the UMA cache, `LEX_EMBED_ALLOWED_ORIGINS` parsing, `LEX_EXTRA_ALLOWED_HOSTS`,
  `LEX_INSTANCE_HOSTS`, the 2.5 sign-in upgrade notes, the other security switches. No stale
  `?auth_token=` or `Refresh*Middleware`.
- **REST.** `filter_values` (limits, truncation at 5,000 values / 50,000 rows), typed
  `__in`/`__exact`, `__blank`, `FILTER_NOT_ALLOWED`, value-list eligibility and opt-out,
  `lex_column_options`, credential-name stripping, `<fk>__short_description`, `?serializer=`,
  clearable files, the chunked-upload protocol (32 MiB, 5 GiB, 24 h), PDF scopes, export and
  download audit. The filter bar added and then removed inside #822 left no trace.
- **Modelling.** Scheduled jobs, `calculate_on_create` and `calculation_closed_reason()`, nested
  and generated-row log nodes, cancel and stuck-run tools, batch calculations, change
  detection, timezone-aware assignment, initial-data lock, bitemporal levels and the activation
  applier, Celery recovery, `rebase_incident_datetimes`. Process/ProcessFlow (removed in 2.4.0)
  has no page left.
- **Dashboards.** `lex_view` events, `Flow`, `filters`/`on_filter`, the other `lex_view`
  arguments, `lex_calculation*`, `lex_widgets`, `WidgetSpecError`, model and standalone
  dashboards, `main()`, the 2.5 dashboard changes, the Reflex APIs, `LEX_THEME_FOLLOW`.
- **Operations.** `lex reflex`, `lex run_scheduler`, recovery entry points, backfill and
  normalize commands, `keycloak_backup`, migration snapshots, the pytest plugin, health
  endpoints, `lex start`, database profiles, `lex-generate-configs`. Documented environment
  variable defaults agree with the source.
- **Interface.** Value-list and condition filters, table settings and column formats, the
  view/edit/create drawers, the ID column, large uploads, staying signed in, PDF scopes, themes,
  grouping and pivoting, creating saved views, live updates.
- **Navigation.** Every page is linked from its section index; no orphan pages.

## Method

1. **Gates.** lex-app's own docs checks, run from the `v2.5.0` tree against `content/` — all
   pass:

   ```bash
   mkdir -p /tmp/lex-2.5.0 && git -C ../lex-app archive v2.5.0 | tar -x -C /tmp/lex-2.5.0
   python3 /tmp/lex-2.5.0/.github/scripts/check_doc_env_vars.py "$PWD/content"
   python3 /tmp/lex-2.5.0/.github/scripts/check_doc_commands.py "$PWD/content"
   python3 /tmp/lex-2.5.0/.github/scripts/check_doc_imports.py "$PWD/content"
   ```

2. **Sweeps the gates cannot do.** Documented environment-variable defaults against the literal
   defaults in the source; settings read with `getattr(settings, …)`; navigation and orphan
   pages; figures and videos by capture date; open PRs and unmerged branches by content rather
   than by branch status.
3. **Release by release.** The 31 PRs merged between `v2.4.2` and `v2.5.0`, the published v2.5.0
   release notes, the CHANGELOG from 2.1.1 to 2.4.2, and the frontend PRs in `v2.2.1..v2.3.0`.
4. **Six area audits** — auth and security, dashboards, REST API, modelling and calculations,
   CLI and operations, interface. Each inventoried the public surface from source, grepped
   `content/` for every item, and read the matching sections before judging.
5. **Verification.** Every P1 and every item marked ✓ was re-read in the source for this list.
   One candidate was dropped on re-check: the upload and value-list limits are documented
   (`ship-and-operate/custom frontend.md:137`, `reference/Grid Filter API.md:84`); only the
   "your team sets" wording survives, as API-15.
6. **Fact-check after the merge.** Seven reviewers that had not written the pages checked every
   line #271 and #272 added — over 1,100 claims — against the 2.5.0 and 2.3.0 source and the
   Northwind demo's `main`. Each statement they found wrong or loose was re-read in the source
   by hand and corrected in a follow-up PR; two were framework issues: FW-29 is new, and FW-26
   turned out wider than first written. Claims that rest on the platform, on Reflex
   Enterprise or on older releases could not be checked against these sources. A second
   reviewer then re-checked that PR's own changes the same way: one statement was wrong (an
   impossible `as_of` date alone is ignored, not answered with `500`) and six were loose. Each
   was confirmed in the source by hand and corrected in a fourth PR, and three framework issues
   came out of it (FW-30 to FW-32).
