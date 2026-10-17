---
title: Request scope
---

A user of a multi-tenant application often works *as* one of several organisations, workspaces or clients, and chooses which one per request. `REQUEST_SCOPE` gives that choice one query parameter and one meaning on every generic endpoint:

```python title="lex_config.py"
REQUEST_SCOPE = {"param": "workspace", "resolver": "myproject.scope.resolve"}
```

```python title="myproject/scope.py"
from rest_framework.exceptions import NotFound

def resolve(request, value):
    workspaces = Workspace.objects.filter(members=request.user)
    if value is None:
        return workspaces.order_by("name").first()   # no parameter: a default
    workspace = workspaces.filter(slug=value).first()
    if workspace is None:
        raise NotFound()                             # not one of this user's
    return workspace
```

```bash
curl -H "Api-Key: …" "https://app.example.com/api/model_entries/invoice/list?workspace=acme"
```

> [!note]
> Since Lex App 3.0.

## What Lex App does with it

- **The resolver decides.** It runs once per request with the parameter's value, or with `None` when the parameter is absent, so it can choose a default (an API key's own organisation, say). It returns the scope — any object, or `None` for none — or raises `NotFound` (or `Http404`) for a value the caller may not use; the request then answers 404, as for anything outside their access.
- **The parameter filters nothing.** It is reserved: a list never reads it as a field filter.
- **The scope is `request.lex_scope`** for the rest of the request.
- **`DB_CONTEXT` receives it** as `scope=` when your function accepts that keyword (or `**kwargs`), so row-level security policies can read it:

  ```python title="myproject/db.py"
  from django.db import connection

  def set_db_user(user, *, local, scope=None):
      with connection.cursor() as cursor:
          cursor.execute("SELECT set_config('app.user_id', %s, %s)", ["" if user is None else str(user.pk), local])
          cursor.execute("SELECT set_config('app.workspace_id', %s, %s)", ["" if scope is None else str(scope.pk), local])
  ```

- **A model narrows itself to the scope** with `lex_scope_queryset`. Its list, its single records, their history and the record an action runs on are taken from the narrowed queryset, so a row outside the scope answers 404:

  ```python
  class Invoice(LexModel):
      @classmethod
      def lex_scope_queryset(cls, queryset, scope, request):
          return queryset.filter(workspace=scope) if scope is not None else queryset.none()
  ```

The scope applies to Lex App's generic record endpoints and to [[access-and-dashboards/custom-api#Record actions|record actions]]; your own endpoints under `API_PREFIX` are not affected. A `REQUEST_SCOPE` that is not `{"param": "<name>", "resolver": "<dotted path>"}`, or a resolver that cannot be imported, stops the server at startup.

## See also

- [[ship-and-operate/row-level-security]] — `DB_CONTEXT`
- [[ship-and-operate/database-decides]] — letting the policies decide what a caller sees
- [[access-and-dashboards/generic-api]] — opening the generic endpoints to your clients
