---
title: Getting Started
---

LEX is a Python/Django framework that gives you calculation models, lifecycle hooks, permissions, logging, bitemporal history, and Streamlit dashboards — all out of the box. You define your models and business logic; LEX handles the rest.

## Who Is This For?

If you're a **new developer**, start with [[installation]] and then try the [[tutorial/index|TeamBudget Tutorial]] to build a real app. If you're a **business analyst**, you'll want to focus on [[features/calculations|calculations]], [[features/permissions|permissions]], and [[features/streamlit dashboards|dashboards]]. If you're **migrating from V1**, head to [[migration/import migration|Import Migration]] first.

## Quick Start

```bash
# Install the framework
pip install lex-app

# Set up your project (generates .run/, .env, migrations/)
lex setup

# Initialize (migrations + Keycloak sync)
lex Init

# Start the development server
python -m lex start --reload --loop asyncio lex_app.asgi:application
```

For the full walkthrough, continue to [[installation]].

## Prerequisites

Before starting, make sure you have:

- Access to your project's source code repository
- Python **3.12** installed locally
- Access to [excellence-cloud.de](https://excellence-cloud.de) for client configuration
- Familiarity with your project's model structure
