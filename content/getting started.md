---
title: Getting Started
---

Lex App is an [open-source](https://github.com/ExcellenceCloudGmbH/lex-app) [Python](https://www.python.org/)/[Django](https://docs.djangoproject.com/) framework that gives you calculation models, lifecycle hooks, permissions, logging, bitemporal history, and [Streamlit](https://docs.streamlit.io/) dashboards — all out of the box. You define your models and business logic; Lex App handles the rest.

## Who Is This For?

If you're a **new developer**, start with [[start-here/installation]] and then try the [[start-here/tutorial/index|TeamBudget Tutorial]] to build a real app. If you're a **business analyst**, you'll want to focus on [[calculations/calculation models|calculations]], [[access-and-dashboards/permissions|permissions]], and [[access-and-dashboards/streamlit dashboards|dashboards]]. If you're **migrating from V1**, head to the [[migrating-from-v1/refactoring/index|Refactoring Series]] first.

## Quick Start

```bash
# Install the framework
pip install lex-app

# Set up your project (generates .run/, .env, migrations/)
lex setup

# Initialize (migrations + Keycloak sync)
lex Init

# Start the development server
lex start --reload --loop asyncio lex_app.asgi:application
```

For the full walkthrough, continue to [[start-here/installation]].

## Prerequisites

Before starting, make sure you have:

- Access to your project's source code repository
- Python **3.12** installed locally
- Access to [Excellence Cloud](https://excellence-cloud.de) for client configuration
- Familiarity with your project's model structure
