---
title: Generic API for your clients
---

Lex App serves every model on its generic endpoints (`api/model_entries/<model>/…`), and the bundled frontend is built on them. A project whose own web app, mobile app or integrators use those endpoints opens them model by model and keeps everything else for operators.

> [!note]
> Since Lex App 3.0. The default, `GENERIC_API = "all"`, leaves the generic endpoints as they were.

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
| `action` | only the model's [[access-and-dashboards/actions\|actions]], none of its record routes |

`True` stands for the first five. History, bulk, export and file download reach more than one record's current data — who changed what, many rows at once, whole files — so a model names them explicitly. A value that is not `True`, `False` or a set of these names (a typo, or a plain string such as `"list"`) stops the server at startup with an error naming the model.

The actions of an exposed model are reachable whatever operations it names; each action's own `permission` decides. `{"action"}` exposes the actions alone — for a model whose records change only through its operations. On a model that is not exposed they are 404 like everything else.

## Everything else is 404

For a caller who is not a superuser, the rest of `api/` does not exist. It answers 404 `{"code": "NOT_FOUND", "detail": "Not found.", "error": "Not found."}`, the same as a misspelt path:

- models without `lex_api_exposed`, including Django's users and every history table;
- an operation the model does not name — a PATCH on a read-only model is 404, not 405;
- Lex App's own endpoints: `api/model-structure`, `api/run_step/…`, global search, the calculation log tree, `api/user/` and the others the bundled frontend uses.

Superusers reach all of it, so the bundled frontend keeps working for operators; for everyone else its requests answer 404. An anonymous caller gets 404 for a closed path and the usual sign-in answer for an exposed one; `api/user/` keeps its 401 for anonymous callers so the frontend can send operators to sign in. Always open: `api/health` and, with `API_URLCONF`, [[access-and-dashboards/custom-api|your own API prefix]].

A path under `api/` that no route matches is 404 for everyone, superusers included, in every mode — not the frontend's `index.html` with 200, which made a removed or misspelt endpoint look like a success (security flag `NOT_FOUND`).

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

## Short paths

The record routes carry a `calculationId` segment that only the bundled frontend uses. Your clients can leave it out; Lex App then assigns one per request (`api_<hex>`, the `calculation_id` of the request's audit entries):

| Short path | Long form |
|---|---|
| `api/model_entries/<model>/list` | the same |
| `api/model_entries/<model>/one` | `…/<model>/<calculationId>/one` |
| `api/model_entries/<model>/one/<uuid>` | `…/<model>/<calculationId>/one/<uuid>` |
| `api/model_entries/<model>/one/<uuid>/history` | `…/<model>/<calculationId>/history/<uuid>` |
| `api/model_entries/<model>/one/<uuid>/action/<name>` | `…/<model>/<calculationId>/one/<uuid>/action/<name>` |
| `api/model_entries/<model>/action/<name>` | `…/<model>/<calculationId>/action/<name>` |

A record is addressed by its [[access-and-dashboards/custom-api#Public identifiers|public identifier]] on the short paths; there is no short form with an integer key. The long forms keep working.

## Public identifiers in and out

For clients that know a record only by its uuid, two more settings make the responses look like your API, not Lex App's internals:

```python
from lex.api.project import LexLookupRelatedField


class Document(LexModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=200)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    lex_lookup_field = "uuid"
    lex_lookup_allow_pk = False
    lex_api_exposed = True
    lex_api_internal_fields = False


class DocumentSerializer(serializers.ModelSerializer):
    folder = LexLookupRelatedField(queryset=Folder.objects.all())

    class Meta:
        model = Document
        fields = ["uuid", "title", "folder"]


Document.api_serializers = {"default": DocumentSerializer}
```

```json
{"uuid": "7c0e…", "title": "Plan", "folder": "2f1a…"}
```

- **`lex_api_internal_fields = False`** — the responses are exactly the serializer's field list. Lex App adds nothing: no integer `id`, `id_field`, `short_description`, `lex_reserved_scopes` or `<fk>__short_description`. It applies to the model's serializers in `api_serializers`. The bundled frontend relies on those fields, so set it on models only your own clients read.
- **`LexLookupRelatedField`** — a foreign key read and written as the related record's public identifier (its `lex_lookup_field`; the primary key if it has none). The queryset is evaluated per request: a related record that does not exist or that the caller cannot see — hidden by row-level security, or missing from the queryset you pass — answers 404, as for any record outside their access. `missing="invalid"` keeps DRF's 400 field error instead. For a read-only field pass the model: `LexLookupRelatedField(model=Folder, read_only=True)`.
- **List filters by public identifier** — a foreign key to a model with `lex_lookup_allow_pk = False` is filtered by that model's public identifier: `?folder=<uuid>`.

## OpenAPI document

With the [[access-and-dashboards/custom-api#OpenAPI schema|OpenAPI schema]] switched on, Lex App can describe the exposed records too, so a typed client is generated from one document:

```python title="lex_config.py"
SCHEMA = {
    "title": "My Project API",
    "version": "1.4.0",
    "generic": {"short_paths": True},                    # document the exposed models
    "error_component": "myproject.api.ErrorSerializer",  # the body of every documented 4xx
}
```

Every model with `lex_api_exposed` gets one operation per exposed operation and per action, with a stable operation id:

| Operation id | Path (short) |
|---|---|
| `<model>_list` | GET `…/<model>/list` — an array of the model's serializer |
| `<model>_create` | POST `…/<model>/one` — 201 |
| `<model>_retrieve`, `<model>_update`, `<model>_delete` | GET, PATCH, DELETE `…/<model>/one/{uuid}` |
| `<model>_history` | GET `…/<model>/one/{uuid}/history` |
| `<model>_<action>` | `…/<model>/one/{uuid}/action/<action>` or `…/<model>/action/<action>` |

`<model>` is the model's lowercase name. Path parameters are typed (a `uuid` lookup field is a uuid). Request and response bodies are the model's `api_serializers["default"]` as you declared it, or the generated serializer. `"short_paths": False` documents the long forms with their `calculationId`; the short form is the default. Since short paths address records by uuid, models documented with them need a `lex_lookup_field`.

The parameters a model documents:

```python
from drf_spectacular.types import OpenApiTypes


class Document(LexModel):
    lex_api_tag = "Documents"                      # default: the class name
    lex_api_filters = ("folder", "title")          # list filters to document, besides ordering
    lex_query_parameters = {                       # further query parameters on every operation
        "lang": (OpenApiTypes.STR, "Language of the titles"),
    }
```

`lex_api_filters` and `lex_query_parameters` only describe: which filters a list accepts is decided by the [[access-and-dashboards/permissions#Filtering and ordering|filter rules]]. The parameter of a [[access-and-dashboards/request-scope|request scope]] is documented on every operation.

An action's operation carries its input (query parameters for a GET action, a multipart body with `media="multipart"`), its output serializer (an array of it with `many=True`, a file with `output=OpenApiTypes.BINARY`), its status, and the `summary`, `description`, `operation_id`, `tags` and `responses` of its declaration — see [[access-and-dashboards/actions#Describing an action|Describing an action]]. With `error_component`, the operations' 400 and 404 answers, and an action's further `responses`, use your error serializer; without it no error answers are documented.

The generic operations are added to the paths `SCHEMA["include"]` keeps, and `lex schema --validate --fail-on-warn` checks the whole document.

## Errors reach your handler

A project with its own `EXCEPTION_HANDLER` sees every error of the generic endpoints — refusals, unknown fields, not-found answers, business errors raised while saving — and can give all of them one shape. See [[access-and-dashboards/custom-api#Errors and database rules|Errors and database rules]].

## See also

- [[access-and-dashboards/permissions]] — what decides inside an exposed operation
- [[access-and-dashboards/api-keys]] — keys for integrators
- [[reference/lex_config]] — every key at a glance
