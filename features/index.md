---
title: Feature List
---

LEX provides a comprehensive set of features for building business applications. Each feature is built into the framework and works out of the box — no extra setup required.

- [[features/calculations|Calculations]] — define business logic in a `calculate()` method with automatic state tracking, error handling, and optional Celery offloading
- [[features/lifecycle hooks|Lifecycle Hooks]] — react to creates, updates, and deletes with explicit `@hook` decorators and built-in validation hooks
- [[features/logging|Logging]] — rich Markdown-formatted logs with the `LexLogger` builder pattern, supporting tables, DataFrames, and code blocks
- [[features/permissions|Permissions]] — field-level and row-level access control using `UserContext` and `PermissionResult`, integrated with Keycloak
- [[features/bitemporal history|Bitemporal History]] — automatic time-travel audit trail tracking both *when things happened* and *when the system learned about it*
- [[features/streamlit dashboards|Streamlit Dashboards]] — attach interactive visualizations directly to your models at the table or record level
- [[features/model structure|Model Structure]] — organize models in the frontend sidebar with `model_structure.yaml`
