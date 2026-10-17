---
title: Custom API endpoints
---

Lex App generates a REST API for every model. When a project needs endpoints that are not CRUD on one model — a dashboard that combines several models, a "submit" action, a webhook from a provider — it adds its own endpoints **through Lex App**, not around it. They are mounted ahead of Lex App's routes and the frontend, and they get Lex App's sign-in, audit logging, transactions, error format and read permissions.

> [!note]
> Since Lex App 3.0. Before, a project had to replace `ROOT_URLCONF`, `MIDDLEWARE` and `REST_FRAMEWORK` in its own settings module to do this. That still works, but it is no longer needed.

## Mount your endpoints

Put your views and a `urlpatterns` list in an underscore module (Lex App's model discovery skips it), then name it in `lex_config.py`:

```python title="lex_config.py"
API_URLCONF = "_api.urls"          # a module with `urlpatterns`
API_PREFIX = "api/myproject/"      # where it is mounted
PUBLIC_PATHS = ["me"]              # paths below the prefix that need no sign-in
```

```python title="_api/urls.py"
from django.urls import path
from _api.views import DashboardView, SubmitView

urlpatterns = [
    path("dashboard", DashboardView.as_view()),
    path("instances/<uuid:uuid>/submit", SubmitView.as_view()),
]
```

The endpoints answer at `/api/myproject/dashboard` and so on (behind `DJANGO_BASE_PATH` if you set one). A prefix that overlaps one of Lex App's own routes (`api/model_entries/`, `oidc/`, `admin/`, …) stops the server with an error naming the clash as soon as the URL configuration loads (the first request, or `lex check`).

## Build views on `LexAPIView`

```python title="_api/views.py"
from rest_framework.response import Response
from lex.api.project import LexAPIView, LexActionError, serialize_for, visible_queryset

class DashboardView(LexAPIView):
    def get(self, request):
        funds = visible_queryset(Fund, request)          # only rows this user may read
        return Response({"funds": funds.count()})

class SubmitView(LexAPIView):
    def post(self, request, uuid):
        instance = self.get_object_or_404(ProcessInstance, uuid=uuid)
        if not instance.is_complete():
            raise LexActionError("Some answers are missing.", code="INCOMPLETE",
                                 fields={"amount": "Required."})
        instance.submit(actor=request.user)
        return Response({"status": instance.status})
```

What every `LexAPIView` does for you:

| | |
|---|---|
| **Sign-in** | Required, unless the view sets `public = True` or its path is in `PUBLIC_PATHS`. A public view still recognises a signed-in caller. `public = True` also makes the view `AllowAny`, which the OpenAPI schema shows as an optional security requirement (`{}`); to keep a view's schema unchanged, list its path in `PUBLIC_PATHS` instead. |
| **Transaction** | The whole request runs in one database transaction. A raised error (`LexActionError`, a DRF exception, a database error) rolls it back; an error `Response` you return yourself is committed like any other answer. Set `atomic = False` to opt out. |
| **Audit** | The request runs inside Lex App's operation context, so model saves record the right actor: `created_by` / `edited_by` hold the caller's username or e-mail. If you erase personal data, include these columns. |
| **Read permission** | `get_object_or_404()` and `visible_queryset()` apply the same rule as the generic list endpoint — a record the caller may not read is "not found" (404), never "forbidden". |
| **Errors** | `{"code", "detail", "error", "fields"}`. Raise `LexActionError(detail, code=..., fields=..., status_code=...)` for business errors. |
| **CSRF cookie** | `ensure_csrf = True` sets it — for the endpoint a browser client calls first. |

`serialize_for(request, obj_or_queryset, SerializerClass, many=False)` serializes with the caller's read permission applied: rows `permission_read` refuses are left out, withheld fields removed, and your serializer's field list stays the positive list.

To reject input keys an endpoint does not declare (an actor, a timestamp the server sets), decorate the serializer:

```python
from lex.api.project import strict_serializer

@strict_serializer
class SubmitInput(serializers.Serializer):
    comment = serializers.CharField(required=False)
```

## Webhooks

A provider calling back server to server has no session and no token; it signs the body instead.

```python
from lex.api.project import LexWebhookView, LexActionError, verify_hmac_sha256

class SignatureWebhook(LexWebhookView):
    service_user = "esign-provider"   # becomes request.user: actor and database context

    def post(self, request, provider):
        if not verify_hmac_sha256(self.raw_body, request.headers.get("X-Signature"),
                                  secret=os.environ["ESIGN_WEBHOOK_SECRET"], prefix="sha256="):
            raise LexActionError("Bad signature.", code="BAD_SIGNATURE", status_code=401)
        ...
```

`LexWebhookView` is public, CSRF-exempt and keeps the body exactly as received in `self.raw_body`. The comparison in `verify_hmac_sha256` is constant-time.

## Errors and database rules

If your database enforces business rules (triggers, constraints), map its errors to business answers once:

```python title="lex_config.py"
DB_ERROR_MAPPER = "_api.errors.map_database_error"
```

```python title="_api/errors.py"
from lex.api.project import LexActionError

def map_database_error(exc):
    if "status conflict" in str(exc):
        return LexActionError("The status changed meanwhile.", code="STATUS_CONFLICT", status_code=409)
    return None   # anything else stays a 500
```

To take over error handling completely, set `EXCEPTION_HANDLER` to your own DRF exception handler. It sees the errors of Lex App's generic endpoints too: they raise their refusals and not-found answers to the handler instead of returning bodies past it.

| On a generic endpoint | Your handler receives |
|---|---|
| A refused create, edit or delete; an unknown field (`lex_strict_input`); a hidden row in history or a bulk request; nothing to export; an unknown HTML report | `LexActionError` carrying the old body's keys and a `code` — `PERMISSION_DENIED`, `EDIT_NOT_ALLOWED`, `DELETE_NOT_ALLOWED`, `UNKNOWN_FIELDS`, `NOT_FOUND`, `NO_DATA`, … |
| A missing or invalid field | DRF's `ValidationError` |
| A `LexActionError` or DRF error raised in model code (`save()`, a hook) | that error, with its own status — no longer wrapped into a 500 |
| A database error | the `LexActionError` your `DB_ERROR_MAPPER` returns for it, otherwise the `DatabaseError` itself |

Without a handler of your own, Lex App's renders the same errors with every key of the old body plus `code` and `detail`, so existing clients keep working: a refused create answers 403 `{"message": …, "code": "PERMISSION_DENIED", "detail": …, "error": …}`. `DB_ERROR_MAPPER` now answers for the generic endpoints as well (an unmapped database error is still a 500 there). Field errors keep DRF's shape unless you set `LEX_ERROR_FORMAT=structured`. `LEX_SEC_ERRORS=false` restores the old behaviour — see [[ship-and-operate/security-defaults]].

## Your own authentication and middleware

Add DRF authentication classes and middleware through `lex_config.py` instead of overriding settings:

```python title="lex_config.py"
AUTHENTICATION_CLASSES = ["_auth.ServiceKeyAuthentication"]   # tried before Lex App's own
MIDDLEWARE_EXTRA = {
    "first": ["_security.HeadersMiddleware"],        # right after Security and GZip middleware
    "after_auth": ["_auth.ServiceKeyMiddleware"],    # request.user known, before the login check
    "last": [],                                      # end of the chain
}
```

Lex App's login check runs before DRF, so a caller that only one of your `AUTHENTICATION_CLASSES` recognises is sent to sign in on a non-public path. Recognise such callers in an `after_auth` middleware (set `request.user` there), use [[access-and-dashboards/api-keys|API_KEY_HEADERS and API_KEY_RESOLVER]] for key headers, or make the path public.

## Keep the generic API for operators only

If your product UI uses only your own endpoints, you can close Lex App's generic `api/*` endpoints to everyone but superusers:

```python title="lex_config.py"
GENERIC_API = "superuser"   # "all" (default) | "records" | "superuser" | "off"
```

Everyone else gets 404 for those paths, as if they did not exist — signed in or not. Only `api/user/` still answers 401 to an anonymous caller, so the bundled frontend can send operators to sign in. Your API prefix (when `API_URLCONF` is set) and `api/health` stay open. The switch also closes the [record actions](#record-actions) for everyone else, because their routes live under `api/model_entries/`, and it closes the WebSockets (`ws/`) to everyone but superusers. `"off"` also disables the bundled frontend, which is built on the generic endpoints.

If your clients should use the generic endpoints for some models instead of your own, open those models with `GENERIC_API = "records"` and `lex_api_exposed` — see [[access-and-dashboards/generic-api]].

## OpenAPI schema

```python title="lex_config.py"
SCHEMA = {
    "title": "My Project API",
    "version": "1.4.0",
    "public": True,                 # serve schema and docs without sign-in
    # "description": "…",          # shown on the docs page
    # "include": ["api/myproject/"] # default: API_PREFIX
    # "settings": {"REDOC_DIST": "https://cdn.jsdelivr.net/npm/redoc@2.1.5", "ENUM_NAME_OVERRIDES": {…}},
}
```

Lex App then serves the OpenAPI document at `<API_PREFIX>schema` and a Redoc page at `<API_PREFIX>docs`, and `lex schema --validate --fail-on-warn --file openapi.yaml` writes it for client generation. Only the included prefixes are documented; the generic `model_entries` endpoints are left out unless `SCHEMA["generic"]` describes the models you expose — see [[access-and-dashboards/generic-api#OpenAPI document|OpenAPI document]]. `settings` are further drf-spectacular settings; the served schema, the docs page and `lex schema` all use them. Lex App's own Bearer and API-key authentication are described as `bearerAuth` and `apiKeyAuth`. Describe your own authentication classes with a drf-spectacular `OpenApiAuthenticationExtension` and they appear in the schema too — an extension for `LexAPIKeyAuthentication` replaces Lex App's (for example to name your `API_KEY_HEADERS` header).

## Record actions

For operations on one model that are not create/read/update/delete — approve, submit, close — you do not need a custom endpoint at all. Declare an action on the model:

```python
from lex.api.project import lex_action, LexActionError

class Invoice(LexModel):
    @lex_action(permission="edit", input=ApproveInput)
    def approve(self, context, data):
        if self.status != "submitted":
            raise LexActionError("Only submitted invoices can be approved.", code="NOT_SUBMITTED")
        self.status = "approved"
        self.save()
        return {"status": self.status}
```

It answers at `POST api/model_entries/<model>/<calculationId>/one/<pk>/action/approve`, with the record's read permission, validated input, its own permission, one transaction and an audit-log entry. [[access-and-dashboards/actions]] has the whole of it: collection actions, permissions that see the input, refusals as 404, statuses and headers, throttling.

## Public identifiers

Integer primary keys are guessable and differ between systems. A model can be addressed by a public uuid instead:

```python
class Invoice(LexModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    lex_lookup_field = "uuid"
    lex_lookup_allow_pk = False   # optional: close the integer routes
```

This adds `api/model_entries/<model>/<calculationId>/one/<uuid>`, `…/history/<uuid>` and `file-download?lookup=<uuid>` beside the integer routes, and the [[access-and-dashboards/generic-api#Short paths|short paths]] without `calculationId` (`…/<model>/one/<uuid>`). Responses are unchanged. A `lex_lookup_field` that is not a unique `UUIDField` stops the server at startup.

## See also

- [[reference/lex_config]] — every key at a glance
- [[ship-and-operate/security-defaults]] — what changed in 3.0 and how to opt out
- [[access-and-dashboards/permissions]] — the permission methods `visible_queryset()` applies
