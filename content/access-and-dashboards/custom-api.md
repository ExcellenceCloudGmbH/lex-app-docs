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

The endpoints answer at `/api/myproject/dashboard` and so on (behind `DJANGO_BASE_PATH` if you set one). A prefix that overlaps one of Lex App's own routes (`api/model_entries/`, `oidc/`, `admin/`, …) stops the server at startup with an error naming the clash.

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
| **Sign-in** | Required, unless the view sets `public = True` or its path is in `PUBLIC_PATHS`. A public view still recognises a signed-in caller. |
| **Transaction** | The whole request runs in one database transaction. An error answer rolls it back. Set `atomic = False` to opt out. |
| **Audit** | The request runs inside Lex App's operation context, so model saves record the right actor. |
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

To take over error handling completely, set `EXCEPTION_HANDLER` to your own DRF exception handler. Lex App's generic endpoints keep their own error bodies unless you set `LEX_ERROR_FORMAT=structured` — see [[ship-and-operate/security-defaults]].

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

## Keep the generic API for operators only

If your product UI uses only your own endpoints, you can close Lex App's generic `api/*` endpoints to everyone but superusers:

```python title="lex_config.py"
GENERIC_API = "superuser"   # "all" (default) | "superuser" | "off"
```

Everyone else gets 404 for those paths, as if they did not exist. Your API prefix and `api/health` stay open. `"off"` also disables the bundled frontend, which is built on the generic endpoints.

## OpenAPI schema

```python title="lex_config.py"
SCHEMA = {
    "title": "My Project API",
    "version": "1.4.0",
    "public": True,                 # serve schema and docs without sign-in
    # "include": ["api/myproject/"] # default: API_PREFIX
}
```

Lex App then serves the OpenAPI document at `<API_PREFIX>schema` and a Redoc page at `<API_PREFIX>docs`, and `lex schema --validate --fail-on-warn --file openapi.yaml` writes it for client generation. Only the included prefixes are documented; the generic `model_entries` endpoints are left out. Describe your own authentication classes with a drf-spectacular `OpenApiAuthenticationExtension` and they appear in the schema too. Every key and option: [[reference/openapi]].

## See also

- [[reference/lex_config]] — every key at a glance
- [[ship-and-operate/security-defaults]] — what changed in 3.0 and how to opt out
- [[access-and-dashboards/permissions]] — the permission methods `visible_queryset()` applies
