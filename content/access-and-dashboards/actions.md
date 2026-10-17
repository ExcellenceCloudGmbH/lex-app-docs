---
title: Actions
---

Operations that are not create, read, update or delete — approve, submit, sign, import, archive — are declared on the model with `@lex_action`. Each gets its own URL with the guarantees of the generic endpoints: sign-in, read permission, validated input, a permission of its own, one transaction, the database context, an audit-log entry and Lex App's error format. A project can run every operation of its product this way, without a hand-written endpoint.

```python
from rest_framework import serializers
from lex.api.project import ActionResult, LexActionError, lex_action


class ApproveInput(serializers.Serializer):
    note = serializers.CharField(max_length=200)


class Invoice(LexModel):
    @lex_action(permission="edit", input=ApproveInput)
    def approve(self, context, data):
        if self.status != "submitted":
            raise LexActionError("Only submitted invoices can be approved.", code="NOT_SUBMITTED", status_code=409)
        self.status = "approved"
        self.note = data["note"]
        self.save()
        return {"status": self.status}

    @lex_action(detail=False, permission="permission_import", input=ImportInput, status=201)
    def import_batch(cls, context, data):
        ...

    @classmethod
    def permission_import(cls, user_context, data):
        return "finance" in user_context.groups and len(data["rows"]) <= 1000
```

`context` is the caller's [[access-and-dashboards/permissions#The UserContext Object|UserContext]]; `data` is the validated input. A record action is an instance method; a collection action (`detail=False`) is called on the class. The URL name is the method's name unless `name=` says otherwise.

| Route | For |
|---|---|
| `POST api/model_entries/<model>/<calculationId>/one/<pk>/action/<name>` | a record action |
| `POST …/one/<uuid>/action/<name>` | the same, by [[access-and-dashboards/custom-api#Public identifiers\|public identifier]] |
| `POST api/model_entries/<model>/<calculationId>/action/<name>` | a collection action |

`methods=("get",)` serves an action on GET instead of POST; several methods are allowed.

> [!note]
> Since Lex App 3.0.

## What happens on a call

1. **Find.** An action that does not exist on the model, or not for this kind of route, is 404; a method it does not allow, 405. For a record action the record must exist, be readable for the caller and lie inside the [[access-and-dashboards/request-scope|request scope]] — otherwise 404.
2. **Validate.** `input` is a DRF serializer. Keys it does not declare answer 400 `UNKNOWN_FIELDS`, invalid values DRF's 400. A GET action validates its query string; the request scope's parameter is not part of it. Without `input`, `data` is the body (or query string) as sent.
3. **Permit.** The action's permission decides, with the validated input — see below.
4. **Run.** In one transaction, with the caller's [[ship-and-operate/row-level-security|database context]] and audit context: records the method saves name the caller in `created_by` / `edited_by`.
5. **Record.** After the method succeeded, an [audit-log entry](#audit-log).
6. **Answer.** From what the method returned — see [Answers](#answers).

A throttle and a model's `modification_restriction` are checked before all of this, like DRF permissions.

## Who may run it

| `permission=` | Allows the run when |
|---|---|
| `"edit"` | `permission_edit` does not deny the record outright (record actions only) |
| `"create"` | `permission_create` allows |
| `"delete"` | `permission_delete` allows the record (record actions only) |
| any other name | that method on the model returns true — an instance method for a record action, a classmethod for a collection action |
| not set | never: an action must say who may run it |

A permission method takes `(user_context)` or `(user_context, data)`. With the second argument it sees the validated input and can decide on it: which step, which amount, which file. It may also raise `LexActionError` or DRF's `NotFound` to answer in its own words — a 409 `WRONG_STATE` says more than a refusal. Any other exception denies the run and is logged.

A refusal answers 400 `ACTION_NOT_ALLOWED` — never 403, which signs the bundled frontend's user out. Where anything outside a caller's access should not exist, answer 404 instead:

```python
@lex_action(permission="permission_sign", denied="not_found")   # this action
def sign(self, context, data): ...
```

```python title="lex_config.py"
ACTION_DENIED = "not_found"   # every action; default "refused"
```

Any other value of either stops the server at startup.

## Answers

| The method returns | The response |
|---|---|
| a dict or list | JSON, status 200 or `status=` |
| data, with `output=` a serializer | the serialized data (a list, tuple or queryset as `many`) |
| `None` | 204 |
| `ActionResult(data, status=…, headers=…)` | status and headers decided while running |
| an `HttpResponse` | passed through untouched — a PDF, a CSV |

```python
@lex_action(permission="edit", status=201, headers={"Cache-Control": "no-store"})
def issue_token(self, context, data):
    return {"token": make_token(self)}

@lex_action(permission="edit")
def upsert_note(self, context, data):
    created = not self.notes.exists()
    ...
    return ActionResult({"created": created}, status=201 if created else 200)
```

`headers=` are added to every answer of the action, an `HttpResponse` included where it does not set them itself; an `ActionResult`'s own headers win. A `LexActionError(detail, code=…, fields=…, status_code=…)` raised in the method rolls the transaction back and answers `{"code", "detail", "error", "fields"}`; your `DB_ERROR_MAPPER` answers database errors.

`atomic=False` runs the method without the surrounding transaction, for long work that commits in steps.

## Throttling

```python
@lex_action(methods=("get",), permission="permission_lookup", input=LookupInput, throttle="lookup")
def lookup_address(cls, context, data): ...
```

```python title="lex_config.py"
THROTTLE_RATES = {"lookup": "30/min"}
```

Calls are counted per signed-in user (per client address for anyone else) and scope; beyond the rate the action answers 429 `THROTTLED`. Rates use DRF's notation (`"<n>/sec|min|hour|day"`) and are counted in Django's cache, so several web processes share a count only if that cache is shared. A throttle whose scope has no rate stops the server at startup.

## Audit log

An action that succeeded leaves one entry with `action = "action"` and status `success`. Its payload names the action, the record and the input — `{"lex_action": "approve", "id": 42, "ref": "<uuid>", "input": {...}}`, `ref` for models with a public identifier — and follows [[history-and-audit/audit logs#Keep personal data out of the log (3.0)|AUDIT_PAYLOAD and AUDIT_ACTOR]]. Uploaded files are recorded by name, never by content.

A run that raised leaves an entry with status `failure` and the error's code (`NOT_SUBMITTED`, or the exception's class name). It is written in a transaction of its own, so the rollback of the run does not take it along — with `atomic=False` too. A refused run or invalid input leaves no entry.

## Describing an action

`summary`, `description`, `operation_id`, `tags`, `responses` (further statuses, `{409: "Not submitted"}`) and `media="multipart"` (the input is a file upload) describe the action for an API document. They change nothing at runtime.

## See also

- [[access-and-dashboards/custom-api]] — endpoints of your own, when an operation is not about one model
- [[access-and-dashboards/generic-api]] — opening actions to your clients
- [[access-and-dashboards/permissions]] — the methods `"edit"`, `"create"` and `"delete"` use
