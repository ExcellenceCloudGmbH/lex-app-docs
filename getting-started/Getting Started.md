---
title: Getting Started
description: Overview of LEX and how to get up and running
---

# Getting Started with LEX

[[Home]] / Getting Started

---

## What is LEX?

**LEX** is a Python/Django framework for building business applications with complex logic. It provides:

- ✅ **Calculation models** — automatic state tracking (`IN_PROGRESS`, `SUCCESS`, `ERROR`), error handling, and Celery support
- ✅ **Lifecycle hooks** — explicit `@hook` decorators for reacting to model changes
- ✅ **Rich logging** — markdown-formatted logs with tables, code blocks, and DataFrames
- ✅ **Fine-grained permissions** — field-level and row-level access control, integrated with Keycloak
- ✅ **Bitemporal history** — automatic time-travel audit trail for every model
- ✅ **Streamlit dashboards** — interactive visualizations attached directly to models

---

## Who Is This Guide For?

| Role | What to Focus On |
|---|---|
| **New developer** | [[Setup & Installation]], [[../guides/Calculations\|Calculations]], [[../tutorial/Tutorial Overview\|Tutorial]] |
| **Business analyst** | [[../guides/Calculations\|Calculations]], [[../guides/Permissions\|Permissions]], [[../guides/Streamlit Dashboards\|Dashboards]] |
| **Migrating from V1** | [[../guides/Import Migration\|Import Migration]], then all guides |
| **Ops / DevOps** | [[../migration-workflow/Migration Workflow Overview\|Migration Workflow]] |

---

## Prerequisites

Before starting, make sure you have:

- [ ] Access to your project's source code repository
- [ ] Python **3.12** installed locally
- [ ] Access to [excellence-cloud.de](https://excellence-cloud.de) for client configuration
- [ ] Familiarity with your project's current model structure

---

## Quick Start

If you're in a hurry, here's the minimum to get running:

```bash
# 1. Install the framework
pip install lex-app

# 2. Run the setup wizard (generates configs + .env)
lex setup

# 3. Initialize (migrations + Keycloak sync)
lex Init

# 4. Start the development server
python -m lex start --reload --loop asyncio lex_app.asgi:application
```

For the full walkthrough, continue to [[Setup & Installation]].

---

> **Next:** [[Setup & Installation]] →
