---
title: API keys
---

Machines — an integration, a nightly import, a partner system — call Lex App's API with a key instead of a sign-in. Since 3.0 there are two kinds.

| | Scoped key (`LexAPIKey`) | Classic key |
|---|---|---|
| Acts as | a real user you choose | a technical identity |
| Permissions | the scopes you give the key, and the user's groups | every scope on every model |
| Audit actor | the user | "Technical User" |
| Limited to paths | yes, optional | no |

Use scoped keys for anything new. Classic keys keep working unchanged.

## Create a scoped key

Create a user for the integration (it needs no password), then issue a key:

```bash
lex create_api_key --user quantium-sync --name "Quantium sync" --scopes read,list,edit --prefix api/myproject/
```

The key is printed once — only a hash is stored. `--expires-in-days 90` sets an expiry; revoking happens in the Django admin (Authentication → Lex API keys).

## Use it

Send it in the `Api-Key` header or as `Authorization: Api-Key <key>`:

```bash
curl -H "Api-Key: AbCdEf12.secret…" https://app.example.com/api/model_entries/invoice/list
```

The request then runs as the key's user:

- the default permission methods check the key's **scopes** (`read`, `list`, `edit`, `create`, `delete`, `export`) on every model; your own permission methods see the user (`user_context.user`, `user_context.groups`);
- `created_by` / `edited_by` and the audit log name the user;
- the [[ship-and-operate/row-level-security|database context]] is set for the user;
- outside its `--prefix` paths the key finds nothing (404). A prefix is a plain string prefix of the full request path, including `DJANGO_BASE_PATH`;
- no CSRF token is needed.

Revoked and expired keys are ignored.

## Project options

```python title="lex_config.py"
API_KEY_HEADERS = ["HTTP_X_MYPROJECT_KEY"]       # also accept the key in X-MyProject-Key
API_KEY_RESOLVER = "myproject.keys.resolve"      # replace the lookup
```

`API_KEY_RESOLVER` receives the raw key and returns a key object (a `LexAPIKey`, or anything with `user`, `scopes`, `allows_path(path)`, `revoked`, `has_expired`) or `None`. Use it when the key table cannot be read before anyone is signed in, for example under row-level security, where a database function has to do the lookup.

## See also

- [[access-and-dashboards/permissions]]
- [[reference/CLI Commands#API Commands|CLI: lex create_api_key]]
