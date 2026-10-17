---
title: The database decides
---

Some projects keep every access rule in PostgreSQL: row-level security (RLS) policies that read who is asking from the setting `DB_CONTEXT` makes (see [[ship-and-operate/row-level-security|database context]]). Lex App's own permission checks are then in the way — its default hooks ask Keycloak for scopes the project does not use, and lists run a read check per row that the database has already made. Let the database decide instead:

```python title="lex_config.py"
PERMISSION_SOURCE = "database"          # every model of the project; default "python"
DB_CONTEXT = "myproject.db.set_db_user"
```

or for one model:

```python
class Invoice(LexModel):
    lex_permission_source = "database"  # "python" keeps a model on the hooks when the key says "database"
```

The model's attribute wins over the key. Lex App's own models (the audit log, the calculation logs) keep their rules unless they set the attribute; Django's models are not affected. An unknown value stops the server at startup.

> [!note]
> Since Lex App 3.0. PostgreSQL only.

## What changes for a database-mode model

| | `"python"` (default) | `"database"` |
|---|---|---|
| Lex App's default `permission_read`, `permission_edit`, `permission_export`, `permission_create`, `permission_delete`, `permission_list` | answer from Keycloak scopes | allow |
| Rows of a list | filtered by `permission_read_queryset`, or by `permission_read` row by row | exactly what the database returns |
| Saving an existing record the policy hides from UPDATE | Django finds no row and inserts a new one | `RowNotWritable`, answered 404 |
| Keycloak's permission (UMA) call per request | made | skipped, when `PERMISSION_SOURCE = "database"` |

Your own `permission_*` overrides still apply where Lex App asks them for one record — reading it, creating, changing and deleting. A list in database mode runs no Python read check at all, not even your `permission_read` or `permission_read_queryset`, so keep row rules in the policies and use overrides for what the database cannot know.

Keycloak's userinfo is still fetched. The permission call is skipped only when the key says `"database"`: with the attribute on single models, the other models still need their scopes.

## Policies refuse with 404

Lex App saves an existing record of a database-mode model with `force_update`. An UPDATE that reaches no row — the policy lets the caller read the row but not change it — raises `RowNotWritable` (`lex.core.permission_source`, a `DatabaseError`) instead of turning into an INSERT. A write a policy rejects outright (SQLSTATE 42501, "row-level security") is a policy refusal too, in either mode.

The generic endpoints and Lex App's exception handler answer both 404 `NOT_FOUND`: for this caller the row does not exist. Your `DB_ERROR_MAPPER` is asked first. With an `EXCEPTION_HANDLER` of your own, it receives the database error and answers it itself; `lex.core.permission_source.is_policy_refusal(exc)` tells you whether it is one. Code of your own that calls `save()` can catch `RowNotWritable`.

## Lex App checks that the database really decides

The mode is only safe when every query goes through the policies. On the first request Lex App checks, for every database-mode model with a table of its own:

- row-level security is enabled on its table, its history table and its meta-history table;
- the role the application's sessions run as (`current_user`, so a `SET ROLE` after connecting counts) is not a superuser, has no `BYPASSRLS` and does not own those tables (an owner bypasses its tables' policies).

If anything fails, each reason is logged as an error and every request answers 503 `{"code": "SERVICE_MISCONFIGURED", "detail": "The service is not configured safely."}` until the process restarts with the problem fixed. If the check itself cannot run (the database is unreachable), that is logged and the check is not repeated.

```sql
-- in a migration (RunSQL), with the table names Lex App assigns (Model._meta.db_table)
ALTER TABLE myproject_invoice ENABLE ROW LEVEL SECURITY;
ALTER TABLE myproject_historicalinvoice ENABLE ROW LEVEL SECURITY;
ALTER TABLE myproject_metahistoricalinvoice ENABLE ROW LEVEL SECURITY;

CREATE POLICY invoice_owner ON myproject_invoice
    USING (owner_id = nullif(current_setting('app.user_id', true), '')::int);
```

A table with row-level security and no policy refuses the application role every row, so the history tables need policies too: the application writes a history row with every save. Run migrations as the role that owns the tables and the application as a restricted one — see [[ship-and-operate/row-level-security]].

Test suites that run as the tables' owner switch the check off with `LEX_DATABASE_DECIDES_CHECK=false`. Never set it in a deployment.

## See also

- [[ship-and-operate/row-level-security]] — `DB_CONTEXT`, the setting the policies read
- [[access-and-dashboards/request-scope]] — the organisation or workspace a request acts in
- [[access-and-dashboards/permissions]] — the Python hooks this mode replaces
