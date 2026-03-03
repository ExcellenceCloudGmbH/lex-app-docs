---
title: Welcome to LEX
---

LEX is a Python/Django framework for building business applications with complex logic — calculations, permissions, audit trails, and interactive dashboards — out of the box. It handles the infrastructure so you can focus on your domain.

## Get Started

LEX requires **Python 3.12** and a PostgreSQL database. Then, in your terminal:

```bash
pip install lex-app
lex setup
lex Init
python -m lex start --reload --loop asyncio lex_app.asgi:application
```

This will get you a running LEX application. Once you've done so, see how to:

1. [[getting started|Get started]] with LEX
2. [[installation|Install and configure]] your environment
3. Understand the [[project structure]]
4. [[running your app|Run your app]] locally

If you'd prefer a hands-on tutorial, try the [[tutorial/index|TeamBudget Tutorial]] to build a complete app from scratch.

## Features

LEX comes with a rich set of features for building business applications:

- [[features/calculations|Calculations]] with automatic state tracking, error handling, and Celery support
- [[features/lifecycle hooks|Lifecycle hooks]] for reacting to model changes with `@hook` decorators
- [[features/permissions|Fine-grained permissions]] at the field and row level, integrated with Keycloak
- [[features/logging|Rich logging]] with Markdown-formatted output via the `LexLogger` builder pattern
- [[features/bitemporal history|Bitemporal history]] tracking every change with full time-travel support
- [[features/streamlit dashboards|Streamlit dashboards]] attached directly to your models
- [[features/model structure|Model structure]] configuration for the frontend sidebar

For a comprehensive list, visit the [[features/index|features overview]].

## Migrating from V1?

If you're coming from V1 (`generic_app`), check out the [[migration/index|migration guide]] for a step-by-step workflow to update your project. You can also refer to the [[migration/import migration|import migration]] guide for a quick find-and-replace table.

## Reference

For day-to-day development, the [[reference/index|reference section]] has quick-lookup cards for [[reference/CLI Commands|CLI commands]], the [[reference/LexLogger API|LexLogger API]], and the complete [[reference/V1 to V2 Import Map|import map]].
