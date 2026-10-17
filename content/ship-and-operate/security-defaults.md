---
title: Security defaults
---

Lex App 3.0 turns on a set of hardenings that earlier versions left off. Each one closes a way data could leak or be changed by someone who should not. They are **on by default**; while you migrate, you can switch them off — all at once or one at a time.

## What is on

| Flag | On means | Before 3.0 |
|---|---|---|
| `TRACEBACKS` | Error responses carry no server traceback, unless `DEBUG` is on or `LEX_API_TRACEBACKS=true` | Every 500 from the generic CRUD endpoints included the full traceback |
| `FAIL_CLOSED` | An exception inside a permission method denies access and is logged | An exception counted as "allowed" |
| `NOT_FOUND` | A record the user may not read answers 404; so does a path under `api/` that no route matches | 200 with `{}`; an unknown `api/` path answered the frontend's `index.html` with 200 |
| `READ_SURFACES` | History, global search, export and file download apply read permission | They did not |
| `EDIT` | `permission_edit` on PATCH/PUT, bulk PATCH and `run_step`; `permission_delete` per row on bulk delete; `permission_create` on `run_step` | Not enforced on these paths |
| `FILTERS` | List filters and ordering only on fields a response can contain | Any model field |
| `OIDC_REDIRECT` | `next`/`fail` on `/oidc/*` must be relative, the site's own origin, or an origin in `CORS_ALLOWED_ORIGINS` / `CORS_ORIGIN_WHITELIST` / `CSRF_TRUSTED_ORIGINS` (wildcards like `https://*.example.com` included); otherwise 400 | Any URL was followed — an open redirect |
| `INTERNAL` | Only superusers change Django's users, groups and permissions through the generic API, write to the server log (`POST api/logs`) or delete unused files; the calculation log tree and its PDFs show only logs of records the caller may read — see [[access-and-dashboards/generic-api#Operator endpoints in every mode\|Operator endpoints]] | Every signed-in user could |
| `ERRORS` | The generic endpoints raise their refusals and errors to the exception handler, so a project's `EXCEPTION_HANDLER` sees every one; a `LexActionError`, DRF error or mapped database error from model code keeps its status — see [[access-and-dashboards/custom-api#Errors and database rules\|Errors and database rules]] | Error bodies were returned past the handler, and errors raised while saving became a 500 |

> [!note]
> The bundled frontend works unchanged with every flag on: new denials answer 400 or 404, never a new 403 (a 403 signs the user out of the frontend).

## Switching them off

```bash title=".env"
LEX_LEGACY_SECURITY=true      # all flags off — the pre-3.0 behaviour
LEX_SEC_EDIT=true             # …but keep this one on
```

```bash title=".env"
LEX_SEC_FILTERS=false         # only this one off
```

A per-flag `LEX_SEC_<FLAG>` always wins over `LEX_LEGACY_SECURITY`. The opt-out is a migration aid: it logs a deprecation warning once, the first time a legacy check runs, and will be removed in a later major release.

## Related switches

| Variable | Default | Purpose |
|---|---|---|
| `LEX_API_TRACEBACKS` | unset | `true` puts tracebacks back into error responses even with `DEBUG` off (for a staging system) |
| `LEX_ERROR_FORMAT` | unset | `structured` makes every error body `{code, detail, error, fields}`; leave unset for the bundled frontend, which reads DRF's field-error shape |
| `LEX_CORS_ALLOWED_ORIGINS` | unset | Comma-separated origins allowed to make credentialed cross-origin requests. When set, it replaces the permissive defaults (`CORS_ORIGIN_ALLOW_ALL` and `"*"`) |

## See also

- [[reference/Environment Variables]]
- [[access-and-dashboards/custom-api]]
- [[access-and-dashboards/permissions]]
