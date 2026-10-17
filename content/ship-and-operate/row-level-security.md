---
title: Database context and row-level security
---

Some projects let PostgreSQL decide who sees which rows — row-level security (RLS) policies that read "who is asking" from a setting such as `app.user_id`. That setting has to be made at the start of every transaction. Inside a request that is easy; but Lex App also runs work in Celery tasks, on its calculation thread pool and in `on_commit` callbacks, where nobody would set it — and the database would see an anonymous caller.

Register one function and Lex App calls it everywhere:

```python title="lex_config.py"
DB_CONTEXT = "myproject.db.set_db_user"
```

```python title="myproject/db.py"
from django.db import connection

def set_db_user(user, *, local):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT set_config('app.user_id', %s, %s)",
            ["" if user is None else str(user.pk), local],
        )
```

| Where | When Lex App calls it | `local` |
|---|---|---|
| Every request | after the login check and the API-key lookup, inside one transaction around the rest of the request | `True` — ends with the transaction |
| A project endpoint (`LexAPIView`) | again after DRF authentication, in case your own authentication chose the user | `True` |
| A Celery task | at the start, with the user who started the work; with `None` at the end | `False` |
| The calculation thread pool | the same, around the calculation | `False` |
| `on_commit` callbacks Lex App registers | in a fresh transaction with the same user | `True` |

`user` is `None` for anonymous callers. Without `DB_CONTEXT` nothing changes: no extra transaction per request, no calls.

With a [[access-and-dashboards/request-scope|request scope]], the function also receives the organisation or workspace the request acts in as `scope=` — when its signature accepts that keyword. On the generic record endpoints and in actions Lex App calls it once more with the scope after DRF authentication.

Not covered: management commands, `lex shell`, Streamlit and Reflex apps, and WebSocket consumers. Code there sets the context itself — call your `DB_CONTEXT` function inside `transaction.atomic()` with `local=True`.

To let these policies decide what a caller sees and changes, instead of Lex App's permission hooks, see [[ship-and-operate/database-decides]].

> [!note]
> Run migrations as a database role that owns the tables, and the application as a role without `BYPASSRLS` — a superuser ignores every policy. Under RLS the API-key table may be unreadable before sign-in; see `API_KEY_RESOLVER` in [[access-and-dashboards/api-keys]].

## Lex App's own database functions

The bitemporal activation applier installs three `SECURITY DEFINER` functions owned by the migration role: `lex_apply_due_activations()`, `lex_pending_activations()` and `lex_bitemporal_tables()`. PostgreSQL lets every role execute a new function, so a restricted application role could call them and write as the owner, past your policies. Name the roles that may run them:

```python title="lex_config.py"
BITEMPORAL_FUNCTION_ROLES = ["cron_role"]   # the role your pg_cron job runs as; [] if none
```

After every `lex migrate`, Lex App then revokes EXECUTE from PUBLIC and grants it to these roles only (the owner keeps it). Unset, the functions stay executable by every role, as PostgreSQL makes them: Lex App does not change that by default because the pg_cron job may run as a server admin that is not a superuser on managed PostgreSQL.

The application only reads `lex_activation_applier_state` (to see whether the applier is alive); it needs no other right on that table.
