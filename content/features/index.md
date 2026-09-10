---
title: Building Blocks
---

Lex App provides a set of building blocks that you compose to create your application. Each one solves a specific problem — you only use what you need. They're organized into four groups that mirror how data flows through your app.

## The ETL Pipeline

Every Lex App project follows the Extract → Transform → Load pattern. Your folder structure reflects this:

| Stage | Folder | What Lives Here |
|---|---|---|
| **Extract** | `Upload/` | `CalculationModel` subclasses that ingest CSVs, Excel files, API data |
| **Transform** | `Input/` | Input models — your core business entities and domain logic |
| **Load** | `Reports/` | `CalculationModel` subclasses that compute summaries and analytics |

## Building Blocks by Category

### [[model-your-data/index|Data Pipeline]]
How data enters and is structured — [[model-your-data/serializers|serializers]], [[model-your-data/lifecycle hooks|lifecycle hooks]], and [[model-your-data/model structure|model structure]].

### [[calculations/index|Processing]]
How business logic runs — [[calculations/calculation models|calculations]], [[calculations/celery and async calculations|Celery async dispatch]], and [[calculations/logging|LexLogger]] for rich calculation output.

### [[history-and-audit/index|Tracking & Audit]]
Every action leaves a trail — [[history-and-audit/audit logs|audit logs]] for operation tracking and [[history-and-audit/bitemporal history|bitemporal history]] for data over time.

### [[access-and-dashboards/index|Access & UI]]
Who sees what and how it's presented — [[access-and-dashboards/permissions|permissions]] and [[access-and-dashboards/streamlit dashboards|Streamlit dashboards]].
