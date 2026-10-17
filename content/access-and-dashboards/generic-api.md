---
title: Generic API for your clients
---

Lex App serves every model on its generic endpoints (`api/model_entries/<model>/…`), and the bundled frontend is built on them. A project whose own web app, mobile app or integrators use those endpoints opens them model by model and keeps everything else for operators.

> [!note]
> Since Lex App 3.0. Without the settings on this page nothing changes.

## Open the records you mean to

```python title="lex_config.py"
GENERIC_API = "records"
```

```python
class Invoice(LexModel):
    lex_api_exposed = True                         # list, retrieve, create, update, delete

class Customer(LexModel):
    lex_api_exposed = {"list", "retrieve"}         # read only

class Payment(LexModel):
    lex_api_exposed = {"list", "retrieve", "history", "export"}
```

In mode `"records"` every signed-in user and every API key reaches the operations a model names, and nothing else of the generic API. Inside them the model's permission methods still decide, as on every other path: a record the caller may not read is 404, a field they may not edit is 400 — see [[access-and-dashboards/permissions#How the API enforces them (3.0)|how the API enforces permissions]].

| Operation | Routes |
|---|---|
| `list` | `api/model_entries/<model>/list` (GET, and the grid's POST read) |
| `retrieve` | GET `api/model_entries/<model>/<calculationId>/one/<pk>`, or `…/one/<uuid>` with a [[access-and-dashboards/custom-api#Public identifiers\|public identifier]] |
| `create` | POST `api/model_entries/<model>/<calculationId>/one` |
| `update` | PATCH or PUT on a record |
| `delete` | DELETE on a record |
| `history` | `api/model_entries/<model>/<calculationId>/history/<pk>` (or `/<uuid>`) |
| `bulk` | `api/model_entries/<model>/many` |
| `export` | `api/<model>/export` |
| `file` | `api/<model>/file-download` |

`True` stands for the first five. History, bulk, export and file download reach more than one record's current data — who changed what, many rows at once, whole files — so a model names them explicitly. A value that is not `True`, `False` or a set of these names (a typo, or a plain string such as `"list"`) stops the server at startup with an error naming the model.

The [[access-and-dashboards/actions|actions]] of an exposed model are reachable whatever operations it names; each action's own `permission` decides. On a model that is not exposed they are 404 like everything else.

## Everything else is 404

For a caller who is not a superuser, the rest of `api/` does not exist. It answers 404 `{"code": "NOT_FOUND", "detail": "Not found.", "error": "Not found."}`, the same as a misspelt path:

- models without `lex_api_exposed`, including Django's users and every history table;
- an operation the model does not name — a PATCH on a read-only model is 404, not 405;
- Lex App's own endpoints: `api/model-structure`, `api/run_step/…`, global search, the calculation log tree, `api/user/` and the others the bundled frontend uses.

Superusers reach all of it, so the bundled frontend keeps working for operators; for everyone else its requests answer 404. An anonymous caller gets 404 for a closed path and the usual sign-in answer for an exposed one; `api/user/` keeps its 401 for anonymous callers so the frontend can send operators to sign in. Always open: `api/health` and, with `API_URLCONF`, [[access-and-dashboards/custom-api|your own API prefix]].

WebSockets follow the switch too: in every mode except `"all"` only superusers open a socket under `ws/`, because the sockets carry events about every model. Anyone else's handshake is closed with code 4404.

## The modes

| `GENERIC_API` | Who uses the generic endpoints |
|---|---|
| `"all"` (default) | Everyone the endpoints themselves admit — the behaviour before 3.0 |
| `"records"` | Every signed-in user and API key, for the operations exposed models name; the rest superusers only |
| `"superuser"` | Superusers only — see [[access-and-dashboards/custom-api#Keep the generic API for operators only\|Keep the generic API for operators only]] |
| `"off"` | Nobody; this also disables the bundled frontend |

An unknown mode stops the server at startup.

## Operator endpoints in every mode

Whatever `GENERIC_API` says, a caller who is not a superuser:

- cannot change Django's users, groups or permissions through the generic API — 400 `EDIT_NOT_ALLOWED`;
- cannot write to the server log (`POST api/logs`) or delete unused files (`api/delete-unused-files`) — 404;
- sees in the calculation log tree only the logs of a calculation that ran on a record they may read. A calculation without a record shows nothing, the tree without a `calculation_id` is empty, and the PDF of a log they may not see (`api/download-pdf/<id>/`) is 404.

This is the security flag `INTERNAL`; [[ship-and-operate/security-defaults]] has the opt-out.

## Errors reach your handler

A project with its own `EXCEPTION_HANDLER` sees every error of the generic endpoints — refusals, unknown fields, not-found answers, business errors raised while saving — and can give all of them one shape. See [[access-and-dashboards/custom-api#Errors and database rules|Errors and database rules]].

## See also

- [[access-and-dashboards/permissions]] — what decides inside an exposed operation
- [[access-and-dashboards/api-keys]] — keys for integrators
- [[reference/lex_config]] — every key at a glance
