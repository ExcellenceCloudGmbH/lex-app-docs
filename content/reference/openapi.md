---
title: "OpenAPI schema"
---

Lex App can describe your own API endpoints (see [[access-and-dashboards/custom-api]]) as an OpenAPI 3 document, served by the app and written to a file for client generation. It is built with [drf-spectacular](https://drf-spectacular.readthedocs.io/).

> [!note]
> Since Lex App 3.0. Nothing is served or generated until you set `SCHEMA`.

## Configure

```python title="lex_config.py"
API_URLCONF = "_api.urls"
API_PREFIX = "api/myproject/"
SCHEMA = {
    "title": "My Project API",
    "version": "1.4.0",
    "description": "Endpoints of the My Project frontend.",
    "public": True,
    "include": ["api/myproject/"],
    "settings": {"COMPONENT_SPLIT_REQUEST": True},
}
```

| Key | Default | Meaning |
|---|---|---|
| `title` | `"API"` | `info.title` of the document |
| `version` | `"1.0.0"` | `info.version` |
| `description` | none | `info.description` |
| `public` | `False` | `True` serves the schema and the docs page without sign-in |
| `include` | `[API_PREFIX]` | Path prefixes that are documented; everything else is left out |
| `settings` | `{}` | Further drf-spectacular settings (`SPECTACULAR_SETTINGS` keys) for this document |

Only paths under `include` appear. Lex App's generic endpoints (`api/model_entries/…`, `api/model-structure`, …) are never part of it, and a `DJANGO_BASE_PATH` is put in front of every prefix for you.

## Where it is served

| URL | What |
|---|---|
| `<API_PREFIX>schema` | The OpenAPI document (YAML; `?format=json` for JSON) |
| `<API_PREFIX>docs` | A Redoc page rendering it |

Without `public: True` both need a signed-in caller, like any other project endpoint.

## Write it to a file

```bash
lex schema --validate --fail-on-warn --file openapi.yaml
```

`lex schema` takes the options of drf-spectacular's `spectacular` command (`--file`, `--format`, `--validate`, `--fail-on-warn`) and applies `SCHEMA`. Commit the file and generate your client from it; `--fail-on-warn` makes the build fail when a view cannot be described, instead of silently documenting it as untyped.

## Authentication in the document

The security schemes list how callers can sign in:

| Scheme | Where it comes from |
|---|---|
| `bearerAuth` | Lex App's bearer-token middleware (Keycloak tokens) |
| `cookieAuth` | Django session sign-in (drf-spectacular's own description) |
| Your own classes | Each class in `lex_config.AUTHENTICATION_CLASSES` that has a drf-spectacular `OpenApiAuthenticationExtension` |

Describe a custom authentication class like this, in a module your project imports:

```python title="_api/schema.py"
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class ServiceKeyScheme(OpenApiAuthenticationExtension):
    target_class = "_auth.ServiceKeyAuthentication"
    name = "serviceKey"

    def get_security_definition(self, auto_schema):
        return {"type": "apiKey", "in": "header", "name": "X-Service-Key"}
```

## See also

- [[access-and-dashboards/custom-api]] — building the endpoints this document describes
- [[reference/lex_config]] — every `lex_config.py` key
- [[reference/CLI Commands]] — `lex schema` among the other commands
