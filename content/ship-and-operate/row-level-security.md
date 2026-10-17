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

Not covered: management commands, `lex shell`, Streamlit and Reflex apps, and WebSocket consumers. Code there sets the context itself — call your `DB_CONTEXT` function inside `transaction.atomic()` with `local=True`.

> [!note]
> Run migrations as a database role that owns the tables, and the application as a role without `BYPASSRLS` — a superuser ignores every policy. Under RLS the API-key table may be unreadable before sign-in; see `API_KEY_RESOLVER` in [[access-and-dashboards/api-keys]].

## Lex App's own database functions

The bitemporal activation applier installs three `SECURITY DEFINER` functions owned by the migration role: `lex_apply_due_activations()`, `lex_pending_activations()` and `lex_bitemporal_tables()`. PostgreSQL lets every role execute a new function, so a restricted application role could call them and write as the owner, past your policies. Lex App leaves them executable because the pg_cron job that calls them runs as the server admin, which on managed PostgreSQL is not always a superuser. With a restricted application role, revoke them in a migration of your own and grant them to the role that runs the cron job:

```sql
REVOKE EXECUTE ON FUNCTION lex_apply_due_activations(), lex_pending_activations(), lex_bitemporal_tables() FROM PUBLIC;
GRANT EXECUTE ON FUNCTION lex_apply_due_activations(), lex_pending_activations(), lex_bitemporal_tables() TO cron_role;  -- if pg_cron runs them
```

The application only reads `lex_activation_applier_state` (to see whether the applier is alive); it needs no other right on that table.
