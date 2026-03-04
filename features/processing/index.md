---
title: Processing
---

Once data is in the system, it needs to be transformed into business insight. LEX provides building blocks for running calculations, logging their results, and scaling them across workers.

```mermaid
flowchart LR
    A["User clicks\nCalculate"] --> B["CalculationModel\nstate machine"]
    B --> C{"Parallel?"}
    C -- Yes --> D["Celery workers"]
    C -- No --> E["Synchronous"]
    D --> F["Results saved\n+ LexLogger output"]
    E --> F
```

## Building Blocks

### [[features/processing/calculations|Calculations]]
The `CalculationModel` base class gives you a built-in state machine (`NOT_CALCULATED` → `IN_PROGRESS` → `SUCCESS`), automatic error capture, and a calculate button in the UI. You implement one method — `calculate()` — and the framework handles everything else.

### [[features/processing/celery and async calculations|Celery & Async Calculations]]
When a calculation triggers many children, LEX can dispatch them to [Celery](https://docs.celeryq.dev/) workers in parallel. If Celery isn't available, the framework falls back to synchronous processing automatically — your code doesn't change either way.

### [[features/processing/logging|Logging]]
`LexLogger` produces rich, Markdown-formatted log entries during calculations. Tables, headings, DataFrames, code blocks — all stored in the database and displayed in the frontend's calculation log panel. Context-aware: it automatically links logs to the correct calculation and model instance.
